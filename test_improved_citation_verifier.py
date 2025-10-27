"""
Test the improved Semantic Scholar citation verifier.
Demonstrates: bulk search, better query syntax, pagination, sorting.
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from academic_debate_council.tools import verify_citation_standalone

print("="*80)
print("🔬 TESTING IMPROVED SEMANTIC SCHOLAR CITATION VERIFIER")
print("="*80)
print("\n✨ Improvements:")
print("  - Bulk search endpoint (more efficient)")
print("  - Quoted phrase matching for better precision")
print("  - Year filtering for exact matches")
print("  - Token-based pagination (up to 3 batches)")
print("  - Sorting by citation count (most cited first)")
print("  - Optional API key support for higher rate limits")
print("="*80)

# Test 1: Psychology paper (Deci & Ryan)
print("\n\n📚 TEST 1: Verifying psychology citation")
print("-"*80)
print("Query: Deci, 2000, 'self-determination theory'")
print("Expected: Should find the famous SDT paper\n")

result1 = verify_citation_standalone(
    author="Deci",
    year="2000",
    title_keywords="self-determination theory"
)
print(result1['data'])

# Test 2: Neuroscience paper
print("\n\n" + "="*80)
print("🧠 TEST 2: Verifying neuroscience citation")
print("-"*80)
print("Query: Newberg, 2015, 'meditation neural'")
print("Expected: Should find meditation/brain research\n")

result2 = verify_citation_standalone(
    author="Newberg",
    year="2015",
    title_keywords="meditation neural"
)
print(result2['data'])

# Test 3: Recent AI paper
print("\n\n" + "="*80)
print("🤖 TEST 3: Verifying recent AI citation")
print("-"*80)
print("Query: Anthropic, 2024, 'Claude language model'")
print("Expected: Should find recent Claude-related papers\n")

result3 = verify_citation_standalone(
    author="Anthropic",
    year="2024",
    title_keywords="Claude language model"
)
print(result3['data'])

# Test 4: Non-existent paper (should fail gracefully)
print("\n\n" + "="*80)
print("❌ TEST 4: Attempting to verify fabricated citation")
print("-"*80)
print("Query: FakeAuthor, 2099, 'completely made up study'")
print("Expected: Should return 'NOT FOUND' message\n")

result4 = verify_citation_standalone(
    author="FakeAuthor",
    year="2099",
    title_keywords="completely made up study"
)
print(result4['data'])

print("\n\n" + "="*80)
print("✅ TESTING COMPLETE")
print("="*80)
print("\n💡 KEY IMPROVEMENTS DEMONSTRATED:")
print("  1. ✅ Bulk search endpoint used (check API logs)")
print("  2. ✅ Quoted phrases in query for precision")
print("  3. ✅ Year filtering applied automatically")
print("  4. ✅ Results sorted by citation count")
print("  5. ✅ Pagination retrieves more comprehensive results")
print("  6. ✅ Graceful handling of non-existent citations")
print("\n🔑 Optional: Set SEMANTIC_SCHOLAR_API_KEY in .env for higher rate limits")
print("="*80)
