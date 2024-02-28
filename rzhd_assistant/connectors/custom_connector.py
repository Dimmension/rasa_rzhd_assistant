import inspect
import logging

from typing import Text, Callable, Awaitable
from asyncio import CancelledError
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)

logger = logging.getLogger(__name__)


class CustomConnector(InputChannel):
    @classmethod
    def name(cls) -> Text:
        """Return name of custom_chennel for using in Rasa.

        Returns:
            Text: name of custom_chennel
        """
        return "custom_connector"

    def blueprint(
        self,
        on_new_message: Callable[[UserMessage], Awaitable[None]],
    ) -> Blueprint:
        """Process incoming requests."""

        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            text = request.json.get("text")
            input_channel = self.name()
            metadata = self.get_metadata(request)

            collector = CollectingOutputChannel()

            try:
                await on_new_message(
                    UserMessage(
                        text,
                        collector,
                        input_channel=input_channel,
                        metadata=metadata,
                    ),
                )
            except CancelledError:
                logger.error(
                    f'Message handling timed out for user message "{text}".',
                )
            except Exception:
                logger.exception(
                    f'Exception occured while handling user message "{text}".',
                )

            return response.json(collector.messages)

        return custom_webhook
