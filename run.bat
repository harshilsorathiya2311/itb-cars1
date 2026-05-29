@echo off
echo ========================================
echo    YourCars - Start Development Server
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Starting Django development server...
echo.
echo Admin Panel: http://127.0.0.1:8000/admin/
echo Home Page:   http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server.
echo.

python manage.py runserver
