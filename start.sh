#!/bin/bash
# Railway startup script for Chainlit

echo "================================"
echo "RAILWAY DEPLOYMENT STARTING"
echo "================================"

# Debug: Check environment variables
echo ""
echo "Checking environment variables..."
python debug_railway_env.py

# Check if debug script passed
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Environment check failed! Check the logs above."
    echo "Continuing anyway to show error in UI..."
fi

echo ""
echo "Starting Chainlit on PORT: $PORT"
chainlit run chainlit_app.py --host 0.0.0.0 --port $PORT -h
