"""
Debug script to see what's happening with the Hadith API
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('HADITH_API_KEY')

print("=" * 80)
print("🔍 DEBUGGING HADITH API")
print("=" * 80)
print()

print(f"API Key: {api_key[:20]}...")
print()

# Test 1: Basic endpoint with just API key
print("TEST 1: Basic endpoint (no search)")
print("-" * 80)
url1 = f"https://hadithapi.com/api/hadiths?apiKey={api_key}"
print(f"URL: {url1[:60]}...")
response1 = requests.get(url1, timeout=10)
print(f"Status: {response1.status_code}")
if response1.status_code == 200:
    data = response1.json()
    print(f"Response keys: {list(data.keys())}")
    if 'hadiths' in data:
        print(f"Hadiths found: {len(data['hadiths'].get('data', []))}")
else:
    print(f"Error: {response1.text[:200]}")

print()

# Test 2: With search term
print("TEST 2: With English search term")
print("-" * 80)
url2 = f"https://hadithapi.com/api/hadiths?apiKey={api_key}&hadithEnglish=prayer"
print(f"URL: {url2[:70]}...")
response2 = requests.get(url2, timeout=10)
print(f"Status: {response2.status_code}")
if response2.status_code == 200:
    data = response2.json()
    print(f"Response keys: {list(data.keys())}")
    if 'hadiths' in data:
        print(f"Hadiths found: {len(data['hadiths'].get('data', []))}")
        if data['hadiths'].get('data'):
            first = data['hadiths']['data'][0]
            print(f"First hadith keys: {list(first.keys())}")
else:
    print(f"Error: {response2.text[:200]}")

print()

# Test 3: With book filter
print("TEST 3: With book filter (sahih-bukhari)")
print("-" * 80)
url3 = f"https://hadithapi.com/api/hadiths?apiKey={api_key}&book=sahih-bukhari&paginate=5"
print(f"URL: {url3[:70]}...")
response3 = requests.get(url3, timeout=10)
print(f"Status: {response3.status_code}")
if response3.status_code == 200:
    data = response3.json()
    print(f"Response keys: {list(data.keys())}")
    if 'hadiths' in data:
        print(f"Hadiths found: {len(data['hadiths'].get('data', []))}")
else:
    print(f"Error: {response3.text[:200]}")

print()
print("=" * 80)
