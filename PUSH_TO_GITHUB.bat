@echo off
echo ========================================
echo Push Updates to GitHub Repository
echo ========================================
echo.

echo Repository: https://github.com/albarami/wellbeing
echo.

REM Initialize git if needed
if not exist ".git" (
    echo Initializing git repository...
    git init
    git branch -M main
)

REM Set remote if not exists
git remote remove origin 2>nul
git remote add origin https://github.com/albarami/wellbeing.git

echo.
echo Adding all files...
git add .

echo.
echo Creating commit...
git commit -m "Major Update: Citation verifier improvements, WebSocket fixes, deployment guides

- Upgraded Semantic Scholar API integration (bulk search, better queries)
- Fixed WebSocket timeout issues with thread pool executor
- Added comprehensive deployment guides (Hugging Face, Railway, etc.)
- Implemented password protection for private access
- Enhanced error handling and tool execution
- Added documentation for all improvements
- Created easy deployment scripts"

echo.
echo Pushing to GitHub...
git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ Successfully pushed to GitHub!
    echo ========================================
    echo.
    echo Your repository is now updated at:
    echo https://github.com/albarami/wellbeing
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ Push failed
    echo ========================================
    echo.
    echo This might be because:
    echo 1. You need to authenticate with GitHub
    echo 2. You don't have push access to the repository
    echo.
    echo To fix:
    echo 1. Install GitHub CLI: https://cli.github.com/
    echo 2. Run: gh auth login
    echo 3. Try running this script again
    echo.
    echo OR manually push:
    echo git push -u origin main
    echo.
)

pause
