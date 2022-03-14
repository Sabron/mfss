import os
import random

from sabron.models import Settings


def set_settings(name,value):
    settings_token = Settings.objects.filter(name = name).first()
    if settings_token is None:
        Settings.objects.create(
            name = name,
            value = value)
    else:
        settings_token.value =value
        settings_token.save()

def get_settings(name):
    settings_token = Settings.objects.filter(name = name).first()
    if settings_token is None:
        Settings.objects.create(
                name = name,
                value='')
        return ''
    else:
        return settings_token.value


def generate_random_string(length):
    letters = 'WERTYUPASDFHKMNBVCXZ123654789wertyupkhfdsazxcvbnm'
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


