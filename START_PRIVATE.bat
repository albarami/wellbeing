@echo off
echo ========================================
echo Academic Debate System - Private Mode
echo ========================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ✅ .env file created!
    echo.
    echo IMPORTANT: Set a strong password!
    echo 1. Open .env file
    echo 2. Find: APP_PASSWORD=scholar2024
    echo 3. Change to a secure password
    echo.
    pause
    exit /b
)

echo 🔐 Starting password-protected application...
echo.
echo Only users with the password can access!
echo.
echo Your app will be at: http://localhost:8000
echo.

chainlit run chainlit_app_with_auth.py

pause
