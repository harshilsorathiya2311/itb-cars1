#!/usr/bin/env python
"""
Create default admin user if not exists.
Run: python manage.py create_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from showroom.models import UserProfile


class Command(BaseCommand):
    help = 'Create default admin user (username: admin, password: admin)'

    def handle(self, *args, **kwargs):
        if User.objects.filter(username='admin').exists():
            admin = User.objects.get(username='admin')
            admin.set_password('admin')
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            UserProfile.objects.get_or_create(user=admin)
            self.stdout.write(self.style.WARNING('Admin user already exists. Password has been reset.'))
        else:
            admin = User.objects.create_superuser('admin', 'admin@yourcars.com', 'admin')
            UserProfile.objects.get_or_create(user=admin, defaults={'phone_number': ''})
            self.stdout.write(self.style.SUCCESS('Default admin user created successfully!'))

        self.stdout.write(self.style.SUCCESS('Username: admin'))
        self.stdout.write(self.style.SUCCESS('Password: admin'))
        self.stdout.write(self.style.SUCCESS('Login: http://127.0.0.1:8000/admin/login/'))
