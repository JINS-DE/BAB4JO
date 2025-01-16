from django.urls import path,include
from .import views
urlpatterns = [
    path('', views.list, name='b_list'),
    path('write/', views.write, name='b_write'),
    path('detail/<int:num>/', views.detail, name='b_detail'),
    path('download/<str:file_name>/', views.download, name='download'),
    path('delete/<int:num>/', views.delete, name ='b_delete'),
    path('modify/<int:num>/', views.modify, name='b_modify'),
    path('rest/', include('board.rest_urls')),
    path('boardsearch/', views.b_search, name='b_search'),

]