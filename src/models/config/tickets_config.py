from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class TicketsConfig(BaseConfig):
    guild_id: int
    ticket_channel_id: int | None = None
    ticket_message_id: int | None = None
    ticket_report_channel_id: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "ticketChannelId": self.ticket_channel_id,
            "ticketMessageId": self.ticket_message_id,
            "ticketReportChannelId": self.ticket_report_channel_id
        }