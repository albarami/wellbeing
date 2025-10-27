"""
Test what format the tools actually return.
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from academic_debate_council.tools import (
    search_hadith_standalone,
    get_quran_verse_standalone,
    verify_citation_standalone
)

print("="*80)
print("🔍 TESTING TOOL RETURN FORMATS")
print("="*80)

# Test 1: Quran verse
print("\n📖 TEST 1: Quran verse return type...")
result = get_quran_verse_standalone(4, 103)
print(f"Type: {type(result)}")
print(f"Content: {result}")

# Test 2: Hadith search
print("\n📜 TEST 2: Hadith search return type...")
result = search_hadith_standalone("prayer")
print(f"Type: {type(result)}")
print(f"Content: {result}")

# Test 3: Citation
print("\n📚 TEST 3: Citation return type...")
result = verify_citation_standalone("Deci", "2000", "motivation")
print(f"Type: {type(result)}")
print(f"Content: {result}")

print("\n" + "="*80)
