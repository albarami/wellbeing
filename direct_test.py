"""
Direct test - imports and runs the code directly from file
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('HADITH_API_KEY')

print("=" * 80)
print("🔍 DIRECT CODE TEST")
print("=" * 80)
print()

print(f"API Key: {api_key[:20]}...")
print()

# Replicate the EXACT code from islamic_texts.py
query = "prayer obligation"
max_results = 3

try:
    # Use hadithapi.com search endpoint (no trailing slash!)
    search_url = "https://hadithapi.com/api/hadiths"
    
    params = {
        'apiKey': api_key,
        'hadithEnglish': query,
        'paginate': max_results
    }
    
    print(f"URL: {search_url}")
    print(f"Params: {params}")
    print()
    
    response = requests.get(search_url, params=params, timeout=15)
    
    print(f"Status Code: {response.status_code}")
    print(f"URL called: {response.url}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        
        if 'hadiths' in data:
            hadiths = data['hadiths']  # Direct list
            
            print(f"✅ Found {len(hadiths)} hadiths!")
            print()
            
            if hadiths:
                first = hadiths[0]
                print(f"First hadith:")
                print(f"  Number: {first.get('hadithNumber')}")
                print(f"  Text: {first.get('hadithEnglish', '')[:100]}...")
                print(f"  Status: {first.get('status')}")
                print()
                print("✅ SUCCESS - Code is working!")
        else:
            print("❌ No 'hadiths' key in response")
            print(f"Keys: {list(data.keys())}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
