from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:id>', views.view_user, name = 'view_user'),
    ]