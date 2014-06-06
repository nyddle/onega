from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseNotFound, HttpResponse
from django.views.generic import View, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model, \
    authenticate

from .models import ImageGallery
from .forms import RegistrationForm, CodeForm, LoginForm as AuthenticationForm


class HomeView(View):
    """
    Home page
    """

    def get(self, request, method='reg'):
        return self._render_stuff(method)


    def post(self, request, method):
        if method == 'login':
            # todo: check is user blocked and if yes check block date
            form = AuthenticationForm(request, request.POST)
            print(form.errors)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect(reverse('home'))
        elif method == 'reg':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect(reverse('home'))
        else:
            return HttpResponseNotFound
        return self._render_stuff(method)

    def _render_stuff(self, method):
        template_data = {'method': method}
        if self.request.settings.get('gallery'):
            template_data['photos'] = ImageGallery.objects.all()

        if self.request.settings.get('video'):
            template_data['video'] = request.settings['video']
        if not self.request.user.is_authenticated():
            if self.request.POST:
                if method == 'login':
                    template_data['forms'] = {'reg': RegistrationForm(),
                                              'login': AuthenticationForm(self.request.POST or None)}
                else:
                    template_data['forms'] = {'reg': RegistrationForm(self.request.POST or None),
                                              'login': AuthenticationForm()}
            else:
                template_data['forms'] = {'reg': RegistrationForm(), 'login': AuthenticationForm()}
        return render(self.request, 'chips/home.html', template_data)


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
