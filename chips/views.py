from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseNotFound, HttpResponse
from django.views.generic import View, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model, \
    authenticate

from .models import ImageGallery, VideoGallery
from .forms import RegistrationForm, CodeForm


class HomeView(View):
    """
    Home page
    """
    def get(self, request, method='registration'):
        template_data = {'method': method}
        if request.settings.get('gallery'):
            template_data['photos'] = ImageGallery.objects.all()

        if request.settings.get('video'):
            template_data['videos'] = ImageGallery.objects.all().first()
        if not request.user.is_authenticated():
            template_data['forms'] = {'registration': RegistrationForm(), 'login': AuthenticationForm()}
        return render(request, 'chips/home.html', template_data)

    def post(self, request, method):
        if method == 'login':
            # todo: check is user blocked and ig yes check block date
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect(reverse('home'))
        elif method == 'registration':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect(reverse('home'))
        else:
            return HttpResponseNotFound

        # todo: refactor and fix code duplication
        template_data = {}
        if request.settings.get('gallery'):
            template_data['photos'] = ImageGallery.objects.all()

        if request.settings.get('video'):
            template_data['videos'] = ImageGallery.objects.all().first()
        if not request.user.is_authenticated():
            template_data['forms'] = {'registration': RegistrationForm(request.POST),
                                      'login': AuthenticationForm(request.POST)}
        return render(request, 'chips/home.html', template_data)


class ProfileView(FormView):
    template_name = 'chips/profile.html'
    form_class = CodeForm

    def get_success_url(self):
        return reverse('profile')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['customer'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['codes'] = self.request.user.promocode_set.all()
        return data

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
