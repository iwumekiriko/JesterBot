import random
import asyncio
from enum import Enum
from uuid import UUID
from collections import Counter
from typing import List, Dict, Tuple

from disnake import (MessageCommandInteraction,
                      Embed, Member, Guild)
from disnake.errors import NotFound

from src.localization import get_localizator
from src.logger import get_logger

from ._base_lootbox import BaseLootbox
from src.utils.ui import BaseEmbed
from .._api_interaction import (
    handle_lootbox_prize,
    get_user_lootbox_roles
)
from src.models.inventory_items import Item
from src.models.lootboxes import LootboxTypes, RolesData, LootboxRole
from src.utils._cards import item_card, items_summary_card
from src.customisation import ROLES_LOOTBOX_THUMBNAIL


logger = get_logger()
_ = get_localizator("lootboxes-roles")


LOOTBOX_OPENING_TIME = 5


class RolesPrizes(str, Enum):
    COINS = _("lootboxes-roles_coins_prize")
    EXP_BOOSTER = _("lootboxes-roles_exp_booster_prize")
    LOOTBOX_KEY_ROLES = _("lootboxes-roles_lootbox_key_roles_prize")
    ROLE = _("lootboxes-roles_role_prize")

    @staticmethod
    def base_chances() -> Dict['RolesPrizes', int]:
        return {
            RolesPrizes.COINS: 4950,
            RolesPrizes.EXP_BOOSTER: 3542,
            RolesPrizes.LOOTBOX_KEY_ROLES: 1225,
            RolesPrizes.ROLE: 283
        }


class RolesLootbox(BaseLootbox):
    def __init__(
        self,
        interaction: MessageCommandInteraction,
        uuid: UUID
    ) -> None:
        super().__init__(interaction, uuid)

    async def _get_user_lootbox_roles(self) -> List[LootboxRole]:
        return await get_user_lootbox_roles(
            self._guild.id, LootboxTypes.ROLES_LOOTBOX, self._user.id)

    async def _calculate_chances(self) -> Dict[RolesPrizes, float]:
        user_data = await self._get_user_data(type=LootboxTypes.ROLES_LOOTBOX)
        base = RolesPrizes.base_chances()
        if isinstance(user_data.data, RolesData):
            roles_data = user_data.data

        lootbox_roles = await self._get_user_lootbox_roles()
        available_roles = [role for role in lootbox_roles if not role.got_by_user]
        has_available_roles = bool(available_roles)

        pity_boost = min((roles_data.roles_attempts or 0) * 0.05, 10.0)

        if has_available_roles:
            adjusted = {
                RolesPrizes.ROLE: base[RolesPrizes.ROLE] + pity_boost * 100,
                **{
                    p: base[p] * (1 - pity_boost / 100) for p in base if p != RolesPrizes.ROLE
                }
            }
        else:
            role_chance = base.get(RolesPrizes.ROLE, 0)
            non_role_prizes = [p for p in base if p != RolesPrizes.ROLE]
            total_non_role = sum(base[p] for p in non_role_prizes)

            adjusted = {
                p: base[p] + (base[p] / total_non_role * role_chance)
                for p in non_role_prizes
            }

        total = sum(adjusted.values())
        return {p: (adjusted[p] / total * 100) for p in adjusted}

    async def get_description(self) -> str:
        chances = await self._calculate_chances()
        lines = []

        lootbox_roles = await self._get_user_lootbox_roles()
        available_roles = [role for role in lootbox_roles if not role.got_by_user]
        has_available_roles = bool(available_roles)

        for prize, chance in sorted(chances.items(), key=lambda x: x[1], reverse=True):
            if prize == RolesPrizes.ROLE and not has_available_roles: continue
            lines.append(f"{prize.value}: **{chance:.2f}%**")

        roles_list = (' **/** '.join(f'~~<@&{r.guild_role_id}>~~'
                      if r.got_by_user else f'<@&{r.guild_role_id}>'
                      for r in lootbox_roles))
        lines.append(_("lootboxes-roles_roles_listing", listing=roles_list)) 
        return "\n".join(lines)

    async def get_prize(self, count: int) -> None:
        await self._interaction.edit_original_message(
            embed=BaseEmbed(description=_("lootboxes-roles_wait_for_opening_desc"))
        )

        prizes = await self._get_roles_prizes(count)
        prizes_data = await self._prize_giver(prizes)
        self.items_received(prizes_data)

        await self._prize_handler(self._interaction, prizes_data)

    @classmethod
    async def create_embed(
        cls, guild: Guild, user: Member
    ) -> Embed:
        instance = cls.__new__(cls)
        instance._guild = guild
        instance._user = user

        description = await instance.get_description()
        return BaseEmbed(
            title=_("lootboxes-roles-embed_title"),
            description=description
        ).set_thumbnail(ROLES_LOOTBOX_THUMBNAIL)

    async def _get_roles_prizes(self, count: int) -> Dict[RolesPrizes, int]:
        chances = await self._calculate_chances()
        prizes = random.choices(
            population=list(chances.keys()),
            weights=list(chances.values()),
            k=count
        )
        logger.info("User %s from Guild %s opened ROLES_LOOTBOXes: %s",
                     self._user.id, self._guild.id, prizes)
        user_data = await self._get_user_data(type=LootboxTypes.ROLES_LOOTBOX)
        user_data.data.total_attempts += count

        dropped_roles = prizes.count(RolesPrizes.ROLE)
        if isinstance(user_data.data, RolesData):
            roles_data = user_data.data
            roles_data.roles_attempts = (roles_data.roles_attempts + count 
                                         if dropped_roles <= 0 else 0)
        await self._save_user_data(user_data)
        return dict(Counter(prizes))


    async def _prize_giver(
        self,
        prizes: Dict[RolesPrizes, int]
    ) -> List[Item]:
        received = []

        for item, count in prizes.items():
            match item:

                case RolesPrizes.COINS:
                    received.extend(await self._handle_coins_reward(count))

                case RolesPrizes.EXP_BOOSTER:
                    received.extend(await self._handle_exp_booster_reward(count))

                case RolesPrizes.LOOTBOX_KEY_ROLES:
                    received.extend(await self._handle_lootbox_key_reward(count))

                case RolesPrizes.ROLE:
                    received.extend(await self._handle_role_reward(count))

                case _:
                    raise ValueError("prize type is not matched")

        return received

    async def _prize_handler(
        self,
        inter: MessageCommandInteraction,
        prizes: List[Item]
    ) -> None:
        try:
            count = len(prizes)
            match count:

                case 1:
                    prize = prizes[0]
                    await inter.edit_original_message(
                        embed=BaseEmbed().set_image(
                            prize.lootbox_gif))
                    await asyncio.sleep(LOOTBOX_OPENING_TIME)
                    await inter.edit_original_message(embed=item_card(prize))

                case _ if count > 1:
                    await inter.edit_original_message(
                        embed=BaseEmbed().set_image(
                            prizes[-1].lootbox_gif))
                    await asyncio.sleep(LOOTBOX_OPENING_TIME)
                    await inter.edit_original_message(embed=items_summary_card(prizes))

        except NotFound:
            return

    async def _handle_coins_reward(self, count: int) -> list[Item]:
        from src.models.inventory_items import Coin

        received = []

        amounts = self._get_coins_params(count)
        for amount, count in amounts.items():
            item = await handle_lootbox_prize(
                self._guild.id,
                self._user.id,
                Coin,
                body={
                    "Amount": amount,
                    "Quantity": count
                }
            )
            received.append(item)

        return received

    def _get_coins_params(self, count) -> Dict[int, int]:
        amount_choices = { 45: 1000, 35: 2000, 12: 4000, 5: 8000, 2: 1, 1: 20000 }
        return dict(Counter(random.choices(
            population=list(amount_choices.values()),
            weights=list(amount_choices.keys()), k=count)))

    async def _handle_exp_booster_reward(self, count: int) -> list[Item]:
        from src.models.inventory_items import ExpBooster

        received = []

        boosters_data = self._get_exp_booster_params(count)
        for (value, duration), quantity in boosters_data.items():
            item = await handle_lootbox_prize(
                self._guild.id,
                self._user.id,
                ExpBooster,
                body={
                    "Value": value,
                    "Duration": duration,
                    "Quantity": quantity
                },
            )
            received.append(item)

        return received

    def _get_exp_booster_params(self, count: int) -> Dict[Tuple[int, int], int]:
        value_choices = { 70: 2, 30: 3 }
        duration_choices = { 45: 600, 35: 900, 12: 1800, 5: 3600, 3: 10800 }

        values = random.choices(
            population=list(value_choices.values()),
            weights=list(value_choices.keys()), k=count)
        durations = random.choices(
            population=list(duration_choices.values()),
            weights=list(duration_choices.keys()), k=count)

        boosters_data = {}
        for value, duration in zip(values, durations):
            key = (value, duration)
            boosters_data[key] = boosters_data.get(key, 0) + 1

        return boosters_data

    async def _handle_lootbox_key_reward(self, count) -> List[Item]:
        from src.models.inventory_items import LootboxKey

        received = []

        received.append(await handle_lootbox_prize(
            self._guild.id,
            self._user.id,
            LootboxKey,
            body={
                "Type": LootboxTypes.ROLES_LOOTBOX.value,
                "Quantity": count
            },
        ))
        return received

    async def _handle_role_reward(self, count: int) -> List[Item]:
        from src.models.inventory_items import Role
        from src.utils._extra import add_role_with_id

        lootbox_roles = await self._get_user_lootbox_roles()
        available_roles = [role for role in lootbox_roles if not role.got_by_user]

        if not available_roles:
            return await self._handle_coins_reward(count) if count > 0 else []

        reward_count = min(count, len(available_roles))
        received = []

        random.shuffle(available_roles)

        for role in available_roles[:reward_count]:
            reward = await handle_lootbox_prize(
                self._guild.id, self._user.id, Role,
                body={"GuildRoleId": role.guild_role_id}
            )
            received.append(reward)

        if received:
            await add_role_with_id(
                self._guild, self._user,
                role_id=received[-1].guild_role_id
            )

        remaining_rewards = count - len(received)
        if remaining_rewards > 0:
            received.extend(await self._handle_coins_reward(remaining_rewards))

        return received
