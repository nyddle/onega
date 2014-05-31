from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import ImageGallery, VideoGallery
from .forms import RegistrationForm


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
        if not request.user.is_authenticated():
            template_data['forms'] = {'registration': RegistrationForm(), 'login': AuthenticationForm()}
        return render(request, 'chips/home.html', template_data)


class ProfileView(View):

    @login_required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'chips/profile.html', {})

