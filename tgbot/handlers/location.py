import traceback
import telegram

from tgbot.handlers.static_text import share_location, thanks_for_location
from tgbot.models import User, Location

from apps.util import generalmodule

def ask_for_location(update, context):
    """ Entered /ask_location command"""
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id, text=share_location,
        reply_markup=telegram.ReplyKeyboardMarkup([
            [telegram.KeyboardButton(text="Send 🌏🌎🌍", request_location=True)]
        ], resize_keyboard=True), #'False' will make this button appear on half screen (become very large). Likely,
        # it will increase click conversion but may decrease UX quality.
    )


def location_handler(update, context):
    try:
        u = User.get_user(update, context)
        lat, lon = update.message.location.latitude, update.message.location.longitude
        # TODO Зависает при добавлении 
        #l = Location.objects.create(user=u, latitude=lat, longitude=lon)
        update.message.reply_text('OK')
        update.message.reply_text(
            thanks_for_location,
            reply_markup=telegram.ReplyKeyboardRemove(),
        )    
    except Exception as err:
        generalmodule.error(traceback.format_exc())  
