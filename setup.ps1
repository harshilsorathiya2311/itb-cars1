# YourCars Setup Script for Windows
# Run this script to set up the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   YourCars Project Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create virtual environment
Write-Host "[Step 1] Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
Write-Host "Virtual environment created." -ForegroundColor Green
Write-Host ""

# Step 2: Activate virtual environment
Write-Host "[Step 2] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "Virtual environment activated." -ForegroundColor Green
Write-Host ""

# Step 3: Install dependencies
Write-Host "[Step 3] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "Dependencies installed." -ForegroundColor Green
Write-Host ""

# Step 4: Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "[Step 4] Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ".env file created. Update with your credentials." -ForegroundColor Green
} else {
    Write-Host "[Step 4] .env file already exists." -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Run migrations
Write-Host "[Step 5] Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
Write-Host "Database migrations complete." -ForegroundColor Green
Write-Host ""

# Step 6: Create superuser prompt
Write-Host "[Step 6] Create a superuser? (y/n)" -ForegroundColor Yellow
$response = Read-Host
if ($response -eq "y" -or $response -eq "Y") {
    python manage.py createsuperuser
    Write-Host "Superuser created." -ForegroundColor Green
}
Write-Host ""

# Step 7: Collect static files
Write-Host "[Step 7] Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
Write-Host "Static files collected." -ForegroundColor Green
Write-Host ""

# Done
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the server, run:" -ForegroundColor White
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host "  python manage.py runserver" -ForegroundColor Green
Write-Host ""
Write-Host "Admin Panel: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "Home Page:   http://127.0.0.1:8000/" -ForegroundColor White
Write-Host ""
