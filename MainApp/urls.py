from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Accounts
    url(r'^accounts/register/$', views.BgRegistrationView.as_view(),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
