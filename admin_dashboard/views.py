# admin_dashboard/views.py

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from bookings.models import Booking
from django.db.models import Count, Avg, F, ExpressionWrapper, fields
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_home(request):
    return render(request, 'admin_dashboard/dashboard_home.html')
# admin_dashboard/views.py

@staff_member_required
def analytics(request):
    total_trips = Booking.objects.filter(status='completed').count()
    
    average_trip_time = Booking.objects.filter(status='completed').annotate(
        trip_duration=ExpressionWrapper(
            F('end_time') - F('start_time'),
            output_field=fields.DurationField()
        )
    ).aggregate(average_duration=Avg('trip_duration'))['average_duration']

    driver_performance = Booking.objects.filter(status='completed').values('driver__username').annotate(
        trips_completed=Count('id'),
        average_trip_time=Avg(ExpressionWrapper(
            F('end_time') - F('start_time'),
            output_field=fields.DurationField()
        ))
    )

    context = {
        'total_trips': total_trips,
        'average_trip_time': average_trip_time,
        'driver_performance': driver_performance,
    }
    return render(request, 'admin_dashboard/analytics.html', context)
