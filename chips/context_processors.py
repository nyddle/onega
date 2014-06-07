# -*- coding: utf-8 -*-
def get_settings(request):
    video = False
    gallery = False
    if request.settings.get('gallery'):
        gallery = True
    if request.settings.get('video') is not None:

        video = True
    return {'is_video_enabled': video, 'is_gallery_enabled': gallery}