#!/bin/bash
cd "D:/Academic debate"
git config user.name "Salim AL-Barami"
git config user.email "albarami@users.noreply.github.com"
git commit -m "Major update with citation improvements and deployment guides"
git branch -M main
git push -u origin main --force
