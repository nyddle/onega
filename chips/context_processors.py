# -*- coding: utf-8 -*-
from datetime import datetime

from django.utils import timezone

from .models import Phase


def get_settings(request):
    video = False
    gallery = False
    if request.settings.get('gallery'):
        gallery = True
    if request.settings.get('video') is not None:

        video = True
    return {'is_video_enabled': video, 'is_gallery_enabled': gallery}


def get_remaining_time(request):
    phase = Phase.objects.all().first()
    if not phase:
        to_the_end_of_phase = None
    else:
        try:
            now = datetime.utcnow().replace(tzinfo=timezone.get_default_timezone()).now()
            to_the_end_of_phase = (datetime.combine(phase.date, datetime.min.time()) - now).days + 1
            if to_the_end_of_phase < 0:
                to_the_end_of_phase = None
        except:
            to_the_end_of_phase = None

    if to_the_end_of_phase is not None:
        days = _get_pronounce(to_the_end_of_phase)
    else:
        days = None
    return {'to_the_end_of_phase': to_the_end_of_phase, 'days': days,
            'current_phase': phase.current_phase}


def _get_pronounce(val):
    str_v = str(val)
    last = str_v[-1]
    if len(str_v) == 1:
        if last == u'1':
            return u'день'
        elif last in (u'2', u'3', u'4'):
            return u'дня'

    return u'дней'