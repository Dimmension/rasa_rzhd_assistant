"""
Module that provides functions for connect RASA and Telegram Bots.

It send POST request with JSON data to RASA server
and get JSON data with answer from RASA.
"""
import os

import telegram
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from request_to_rasa import get_rasa_json

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


async def rasa_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_rasa_json(update.message.text),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*Привет я Виталий, цифровой помощник Могу рассказать тебе о ПТЭ*',
        # parse_mode=telegram.constants.PARSEMODE_MARKDOWN_V2,
        parse_mode='MarkdownV2',
    )


if __name__ == '__main__':
    application = (
        ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    )

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), rasa_answer,
    )

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
