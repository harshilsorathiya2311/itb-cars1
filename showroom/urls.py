from django.urls import path
from . import views

app_name = 'showroom'

urlpatterns = [
    path('', views.home, name='home'),

    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/book/', views.book_test_drive, name='book_test_drive'),

    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('showrooms/', views.showroom_locations, name='showroom_locations'),

    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('panel/login/', views.admin_login, name='admin_login'),
    path('panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('panel/brands/', views.admin_manage_brands, name='admin_manage_brands'),
    path('panel/cars/', views.admin_manage_cars, name='admin_manage_cars'),
    path('panel/bookings/', views.admin_manage_bookings, name='admin_manage_bookings'),
    path('panel/users/', views.admin_manage_users, name='admin_manage_users'),
]