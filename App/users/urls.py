from django.urls import path
from django.conf.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main page
    path('link_bgg/', views.link_bgg, name='link_bgg'),

]
