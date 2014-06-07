# -*- coding: utf-8 -*-
from .models import SiteSettings, ValidCode, PromoCode


def get_site_settings():
    """
    Convert setting to dict
    """
    site_settings = SiteSettings.objects.all()
    result = {}
    for settings in site_settings:
        if settings.enabled:
            result[settings.key] = settings.additional_data
    return result


def validate_code(code):
    try:
        ValidCode.objects.get(code=code)
    except ValidCode.DoesNotExist:
        return False

    if PromoCode.objects.filter(code=code).first():
        return False

    return True
