from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Count
from django.core.paginator import Paginator

from .models import Brand, Car, TestDriveBooking
from .forms import UserRegistrationForm, TestDriveBookingForm
from .sms_utils import send_booking_sms


def admin_required(view_func):
    """Decorator to check if user is admin/staff."""
    return user_passes_test(lambda u: u.is_staff, login_url='admin_login')(view_func)


def home(request):
    """Home page displaying featured cars."""
    cars = Car.objects.select_related('brand').all()[:6]
    brands = Brand.objects.all()
    featured_car = Car.objects.filter(name='5 Series').select_related('brand').first()
    bmw_car_360 = Car.objects.filter(brand__name__iexact='BMW').select_related('brand').first()
    context = {
        'cars': cars,
        'brands': brands,
        'featured_car': featured_car,
        'bmw_car_360': bmw_car_360,
    }
    return render(request, 'showroom/home.html', context)


def car_list(request):
    """Display all cars with optional brand filter and search."""
    cars = Car.objects.select_related('brand').all()
    brands = Brand.objects.all()

    brand_id = request.GET.get('brand')
    search_query = request.GET.get('search')
    sort = request.GET.get('sort', '-date')

    if brand_id:
        cars = cars.filter(brand_id=int(brand_id))
    if search_query:
        cars = cars.filter(
            Q(name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(brand__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Sorting
    if sort == 'price_asc':
        cars = cars.order_by('price')
    elif sort == 'price_desc':
        cars = cars.order_by('-price')
    elif sort == 'name':
        cars = cars.order_by('name')
    else:
        cars = cars.order_by('-date')

    # Get price range for display
    price_agg = Car.objects.aggregate(min_price=models.Min('price'), max_price=models.Max('price'))

    context = {
        'cars': cars,
        'brands': brands,
        'selected_brand': brand_id,
        'search_query': search_query,
        'sort': sort,
        'price_range': price_agg,
    }
    return render(request, 'showroom/car_list.html', context)


def car_detail(request, car_id):
    """Display car details and booking option."""
    car = get_object_or_404(Car.objects.select_related('brand'), id=car_id)
    related_cars = Car.objects.select_related('brand').filter(brand=car.brand).exclude(id=car.id)[:3]

    context = {
        'car': car,
        'related_cars': related_cars,
    }
    return render(request, 'showroom/car_detail.html', context)


@login_required
def book_test_drive(request, car_id):
    """Book a test drive for a specific car (logged-in users only)."""
    car = get_object_or_404(Car, id=car_id)

    existing_booking = TestDriveBooking.objects.filter(user=request.user, car=car).first()

    if request.method == 'POST':
        if existing_booking:
            messages.warning(request, 'You already have a booking for this car.')
            return redirect('my_bookings')

        form = TestDriveBookingForm(request.POST, user=request.user, car=car)
        if form.is_valid():
            booking = form.save()
            sms_result = send_booking_sms(booking, notification_type='created')
            if sms_result['success']:
                messages.success(request, f'Test drive booked for {car.brand} {car.name}! SMS confirmation sent.')
            else:
                messages.success(request, f'Test drive booked for {car.brand} {car.name}!')
            return redirect('my_bookings')
    else:
        form = TestDriveBookingForm(user=request.user, car=car)

    context = {
        'form': form,
        'car': car,
        'existing_booking': existing_booking,
    }
    return render(request, 'showroom/book_test_drive.html', context)


@login_required
def my_bookings(request):
    """Display user's test drive bookings."""
    bookings = request.user.bookings.select_related('car__brand').all()
    context = {
        'bookings': bookings,
    }
    return render(request, 'showroom/my_bookings.html', context)


def showroom_locations(request):
    """Display all brand showroom locations with cars."""
    brands = Brand.objects.all().prefetch_related('cars')
    context = {
        'brands': brands,
    }
    return render(request, 'showroom/showroom_locations.html', context)


def user_register(request):
    """User registration page - redirects to login after successful registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login with your credentials.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'showroom/register.html', {'form': form})


def user_login(request):
    """User login page."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'showroom/login.html')


@login_required
def user_logout(request):
    """User logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def admin_login(request):
    """Admin login page - redirects to admin dashboard."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials.')

    return render(request, 'showroom/admin_login.html')


@admin_required
def admin_dashboard(request):
    """Admin dashboard with stats and quick actions."""
    total_cars = Car.objects.count()
    total_brands = Brand.objects.count()
    total_bookings = TestDriveBooking.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    pending_bookings = TestDriveBooking.objects.filter(status='Pending').count()
    approved_bookings = TestDriveBooking.objects.filter(status='Approved').count()
    rejected_bookings = TestDriveBooking.objects.filter(status='Rejected').count()

    recent_bookings = TestDriveBooking.objects.select_related('user', 'car__brand').order_by('-booking_date')[:5]
    recent_users = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    brand_car_count = Brand.objects.annotate(car_count=Count('cars')).order_by('-car_count')[:5]
    recent_cars = Car.objects.select_related('brand').order_by('-date')[:6]

    context = {
        'total_cars': total_cars,
        'total_brands': total_brands,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
        'recent_bookings': recent_bookings,
        'recent_users': recent_users,
        'brand_car_count': brand_car_count,
        'recent_cars': recent_cars,
    }
    return render(request, 'showroom/admin/dashboard.html', context)


@admin_required
def admin_manage_brands(request):
    """Admin: List, add, edit, delete brands."""
    brands = Brand.objects.annotate(car_count=Count('cars')).order_by('name')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name', '').strip()
            if name and not Brand.objects.filter(name__iexact=name).exists():
                Brand.objects.create(name=name)
                messages.success(request, f'Brand "{name}" added successfully.')
            else:
                messages.error(request, 'Brand name is required or already exists.')
        elif action == 'edit':
            brand_id = request.POST.get('brand_id')
            brand = get_object_or_404(Brand, id=brand_id)
            new_name = request.POST.get('name', '').strip()
            if new_name:
                brand.name = new_name
            brand.showroom_location = request.POST.get('showroom_location', '').strip()
            brand.showroom_city = request.POST.get('showroom_city', '').strip()
            brand.showroom_phone = request.POST.get('showroom_phone', '').strip()
            brand.save()
            messages.success(request, f'Brand "{brand.name}" updated.')
        elif action == 'delete':
            brand_id = request.POST.get('brand_id')
            brand = get_object_or_404(Brand, id=brand_id)
            if brand.cars.exists():
                messages.error(request, f'Cannot delete "{brand.name}". It has {brand.cars.count()} car(s).')
            else:
                brand.delete()
                messages.success(request, f'Brand "{brand.name}" deleted.')
        return redirect('admin_manage_brands')

    context = {'brands': brands}
    return render(request, 'showroom/admin/brands.html', context)


@admin_required
def admin_manage_cars(request):
    """Admin: List, add, edit, delete cars."""
    cars = Car.objects.select_related('brand').order_by('-date')
    brands = Brand.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            car = Car(
                brand=get_object_or_404(Brand, id=request.POST.get('brand_id')),
                name=request.POST.get('name', '').strip(),
                price=request.POST.get('price', '0'),
                title=request.POST.get('title', '').strip(),
                description=request.POST.get('description', '').strip(),
            )
            if request.FILES.get('image'):
                car.image = request.FILES['image']
            car.save()
            messages.success(request, f'Car "{car.brand.name} {car.name}" added.')
        elif action == 'edit':
            car = get_object_or_404(Car, id=request.POST.get('car_id'))
            car.brand = get_object_or_404(Brand, id=request.POST.get('brand_id'))
            car.name = request.POST.get('name', '').strip()
            car.price = request.POST.get('price', car.price)
            car.title = request.POST.get('title', '').strip()
            car.description = request.POST.get('description', '').strip()
            if request.FILES.get('image'):
                car.image = request.FILES['image']
            car.save()
            messages.success(request, f'Car "{car.brand.name} {car.name}" updated.')
        elif action == 'delete':
            car = get_object_or_404(Car, id=request.POST.get('car_id'))
            car_name = str(car)
            car.delete()
            messages.success(request, f'Car "{car_name}" deleted.')
        return redirect('admin_manage_cars')

    context = {
        'cars': cars,
        'brands': brands,
    }
    return render(request, 'showroom/admin/cars.html', context)


@admin_required
def admin_manage_bookings(request):
    """Admin: Manage test drive bookings."""
    bookings = TestDriveBooking.objects.select_related('user', 'car__brand').order_by('-booking_date')

    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = get_object_or_404(TestDriveBooking, id=booking_id)

        if action == 'approve':
            booking.status = 'Approved'
            messages.success(request, f'Booking approved for {booking.user.username}.')
            sms_type = 'approved'
        elif action == 'reject':
            booking.status = 'Rejected'
            messages.warning(request, f'Booking rejected for {booking.user.username}.')
            sms_type = 'rejected'
        else:
            sms_type = None
        booking.save()

        if sms_type:
            sms_result = send_booking_sms(booking, notification_type=sms_type)
            if sms_result['success']:
                messages.info(request, sms_result['message'])

        return redirect('admin_manage_bookings')

    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'bookings_total': TestDriveBooking.objects.count(),
        'pending_count': TestDriveBooking.objects.filter(status='Pending').count(),
        'approved_count': TestDriveBooking.objects.filter(status='Approved').count(),
        'rejected_count': TestDriveBooking.objects.filter(status='Rejected').count(),
    }
    return render(request, 'showroom/admin/bookings.html', context)


@admin_required
def admin_manage_users(request):
    """Admin: Manage registered users."""
    users = User.objects.filter(is_staff=False).order_by('-date_joined')

    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query)
        )

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id, is_staff=False)
            user.delete()
            messages.success(request, f'User "{user.username}" deleted.')
        return redirect('admin_manage_users')

    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)

    context = {'users': users, 'search_query': search_query}
    return render(request, 'showroom/admin/users.html', context)
