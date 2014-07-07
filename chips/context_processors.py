# -*- coding: utf-8 -*-
from datetime import datetime

from django.utils import timezone

from .models import Raffle


def get_settings(request):
    video = False
    gallery = False
    if request.settings.get('gallery'):
        gallery = True
    if request.settings.get('video') is not None:
        video = True
    prize = request.settings.get('super_prize', 0)

    return {'is_video_enabled': video, 'is_gallery_enabled': gallery,
            'super_prize': prize}


def get_remaining_time(request):
    raffle = Raffle.objects.all().first()
    if not raffle:
        to_the_end_of_raffle = None
    else:
        try:
            now = datetime.utcnow().replace(tzinfo=timezone.get_default_timezone()).now()
            to_the_end_of_raffle = (datetime.combine(raffle.date, datetime.min.time()) - now).days + 1
            if to_the_end_of_raffle < 0:
                to_the_end_of_raffle = None
        except:
            to_the_end_of_raffle = None

    if to_the_end_of_raffle is not None:
        days = _get_pronounce(to_the_end_of_raffle)
    else:
        days = None
    if raffle:
        return {'to_the_end_of_raffle': to_the_end_of_raffle, 'days': days,
            'current_raffle': raffle.number}
    else:
        return {'to_the_end_of_raffle': to_the_end_of_raffle, 'days': days,
               'current_raffle': '1'}


def _get_pronounce(val):
    str_v = str(val)
    last = str_v[-1]
    if len(str_v) == 1:
        if last == u'1':
            return u'день'
        elif last in (u'2', u'3', u'4'):
            return u'дня'
    return u'дней'
