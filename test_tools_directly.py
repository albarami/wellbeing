"""
Direct test of verification tools to confirm they work independently.
"""
import sys
import os

# Add the src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*80)
print("🧪 TESTING VERIFICATION TOOLS DIRECTLY")
print("="*80)

# Test 1: Import tools
print("\n📦 TEST 1: Importing tools...")
try:
    from academic_debate_council.tools import (
        search_hadith_standalone,
        get_quran_verse_standalone,
        search_madhab_fatwa_standalone,
        verify_citation_standalone,
        verify_medical_claim_standalone,
        perplexity_fact_check_standalone
    )
    print("✅ All tools imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Get Quran Verse
print("\n📖 TEST 2: Getting Quran verse...")
try:
    result = get_quran_verse_standalone(4, 103)
    if "4:103" in result and "صَّلَوٰة" in result:
        print("✅ Quran verse retrieved successfully")
        print(f"   Preview: {result[:100]}...")
    else:
        print(f"⚠️ Unexpected result: {result[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Search Hadith
print("\n📜 TEST 3: Searching hadith...")
try:
    result = search_hadith_standalone("prayer time")
    if "Sahih" in result or "hadith" in result.lower():
        print("✅ Hadith search returned results")
        print(f"   Preview: {result[:150]}...")
    else:
        print(f"⚠️ Unexpected result: {result[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Search Madhab Fatwa
print("\n🕌 TEST 4: Searching madhab fatwa...")
try:
    result = search_madhab_fatwa_standalone("workplace prayer", "hanafi")
    print(f"✅ Madhab search completed")
    print(f"   Preview: {result[:150]}...")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Verify Citation
print("\n📚 TEST 5: Verifying academic citation...")
try:
    result = verify_citation_standalone("Deci", "2000", "self-determination")
    if "Deci" in result or "citation" in result.lower():
        print("✅ Citation verification completed")
        print(f"   Preview: {result[:150]}...")
    else:
        print(f"⚠️ Unexpected result: {result[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 6: Verify Medical Claim
print("\n🏥 TEST 6: Verifying medical research...")
try:
    result = verify_medical_claim_standalone("prayer stress reduction")
    print(f"✅ Medical claim verification completed")
    print(f"   Preview: {result[:150]}...")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 7: Perplexity Fact Check
print("\n🌐 TEST 7: Perplexity fact check...")
try:
    result = perplexity_fact_check_standalone("Qatar workplace prayer breaks policy")
    if len(result) > 50:
        print("✅ Perplexity fact check completed")
        print(f"   Preview: {result[:150]}...")
    else:
        print(f"⚠️ Short result: {result}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*80)
print("✅ TOOL TESTING COMPLETE")
print("="*80)
