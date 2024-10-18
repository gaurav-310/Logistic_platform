# admin_dashboard/urls.py

from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('analytics/', views.analytics, name='analytics'),
]