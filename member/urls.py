from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='m_login' ),
    path('logout/', auth_views.LogoutView.as_view(), name='m_logout' ),
    path('register/', views.register, name='m_register'),
    path('membership/', views.membership, name='m_membership'),
    path('info/<int:id>/', views.info, name='m_info'),
    path('delete/<int:id>/', views.delete, name='m_delete'),
    path('modify/<int:id>/', views.modify, name='m_modify'),
    path("rest/", include("member.rest_urls")),
    path('m_download/<str:profile>/',views.m_download, name="m_download"),
]
