@echo off
echo ================================================================================
echo  Academic Debate Council - Chainlit Server
echo  Anti-Freeze Improvements Applied
echo ================================================================================
echo.
echo Improvements:
echo  - Background heartbeat every 5 seconds prevents WebSocket timeout
echo  - API retry logic with progressive timeouts (5s, 10s)
echo  - Stream speed reduction to prevent API rate limiting
echo  - Task-level timeout protection (4 minutes max per agent)
echo  - Graceful error handling for all API failures
echo.
echo Starting Chainlit server...
echo.
echo IMPORTANT: Keep this window open while using the application!
echo            Access at: http://localhost:8000
echo.
echo ================================================================================
echo.

chainlit run chainlit_app.py -w

echo.
echo Server stopped.
pause
