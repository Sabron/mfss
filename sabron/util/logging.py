import os

from datetime import datetime
from django.conf import settings
from django.core.files import File


def set():
    if not os.path.exists(settings.MEDIA_ROOT):
        try:
            os.mkdir(settings.MEDIA_ROOT)
        except OSError:
            return

    if not os.path.exists(settings.MEDIA_ROOT+'/download'):
        try:
            os.mkdir(settings.MEDIA_ROOT+'/download')
        except OSError:
            return

    if not os.path.exists(settings.BASE_DIR + "/log"):
        try:
            os.mkdir(settings.BASE_DIR + "/log")
        except OSError:
            return
    if not os.path.exists(settings.BASE_DIR + "/log/message"):
        try:
            os.mkdir(settings.BASE_DIR + "/log/message")
        except OSError:
            return
    if not os.path.exists(settings.BASE_DIR + "/log/error"):
        try:
            os.mkdir(settings.BASE_DIR + "/log/error")
        except OSError:
            return
    if not os.path.exists(settings.BASE_DIR + "/log/log"):
        try:
            os.mkdir(settings.BASE_DIR + "/log/log")
        except OSError:
            return
    if not os.path.exists(settings.MEDIA_ROOT + "/tgbot"):
        try:
            os.mkdir(settings.MEDIA_ROOT + "/tgbot")
        except OSError:
            return



def message(message):
    DirLogs = settings.BASE_DIR + "/log"
    if not os.path.exists(DirLogs):
        try:
            os.mkdir(DirLogs)
        except OSError:
            return
    DirLogs = settings.BASE_DIR + "/log/message"
    if not os.path.exists(DirLogs):
        try:
            os.mkdir(DirLogs)
        except OSError:
            return
    date = datetime.now()
    month = "0" if date.month < 10 else ""
    month += str(date.month)
    day = "0" if date.day < 10 else ""
    day += str(date.day)
    StrDate = "%s%s%s" % (str(date.year), month, day)
    file = open(DirLogs + '/message_' + StrDate + '.log', 'a')
    my_file = File(file)
    my_file.write("[%s]: %s\n" % (
        str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
        str(message)
        ))
    my_file.closed
    file.closed


def log(message):
    DirLogs = settings.BASE_DIR + "/log"
    if not os.path.exists(DirLogs):
        try:
            os.mkdir(DirLogs)
        except OSError:
            return
    DirLogs = settings.BASE_DIR + "/log/log"
    if not os.path.exists(DirLogs):
        try:
            os.mkdir(DirLogs)
        except OSError:
            return
    date = datetime.now()
    month = "0" if date.month < 10 else ""
    month += str(date.month)
    day = "0" if date.day < 10 else ""
    day += str(date.day)
    StrDate = "%s%s%s" % (str(date.year), month, day)
    file = open(DirLogs + '/message_' + StrDate + '.log', 'a')
    my_file = File(file)
    my_file.write("[%s]: %s\n" % (
        str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
        str(message)))
    my_file.closed
    file.closed


def error(message):
    DirLogs = settings.BASE_DIR + "/log"
    if not os.path.exists(DirLogs):
        try:
            os.mkdir(DirLogs)
        except OSError:
            return
    DirLogs = settings.BASE_DIR + "/log/error"
    if not os.path.exists(DirLogs):
        try:
            os.mkdir(DirLogs)
        except OSError:
            return
    date = datetime.now()
    month = "0" if date.month < 10 else ""
    month += str(date.month)
    day = "0" if date.day < 10 else ""
    day += str(date.day)
    StrDate = "%s%s%s" % (str(date.year), month, day)
    file = open(DirLogs + '/errors_' + StrDate + '.log', 'a')
    my_file = File(file)
    my_file.write("[%s]: %s\n" % (
        str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
        str(message)))
    my_file.closed
    file.closed


def check_dir():
    try:
        if not os.path.exists(settings.MEDIA_ROOT):
            try:
                os.mkdir(settings.MEDIA_ROOT)
            except OSError:
                logging.error(traceback.format_exc())
                return
        if not os.path.exists(settings.MEDIA_ROOT+"/att"):
            try:
                os.mkdir(settings.MEDIA_ROOT+"/att")
            except OSError:
                logging.error(traceback.format_exc())
                return
        if not os.path.exists(settings.MEDIA_ROOT+"/att/biophoto"):
            try:
                os.mkdir(settings.MEDIA_ROOT+"/att/biophoto")
            except OSError:
                logging.error(traceback.format_exc())
                return
        if not os.path.exists(settings.ATT_ROOT):
            try:
                os.mkdir(settings.ATT_ROOT)
            except OSError:
                logging.error(traceback.format_exc())
                return
        if not os.path.exists(settings.ATT_ROOT+"/USERPIC"):
            try:
                os.mkdir(settings.ATT_ROOT+"/USERPIC")
            except OSError:
                logging.error(traceback.format_exc())
                return
    except Exception as err:
        logging.error('%s\n%s' % (traceback.format_exc(), str(err)))
