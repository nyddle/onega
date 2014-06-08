# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from captcha.fields import CaptchaField, CaptchaTextInput

from .models import Customer, PromoCode
from .utils import validate_code
from .utils import load_template_data


class ThemedPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'fill-field'}))


class ThemedSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Новый пароль",
                                    widget=forms.PasswordInput(attrs={'class': 'fill-field'}))
    new_password2 = forms.CharField(label="Повторите пароль",
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
        self.customer.add_wrong_code()
        self.customer.block_user()
        raise forms.ValidationError("Неправильный промокод!")

    def save(self, commit=True):
        code = super(CodeForm, self).save(commit=False)
        code.customer = self.customer
        if commit:
            code.save()
        return code


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' fill-field--w261--type--red-field'
                    self.fields[f_name].widget.attrs['class'] = classes

    username = forms.CharField(max_length=254, widget=forms.EmailInput(attrs={'class': 'fill-field fill-field--w261 fill-field--w261--type'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fill-field fill-field--w261 fill-field--w261--type1'}))


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' red'
                    self.fields[f_name].widget.attrs['class'] = classes

    promo = forms.CharField(label='Введите промокод', required=False,
                            widget=forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 630px;'}))
    captcha = CaptchaField(label="Код на картинке", widget=CaptchaTextInput(attrs={'class': 'fill-field'}))

    rules_confirmation = forms.BooleanField(
        label='С условиями игры ознакомлен',
        widget=forms.CheckboxInput(attrs={'id': 'agreeCheck',
                                          'class': 'check-block__check'}))

    promocode_failed = False

    class Meta:
        model = Customer
        exclude = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions', 'password', 'last_login',
                   'banks', 'blocks_count')
        labels = {
            "first_name": "Имя",
            "last_name": "Отчество",
            "surname": "Фамилия",
            "post_index": "Почтовый индекс",
            "region": "Область",
            "district": "Район",
            "city": "Город",
            "street": "Улица",
            "building": "Дом",
            "corpus": "Корпус",
            "apartment": "Квартира",
            "phone": "Телефон",
            "email": "Адрес электронной почты",
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
            "phone": forms.TextInput(attrs={'class': 'fill-field', 'style': 'width: 562px;'}),
            "email": forms.EmailInput(attrs={'class': 'fill-field', 'style': 'width: 562px;'}),
        }

    def clean_promo(self):
        promo = self.cleaned_data.get('promo', '')

        if len(promo.strip()) > 0:
            if validate_code(promo):
                return promo
            else:
                self.promocode_failed = True
                raise forms.ValidationError("Неправильный промокод!")
        return promo

    def is_promo_failed(self):
        return self.promocode_failed

    def save(self, commit=True):
        customer = super(RegistrationForm, self).save(commit=False)
        password = Customer.objects.make_random_password()
        customer.set_password(password)
        if commit:
            send_mail(u'Регистрация завершена',
                      u"Вы успешно зарегистрировались! Ваш пароль %s" % password,
                      settings.EMAIL_FROM, [self.cleaned_data['email']])
            customer.save()
            # todo: add to user
            if len(self.cleaned_data.get('promo', '')) > 0:
                PromoCode.objects.create(customer=customer, code=self.cleaned_data['promo'])
        return customer

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return email
        raise forms.ValidationError("Этот адрес уже занят")
