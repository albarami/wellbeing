#!/usr/bin/env python3
"""
Debug script to check Railway environment variables.
This will help identify if the API key is being set correctly in Railway.
"""

import os
import sys

print("=" * 60)
print("RAILWAY ENVIRONMENT DEBUG")
print("=" * 60)

# Check Railway detection
railway_static_url = os.getenv('RAILWAY_STATIC_URL')
railway_env_name = os.getenv('RAILWAY_ENVIRONMENT_NAME')
railway_project_id = os.getenv('RAILWAY_PROJECT_ID')
railway_service_id = os.getenv('RAILWAY_SERVICE_ID')

print("\n1. RAILWAY DETECTION:")
print(f"   RAILWAY_STATIC_URL: {railway_static_url or 'NOT SET'}")
print(f"   RAILWAY_ENVIRONMENT_NAME: {railway_env_name or 'NOT SET'}")
print(f"   RAILWAY_PROJECT_ID: {railway_project_id or 'NOT SET'}")
print(f"   RAILWAY_SERVICE_ID: {railway_service_id or 'NOT SET'}")

is_railway = railway_static_url or railway_env_name
print(f"\n   Is Railway? {bool(is_railway)}")

# Check API Key
anthropic_key = os.getenv('ANTHROPIC_API_KEY')
print("\n2. ANTHROPIC API KEY:")
if anthropic_key:
    # Safely display partial key
    key_start = anthropic_key[:10] if len(anthropic_key) > 10 else anthropic_key[:4]
    key_end = anthropic_key[-4:]
    print(f"   ✅ FOUND: {key_start}...{key_end}")
    print(f"   Length: {len(anthropic_key)} characters")
    print(f"   Starts with 'sk-ant-': {anthropic_key.startswith('sk-ant-')}")
else:
    print("   ❌ NOT FOUND")
    print("\n   TROUBLESHOOTING STEPS:")
    print("   1. Go to Railway Dashboard → Your Project")
    print("   2. Click on your service")
    print("   3. Go to 'Variables' tab")
    print("   4. Add variable: ANTHROPIC_API_KEY")
    print("   5. Paste your API key (starts with sk-ant-)")
    print("   6. Click 'Add' and redeploy")

# Check all environment variables (sanitized)
print("\n3. ALL ENVIRONMENT VARIABLES:")
env_vars = sorted(os.environ.keys())
for var in env_vars:
    value = os.getenv(var, '')
    # Sanitize sensitive values
    if 'KEY' in var or 'SECRET' in var or 'TOKEN' in var or 'PASSWORD' in var:
        if value:
            display = f"{value[:6]}...{value[-4:]}" if len(value) > 10 else "***"
        else:
            display = "NOT SET"
    else:
        display = value[:50] + "..." if len(value) > 50 else value

    print(f"   {var}: {display}")

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)

# Exit with error if no API key
if not anthropic_key:
    print("\n❌ CRITICAL: ANTHROPIC_API_KEY is not set!")
    sys.exit(1)
else:
    print("\n✅ SUCCESS: API key is properly configured!")
    sys.exit(0)
