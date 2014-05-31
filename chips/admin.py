from django.contrib import admin

from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField

from .models import ImageGallery, VideoGallery, SiteSettings, ValidCode, PromoCode


class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('photo', )

    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput}
    }


class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('video', )


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'customer')


class ValidCodeAdmin(admin.ModelAdmin):
    list_display = ('code', )


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')

admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(VideoGallery, VideoGalleryAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(ValidCode, ValidCodeAdmin)
