# bookings/urls.py

from django.urls import path,include
from . import views


app_name = 'bookings'

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    # path('bookings/', include('bookings.urls', namespace='bookings')),
]
