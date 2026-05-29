<<<<<<< HEAD
# YourCars - Django Car Showroom Application

A complete Django web application for a car showroom with test drive booking functionality, user authentication, and SMS notifications.

## Features

- **User Authentication**: Registration, login, logout
- **Car Catalog**: Browse cars by brand, search functionality
- **Test Drive Booking**: Users can book test drives (logged-in only)
- **Admin Panel**: Manage cars, brands, users, and bookings
- **SMS Notifications**: Twilio integration for booking status updates
- **Responsive Design**: Bootstrap 5 frontend

## Project Structure

```
django_yourcars/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── setup.ps1                    # PowerShell setup script
├── run.bat                      # Quick start script
├── .env                         # Environment variables (API keys)
├── .env.example                 # Template for .env
├── db.sqlite3                   # SQLite database
├── Yourcars/                    # Project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
└── showroom/                    # Main application
    ├── __init__.py
    ├── models.py                # Database models
    ├── views.py                 # View functions
    ├── urls.py                  # URL routing
    ├── forms.py                 # Django forms
    ├── admin.py                 # Admin customization
    ├── sms_utils.py             # Twilio SMS integration
    ├── apps.py
    ├── management/
    │   └── commands/
    │       └── seed_data.py     # Sample data seeding
    ├── static/showroom/css/
    │   └── style.css            # Custom styles
    └── templates/showroom/
        ├── base.html            # Base template
        ├── home.html            # Home page
        ├── car_list.html        # Car listing
        ├── car_detail.html      # Car details
        ├── book_test_drive.html # Booking form
        ├── my_bookings.html     # User bookings
        ├── login.html           # Login page
        ├── register.html        # Registration page
        └── admin_bookings.html  # Admin booking management
```

## Quick Start

### Option 1: Automated Setup (Recommended)

```powershell
.\setup.ps1
```

### Option 2: Manual Setup

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (copy from example)
copy .env.example .env

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Load sample data (optional)
python manage.py seed_data

# 8. Run server
python manage.py runserver
```

### Option 3: Quick Start

```powershell
.\run.bat
```

## Configuration

### Environment Variables (.env)

Edit the `.env` file to configure:

```env
DJANGO_SECRET_KEY=your-secret-key-here

# Twilio SMS Configuration (optional)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

### Getting Twilio Credentials

1. Sign up at [Twilio](https://www.twilio.com/)
2. Get Account SID and Auth Token from dashboard
3. Get/buy a Twilio phone number
4. Add credentials to `.env` file

## Access Points

- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Car List**: http://127.0.0.1:8000/cars/
- **Register**: http://127.0.0.1:8000/register/
- **Login**: http://127.0.0.1:8000/login/

## Default Credentials

After running `createsuperuser`, use your chosen credentials to access the admin panel.

## Models

| Model | Description |
|-------|-------------|
| Brand | Car manufacturer (Toyota, BMW, etc.) |
| Car | Vehicle details with brand relationship |
| TestDriveBooking | User booking with status tracking |
| UserProfile | Extended user data (phone number) |

## URL Routes

| URL | View | Access |
|-----|------|--------|
| `/` | Home page | Public |
| `/cars/` | Car list with filters | Public |
| `/cars/<id>/` | Car detail | Public |
| `/cars/<id>/book/` | Book test drive | Logged-in |
| `/my-bookings/` | User bookings | Logged-in |
| `/register/` | User registration | Public |
| `/login/` | User login | Public |
| `/logout/` | User logout | Logged-in |
| `/admin/bookings/` | Manage bookings | Admin only |

## Tech Stack

- **Backend**: Django 5.x
- **Database**: SQLite (default)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **SMS**: Twilio API
- **Authentication**: Django built-in auth

## License

MIT License
=======
# itb-cars1
>>>>>>> af113c6e67006bbbfcd7aff8b7e0ac75140ec225
