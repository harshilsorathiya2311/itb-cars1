from django import forms
from django.contrib.auth.models import User
from .models import TestDriveBooking, UserProfile


class UserRegistrationForm(forms.ModelForm):
    """Professional user registration form with all details."""
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password',
            'id': 'id_password'
        })
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'id_password_confirm'
        })
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 (234) 567-8900',
            'id': 'id_phone_number'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'John',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Doe',
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match.')

        username = cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            self.add_error('username', 'This username is already taken.')

        email = cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'An account with this email already exists.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'phone_number': self.cleaned_data['phone_number']}
            )
        return user


class TestDriveBookingForm(forms.ModelForm):
    """Form for booking a test drive."""
    class Meta:
        model = TestDriveBooking
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.user = self.user
        booking.car = self.car
        if commit:
            booking.save()
        return booking
