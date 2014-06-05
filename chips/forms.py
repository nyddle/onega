# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
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
    error_css_class = 'red'

    promo = forms.CharField(label='Введите промокод', required=False)
    captcha = CaptchaField(label="Код на картинке",
                           widget=CaptchaTextInput(
                               attrs={'class': 'fill-field'}))

    rules_confirmation = forms.BooleanField(
        label='С условиями игры ознакомлен',
        widget=forms.CheckboxInput(attrs={'id': 'agreeCheck',
                                          'class': 'check-block__check'}))

    class Meta:
        model = Customer
        exclude = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions', 'password', 'last_login',
                   'blocked_at')
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
            "first_name": forms.TextInput(attrs={'class': 'fill-field'}),

            "last_name": forms.TextInput(attrs={'class': 'fill-field'}),

            "surname": forms.TextInput(attrs={'class': 'fill-field'}),

            "post_index": forms.TextInput(attrs={'class': 'fill-field'}),

            "region": forms.TextInput(attrs={'class': 'fill-field'}),

            "district": forms.TextInput(attrs={'class': 'fill-field'}),

            "city": forms.TextInput(attrs={'class': 'fill-field'}),
            "street": forms.TextInput(attrs={'class': 'fill-field'}),
            "building": forms.TextInput(attrs={'class': 'fill-field'}),
            "corpus": forms.TextInput(attrs={'class': 'fill-field'}),
            "apartment": forms.TextInput(attrs={'class': 'fill-field'}),
            "phone": forms.TextInput(attrs={'class': 'fill-field'}),
            "email": forms.EmailInput(attrs={'class': 'fill-field'}),
        }

    def clean_promo(self):
        promo = self.cleaned_data.get('promo', '')
        if len(promo) > 0 and validate_code(promo):
            return promo
        raise forms.ValidationError("Неправильный промокод!")

    def save(self, commit=True):
        customer = super().save(commit=False)
        password = Customer.objects.make_random_password()
        # todo: send mail
        customer.set_password(password)
        if commit:
            customer.save()
            customer = authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password1'])
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
