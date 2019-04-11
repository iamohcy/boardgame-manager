from django.urls import path
from django.conf.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main page
    path('', views.index, name='index'),

    # View user collection
    path('user/<str:username>', views.user_page, name='user_page'),

    # Accounts
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True,
                                                         template_name='registration/login.html'), name='auth_login'),
    path('accounts/login/', auth_views.LogoutView.as_view(), name='auth_logout'),
    path('accounts/register/', views.BgRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.default.urls')),
]
