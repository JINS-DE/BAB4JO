from django.urls import path
from . import rest_views

urlpatterns = [
    path("id_chk/",rest_views.id_chk, name="id_chk"),
    path("get_data/",rest_views.get_data, name="get_data"),
    path('main/header/', rest_views.main_header, name="main_header"),
]
