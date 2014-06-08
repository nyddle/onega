# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers

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
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Отчество')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    # todo: what is maxlength here?
    post_index = models.CharField(max_length=6, blank=True, verbose_name='Индекс')
    # todo: what is maxlength here?
    region = models.CharField(max_length=255, blank=True, verbose_name='Область')
    district = models.CharField(max_length=255, blank=True, verbose_name='Район')
    # todo: what is maxlength here?
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Ул.')
    building = models.CharField(max_length=255, verbose_name='Дом')
    corpus = models.CharField(max_length=255, blank=True, verbose_name='Корп.')
    apartment = models.IntegerField(max_length=255, blank=True, null=True, verbose_name='Кв.')
    phone = models.CharField(max_length=255, blank=True, verbose_name='Тел.')
    email = models.EmailField(unique=True, verbose_name='Почта')
    banks = models.IntegerField(default=0, verbose_name='Упаковок')

    blocks_count = models.IntegerField(default=0, verbose_name='Блокирован раз')

    is_staff = models.BooleanField(default=False, verbose_name='Админ')
    is_active = models.BooleanField(default=True, verbose_name='Разблокирован')

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def codes_amount(self):
        return self.promocode_set.count()

    codes_amount.short_description = u'Количество кодов'

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
            codes += '<a href="{}">{}</a>\n'.format(code.get_admin_url(), code.code)
        return codes

    get_codes.short_description = u'Промокоды'
    get_codes.allow_tags = True

    def is_user_blocked(self):
        if not self.is_active:
            return True
        codes = self.wrongcode_set.all().values_list('date', flat=True)[5:]

        if len(codes) > 4 and (codes[len(codes)-1] - codes[0]).days < 1:
            return True
        return False

    def add_wrong_code(self):
        WrongCode.objects.create(customer=self)

    def block_user(self):
        if self.is_user_blocked():
            self.blocks_count = self.blocks_count + 1
            if self.blocks_count > 2:
                self.is_active = False
            self.save()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


# todo: add initial data for settings
class SiteSettings(models.Model):
    """
    Keep site settings like photo gallery enabling/disabling
    """
    key = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    additional_data = models.TextField(blank=True)

    class Meta:
        verbose_name = 'настройки'
        verbose_name_plural = 'настройки'


class ValidCode(models.Model):
    code = models.CharField(max_length=255, unique=True, primary_key=True)

    class Meta:
        verbose_name = 'уникальный код'
        verbose_name_plural = 'уникальные коды'


class ImageGallery(models.Model):
    photo = ThumbnailerImageField(upload_to='images')

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'


class Phase(models.Model):
    PHASES = ((0, '1'), (1, '2'), (2, '3'), (3, 'Игра окончена'))
    current_phase = models.IntegerField(choices=PHASES, verbose_name='Фаза')
    date = models.DateField(null=True, blank=True, verbose_name='Дата окончания фазы')

    class Meta:
        verbose_name = 'фаза'
        verbose_name_plural = 'фазы'

    def __str__(self):
        return str(self.get_current_phase_display())


class PriseType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')

    class Meta:
        verbose_name = 'приз'
        verbose_name_plural = 'призы'

    def __str__(self):
        return str(self.name)


class PromoCode(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='Пользователь')
    # todo: what is maxlength here?
    code = models.CharField(max_length=255, unique=True, verbose_name='Код')
    added = models.DateTimeField(auto_now=True, verbose_name='Добавлен')
    winner = models.BooleanField(default=False, blank=True, verbose_name='Выигрышный код')
    on_phase = models.ForeignKey(Phase, null=True, blank=True, verbose_name='Фаза')
    prise_name = models.ForeignKey(PriseType, null=True, blank=True, verbose_name='Приз')

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    class Meta:
        verbose_name = 'пользовательский код'
        verbose_name_plural = 'пользовательские коды'


class WrongCode(models.Model):
    customer = models.ForeignKey(Customer)
    date = models.DateTimeField(auto_now=True)


class DiscreditedIP(models.Model):
    ip = models.CharField(max_length=100, unique=True)
    failed = models.IntegerField(default=0)
    blocked = models.IntegerField(default=0)


class WrongIPByCode(models.Model):
    date = models.DateTimeField(auto_now=True)
    ip = models.ForeignKey(DiscreditedIP)
