import asyncio
import json
import logging

from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

from vk_api import VkApi
from vk_api.utils import get_random_id

from typing import Dict, Text, Any, List, Optional, Callable, Awaitable

from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel
from rasa.shared.exceptions import RasaException

logger = logging.getLogger(__name__)


class VkOutput(OutputChannel):
    """Output channel for Vk."""

    @classmethod
    def name(cls) -> Text:
        return 'vk'

    def __init__(self, access_token: Text) -> None:
        self.access_token = access_token
        self.vk = VkApi(token=self.access_token)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any,
    ) -> None:
        logger.warning(
            f'MESSAGE, THAT WILL BE SENDED: to {recipient_id}, with TEXT: {text}')
        """Send text message."""
        for message_part in text.strip().split('\n\n'):
            self.vk.method('messages.send', {
                'user_id': recipient_id,  # 65423827
                'message': message_part,
                'random_id': get_random_id(),
            })


class VkInput(InputChannel):
    """Telegram input channel."""

    @classmethod
    def name(cls) -> Text:
        return 'vk'

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        """Load creditionals"""
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(
            credentials.get('access_token'),
            credentials.get('secret_key'),
            credentials.get('webhook_url'),
        )

    def __init__(
        self,
        access_token: Optional[Text],
        secret_key: Optional[Text],
        webhook_url: Optional[Text],
        debug_mode: bool = True,
    ) -> None:
        self.access_token = access_token
        self.secret_key = secret_key
        self.webhook_url = webhook_url
        self.debug_mode = debug_mode

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]],
    ) -> Blueprint:
        vk_webhook = Blueprint('vk_webhook', __name__)
        out_channel = VkOutput(self.access_token)

        @vk_webhook.route('/', methods=['GET'])
        async def health(_: Request) -> HTTPResponse:
            return response.json({'status': 'ok'})

        @vk_webhook.route('/webhook', methods=['GET', 'POST'])
        async def message(request: Request) -> Any:
            if request.method == 'POST':

                request_dict = request.json

                if isinstance(request_dict, Text):
                    request_dict = json.loads(request_dict)

                if 'type' not in request_dict.keys():
                    return response.text('not vk')

                if request_dict['type'] == 'confirmation':
                    return response.text(self.secret_key)

                if request_dict['type'] == 'message_new':
                    sender_id = request_dict['object']['message']['from_id']
                    text = request_dict['object']['message']['text']

                    metadata = self.get_metadata(request_dict)

                    try:
                        await on_new_message(
                            UserMessage(
                                text,
                                out_channel,
                                sender_id,
                                input_channel=self.name(),
                                metadata=metadata,
                            ),
                        )

                    except Exception as error:
                        logger.error(
                            f'Exception when trying to handle message.{error}')
                        logger.debug(error, exc_info=True)
                        if self.debug_mode:
                            raise
                        pass
                return response.text('ok')

        return vk_webhook
