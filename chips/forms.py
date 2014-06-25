# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, \
    SetPasswordForm, UserCreationForm

from captcha.fields import CaptchaField, CaptchaTextInput

from .models import Customer, PromoCode
from .utils import validate_code
from .utils import load_template_data, send_mail


class ThemedPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'fill-field', 'style': 'width: 630px;'}))

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"].lower()
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            tmpl_html = load_template_data('registration/password_reset_email.html', c)
            # msg = EmailMultiAlternatives()
            # msg.attach_alternative(tmpl_html, "text/html")
            # msg.send()
            send_mail(u'Сброс пароля', tmpl_html,
                                         settings.EMAIL_FROM,
                                         [self.cleaned_data['email']])


class ThemedSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=u"Новый пароль",
                                    widget=forms.PasswordInput(attrs={'class': 'fill-field'}))
    new_password2 = forms.CharField(label=u"Повторите пароль",
                                    widget=forms.PasswordInput(attrs={'class': 'fill-field'}))


class CodeForm(forms.ModelForm):

    def __init__(self, customer, data=None, *args, **kwargs):
        self.customer = customer
        super(CodeForm, self).__init__(data, *args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' red'
                    self.fields[f_name].widget.attrs['class'] = classes

    class Meta:
        exclude = ('customer', 'added', 'winner', 'prise_name', 'on_phase')
        model = PromoCode
        widgets = {
            'code': forms.TextInput(
                attrs={'style': 'width: 630px;', 'class': 'fill-field'}
            )
        }

    def clean_code(self):
        promo = self.cleaned_data.get('code')
        if validate_code(promo):
            return promo
        if not self.customer.should_be_blocked():
            if not self.customer.block_user():
                self.customer.add_wrong_code()
        raise forms.ValidationError("Неправильный промокод!")

    def save(self, commit=True):
        code = super(CodeForm, self).save(commit=False)
        code.customer = self.customer
        if commit:
            code.save()
        return code


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' red'
                    self.fields[f_name].widget.attrs['class'] = classes
                    print(self.fields[f_name].widget.attrs['class'])

    username = forms.CharField(
        max_length=254, widget=forms.EmailInput(attrs={'class':
                                                           'fill-field fill-field--w261 fill-field--w261--type'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':
                                              'fill-field fill-field--w261 fill-field--w261--type1'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            username = username.lower()
            self.user_cache = authenticate(username=username,
                                           password=password)

            if self.user_cache is None:
                self._errors['username'] = 'invalid_login'
                self._errors['password'] = 'invalid_login'
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                self._errors['username'] = 'inactive'
                self._errors['password'] = 'inactive'
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' red'
                    self.fields[f_name].widget.attrs['class'] = classes

    promo = forms.CharField(label=u'Введите промокод', required=False,
                            widget=forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 630px;'}))
    captcha = CaptchaField(label=u"Код на картинке", widget=CaptchaTextInput(attrs={'class': 'fill-field'}))

    rules_confirmation = forms.BooleanField(
        label=u'С условиями игры ознакомлен',
        widget=forms.CheckboxInput(attrs={'id': 'agreeCheck',
                                          'class': 'check-block__check'}))

    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput(attrs={'class': 'fill-field'}))
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'fill-field'}),
        help_text="Enter the same password as above, for verification.")

    promocode_failed = False

    class Meta:
        model = Customer
        exclude = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions', 'password', 'last_login',
                   'banks', 'blocks_count')
        labels = {
            "first_name": u"Имя",
            "last_name": u"Отчество",
            "surname": u"Фамилия",
            "post_index": u"Почтовый индекс",
            "region": u"Область",
            "district": u"Район",
            "city": u"Город",
            "street": u"Улица",
            "building": u"Дом",
            "corpus": u"Корпус",
            "apartment": u"Квартира",
            "phone": u"Телефон",
            "email": u"Адрес электронной почты",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 261px;'}),

            "last_name": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 261px;'}),

            "surname": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 261px;'}),

            "post_index": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 159px;'}),

            "region": forms.TextInput(attrs={'class': 'fill-field drop-panel__button select',
                                             'style': 'width: 221px;'}),
            "district": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 210px;'}),
            "city": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 180px;'}),
            "street": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 562px;'}),
            "building": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 71px;'}),
            "corpus": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 71px;'}),
            "apartment": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 71px;'}),
            "phone": forms.TextInput(attrs={'class': 'fill-field'}),
            "email": forms.EmailInput(attrs={'class': 'fill-field'}),
        }

    def clean_promo(self):
        promo = self.cleaned_data.get('promo', '')

        if len(promo.strip()) > 0:
            if validate_code(promo):
                return promo
            else:
                self.promocode_failed = True
                raise forms.ValidationError(u"Неправильный промокод!")
        return promo

    def is_promo_failed(self):
        return self.promocode_failed

    def save(self, commit=True):
        customer = super(RegistrationForm, self).save(commit=False)
        password = self.cleaned_data["password1"]
        customer.set_password(password)
        customer.email = customer.email.lower()
        if commit:
            customer.save()
            tmpl = load_template_data('mails/reg_confirm_text.html',
                                      {'password': password,
                                       'email': customer.email,
                                       'first_name': customer.first_name,
                                       'id': customer.pk})

            tmpl_html = load_template_data('mails/reg_confirm.html',
                                      {'password': password,
                                       'email': customer.email,
                                       'first_name': customer.first_name,
                                       'id': customer.pk})

            send_mail(u'Регистрация участия в рекламной игре «Онега. Вкусно перекуси – с удовольствием отдохни»',
                                         tmpl_html, settings.EMAIL_FROM,
                                         [self.cleaned_data['email']], text=tmpl)

            if len(self.cleaned_data.get('promo', '')) > 0:
                PromoCode.objects.create(customer=customer, code=self.cleaned_data['promo'])
        return customer

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data.get('email')
        if username:
            username = username.lower()
        email = username
        try:
            Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return email
        raise forms.ValidationError(u"Этот адрес уже занят")
