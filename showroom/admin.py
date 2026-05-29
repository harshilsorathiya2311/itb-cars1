from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Car, TestDriveBooking, UserProfile


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'showroom_city', 'showroom_phone')
    search_fields = ('name', 'showroom_city')
    list_filter = ('showroom_city',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('image_thumbnail', 'id', 'name', 'brand', 'price', 'date')
    list_filter = ('brand',)
    search_fields = ('name', 'title', 'description')

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="50" style="object-fit:cover; border-radius:4px;" />', obj.image.url)
        return 'No image'
    image_thumbnail.short_description = 'Image'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number')
    search_fields = ('user__username', 'phone_number')


@admin.register(TestDriveBooking)
class TestDriveBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'car__name', 'car__brand__name')
    actions = ['approve_bookings', 'reject_bookings']

    @admin.action(description='Approve selected bookings')
    def approve_bookings(self, request, queryset):
        queryset.update(status='Approved')
        self.message_user(request, 'Selected bookings approved.')

    @admin.action(description='Reject selected bookings')
    def reject_bookings(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, 'Selected bookings rejected.')
