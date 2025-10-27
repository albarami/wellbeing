"""Quick test of verification tools without CrewAI"""

print("Testing citation verification...")
from src.academic_debate_council.tools.citation_verifier import verify_citation_standalone

result = verify_citation_standalone('Cipriani', '2018', 'antidepressant efficacy')
print(result['data'][:500])
print("\n✅ Citation verification works!")

print("\n" + "="*80)
print("Testing Quran verse retrieval...")
from src.academic_debate_council.tools.islamic_texts import get_quran_verse_standalone

result2 = get_quran_verse_standalone(2, 177)
print(result2['data'][:500])
print("\n✅ Quran verse retrieval works!")
