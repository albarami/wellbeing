#!/bin/bash
# Railway startup script for Chainlit
chainlit run chainlit_app.py --host 0.0.0.0 --port ${PORT:-8000} -h
