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
    path('booking/<int:booking_id>/details/', views.booking_detail_view, name='booking_detail'),
    path('booking/<int:booking_id>/update_status/', views.update_job_status, name='update_job_status'),
    path('booking/<int:booking_id>/complete/', views.complete_booking, name='complete_booking'),
    
    path('admin_dashboard/manage_users/', views.manage_users, name='manage_users'),
    path('admin_dashboard/view_all_bookings/', views.view_all_bookings, name='view_all_bookings'),
    path('admin_dashboard/analytics/', views.analytics, name='analytics'),
]
