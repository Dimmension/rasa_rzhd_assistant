import asyncio
import json
import logging
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from aiogram import Bot
from aiogram.types import (
    Update,
    Message,
)
from aiogram.utils.exceptions import TelegramAPIError
from typing import Dict, Text, Any, List, Optional, Callable, Awaitable

from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel
from rasa.shared.exceptions import RasaException

logger = logging.getLogger(__name__)


class DiscordOutput(OutputChannel):
    """Output channel for Telegram."""

    @classmethod
    def name(cls) -> Text:
        return "telegram"

    def __init__(self, access_token: Optional[Text]) -> None:
        super().__init__(access_token)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Sends text message."""
        for message_part in text.strip().split("\n\n"):
            await self.send_message(recipient_id, message_part)


class DiscordInput(InputChannel):
    """Discord input channel"""

    @classmethod
    def name(cls) -> Text:
        return "discord"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(
            credentials.get("access_token"),
            credentials.get("webhook_url"),
        )

    def __init__(
        self,
        access_token: Optional[Text],
        webhook_url: Optional[Text],
        debug_mode: bool = True,
    ) -> None:
        self.access_token = access_token
        self.webhook_url = webhook_url
        self.debug_mode = debug_mode

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:
        discord_webhook = Blueprint("discord_webhook", __name__)
        out_channel = DiscordOutput(self.access_token)

        @discord_webhook.route("/", methods=["GET"])
        async def health(_: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @discord_webhook.route("/webhook", methods=["GET", "POST"])
        async def message(request: Request) -> Any:
            if request.method == "POST":

                request_dict = request.json
                if isinstance(request_dict, Text):
                    request_dict = json.loads(request_dict)
                update = Update(**request_dict)
                credentials = await out_channel.get_me()
                if not credentials.username == self.verify:
                    logger.debug(
                        "Invalid access token, check it matches Telegram")
                    return response.text("failed")

                msg = update.message
                if self._is_user_message(msg):
                    text = msg.text.replace("/bot", "")

                sender_id = msg.chat.id
                metadata = self.get_metadata(request)
                try:
                    await on_new_message(
                        UserMessage(
                            text,
                            out_channel,
                            sender_id,
                            input_channel=self.name(),
                            metadata=metadata,
                        )
                    )
                except Exception as e:
                    logger.error(
                        f"Exception when trying to handle message.{e}")
                    logger.debug(e, exc_info=True)
                    if self.debug_mode:
                        raise
                    pass

                return response.text("success")

        return discord_webhook

    def get_output_channel(self) -> TelegramOutput:
        """Loads the telegram channel."""
        channel = TelegramOutput(self.access_token)

        try:
            asyncio.run(channel.set_webhook(url=self.webhook_url))
        except TelegramAPIError as error:
            raise RasaException(
                "Failed to set channel webhook: " + str(error)
            ) from error

        return channel
