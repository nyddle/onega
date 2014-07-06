# -*- coding: utf-8 -*-
from datetime import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from cloudinary.models import CloudinaryField

from easy_thumbnails.fields import ThumbnailerImageField


class CustomerManager(BaseUserManager):
    """
    Override default django model manager for django auth
    """
    def create_user(self, email, password, first_name, last_name, surname, city, street, building, **extra_fields):
        return self._create_user(email, password, first_name, last_name, surname, city, street, building, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # it's not a regular user.
        return self._create_user(email, password, '', '', '', '', '', '', True, True, **extra_fields)

    def _create_user(self, email, password, first_name, last_name, surname, city, street, building, is_staff=False,
                     is_superuser=False, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, city=city,
                          first_name=first_name, last_name=last_name, surname=surname, street=street, building=building,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    """
    User model
    """
    first_name = models.CharField(max_length=100, verbose_name=u'Имя')
    last_name = models.CharField(max_length=100, verbose_name=u'Отчество')
    surname = models.CharField(max_length=100, verbose_name=u'Фамилия')
    # todo: what is maxlength here?
    post_index = models.CharField(max_length=6, blank=True, verbose_name=u'Индекс')
    # todo: what is maxlength here?
    region = models.CharField(max_length=255, blank=True, verbose_name=u'Область')
    district = models.CharField(max_length=255, blank=True, verbose_name=u'Район')
    # todo: what is maxlength here?
    city = models.CharField(max_length=255, verbose_name=u'Город')
    street = models.CharField(max_length=255, verbose_name=u'Ул.')
    building = models.CharField(max_length=255, verbose_name=u'Дом')
    corpus = models.CharField(max_length=255, blank=True, verbose_name=u'Корп.')
    apartment = models.IntegerField(max_length=255, blank=True, null=True, verbose_name=u'Кв.')
    phone = models.CharField(max_length=255, blank=True, verbose_name=u'Тел.')
    email = models.EmailField(unique=True, verbose_name=u'Почта')
    banks = models.IntegerField(default=0, verbose_name=u'Упаковок')

    blocks_count = models.IntegerField(default=0, verbose_name=u'Блокирован раз')

    is_staff = models.BooleanField(default=False, verbose_name=u'Админ')
    is_active = models.BooleanField(default=True, verbose_name=u'Разблокирован')

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def codes_amount(self):
        return self.promocode_set.count()

    codes_amount.short_description = u'Количество кодов'

    def __unicode__(self):
        return u'№{}({})'.format(self.get_ugly_ID(), self.email)

    def get_ugly_ID(self):
        str_id = str(self.pk)
        while len(str_id) < 7:
            str_id = '0{}'.format(str_id)
        return str_id

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.surname, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_codes(self):
        codes = ''
        for code in self.promocode_set.all():
            codes += u'<a href="{}">{}</a>\n'.format(code.get_admin_url(), code.code)
        return codes

    get_codes.short_description = u'Промокоды'
    get_codes.allow_tags = True

    def should_be_blocked(self):
        if not self.is_active:
            return True
        codes = self.wrongcode_set.all().order_by('-date').values_list(u'date',
                                                                       flat=True)[:5]
        if len(codes) > 4:
            if (codes[0] - codes[len(codes)-1]).days < 1:
                now = datetime.utcnow().replace(
                    tzinfo=timezone.get_default_timezone()).now()
                if (now - datetime.combine(codes[len(codes)-1],
                                           datetime.min.time())).days < 1:
                    return True
                else:
                    for code in self.wrongcode_set.all().order_by('-date'):
                        if (now - datetime.combine(
                                code.date, datetime.min.time())).days > 1:
                            code.delete()
        return False

    def add_wrong_code(self):
        self.wrongcode_set.create(customer=self)

    def block_user(self):
        if self.should_be_blocked():
            self.blocks_count = self.blocks_count + 1
            if self.blocks_count > 2:
                self.is_active = False
            self.save()
            return True
        return False

    class Meta:
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'


class SiteSettings(models.Model):
    """
    Keep site settings like photo gallery enabling/disabling
    """
    key = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    additional_data = models.TextField(blank=True)

    class Meta:
        verbose_name = u'настройки'
        verbose_name_plural = u'настройки'


class ValidCode(models.Model):
    code = models.CharField(max_length=255, unique=True, primary_key=True)

    class Meta:
        verbose_name = u'уникальный код'
        verbose_name_plural = u'уникальные коды'


class ImageGallery(models.Model):
    photo = CloudinaryField(upload_to=u'images')
    link = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = u'изображение'
        verbose_name_plural = u'изображения'


class Phase(models.Model):
    PHASES = ((0, u'1'), (1, u'2'), (2, u'3'), (3, u'Игра окончена'))
    current_phase = models.IntegerField(choices=PHASES, verbose_name=u'Фаза')
    date = models.DateField(null=True, blank=True, verbose_name=u'Дата окончания фазы')

    class Meta:
        verbose_name = u'фаза'
        verbose_name_plural = u'фазы'

    def __str__(self):
        return str(self.get_current_phase_display())


class PriseType(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Наименование')

    class Meta:
        verbose_name = u'приз'
        verbose_name_plural = u'призы'

    def __str__(self):
        return self.name.encode('utf-8')


class Raffle(models.Model):
    date = models.DateField(verbose_name=u'Дата розыгрыша')
    number = models.IntegerField()

    @classmethod
    def get_current_raffle(self):
        now = datetime.utcnow().replace(
                tzinfo=timezone.get_default_timezone()).now()
        return self.objects.filter(date__gte=now).order_by('date').first()

    def __str__(self):
        return str(self.number)


class PromoCode(models.Model):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('raffle').default = Raffle.get_current_raffle()
        super(PromoCode, self).__init__(*args, **kwargs)

    PHASES = ((0, u'1'), (1, u'2'), (2, u'3'), (3, u'Игра окончена'))
    customer = models.ForeignKey(Customer, verbose_name=u'Пользователь')
    code = models.CharField(max_length=255, unique=True, verbose_name=u'Код')
    added = models.DateTimeField(auto_now=True, verbose_name=u'Добавлен')
    winner = models.BooleanField(default=False, blank=True,
                                 verbose_name=u'Выигрышный код')

    phase = models.IntegerField(null=True, blank=True, verbose_name=u'Фаза',
                                choices=PHASES, default=0)

    raffle = models.ForeignKey(Raffle, null=True)
    prise_name = models.ForeignKey(PriseType, null=True, blank=True,
                                   verbose_name=u'Приз')

    def user_id(self):
        return self.customer.get_ugly_ID()

    def get_full_name(self):
        return self.customer.get_full_name()

    user_id.short_description = u'ID пользователя'
    get_full_name.short_description = u'Полное имя'

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse(u"admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def save(self, *args, **kwargs):
        if self.winner:
            self.raffle = Raffle().get_current_raffle()
            try:
                self._send_win_message()
            except:
                pass
        try:
            phase = Phase.objects.first().current_phase
            self.phase = phase
        except:
            pass
        super(PromoCode, self).save(*args, **kwargs)

    def _send_win_message(self):
        from .utils import load_template_data, send_mail
        tmpl_html = load_template_data('mails/winner.html', {
            'customer': self.customer,
            'prize': self.prise_name
        })
        send_mail(u'Победа в рекламной игре «Онега. '
                  u'Вкусно перекуси – с удовольствием отдохни»',
                  tmpl_html, settings.EMAIL_FROM, [self.customer.email])

    class Meta:
        verbose_name = u'пользовательский код'
        verbose_name_plural = u'пользовательские коды'


class WrongCode(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=u'Пользователь')
    date = models.DateTimeField(auto_now=True, verbose_name=u'Дата логина')

    class Meta:
        verbose_name = u'ввод неверного кода'
        verbose_name_plural = u'вводы неверного кода'

    def __unicode__(self):
        return str(self.date.strftime("%b %d %Y %H:%M:%S"))


class DiscreditedIP(models.Model):
    ip = models.CharField(max_length=100, unique=True)
    failed = models.IntegerField(default=0, verbose_name=u'Количество ошибок')
    blocked = models.IntegerField(default=0,
                                  verbose_name=u'Количество блокировок')

    class Meta:
        verbose_name = u'дискредетированный IP'
        verbose_name_plural = u'дискредетированные IP'


class WrongIPByCode(models.Model):
    date = models.DateTimeField(auto_now=True)
    ip = models.ForeignKey(DiscreditedIP)
