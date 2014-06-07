# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ImageGallery, SiteSettings, ValidCode, PromoCode, Customer


class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('photo', )


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'customer', 'added')


class ValidCodeAdmin(admin.ModelAdmin):
    list_display = ('code', )


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'enabled', 'additional_data')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'surname',
                    'post_index', 'region', 'district', 'city', 'street', 'codes_amount',
                    'building', 'corpus', 'apartment', 'phone', 'banks', 'is_active')

    search_fields = ['email', 'first_name', 'last_name', 'surname',
                    'post_index', 'region', 'district', 'city', 'street',
                    'building', 'corpus', 'apartment']

    list_filter = ('is_active', 'banks')
    list_editable = ('is_active', 'banks')
    readonly_fields = ('codes_amount', )

admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(ValidCode, ValidCodeAdmin)
admin.site.register(Customer, CustomerAdmin)
