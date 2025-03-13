# TODO: create 

from django.urls import path
from . import views

urls = [
    path('init', views.init, name='init'),
]