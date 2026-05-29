from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Brand(models.Model):
    """Car brand model (e.g., Toyota, Honda, BMW)."""
    name = models.CharField(max_length=100, unique=True)
    showroom_location = models.TextField(
        blank=True,
        default='',
        help_text='Full address of the showroom where this brand\'s cars are available'
    )
    showroom_city = models.CharField(max_length=100, blank=True, default='')
    showroom_phone = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        verbose_name_plural = 'Brands'
        ordering = ['name']

    def __str__(self):
        return self.name

    def has_showroom(self):
        return bool(self.showroom_location)


class Car(models.Model):
    """Car model with brand relationship."""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class TestDriveBooking(models.Model):
    """Test drive booking made by users."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.username} - {self.car} ({self.status})"


class UserProfile(models.Model):
    """Extended user profile with phone number for SMS."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Exception:
        pass
