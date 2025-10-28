#!/usr/bin/env python3
"""
Debug script to check environment variables in Railway
"""
import os

print("=== ENVIRONMENT DEBUG ===")
print(f"ANTHROPIC_API_KEY exists: {'ANTHROPIC_API_KEY' in os.environ}")
print(f"ANTHROPIC_API_KEY value: {os.getenv('ANTHROPIC_API_KEY', 'NOT_FOUND')[:20]}...")
print(f"RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT', 'NOT_FOUND')}")
print(f"PORT: {os.getenv('PORT', 'NOT_FOUND')}")

print("\nAll environment variables containing 'API':")
for key, value in os.environ.items():
    if 'API' in key.upper():
        print(f"  {key}: {value[:20]}...")

print("\nAll environment variables containing 'ANTHROPIC':")
for key, value in os.environ.items():
    if 'ANTHROPIC' in key.upper():
        print(f"  {key}: {value[:20]}...")
