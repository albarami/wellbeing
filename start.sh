#!/bin/bash
# Railway startup script for Chainlit
echo "Starting Chainlit on PORT: $PORT"
chainlit run chainlit_app.py --host 0.0.0.0 --port $PORT -h
