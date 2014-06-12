# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseNotFound
from django.views.generic import View, FormView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages

from .models import ImageGallery, DiscreditedIP, WrongIPByCode
from .forms import RegistrationForm, CodeForm, LoginForm as AuthenticationForm
from .utils import get_client_ip


class HomeView(View):
    """
    Home page
    """

    def dispatch(self, request, *args, **kwargs):
        ip_addr = get_client_ip(request)

        ip, created = DiscreditedIP.objects.get_or_create(ip=ip_addr)

        if ip.blocked > 3:
            request.session['ip_blocked'] = True

        attempts = ip.wrongipbycode_set.all()[5:]
        if len(attempts) > 4 and (attempts[len(attempts)-1].date - attempts[0].date).days < 1:
            request.session['ip_blocked'] = True
        else:
            request.session['ip_blocked'] = False
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, method='reg'):
        return self._render_stuff(method)

    def post(self, request, method):

        if method == 'login':
            # todo: check is user blocked and if yes check block date
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                user = form.get_user()
                if not user.should_be_blocked():
                    auth_login(request, form.get_user())
                    return redirect(reverse('home'))
                # return self._render_stuff(method, True)
        elif method == 'reg':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                request.session['registered'] = True
                messages.info(request,
                              u'Ваш логин и пароль отправлены на email, '
                              u'указанный при регистрации.',
                              extra_tags=u'Спасибо за регистрацию!')

                return redirect(reverse('home'))
            else:
                if form.is_promo_failed():
                    ip_addr = get_client_ip(request)
                    ip, created = DiscreditedIP.objects.get_or_create(ip=ip_addr)
                    WrongIPByCode.objects.create(ip=ip)
                    ip.failed += 1
                    ip.save()

                    attempts = ip.wrongipbycode_set.all()[5:]
                    if len(attempts) > 4 and (attempts[len(attempts)-1].date - attempts[0].date).days < 1:
                        request.session['ip_blocked'] = True
                        ip.blocked += 1
                        ip.save()

        else:
            return HttpResponseNotFound
        return self._render_stuff(method)

    # todo: hide registration if phase > 3
    def _render_stuff(self, method, blocked=False):
        template_data = {'method': method, 'blocked': blocked}
        if self.request.settings.get('gallery'):
            template_data['photos'] = ImageGallery.objects.all()

        if self.request.settings.get('video'):
            template_data['video'] = self.request.settings['video']
        if not self.request.user.is_authenticated():
            if self.request.POST:
                if method == 'login':
                    template_data['forms'] = {'reg': RegistrationForm(),
                                              'login': AuthenticationForm(self.request,
                                                                          self.request.POST)}
                else:
                    template_data['forms'] = {'reg': RegistrationForm(self.request.POST or None),
                                              'login': AuthenticationForm()}
            else:
                template_data['forms'] = {'reg': RegistrationForm(), 'login': AuthenticationForm()}

        else:
            template_data['form'] = CodeForm(customer=self.request.user)

        return render(self.request, 'chips/home.html', template_data)


class ProfileView(FormView):
    template_name = 'chips/profile.html'
    form_class = CodeForm

    def get_success_url(self):
        return reverse('profile')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs['customer'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(ProfileView, self).get_context_data(**kwargs)
        data['codes'] = self.request.user.promocode_set.all()
        return data

    def form_valid(self, form):
        form.save()
        return super(ProfileView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ProfileView, self).form_invalid(form)


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        request.session.flush()
        return redirect('home')


class Prize(TemplateView):
    template_name = 'chips/prize.html'