# Complete GitHub Push Script
Set-Location "D:\Academic debate"

Write-Host "Configuring git..." -ForegroundColor Yellow
& git config user.name "Salim AL-Barami"
& git config user.email "albarami@users.noreply.github.com"

Write-Host "Adding files..." -ForegroundColor Yellow
& git add .

Write-Host "Committing..." -ForegroundColor Yellow
& git commit -m "Major update: citation improvements and deployment guides"

Write-Host "Setting branch to main..." -ForegroundColor Yellow
& git branch -M main

Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
& git push -u origin main --force

Write-Host ""
Write-Host "Done! Check output above for any errors." -ForegroundColor Green
Write-Host "Repository: https://github.com/albarami/wellbeing" -ForegroundColor Cyan
