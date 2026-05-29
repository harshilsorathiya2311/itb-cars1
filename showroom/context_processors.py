from .models import TestDriveBooking


def admin_context(request):
    """Add pending bookings count to context for admin sidebar badge."""
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'pending_bookings_count': TestDriveBooking.objects.filter(status='Pending').count()
        }
    return {'pending_bookings_count': 0}
