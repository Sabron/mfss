"""
    Telegram event handlers
"""

import telegram
import traceback

from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler,CallbackContext,
)

from celery.decorators import task  # event processing in async mode

from mfss.settings import TELEGRAM_TOKEN

from tgbot.handlers import admin, commands, files, location
from tgbot.handlers.commands import broadcast_command_with_message
from tgbot.handlers.handlers import secret_level, broadcast_decision_handler
from tgbot.handlers.manage_data import SECRET_LEVEL_BUTTON, CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.static_text import broadcast_command
from tgbot.models import User
from tgbot.handlers.utils import send_message

from django.conf import settings


from sabron.util import logging


def echo(update: telegram.Update, context: CallbackContext) -> None:
    """Echo the user message."""
    try:
        
        text = "Добрый день"
         
        return update.message.reply_text(
            text, 
            parse_mode='HTML',
            disable_web_page_preview=True,
            )
    except Exception as err:
        send_message(
            user_id=64798462,
            text=str(traceback.format_exc()),
            entities=None,
            parse_mode=None)
        logging.error(traceback.format_exc())


def setup_dispatcher(dp):
    """
    Добавление обработчиков событий из Telegram
    """

    dp.add_handler(CommandHandler("start", commands.command_start))

    # admin commands
    dp.add_handler(CommandHandler("admin", admin.admin))
    dp.add_handler(CommandHandler("stats", admin.stats))
    dp.add_handler(CommandHandler("infouser", admin.infouser))

    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    # location
    #dp.add_handler(CommandHandler("ask_location", location.ask_for_location))
    #dp.add_handler(MessageHandler(Filters.location, location.location_handler))


    #dp.add_handler(CallbackQueryHandler(secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))

    #dp.add_handler(MessageHandler(Filters.regex(rf'^{broadcast_command} .*'), broadcast_command_with_message))
    #dp.add_handler(CallbackQueryHandler(broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}"))



    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))




    #EXAMPLES FOR HANDLERS
    #dp.add_handler(MessageHandler(Filters.text, text))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


def run_pooling(): # работа не черех Web hook
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()


@task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


# Global variable - best way I found to init Telegram bot
bot = telegram.Bot(TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]