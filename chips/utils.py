# -*- coding: utf-8 -*-
from .models import SiteSettings, ValidCode


def get_site_settings():
    """
    Convert setting to dict
    """
    site_settings = SiteSettings.objects.all()
    return {settings.key: settings.value for settings in site_settings}


def validate_code(code):
    try:
        ValidCode.objects.get(code=code)
    except ValidCode.DoesNotExist:
        return False
    return True
