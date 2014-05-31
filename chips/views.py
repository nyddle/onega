from django.shortcuts import render
from django.views.generic import View

from .models import ImageGallery, VideoGallery


class HomeView(View):
    """
    Home page
    """
    def get(self, request):
        template_data = {}
        if request.settings.get('gallery'):
            template_data['photos'] = ImageGallery.objects.all()
        if request.settings.get('video'):
            template_data['videos'] = ImageGallery.objects.all().first()

        return render(request, 'chips/home.html', template_data)


class LoginView(View):
    def get(self, request):
        return render(request, 'chips/auth.html', {})
