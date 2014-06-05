# -*- coding: utf-8 -*-
def get_settings(request):
    video = False
    gallery = False
    if request.settings.get('gallery'):
        video = True
    if request.settings.get('video'):
        gallery = True
    return {'is_video_enabled': video, 'is_gallery_enabled': gallery}