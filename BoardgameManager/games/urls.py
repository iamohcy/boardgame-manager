from django.urls import path
from django.conf.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main page
    path('link_bgg/', views.link_bgg, name='link_bgg'),
    # path('set_votes/', views.set_votes, name='set_votes'),
    path('user_collection/<str:username>', views.get_user_collection, name='get_user_collection'),
    path('boardgame_metadata/', views.get_boardgame_metadata, name='get_boardgame_metadata'),
]
