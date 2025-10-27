@echo off
echo ========================================
echo Deploy to Hugging Face Spaces
echo ========================================
echo.

echo BEFORE RUNNING THIS SCRIPT:
echo 1. Create account at https://huggingface.co/join
echo 2. Create new Space:
echo    - Go to https://huggingface.co/new-space
echo    - Name: academic-debate-council
echo    - SDK: Docker
echo    - Visibility: Public
echo 3. Get your write token from https://huggingface.co/settings/tokens
echo.

set /p ready="Have you completed steps 1-3? (Y/N): "
if /i not "%ready%"=="Y" (
    echo.
    echo Please complete the setup steps first.
    pause
    exit /b
)

echo.
set /p username="Enter your Hugging Face username: "
set /p token="Enter your Hugging Face write token: "

echo.
echo ========================================
echo Preparing repository...
echo ========================================

REM Initialize git if needed
if not exist ".git" (
    echo Initializing git repository...
    git init
)

REM Copy README
if exist "README_HF.md" (
    copy /Y README_HF.md README.md
    echo README.md created for Hugging Face
)

REM Add files
echo Adding files to git...
git add .
git commit -m "Initial deployment to Hugging Face Spaces"

REM Set up remote
echo.
echo Setting up Hugging Face remote...
git remote remove huggingface 2>nul
git remote add huggingface https://%username%:%token%@huggingface.co/spaces/%username%/academic-debate-council

echo.
echo ========================================
echo Pushing to Hugging Face...
echo ========================================
git push huggingface main -f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Deployment Successful! 
    echo ========================================
    echo.
    echo Your app will be available at:
    echo https://huggingface.co/spaces/%username%/academic-debate-council
    echo.
    echo IMPORTANT: Add your API keys in Space Settings:
    echo 1. Go to your Space on Hugging Face
    echo 2. Click "Settings" tab
    echo 3. Scroll to "Repository secrets"
    echo 4. Add these secrets:
    echo    - ANTHROPIC_API_KEY
    echo    - HADITH_API_KEY (optional)
    echo    - BRAVE_API_KEY (optional)
    echo    - PERPLEXITY_API_KEY (optional)
    echo.
    echo The Space will automatically rebuild and start!
    echo Build time: 5-10 minutes
    echo.
) else (
    echo.
    echo ========================================
    echo Deployment Failed
    echo ========================================
    echo.
    echo Please check:
    echo - Your username and token are correct
    echo - You created the Space on Hugging Face
    echo - The Space name matches: academic-debate-council
    echo.
)

pause
