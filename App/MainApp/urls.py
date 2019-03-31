from django.urls import path
from django.conf.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main page
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='MainApp/login.html'), name='login'),

    # Accounts
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True,
                                                         template_name='registration/login.html'), name='auth_login'),
    path('accounts/register/', views.BgRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.default.urls')),
]
