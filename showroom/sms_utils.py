"""
SMS utility module for sending notifications via Twilio.
API keys should be stored in environment variables (.env file):
    TWILIO_ACCOUNT_SID=your_account_sid
    TWILIO_AUTH_TOKEN=your_auth_token.
    TWILIO_PHONE_NUMBER=your_twilio_phone_number.
"""

from django.conf import settings


def send_sms(phone_number, message):
    """
    Send SMS notification using Twilio API.

    Args:
        phone_number: Recipient phone number (with country code, e.g., +1234567890)
        message: SMS message body.

    Returns:
        dict with 'success' boolean and 'message' string.
    """
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        return {
            'success': False,
            'message': 'Twilio credentials not configured. Check .env file.'
        }

    try:
        from twilio.rest import Client

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        twilio_message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        return {
            'success': True,
            'message': f'SMS sent successfully. SID: {twilio_message.sid}'
        }

    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to send SMS: {str(e)}'
        }


def send_booking_sms(booking, notification_type='created'):
    """
    Send SMS notification for booking events.

    Args:
        booking: TestDriveBooking instance.
        notification_type: 'created', 'approved', or 'rejected'.

    Returns:
        dict with 'success' boolean and 'message' string.
    """
    user = booking.user
    car = booking.car

    if notification_type == 'created':
        message = (
            f"YourCars: Your test drive booking for {car.brand} {car.name} "
            f"has been BOOKED SUCCESSFULLY! Status: Pending. "
            f"We will notify you once admin approves."
        )
    elif notification_type == 'approved':
        message = (
            f"YourCars: Your test drive booking for {car.brand} {car.name} "
            f"has been APPROVED! Contact us to schedule your visit."
        )
    elif notification_type == 'rejected':
        message = (
            f"YourCars: Your test drive booking for {car.brand} {car.name} "
            f"has been REJECTED. Please try another car or contact support."
        )
    else:
        return {'success': False, 'message': 'Invalid notification type.'}

    try:
        phone_number = user.profile.phone_number
    except Exception:
        phone_number = None

    if not phone_number:
        return {'success': False, 'message': 'User phone number not available.'}

    return send_sms(phone_number, message)
