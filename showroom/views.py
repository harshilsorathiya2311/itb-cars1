from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count, Min, Max

from .models import Brand, Car, TestDriveBooking
from .forms import UserRegistrationForm, TestDriveBookingForm


# -------------------------
# ADMIN DECORATOR
# -------------------------
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff, login_url='admin_login')(view_func)


# -------------------------
# HOME
# -------------------------
def home(request):
    cars = Car.objects.select_related('brand').all()[:6]
    brands = Brand.objects.all()

    featured_car = Car.objects.filter(name='5 Series').select_related('brand').first()
    bmw_car_360 = Car.objects.filter(brand__name__iexact='BMW').select_related('brand').first()

    return render(request, 'showroom/home.html', {
        'cars': cars,
        'brands': brands,
        'featured_car': featured_car,
        'bmw_car_360': bmw_car_360,
    })


# -------------------------
# CAR LIST
# -------------------------
def car_list(request):
    cars = Car.objects.select_related('brand').all()
    brands = Brand.objects.all()

    brand_id = request.GET.get('brand')
    search_query = request.GET.get('search')
    sort = request.GET.get('sort', '-date')

    if brand_id:
        cars = cars.filter(brand_id=brand_id)

    if search_query:
        cars = cars.filter(
            Q(name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(brand__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if sort == 'price_asc':
        cars = cars.order_by('price')
    elif sort == 'price_desc':
        cars = cars.order_by('-price')
    elif sort == 'name':
        cars = cars.order_by('name')
    else:
        cars = cars.order_by('-date')

    price_range = Car.objects.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )

    return render(request, 'showroom/car_list.html', {
        'cars': cars,
        'brands': brands,
        'selected_brand': brand_id,
        'search_query': search_query,
        'sort': sort,
        'price_range': price_range,
    })


# -------------------------
# CAR DETAIL
# -------------------------
def car_detail(request, car_id):
    car = get_object_or_404(Car.objects.select_related('brand'), id=car_id)
    related_cars = Car.objects.filter(brand=car.brand).exclude(id=car.id)[:3]

    return render(request, 'showroom/car_detail.html', {
        'car': car,
        'related_cars': related_cars,
    })


# -------------------------
# BOOK TEST DRIVE
# -------------------------
@login_required
def book_test_drive(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    existing_booking = TestDriveBooking.objects.filter(
        user=request.user,
        car=car
    ).first()

    if request.method == 'POST':
        if existing_booking:
            messages.warning(request, "You already booked this car.")
            return redirect('my_bookings')

        form = TestDriveBookingForm(request.POST, user=request.user, car=car)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.save()

            messages.success(request, f"Test drive booked for {car.name}")
            return redirect('my_bookings')
    else:
        form = TestDriveBookingForm(user=request.user, car=car)

    return render(request, 'showroom/book_test_drive.html', {
        'form': form,
        'car': car,
        'existing_booking': existing_booking,
    })


# -------------------------
# MY BOOKINGS
# -------------------------
@login_required
def my_bookings(request):
    bookings = TestDriveBooking.objects.filter(user=request.user).select_related('car__brand')
    return render(request, 'showroom/my_bookings.html', {'bookings': bookings})


# -------------------------
# AUTH
# -------------------------
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'showroom/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid credentials")

    return render(request, 'showroom/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


# -------------------------
# ADMIN LOGIN
# -------------------------
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')

        messages.error(request, "Invalid admin login")

    return render(request, 'showroom/admin_login.html')


# -------------------------
# ADMIN DASHBOARD
# -------------------------
@admin_required
def admin_dashboard(request):
    return render(request, 'showroom/admin/dashboard.html', {
        'total_cars': Car.objects.count(),
        'total_brands': Brand.objects.count(),
        'total_users': User.objects.filter(is_staff=False).count(),
        'total_bookings': TestDriveBooking.objects.count(),
    })


# -------------------------
# ADMIN PAGES (IMPORTANT FIX)
# -------------------------

@admin_required
def admin_manage_brands(request):
    brands = Brand.objects.annotate(car_count=Count('cars'))
    return render(request, 'showroom/admin/brands.html', {'brands': brands})


@admin_required
def admin_manage_cars(request):
    cars = Car.objects.select_related('brand').all()
    return render(request, 'showroom/admin/cars.html', {'cars': cars})


@admin_required
def admin_manage_bookings(request):
    bookings = TestDriveBooking.objects.select_related('user', 'car__brand').all()
    return render(request, 'showroom/admin/bookings.html', {'bookings': bookings})


@admin_required
def admin_manage_users(request):
    users = User.objects.filter(is_staff=False)
    return render(request, 'showroom/admin/users.html', {'users': users})


# -------------------------
# SHOWROOM LOCATIONS
# -------------------------
def showroom_locations(request):
    brands = Brand.objects.all()
    return render(request, 'showroom/showroom_locations.html', {'brands': brands})