# 🚀 Verification Tools - Quick Reference Card

## 📊 **10 Production-Ready Tools**

| Tool | Type | API Key? | What It Does |
|------|------|----------|--------------|
| `CitationVerifierTool` | API | ❌ No | Verify academic papers (Semantic Scholar) |
| `MedicalClaimVerifierTool` | API | ❌ No | Search medical research (PubMed) |
| `QuranVerseTool` | API | ❌ No | Get Quranic verses (Quran.com) |
| `ShamelaSearchTool` | **WEB SCRAPE** | ❌ No | **Scrape Islamic texts (IslamQA, Seekers)** |
| `QatarStatsTool` | **WEB SCRAPE** | ❌ No | **Scrape Qatar stats (World Bank, Trading Econ)** |
| `MadhabFatwaTool` | **WEB SCRAPE** | ❌ No | **Scrape madhab fatwas (all 4 madhabs)** |
| `HadithSearchTool` | API | ✅ FREE | Search hadith (Sunnah.com) |
| `BraveSearchTool` | API | ✅ FREE | Web search (Brave - 2000/month) |
| `PerplexityFactCheckTool` | API | 💰 Paid | AI fact-checking (Perplexity - $5) |

---

## ⚡ **Works RIGHT NOW (No Setup)**

```python
# Citation verification
from academic_debate_council.tools import verify_citation_standalone
result = verify_citation_standalone("Beck", "1979", "cognitive therapy")

# Quran verses
from academic_debate_council.tools import get_quran_verse_standalone
result = get_quran_verse_standalone(2, 177)

# Islamic text scraping (FUNCTIONAL!)
from academic_debate_council.tools import search_shamela_standalone
result = search_shamela_standalone("workplace prayer")

# Qatar statistics scraping (FUNCTIONAL!)
from academic_debate_council.tools import get_qatar_stats_standalone
result = get_qatar_stats_standalone("population")

# Madhab fatwa scraping (FUNCTIONAL!)
from academic_debate_council.tools import search_madhab_fatwa_standalone
result = search_madhab_fatwa_standalone("fasting", "hanafi")
```

---

## 🔑 **Get FREE API Keys (5 min)**

### Sunnah.com (for hadith)
```
URL: https://sunnah.api-docs.io/
Add to .env: SUNNAH_API_KEY=your_key
```

### Brave Search (for fact-checking)
```
URL: https://brave.com/search/api/
Add to .env: BRAVE_API_KEY=your_key
Free tier: 2000 searches/month
```

---

## 🤖 **Agent Integration**

### Spiritual Agent
```python
from crewai import Agent
from academic_debate_council.tools import (
    HadithSearchTool,
    QuranVerseTool,
    ShamelaSearchTool,
    MadhabFatwaTool
)

spiritual_agent = Agent(
    role="Islamic Scholar",
    tools=[
        HadithSearchTool(),
        QuranVerseTool(),
        ShamelaSearchTool(),    # Scrapes real fatwas
        MadhabFatwaTool()       # Scrapes madhab rulings
    ]
)
```

### Physical/Health Agent
```python
physical_agent = Agent(
    role="Health Analyst",
    tools=[
        CitationVerifierTool(),
        MedicalClaimVerifierTool()
    ]
)
```

### Social Agent
```python
social_agent = Agent(
    role="Qatar Analyst",
    tools=[
        QatarStatsTool(),      # Scrapes real statistics
        BraveSearchTool()
    ]
)
```

---

## 🧪 **Testing**

```bash
# Test everything
python test_verification_tools.py

# Test functional scraping
python test_functional_scraping.py

# Test individual tool
python src/academic_debate_council/tools/citation_verifier.py
python src/academic_debate_council/tools/islamic_texts.py
python src/academic_debate_council/tools/fact_checker.py
```

---

## 📚 **Documentation**

| File | Purpose |
|------|---------|
| `QUICK_START_VERIFICATION.md` | 3-minute overview |
| `FUNCTIONAL_TOOLS_SUMMARY.md` | What's functional |
| `VERIFICATION_TOOLS_GUIDE.md` | Complete guide |
| `SETUP_INSTRUCTIONS.md` | Step-by-step setup |

---

## 🎯 **What Makes These Tools Functional**

### ✅ **Real Web Scraping**
- BeautifulSoup4 + Requests
- Scrapes 2-3 sources per query
- Extracts titles, URLs, text
- Rate limiting built-in

### ✅ **Real API Integration**
- Semantic Scholar (free)
- PubMed (free)
- Quran.com (free)
- Sunnah.com (free key)
- Brave Search (free tier)

### ✅ **Production Quality**
- Error handling
- Graceful fallbacks
- Timeout protection
- Clear output format

---

## 💡 **Example Outputs**

### Islamic Text Search
```
📚 CLASSICAL ISLAMIC TEXT SEARCH RESULTS
Query: workplace prayer
Results found: 3

1. The ruling on praying in the workplace
   Source: IslamQA
   URL: https://islamqa.info/en/answers/...
   Excerpt: Islamic scholars agree that...
```

### Qatar Statistics
```
📊 QATAR STATISTICS (WEB SCRAPED)
Topic: population
Data points found: 2

1. Population, total
   Value: 2,930,524
   Year: 2023
   Source: World Bank
   URL: https://data.worldbank.org/country/qatar
```

### Madhab Fatwas
```
🕌 MADHAB FATWA SEARCH RESULTS
Topic: employment contracts
Madhab: Hanafi

📖 Hanafi Madhab:
  1. Employment Contract Conditions
     Source: IslamQA Hanafi
     URL: https://islamqa.org/hanafi/...
```

---

## 🔥 **Key Differences**

### Before (Placeholders)
```
❌ "Visit psa.gov.qa for Qatar statistics"
❌ "Search islamqa.org manually"
❌ No actual data
❌ No verification
```

### After (Functional)
```
✅ Real scraped data with numbers
✅ Actual URLs to sources
✅ Text excerpts from articles
✅ Multiple sources verified
```

---

## 🚀 **Start Using Now**

```bash
# 1. Install
pip install -e .

# 2. Test
python test_functional_scraping.py

# 3. Integrate
# Add tools to your agents (see examples above)
```

**NO PLACEHOLDERS. ALL FUNCTIONAL. PRODUCTION-READY.** 🎉
