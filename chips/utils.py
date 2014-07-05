# -*- coding: utf-8 -*-
from django.template import loader, Context
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import SiteSettings, ValidCode, PromoCode, Customer


def get_site_settings():
    """
    Convert settings to dict
    """
    site_settings = SiteSettings.objects.all()
    result = {}
    for settings in site_settings:
        if settings.enabled:
            result[settings.key] = settings.additional_data
    print(result)
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
        data = email.split()
        query = Q(email__icontains=email)
        for entry in data:
            query = query | Q(first_name__icontains=entry) | \
                    Q(last_name__icontains=entry) | Q(surname__icontains=entry)

        promocodes = promocodes.filter(Q(customer__in=Customer.objects.filter(query)) | Q(code__icontains=email))
        # if len(promocodes) == 0:
        #     promocodes = promocodes.filter(code__icontains=email)
    paginator = Paginator(promocodes, 40)
    return paginator.page(page_num)


def send_mail(theme, html, from_, to, text=None):
    msg = EmailMultiAlternatives(theme, body=html, from_email=from_, to=to)
    msg.attach_alternative(html, "text/html")
    try:
        r = msg.send()
        print r
    except Exception as exc:
        print(exc)
