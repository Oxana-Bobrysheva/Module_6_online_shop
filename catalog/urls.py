from django.urls import path
from . import views
from catalog import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]