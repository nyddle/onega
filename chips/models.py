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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    # todo: what is maxlength here?
    post_index = models.CharField(max_length=6, blank=True)
    # todo: what is maxlength here?
    region = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)
    # todo: what is maxlength here?
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    corpus = models.CharField(max_length=255, blank=True)
    apartment = models.IntegerField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    blocked_at = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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


# todo: add initial data for settings
class SiteSettings(models.Model):
    """
    Keep site settings as pairs
    """
    key = models.CharField(max_length=255)
    value = models.BooleanField(default=False)
    additional_data = models.TextField(blank=True)


class PromoCode(models.Model):
    customer = models.ForeignKey(Customer)
    # todo: what is maxlength here?
    code = models.CharField(max_length=255, unique=True)


class ValidCode(models.Model):
    code = models.CharField(max_length=255, unique=True)


class ImageGallery(models.Model):
    photo = ThumbnailerImageField(upload_to='images')


class VideoGallery(models.Model):
    video = models.FileField(upload_to='videos')
