import json
import logging
import traceback
from django.views import View
from django.http import JsonResponse

from mfss.settings import DEBUG

from tgbot.handlers.dispatcher import process_telegram_event, TELEGRAM_BOT_USERNAME

from apps.util import generalmodule


logger = logging.getLogger(__name__)

BOT_URL = f"https://t.me/{TELEGRAM_BOT_USERNAME}"


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again. 
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        try:
            if DEBUG:
                process_telegram_event(json.loads(request.body))
            else:  # use celery in production
                process_telegram_event.delay(json.loads(request.body))

            # TODO: there is a great trick to send data in webhook response
            # e.g. remove buttons
            return JsonResponse({"ok": "POST request processed"})
        except Exception as err:
            generalmodule.error(traceback.format_exc())    
            return JsonResponse({"ok": "POST request processed"})
    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})
