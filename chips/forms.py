# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from captcha.fields import CaptchaField, CaptchaTextInput

from .models import Customer, PromoCode
from .utils import validate_code


class CodeForm(forms.ModelForm):
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


class RegistrationForm(forms.ModelForm):
    promo = forms.CharField(label='Введите промокод')
    captcha = CaptchaField(label="Код на картинке",
                           widget=CaptchaTextInput(
                               attrs={'class': 'fill-field fill-field--w209 '
                                               'fill-field--w209--type'}))

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
            "first_name": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w261 '
                             'fill-field--w261--type1'}),

            "last_name": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w261 '
                             'fill-field--w261--type2'}),

            "surname": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w261 '
                             'fill-field--w261--type'}),

            "post_index": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w159 '
                             'fill-field--w159--type'}),
            "region": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w221 fill-field-'
                             '-w221--type drop-panel__button select'}),

            "district": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w210 '
                             'fill-field--w210--type'}),

            "city": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w180 '
                             'fill-field--w180--type'}),
            "street": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w562 '
                             'fill-field--w562--type'}),
            "building": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w71 '
                             'fill-field--w71--type'}),
            "corpus": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w71 '
                             'fill-field--w71--type'}),
            "apartment": forms.TextInput(
                attrs={
                    'class': 'fill-field fill-field--w71 '
                             'fill-field--w71--type'}),
            "phone": forms.TextInput(
                attrs={
                'class': 'fill-field fill-field--w562 '
                         'fill-field--w562--type'}),
            "email": forms.EmailInput(
                attrs={
                    'class': 'fill-field fill-field--w562 '
                             'fill-field--w562--type'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def clean_promo(self):
        promo = self.cleaned_data.get('promo')
        if validate_code(promo):
            return promo
        raise forms.ValidationError("Неправильный промокод!")

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data["password1"])
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
