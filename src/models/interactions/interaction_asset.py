from dataclasses import dataclass, asdict

from src.cogs.interactions._interactions_choice import InteractionActions, InteractionTypes


@dataclass
class InteractionsAsset:
    asset_url: str
    action: InteractionActions
    type: InteractionTypes

    def to_dict(self) -> dict:
        return {
            "assetUrl": self.asset_url,
            "action": self.action.value,
            "type": self.type.value
        }