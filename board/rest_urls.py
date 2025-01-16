from django.urls import path
from.import rest_views

urlpatterns = [
    path('like', rest_views.like, name='b_like'),
    path('add_reply', rest_views.add_reply, name='add_reply'),
    path('reply_data/<int:num>', rest_views.reply_data, name='reply_data'),
    path('blog_search/', rest_views.blog_search, name='blog_search'),
    path('map_load/', rest_views.map_load, name='map_load'),
    path('nav_hit/', rest_views.hit_top3, name='b_hit_top3'),
    path('nav_likes/', rest_views.likes_top3, name='b_likes_top3'),
    path('list_array/', rest_views.list_array, name='b_list_array'),
    path('reply_edit/', rest_views.edit_reply, name="b_replyEdit"), 
]
