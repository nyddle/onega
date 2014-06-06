# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail

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
    blocked_at = models.DateTimeField(null=True, blank=True, verbose_name='')
    banks = models.IntegerField(default=0, verbose_name='Упаковок')

    is_staff = models.BooleanField(default=False, verbose_name='Админ')
    is_active = models.BooleanField(default=True, verbose_name='Разблокирован')

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def codes_amount(self):
        return self.promocode_set.count()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
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
    code = models.CharField(max_length=255, unique=True)

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
    current_phase = models.IntegerField(choices=PHASES)
    date = models.DateField()

    class Meta:
        verbose_name = 'фаза'
        verbose_name_plural = 'фазы'


class PriseType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'приз'
        verbose_name_plural = 'призы'


class PromoCode(models.Model):
    customer = models.ForeignKey(Customer)
    # todo: what is maxlength here?
    code = models.CharField(max_length=255, unique=True)
    added = models.DateTimeField(auto_now=True)
    winner = models.BooleanField(default=False)
    on_phase = models.ForeignKey(Phase, null=True)
    prise_name = models.ForeignKey(PriseType, null=True)

    class Meta:
        verbose_name = 'пользовательский код'
        verbose_name_plural = 'пользовательские коды'
