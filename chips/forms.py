# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

from captcha.fields import CaptchaField, CaptchaTextInput

from .models import Customer, PromoCode
from .utils import validate_code


class CodeForm(forms.ModelForm):
    error_css_class = 'red'

    def __init__(self, customer, data=None, *args, **kwargs):
        self.customer = customer
        super().__init__(data, *args, **kwargs)

    class Meta:
        exclude = ('customer', 'added', 'winner')
        model = PromoCode

    def clean_code(self):
        promo = self.cleaned_data.get('code')
        if validate_code(promo):
            return promo
        raise forms.ValidationError("Неправильный промокод!")

    def save(self, commit=True):
        code = super().save(commit=False)
        code.customer = self.customer
        if commit:
            code.save()
        return code

#
# class LoginForm(AuthenticationForm):
#     pass


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    class Meta:
        model = Customer
        exclude = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions', 'password', 'last_login',
                   'blocked_at', 'banks')
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
                raise forms.ValidationError("Неправильный промокод!")
        return promo

    def save(self, commit=True):
        customer = super().save(commit=False)
        password = Customer.objects.make_random_password()
        customer.set_password(password)
        if commit:
            send_mail('Регистрация завершена', "Вы успешно зарегистрировались! Ваш пароль %s" % password,
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
