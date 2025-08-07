from django.contrib.auth.views import LoginView

from django.urls import path
from users.views import register
from .views import CustomLogoutView
from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name='login'),
    path("register/", register, name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    ]
