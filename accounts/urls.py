from django.urls import re_path, path

from . import views

app_name = "accounts"

urlpatterns = [
    re_path(r'^register/$', views.RegisterView.as_view(success_url='/'), name='register'),
    re_path(r'^login/$', views.LoginFormView.as_view(success_url='/'), name='login'),
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    path(r'profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path(r'accounts/result.html', views.account_result, name='result')
]
