"""
Module that provides functions for connect RASA and Telegram Bots.

It send POST request with JSON data to RASA server
and get JSON data with answer from RASA.
"""

import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
)

from request_to_rasa import get_rasa_answer
from rzhd_assistant.vault import vault_utils


TELEGRAM_TOKEN = vault_utils.rtrieve_secret('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


async def rasa_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_rasa_answer(update.message.text),
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    echo_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND),
        rasa_answer,
    )

    application.add_handler(echo_handler)

    application.run_polling()
