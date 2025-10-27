# 🚀 Quick Start: Verification Tools

## ⚡ 3-Minute Setup

### Step 1: Install Dependencies (30 seconds)
```bash
pip install requests beautifulsoup4
```

### Step 2: Test What Works NOW (1 minute)
```bash
# Test citation verification (works without API keys)
python -c "from src.academic_debate_council.tools.citation_verifier import verify_citation_standalone; print(verify_citation_standalone('Cipriani', '2018', 'antidepressant')['data'])"

# Test Quran retrieval (works without API keys)
python -c "from src.academic_debate_council.tools.islamic_texts import get_quran_verse_standalone; print(get_quran_verse_standalone(2, 177)['data'])"
```

### Step 3: Get FREE API Keys (1.5 minutes)

**Sunnah.com** (for hadith verification):
- Visit: https://sunnah.api-docs.io/
- Click "Get API Key"
- Add to `.env`: `SUNNAH_API_KEY=your_key`

**Brave Search** (for fact-checking):
- Visit: https://brave.com/search/api/
- Sign up for free tier
- Add to `.env`: `BRAVE_API_KEY=your_key`

---

## 🎯 What You Get

### ✅ Works Immediately (No Setup)
- **Citation verification** - Semantic Scholar API
- **Medical research** - PubMed API
- **Quran verses** - Quran.com API

### 🔑 With FREE API Keys
- **Hadith verification** - Sunnah.com
- **Web search** - Brave Search
- **Qatar statistics** - Via Brave Search

---

## 📝 Usage Examples

### Verify a Citation
```python
from academic_debate_council.tools import CitationVerifierTool

tool = CitationVerifierTool()
result = tool._run(
    author="Beck",
    year="1979", 
    title_keywords="cognitive therapy depression"
)
```

### Search Hadith
```python
from academic_debate_council.tools import HadithSearchTool

tool = HadithSearchTool()
result = tool._run(
    query="justice employment",
    collections=['bukhari', 'muslim']
)
```

### Get Quran Verse
```python
from academic_debate_council.tools import QuranVerseTool

tool = QuranVerseTool()
result = tool._run(surah=2, ayah=177)
```

### Fact-Check with Web Search
```python
from academic_debate_council.tools import BraveSearchTool

tool = BraveSearchTool()
result = tool._run(
    query="Qatar labor statistics",
    academic_only=True
)
```

---

## 🤖 Integrate with Agents

```python
from crewai import Agent
from academic_debate_council.tools import (
    CitationVerifierTool,
    HadithSearchTool,
    QuranVerseTool
)

spiritual_agent = Agent(
    role="Islamic Scholar",
    goal="Provide verified Islamic perspective",
    backstory="Expert in Islamic sciences",
    tools=[
        HadithSearchTool(),
        QuranVerseTool()
    ]
)
```

---

## 📊 Run Full Test Suite

```bash
# Test all tools
python test_verification_tools.py
```

---

## 📚 Full Documentation

- **Complete Guide**: `VERIFICATION_TOOLS_GUIDE.md`
- **API Keys Setup**: `.env.example`
- **Integration Examples**: `examples/agent_integration_example.py`

---

## ❓ Troubleshooting

**"Module not found"**
→ Run: `pip install -e .`

**"API key not configured"**  
→ Check `.env` file has the key

**"No results found"**
→ This is correct - try different keywords

---

## 🎯 Next Steps

1. ✅ Test tools: `python test_verification_tools.py`
2. 🔑 Get API keys (5 min)
3. 🤖 Integrate with agents
4. 📊 Measure accuracy improvement

**Goal**: Eliminate hallucinated citations and ground agents in verified sources!
