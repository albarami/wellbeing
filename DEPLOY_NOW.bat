@echo off
echo ========================================
echo Academic Debate System - Quick Deploy
echo ========================================
echo.

echo Choose deployment method:
echo.
echo 1. Chainlit Cloud (Easiest - 5 minutes)
echo 2. ngrok (Temporary demo link - 2 minutes)
echo 3. Show full deployment guide
echo.

set /p choice="Enter choice (1-3): "

if "%choice%"=="1" goto chainlit
if "%choice%"=="2" goto ngrok
if "%choice%"=="3" goto guide
goto end

:chainlit
echo.
echo ========================================
echo Deploying to Chainlit Cloud
echo ========================================
echo.
echo Step 1: Logging in to Chainlit Cloud...
chainlit login

echo.
echo Step 2: Deploying your app...
chainlit deploy

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Your app is now live!
echo.
echo IMPORTANT: Add your API keys in the Chainlit Cloud dashboard:
echo - Go to https://cloud.chainlit.io/
echo - Select your project
echo - Add ANTHROPIC_API_KEY and other keys
echo.
pause
goto end

:ngrok
echo.
echo ========================================
echo Setting up ngrok tunnel
echo ========================================
echo.
echo BEFORE USING NGROK:
echo 1. Download ngrok from: https://ngrok.com/download
echo 2. Sign up for free account: https://ngrok.com/
echo 3. Get your auth token from dashboard
echo 4. Run: ngrok config add-authtoken YOUR_TOKEN
echo.
echo Have you completed these steps? (Y/N)
set /p ready="Ready? (Y/N): "

if /i "%ready%"=="Y" (
    echo.
    echo Starting Chainlit app...
    start cmd /k "cd /d "%~dp0" && chainlit run chainlit_app.py"
    
    timeout /t 3
    
    echo.
    echo Starting ngrok tunnel...
    echo.
    echo Copy the https URL that appears below and share it!
    echo.
    ngrok http 8000
) else (
    echo.
    echo Please complete the setup steps first, then run this script again.
)
pause
goto end

:guide
echo.
echo Opening deployment guide...
start DEPLOYMENT_GUIDE.md
pause
goto end

:end
echo.
echo Press any key to exit...
pause >nul
