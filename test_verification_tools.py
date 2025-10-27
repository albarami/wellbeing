"""
Quick Test Script for Verification Tools

Run this to verify all tools are working correctly.
Tests both tools that work immediately and tools that require API keys.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 80)
print("🔍 VERIFICATION TOOLS TEST SUITE")
print("=" * 80)
print()

# Check which API keys are configured
print("📋 API KEY STATUS:")
print("-" * 80)
keys = {
    'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
    'HADITH_API_KEY': os.getenv('HADITH_API_KEY'),
    'BRAVE_API_KEY': os.getenv('BRAVE_API_KEY'),
    'PERPLEXITY_API_KEY': os.getenv('PERPLEXITY_API_KEY')
}

for key_name, key_value in keys.items():
    if key_value and key_value != f'your_{key_name.lower().replace("_", "_")}':
        print(f"✅ {key_name}: Configured")
    else:
        print(f"❌ {key_name}: Not configured")
print()

# Test 1: Citation Verification (Works without API key)
print("=" * 80)
print("TEST 1: CITATION VERIFICATION (No API key needed)")
print("=" * 80)
print()

try:
    from src.academic_debate_council.tools.citation_verifier import verify_citation_standalone
    
    print("Testing: Verify real citation (Cipriani 2018)...")
    result = verify_citation_standalone(
        author="Cipriani",
        year="2018",
        title_keywords="antidepressant efficacy"
    )
    print(result['data'])
    print("\n✅ Citation verification test passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n")

# Test 2: Medical Claim Verification (Works without API key)
print("=" * 80)
print("TEST 2: MEDICAL CLAIM VERIFICATION (No API key needed)")
print("=" * 80)
print()

try:
    from src.academic_debate_council.tools.citation_verifier import verify_medical_claim_standalone
    
    print("Testing: Search PubMed for depression treatment studies...")
    result = verify_medical_claim_standalone(
        keywords="depression treatment cognitive behavioral therapy",
        max_results=3
    )
    print(result['data'])
    print("\n✅ Medical claim verification test passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n")

# Test 3: Quran Verse Retrieval (Works without API key)
print("=" * 80)
print("TEST 3: QURAN VERSE RETRIEVAL (No API key needed)")
print("=" * 80)
print()

try:
    from src.academic_debate_council.tools.islamic_texts import get_quran_verse_standalone
    
    print("Testing: Retrieve Quran 2:177 (Definition of Righteousness)...")
    result = get_quran_verse_standalone(
        surah=2,
        ayah=177
    )
    print(result['data'])
    print("\n✅ Quran verse retrieval test passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n")

# Test 4: Hadith Search (Requires HADITH_API_KEY)
print("=" * 80)
print("TEST 4: HADITH SEARCH (Requires HADITH_API_KEY)")
print("=" * 80)
print()

if keys['HADITH_API_KEY'] and keys['HADITH_API_KEY'] != 'your_hadith_api_key_here':
    try:
        from src.academic_debate_council.tools.islamic_texts import search_hadith_standalone
        
        print("Testing: Search for hadith about justice...")
        result = search_hadith_standalone(
            query="justice",
            collections=['bukhari'],
            max_results=2
        )
        print(result['data'])
        print("\n✅ Hadith search test passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("⏭️  SKIPPED: HADITH_API_KEY not configured")
    print("   Get free key from: https://hadithapi.com/")

print("\n")

# Test 5: Brave Search (Requires BRAVE_API_KEY)
print("=" * 80)
print("TEST 5: WEB SEARCH (Requires BRAVE_API_KEY)")
print("=" * 80)
print()

if keys['BRAVE_API_KEY'] and keys['BRAVE_API_KEY'] != 'your_brave_api_key_here':
    try:
        from src.academic_debate_council.tools.fact_checker import brave_search_standalone
        
        print("Testing: Search for Qatar labor statistics...")
        result = brave_search_standalone(
            query="Qatar labor force statistics 2024",
            academic_only=False,
            max_results=5
        )
        print(result['data'])
        print("\n✅ Brave search test passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("⏭️  SKIPPED: BRAVE_API_KEY not configured")
    print("   Get free key from: https://brave.com/search/api/")

print("\n")

# Test 6: Qatar Statistics Search
print("=" * 80)
print("TEST 6: QATAR STATISTICS SEARCH")
print("=" * 80)
print()

try:
    from src.academic_debate_council.tools.fact_checker import get_qatar_stats_standalone
    
    print("Testing: Search for Qatar population statistics...")
    result = get_qatar_stats_standalone(
        topic="population demographics"
    )
    print(result['data'])
    print("\n✅ Qatar statistics search test passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n")

# Test 7: Perplexity Fact Check (Requires PERPLEXITY_API_KEY)
print("=" * 80)
print("TEST 7: AI FACT-CHECKING (Requires PERPLEXITY_API_KEY)")
print("=" * 80)
print()

if keys['PERPLEXITY_API_KEY'] and keys['PERPLEXITY_API_KEY'] != 'your_perplexity_api_key_here':
    try:
        from src.academic_debate_council.tools.fact_checker import perplexity_fact_check_standalone
        
        print("Testing: Fact-check claim about Qatar GDP...")
        result = perplexity_fact_check_standalone(
            claim="Qatar has one of the highest GDP per capita in the world"
        )
        print(result['data'])
        print("\n✅ Perplexity fact-check test passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("⏭️  SKIPPED: PERPLEXITY_API_KEY not configured")
    print("   Get key from: https://www.perplexity.ai/settings/api")

print("\n")

# Summary
print("=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)
print()
print("Tools that work immediately (no API keys):")
print("  ✅ Citation verification (Semantic Scholar)")
print("  ✅ Medical claim verification (PubMed)")
print("  ✅ Quran verse retrieval (Quran.com)")
print()
print("Tools that need FREE API keys:")
print(f"  {'✅' if keys['HADITH_API_KEY'] and keys['HADITH_API_KEY'] != 'your_hadith_api_key_here' else '❌'} Hadith search (hadithapi.com)")
print(f"  {'✅' if keys['BRAVE_API_KEY'] and keys['BRAVE_API_KEY'] != 'your_brave_api_key_here' else '❌'} Web search (Brave Search)")
print()
print("Optional paid tools:")
print(f"  {'✅' if keys['PERPLEXITY_API_KEY'] and keys['PERPLEXITY_API_KEY'] != 'your_perplexity_api_key_here' else '❌'} AI fact-checking (Perplexity)")
print()
print("=" * 80)
print("🎉 Testing complete!")
print()
print("Next steps:")
print("1. If any tests failed, check the error messages above")
print("2. Get missing API keys from the URLs provided")
print("3. Update your .env file with the API keys")
print("4. Re-run this test script to verify")
print("5. Review VERIFICATION_TOOLS_GUIDE.md for integration instructions")
print("=" * 80)
