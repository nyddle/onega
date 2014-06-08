# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ImageGallery, SiteSettings, ValidCode, PromoCode, Customer, PriseType, Phase

from import_export import resources
from import_export import fields

from import_export.admin import ImportExportModelAdmin


class PriseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    exclude = ('date', )


class PhaseAdmin(admin.ModelAdmin):
    list_display = ('current_phase', )


class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer
        exclude = ('password', 'id')


class ValidCodeResource(resources.ModelResource):

    id = fields.Field(column_name='id')

    def before_import(dataset, dry_run):
        for x in dataset:
            print x

    class Meta:
        model = ValidCode
        exclude = ('id', )
        fields = ('code', )
        import_id_fields = ('code', )


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
                    'building', 'corpus', 'apartment', 'phone', 'get_codes', 'banks', 'is_active')

    search_fields = ['email', 'first_name', 'last_name', 'surname',
                    'post_index', 'region', 'district', 'city', 'street',
                    'building', 'corpus', 'apartment']

    list_filter = ('is_active', 'banks')
    list_editable = ('is_active', 'banks')
    readonly_fields = ('codes_amount', 'get_codes')
    resource_class = CustomerResource


admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(ValidCode, ValidCodeAdmin)
admin.site.register(PriseType, PriseTypeAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Customer, CustomerAdmin)
