# -*- coding: utf-8 -*-
from .utils import get_site_settings
from .models import Phase


class SettingsMiddleware(object):

    def process_request(self, request):
        request.settings = get_site_settings()
        phase = Phase.objects.filter().first()
        request.phase = phase.current_phase
