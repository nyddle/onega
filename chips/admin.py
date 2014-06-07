# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ImageGallery, SiteSettings, ValidCode, PromoCode, Customer

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer
        exclude = ('password', 'id')

class ValidCodeResource(resources.ModelResource):

    id = fields.Field(column_name='id', primary_key=True)

    class Meta:
        model = ValidCode
        exclude = ('id', )

class PromoCodeResource(resources.ModelResource):

    class Meta:
        model = PromoCode



class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('photo', )


class PromoCodeAdmin(ImportExportModelAdmin):
    list_display = ('code', 'customer', 'added')


class ValidCodeAdmin(ImportExportModelAdmin):
    list_display = ('code', )


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'enabled', 'additional_data')


class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'surname',
                    'post_index', 'region', 'district', 'city', 'street', 'codes_amount',
                    'building', 'corpus', 'apartment', 'phone', 'banks', 'is_active')

    search_fields = ['email', 'first_name', 'last_name', 'surname',
                    'post_index', 'region', 'district', 'city', 'street',
                    'building', 'corpus', 'apartment']

    list_filter = ('is_active', 'banks')
    list_editable = ('is_active', 'banks')
    readonly_fields = ('codes_amount', )
    resource_class = CustomerResource


admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(ValidCode, ValidCodeAdmin)
admin.site.register(Customer, CustomerAdmin)
