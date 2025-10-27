"""
Quick test for hadithapi.com integration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 80)
print("🧪 TESTING HADITH API INTEGRATION")
print("=" * 80)
print()

# Check if API key is configured
api_key = os.getenv('HADITH_API_KEY')
if api_key:
    print(f"✅ HADITH_API_KEY found: {api_key[:20]}...")
else:
    print("❌ HADITH_API_KEY not found in .env file")
    print()
    print("Add to your .env file:")
    print("HADITH_API_KEY=your_actual_api_key_here")
    exit(1)

print()
print("Testing hadith search...")
print("-" * 80)

try:
    # Force reload to get latest code changes
    import sys
    if 'src.academic_debate_council.tools' in sys.modules:
        del sys.modules['src.academic_debate_council.tools']
    if 'src.academic_debate_council.tools.islamic_texts' in sys.modules:
        del sys.modules['src.academic_debate_council.tools.islamic_texts']
    
    from src.academic_debate_council.tools import search_hadith_standalone
    
    # Test search
    result = search_hadith_standalone("prayer obligation", max_results=2)
    
    print(result['data'])
    
    print()
    print("=" * 80)
    print("✅ SUCCESS! Hadith API is working!")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Make sure:")
    print("1. You have added HADITH_API_KEY to .env")
    print("2. The API key is valid")
    print("3. You have internet connection")
