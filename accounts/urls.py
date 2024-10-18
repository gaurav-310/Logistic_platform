# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('driver_dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]