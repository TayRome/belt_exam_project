from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.all_quotes, name = 'all_quotes'),
    path('quotes/post', views.post_quote, name = 'post_quote'),
    path('quotes/add/<int:id>', views.add_favorite, name = 'add_favorite'),
    path('quotes/remove_favorite/<int:id>', views.remove_favorite, name = 'remove_favorite'),
    ]