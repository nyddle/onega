# -*- coding: utf-8 -*-
from django.template import loader, Context
from django.core.paginator import Paginator

from .models import SiteSettings, ValidCode, PromoCode


def get_site_settings():
    """
    Convert settings to dict
    """
    site_settings = SiteSettings.objects.all()
    result = {}
    for settings in site_settings:
        if settings.enabled:
            result[settings.key] = settings.additional_data
    return result


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_code(code):
    """
    Check is promo code valid
    """
    try:
        ValidCode.objects.get(code=code)
    except ValidCode.DoesNotExist:
        return False

    if PromoCode.objects.filter(code=code).first():
        return False
    return True


def load_template_data(template, context):
    t = loader.get_template(template)
    c = Context(context)
    rendered = t.render(c)
    return rendered


def get_winners_code(page_num=1, email=None):
    promocodes = PromoCode.objects.select_related().filter(winner=True)
    if email:
        promocodes = promocodes.filter(customer__email=email)
    paginator = Paginator(promocodes, 2)
    return paginator.page(page_num)
