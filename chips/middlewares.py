# -*- coding: utf-8 -*-
from .utils import get_site_settings


class SettingsMiddleware(object):
    def process_request(self, request):
        request.settings = get_site_settings()
