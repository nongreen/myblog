from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from myblog.utils import get_current_site, get_sha256
from django.views.generic import FormView, RedirectView

from .forms import RegisterForm, LoginForm


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login_form.html'
    success_url = '/'

    def form_valid(self, form):
        if form.is_valid:
            login(self.request, form.get_user())

            return super(LoginView, self).form_valid(form)
        else:
            return self.render_to_response({
                'form': form
            })


# Create your views here.
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/registration_form.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(False)
            user.save()

            url = reverse('accounts:result') + '?type=register&id=' + str(user.id)

            return HttpResponseRedirect(url)
        else:
            self.render_to_response({
                'form': form
            })


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

def account_result(request):
    type = request.GET.get('type')
    id = request.GET.get('id')
    return render(request, 'accounts/result.html', {'content': "Registration successful"})
