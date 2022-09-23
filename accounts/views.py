from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib.auth import login, logout, get_user
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from myblog.utils import get_current_site, get_sha256
from django.views.generic import FormView, RedirectView, DetailView
from .forms import RegisterForm, LoginForm

from accounts.models import BlogUser
from blog.models import Article


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


class ProfileView(DetailView):
    model = BlogUser
    template_name = 'accounts/profile.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = {}

        # author = get_user(self.request)
        author = self.get_object()
        article_list = list(Article.objects.filter(author=author))

        context['user_articles'] = article_list
        context.update(kwargs)

        return super(ProfileView, self).get_context_data(**context)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(username=self.kwargs.get('username'))

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )

        return obj


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def account_result(request):
    type = request.GET.get('type')
    id = request.GET.get('id')
    return render(request, 'accounts/result.html', {'content': "Registration successful"})
