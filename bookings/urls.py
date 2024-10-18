# bookings/urls.py

from django.urls import path,include
from . import views


app_name = 'bookings'

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    # path('bookings/', include('bookings.urls', namespace='bookings')),
    
    path('confirm/', views.confirm_booking, name='confirm_booking'),
    path('accept/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),

]
