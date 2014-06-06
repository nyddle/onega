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
    list_display = ('pk', 'email', 'first_name', 'last_name', 'post_index', 'region', 'district', 'city', 'street',
                    'building', 'corpus', 'apartment', 'phone', 'banks', 'is_active')
    list_editable = ('is_active', 'banks')
    readonly_fields = ('codes_amount', )

admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(ValidCode, ValidCodeAdmin)
admin.site.register(Customer, CustomerAdmin)
