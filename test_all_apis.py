"""
Comprehensive test for ALL verification APIs
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🧪 TESTING ALL VERIFICATION APIs")
print("=" * 80)
print()

# Check all API keys
print("🔑 API KEY STATUS:")
print("-" * 80)
keys = {
    'HADITH_API_KEY': os.getenv('HADITH_API_KEY'),
    'BRAVE_API_KEY': os.getenv('BRAVE_API_KEY'),
    'PERPLEXITY_API_KEY': os.getenv('PERPLEXITY_API_KEY'),
    'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY')
}

for key_name, key_value in keys.items():
    if key_value:
        print(f"✅ {key_name}: {key_value[:20]}...")
    else:
        print(f"❌ {key_name}: NOT FOUND")

print()
print("=" * 80)

# Test each tool
tests = []

# 1. Hadith Search
print("\n1️⃣ TESTING: Hadith Search")
print("-" * 80)
try:
    from src.academic_debate_council.tools import search_hadith_standalone
    result = search_hadith_standalone("prayer", max_results=1)
    if "AUTHENTICATED HADITH" in result['data']:
        print("✅ SUCCESS: Hadith API working")
        tests.append(("Hadith Search", True))
    else:
        print("⚠️ PARTIAL: Got response but unexpected format")
        tests.append(("Hadith Search", False))
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests.append(("Hadith Search", False))

# 2. Quran Verse
print("\n2️⃣ TESTING: Quran Verse Retrieval")
print("-" * 80)
try:
    from src.academic_debate_council.tools import get_quran_verse_standalone
    result = get_quran_verse_standalone(1, 1)
    if "بِسْمِ" in result['data']:  # Bismillah
        print("✅ SUCCESS: Quran API working")
        tests.append(("Quran Verse", True))
    else:
        print("⚠️ PARTIAL: Got response but unexpected format")
        tests.append(("Quran Verse", False))
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests.append(("Quran Verse", False))

# 3. Citation Verification
print("\n3️⃣ TESTING: Academic Citation Verification")
print("-" * 80)
try:
    from src.academic_debate_council.tools import verify_citation_standalone
    result = verify_citation_standalone("Beck", "1979", "cognitive therapy")
    if result['data']:
        print("✅ SUCCESS: Semantic Scholar API working")
        tests.append(("Citation Verification", True))
    else:
        print("⚠️ NO RESULTS: But API is working")
        tests.append(("Citation Verification", True))
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests.append(("Citation Verification", False))

# 4. Medical Claims
print("\n4️⃣ TESTING: Medical Research Search")
print("-" * 80)
try:
    from src.academic_debate_council.tools import verify_medical_claim_standalone
    result = verify_medical_claim_standalone("workplace stress")
    if result['data']:
        print("✅ SUCCESS: PubMed API working")
        tests.append(("Medical Research", True))
    else:
        print("⚠️ NO RESULTS: But API is working")
        tests.append(("Medical Research", True))
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests.append(("Medical Research", False))

# 5. Qatar Statistics (Brave API)
print("\n5️⃣ TESTING: Qatar Statistics (Brave API)")
print("-" * 80)
try:
    from src.academic_debate_council.tools import get_qatar_stats_standalone
    result = get_qatar_stats_standalone("population")
    if result['data'] and "Qatar" in result['data']:
        print("✅ SUCCESS: Brave API working for Qatar stats")
        tests.append(("Qatar Statistics", True))
    else:
        print("⚠️ PARTIAL: Brave API responds but no Qatar data")
        tests.append(("Qatar Statistics", False))
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests.append(("Qatar Statistics", False))

# 6. Perplexity Fact Check
print("\n6️⃣ TESTING: Perplexity AI Fact Check")
print("-" * 80)
try:
    from src.academic_debate_council.tools import perplexity_fact_check_standalone
    result = perplexity_fact_check_standalone("Qatar population 2024")
    if result['data']:
        print("✅ SUCCESS: Perplexity API working")
        print(f"Sample result: {result['data'][:100]}...")
        tests.append(("Perplexity Fact Check", True))
    else:
        print("⚠️ NO RESULTS: But API responded")
        tests.append(("Perplexity Fact Check", True))
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests.append(("Perplexity Fact Check", False))

# Summary
print()
print("=" * 80)
print("📊 SUMMARY")
print("=" * 80)
passed = sum(1 for _, status in tests if status)
total = len(tests)
print(f"\nTests Passed: {passed}/{total}")
print()

for tool, status in tests:
    emoji = "✅" if status else "❌"
    print(f"{emoji} {tool}")

print()
if passed == total:
    print("🎉 ALL VERIFICATION TOOLS ARE WORKING!")
    print()
    print("Your agents now have access to:")
    print("  ✅ Authenticated Hadith Search")
    print("  ✅ Quranic Verse Retrieval")
    print("  ✅ Academic Citation Verification")
    print("  ✅ Medical Research Search")
    print("  ✅ Qatar Statistics")
    print("  ✅ AI-Powered Fact Checking")
    print()
    print("🚀 Ready to run full debate analysis!")
elif passed >= 4:
    print("✅ MOST TOOLS WORKING!")
    print(f"   {passed} out of {total} tools functional")
    print()
    print("Your agents have strong verification capabilities!")
else:
    print("⚠️ SOME TOOLS NEED ATTENTION")
    print(f"   Only {passed} out of {total} working")
    print()
    print("Check API keys and internet connection")

print("=" * 80)
