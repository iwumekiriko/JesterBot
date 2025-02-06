import asyncio
import pytest

import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils.ui import BaseView, BaseEmbed
from src.utils.ui._views import State


class ViewsTestCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self._bot = bot

    @commands.slash_command(name="view_test", description="view testing group")
    async def test_view(
        self,
        interaction: disnake.GuildCommandInteraction
    ): ...

    @test_view.sub_command(name="back_button", description="testing back button")
    async def test_view_back_button(
        self,
        interaction: disnake.GuildCommandInteraction
    ) -> None:
        view = TestView()
        await view.start(interaction)

    @pytest.mark.asyncio
    @test_view.sub_command(name="timeout", description="testing view timeout")
    async def test_view_timeout(
        self,
        interaction: disnake.GuildCommandInteraction
    ) -> None:
        view = TestView(timeout=10)
        await view.start(interaction)

        await asyncio.sleep(10)
        assert view.is_finished()


class TestView(BaseView):
    def __init__(
        self, timeout: float | None = 180
    ) -> None:
        super().__init__(timeout=timeout)
        self.add_item(NextButton1())

    def create_embed(self) -> disnake.Embed:
        return BaseEmbed(
            title = "Test Title 1",
            description = "Test Description 1"
        )

    def to_state(self) -> State:
        return State(
            view = self,
            embed = self.create_embed(),
            content = "Test Content 1"
        )


class NextButton1(disnake.ui.Button):
    view: TestView

    def __init__(self) -> None:
        super().__init__(
            label = "Next1",
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer()
        next_view = TestViewWithBackButton()
        await self.view.start_next(next_view)


class NextButton2(disnake.ui.Button):
    view: TestView

    def __init__(self) -> None:
        super().__init__(
            label = "Next2",
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer()
        next_view = TestViewWithBackButton2()
        await self.view.start_next(next_view)


class TestViewWithBackButton(BaseView):
    def __init__(self) -> None:
        super().__init__()
        self.add_back_button()
        self.add_item(NextButton2())

    def create_embed(self) -> disnake.Embed:
        return BaseEmbed(
            title = "Test Title 2",
            description = "Test Description 2"
        )

    def to_state(self) -> State:
        return State(
            view = self,
            embed = self.create_embed(),
            content = "Test Content 2"
        )
    

class TestViewWithBackButton2(BaseView):
    def __init__(self) -> None:
        super().__init__()
        self.add_back_button()

    def create_embed(self) -> disnake.Embed:
        return BaseEmbed(
            title = "Test Title 3",
            description = "Test Description 3"
        )

    def to_state(self) -> State:
        return State(
            view = self,
            embed = self.create_embed(),
            content = "Test Content 3"
        )
