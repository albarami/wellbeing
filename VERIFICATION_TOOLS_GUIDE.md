# 🔍 Verification Tools Implementation Guide

This guide explains how to use the new API-based verification tools to eliminate hallucinated citations and improve the accuracy of your Academic Debate Council system.

---

## 📋 **OVERVIEW**

Three new tool modules have been added to your system:

1. **`citation_verifier.py`** - Verify academic citations (Semantic Scholar, PubMed)
2. **`islamic_texts.py`** - Verify Islamic sources (Sunnah.com, Quran.com)
3. **`fact_checker.py`** - Real-time fact-checking (Brave Search, Perplexity AI)

### ✅ **What Works Immediately (NO API Keys Required)**

These tools work RIGHT NOW without any setup:

- ✅ **Citation verification** via Semantic Scholar API
- ✅ **Medical claim verification** via PubMed API  
- ✅ **Quran verse retrieval** via Quran.com API

### 🔑 **What Requires FREE API Keys**

Get these to unlock full functionality:

- 🔑 **Hadith verification** - Sunnah.com API (FREE at https://sunnah.api-docs.io/)
- 🔑 **Web search & fact-checking** - Brave Search API (FREE 2000/month at https://brave.com/search/api/)

### 💰 **Optional Paid Services**

- 💰 **Perplexity AI** - Advanced fact-checking ($5 credit at https://www.perplexity.ai/settings/api)

---

## 🚀 **QUICK START**

### **Step 1: Install Dependencies**

```bash
# Install required packages
pip install requests beautifulsoup4

# Or reinstall project with new dependencies
pip install -e .
```

### **Step 2: Test Tools Immediately**

Run the built-in test scripts:

```bash
# Test citation verification (works immediately)
python src/academic_debate_council/tools/citation_verifier.py

# Test Islamic text tools (Quran works immediately)
python src/academic_debate_council/tools/islamic_texts.py

# Test fact-checking tools (requires API keys)
python src/academic_debate_council/tools/fact_checker.py
```

### **Step 3: Get API Keys (5 minutes)**

1. **Sunnah.com API** (FREE - for hadith):
   - Visit: https://sunnah.api-docs.io/
   - Sign up for free
   - Copy your API key
   - Add to `.env`: `SUNNAH_API_KEY=your_key_here`

2. **Brave Search API** (FREE - for fact-checking):
   - Visit: https://brave.com/search/api/
   - Sign up (2000 free searches/month)
   - Copy your API key
   - Add to `.env`: `BRAVE_API_KEY=your_key_here`

---

## 📚 **TOOL REFERENCE**

### **1. Citation Verifier (`citation_verifier.py`)**

#### **Tools Available:**

##### `verify_citation` - Verify Academic Citations
```python
from academic_debate_council.tools.citation_verifier import CitationVerifierTool

tool = CitationVerifierTool()
result = tool._run(
    author="Cipriani",
    year="2018",
    title_keywords="antidepressant efficacy comparative"
)
print(result)
```

**Returns:**
- ✅ Full paper details if found (title, authors, venue, citation count, DOI)
- ❌ Clear message if not found with recommendation to reframe claim

##### `verify_medical_claim` - Search PubMed for Medical Research
```python
from academic_debate_council.tools.citation_verifier import MedicalClaimVerifierTool

tool = MedicalClaimVerifierTool()
result = tool._run(
    keywords="depression treatment efficacy meta-analysis",
    max_results=5
)
print(result)
```

**Returns:**
- ✅ List of PubMed studies with PMIDs and links
- ❌ Message if no studies found with recommendation to reframe

---

### **2. Islamic Texts (`islamic_texts.py`)**

#### **Tools Available:**

##### `search_hadith` - Search Authenticated Hadith
```python
from academic_debate_council.tools.islamic_texts import HadithSearchTool

tool = HadithSearchTool()
result = tool._run(
    query="justice employment",
    collections=['bukhari', 'muslim'],
    max_results=3
)
print(result)
```

**Returns:**
- ✅ Authenticated hadith with collection, book, and number
- ⚠️ Setup message if API key not configured

##### `get_quran_verse` - Retrieve Quranic Verses
```python
from academic_debate_council.tools.islamic_texts import QuranVerseTool

tool = QuranVerseTool()
result = tool._run(
    surah=2,
    ayah=177,
    translation='en.sahih'
)
print(result)
```

**Returns:**
- ✅ Arabic text (Uthmani script) with English translation
- ❌ Error message if verse reference is invalid

##### `search_shamela_texts` - Search Classical Islamic Texts
```python
from academic_debate_council.tools.islamic_texts import ShamelaSearchTool

tool = ShamelaSearchTool()
result = tool._run(
    query="maqasid shariah",
    max_results=5
)
print(result)
```

**Returns:**
- 📚 Guide to manually search Al-Maktaba Al-Shamela
- 🔗 Links to alternative madhab-specific sources

---

### **3. Fact Checker (`fact_checker.py`)**

#### **Tools Available:**

##### `brave_search` - Web Search with Academic Filtering
```python
from academic_debate_council.tools.fact_checker import BraveSearchTool

tool = BraveSearchTool()
result = tool._run(
    query="labor market Qatar kafala system",
    academic_only=True,  # Restrict to academic sources
    max_results=10
)
print(result)
```

**Returns:**
- 🔍 List of web results with titles, URLs, and descriptions
- 📚 Can filter to academic sources only (scholar.google.com, pubmed.gov, etc.)

##### `perplexity_fact_check` - AI-Powered Fact-Checking
```python
from academic_debate_council.tools.fact_checker import PerplexityFactCheckTool

tool = PerplexityFactCheckTool()
result = tool._run(
    claim="Qatar has the highest GDP per capita in the world",
    context="Discussing economic development in Gulf states"
)
print(result)
```

**Returns:**
- 🤖 AI-generated fact-check with cited sources
- 📊 Nuanced analysis of claim accuracy

##### `get_qatar_statistics` - Qatar-Specific Data
```python
from academic_debate_council.tools.fact_checker import QatarStatsTool

tool = QatarStatsTool()
result = tool._run(
    topic="population demographics expatriates"
)
print(result)
```

**Returns:**
- 📊 Links to official Qatar government data sources
- 🔗 Specific URLs for Qatar Statistics Authority, QNV 2030, etc.

---

## 🤖 **INTEGRATING WITH CREWAI AGENTS**

### **Method 1: Add Tools to Agent Configuration**

Update your agent YAML files to include verification tools:

```yaml
# Example: spiritual_agent.yaml
spiritual_agent:
  role: >
    Islamic Spiritual Advisor
  goal: >
    Analyze the topic through the lens of Islamic values
  backstory: >
    You are a knowledgeable Islamic scholar...
  tools:
    - search_hadith
    - get_quran_verse
    - search_shamela_texts
```

### **Method 2: Import Tools in Agent Code**

```python
from crewai import Agent
from academic_debate_council.tools.citation_verifier import (
    CitationVerifierTool, 
    MedicalClaimVerifierTool
)
from academic_debate_council.tools.islamic_texts import (
    HadithSearchTool,
    QuranVerseTool
)
from academic_debate_council.tools.fact_checker import (
    BraveSearchTool,
    QatarStatsTool
)

# Create agent with verification tools
physical_agent = Agent(
    role="Physical & Health Analyst",
    goal="Analyze health and physical wellbeing aspects",
    backstory="You are a health researcher...",
    tools=[
        CitationVerifierTool(),
        MedicalClaimVerifierTool(),
        BraveSearchTool()
    ]
)

spiritual_agent = Agent(
    role="Islamic Spiritual Advisor",
    goal="Provide Islamic perspective",
    backstory="You are an Islamic scholar...",
    tools=[
        HadithSearchTool(),
        QuranVerseTool()
    ]
)
```

### **Method 3: Update Agent Prompts**

Add verification protocols to agent system prompts:

```python
spiritual_agent_prompt = """
You are an Islamic spiritual advisor analyzing topics through Islamic values.

**CITATION PROTOCOL:**
Before citing any hadith:
1. Use search_hadith tool to verify collection and number
2. Only cite if verified with specific reference (e.g., "Bukhari 1:2")
3. If not verified, use general language: "Islamic teachings emphasize..."

Before citing Quran:
1. Use get_quran_verse tool to verify surah and ayah
2. Include Arabic text if available
3. Always cite as: "Quran X:Y"

**IMPORTANT:** 
- Mark verified citations with [VERIFIED]
- Never cite specific sources you cannot verify
- Prefer general references over fabricated citations
"""
```

---

## 🎯 **RECOMMENDED WORKFLOW**

### **Pre-Query Research Phase** (Recommended)

Before agents analyze a topic, gather verified sources:

```python
def research_phase(topic: str):
    """
    Gather verified sources before agent analysis.
    """
    from academic_debate_council.tools.citation_verifier import verify_citation_standalone
    from academic_debate_council.tools.islamic_texts import search_hadith_standalone
    from academic_debate_council.tools.fact_checker import brave_search_standalone
    
    research = {
        'academic_papers': brave_search_standalone(
            query=f"{topic} academic research",
            academic_only=True
        ),
        'medical_studies': verify_medical_claim_standalone(
            keywords=topic
        ),
        'islamic_sources': search_hadith_standalone(
            query=topic,
            collections=['bukhari', 'muslim']
        ),
        'qatar_data': get_qatar_stats_standalone(
            topic=topic
        )
    }
    
    return research

# Use in your main flow
def analyze_topic(topic: str):
    # Step 1: Research
    print("🔍 Gathering verified sources...")
    research = research_phase(topic)
    
    # Step 2: Pass to agents
    print("🤖 Agents analyzing with verified sources...")
    run_agents_with_research(topic, research)
```

---

## 📊 **TESTING & VALIDATION**

### **Run Comprehensive Tests**

Test all tools to ensure they work:

```bash
# Test citation verification
python -c "from academic_debate_council.tools.citation_verifier import *; \
print(verify_citation_standalone('Cipriani', '2018', 'antidepressant'))"

# Test Quran retrieval
python -c "from academic_debate_council.tools.islamic_texts import *; \
print(get_quran_verse_standalone(2, 177))"

# Test fact-checking (requires API keys)
python -c "from academic_debate_council.tools.fact_checker import *; \
print(brave_search_standalone('Qatar labor statistics'))"
```

### **Verify Tool Registration**

Check that CrewAI recognizes your tools:

```python
from crewai import Agent
from academic_debate_council.tools.citation_verifier import CitationVerifierTool

agent = Agent(
    role="Test Agent",
    goal="Test tools",
    backstory="Testing",
    tools=[CitationVerifierTool()]
)

print(f"Agent has {len(agent.tools)} tools")
print(f"Tool names: {[tool.name for tool in agent.tools]}")
```

---

## ⚠️ **COMMON ISSUES & SOLUTIONS**

### **Issue 1: "API Key Not Configured"**

**Solution:** Check your `.env` file has the correct key:
```bash
# Check if .env exists
cat .env | grep SUNNAH_API_KEY

# If not, copy from example
cp .env.example .env
# Then edit .env and add your keys
```

### **Issue 2: "Module Not Found"**

**Solution:** Reinstall the project:
```bash
pip install -e .
```

### **Issue 3: "No Results Found"**

**Solution:** Tools are working correctly - there may genuinely be no results:
- Try different keywords
- Check spelling
- Use more general terms

### **Issue 4: Rate Limit Exceeded**

**Solution:** 
- Brave Search: Wait until next month or upgrade
- PubMed/Semantic Scholar: Tools include delays to respect limits
- Perplexity AI: Top up your account balance

---

## 🎓 **BEST PRACTICES**

### **1. Verify Before Citing**
Always use verification tools BEFORE making specific claims:
```python
# ❌ BAD: Cite without verification
"According to Smith et al. (2020), depression rates increased..."

# ✅ GOOD: Verify first
result = verify_citation("Smith", "2020", "depression rates")
if "VERIFIED" in result:
    "According to Smith et al. (2020), depression rates increased..."
else:
    "Research suggests depression rates have increased..."
```

### **2. Handle Verification Failures Gracefully**
```python
# ✅ GOOD: Reframe when verification fails
hadith = search_hadith("justice employment")
if "NOT FOUND" in hadith:
    # Use general language instead
    "Islamic teachings emphasize justice in employment..."
else:
    # Use specific citation
    "As stated in Bukhari 1:2..."
```

### **3. Cache Results to Avoid Redundant API Calls**
```python
# Store verified citations to avoid re-checking
verified_citations = {}

def get_or_verify(author, year, keywords):
    key = f"{author}_{year}"
    if key not in verified_citations:
        verified_citations[key] = verify_citation(author, year, keywords)
    return verified_citations[key]
```

### **4. Use Academic-Only Search for Research Claims**
```python
# For academic claims, restrict to scholarly sources
result = brave_search(
    query="climate change effects",
    academic_only=True  # ← This filters to .edu, .gov, scholar.google.com
)
```

---

## 📈 **MEASURING IMPROVEMENT**

Track these metrics to measure the impact:

1. **Citation Accuracy Rate**
   - Before: ~0% (hallucinated citations)
   - After: Measure % of verified vs unverified citations

2. **Agent Response Quality**
   - Use Claude to rate responses on factual accuracy
   - Compare before/after implementing tools

3. **User Trust**
   - Track how often users question citations
   - Measure confidence in recommendations

4. **API Usage**
   - Monitor API call counts
   - Optimize to stay within free tiers

---

## 🔄 **NEXT STEPS**

### **Phase 1: Immediate (Day 1)**
- ✅ Test citation_verifier.py (works now)
- ✅ Test Quran verse retrieval (works now)
- 🔑 Get Sunnah.com API key
- 🔑 Get Brave Search API key

### **Phase 2: Integration (Days 2-3)**
- 📝 Update agent configurations to use tools
- 🧪 Test agents with new tools
- 📊 Measure citation accuracy improvement

### **Phase 3: Optimization (Days 4-5)**
- 💾 Implement prompt caching for reference materials
- 🔄 Add research phase before agent execution
- 🎯 Fine-tune agent prompts for tool usage

### **Phase 4: Advanced (Week 2)**
- 🤖 Add Perplexity AI for complex fact-checking
- 🌐 Build custom MCP server for Islamic texts
- 📚 Create reference text libraries for agents

---

## 📞 **SUPPORT & RESOURCES**

### **API Documentation**
- Semantic Scholar: https://api.semanticscholar.org/
- PubMed: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- Sunnah.com: https://sunnah.api-docs.io/
- Quran.com: https://quran.api-docs.io/
- Brave Search: https://brave.com/search/api/
- Perplexity AI: https://docs.perplexity.ai/

### **Troubleshooting**
- Check `.env` file has correct API keys
- Verify internet connection for API calls
- Check API status pages if tools fail
- Review tool output for specific error messages

---

## ✅ **SUCCESS CHECKLIST**

- [ ] Dependencies installed (`requests`, `beautifulsoup4`)
- [ ] Test scripts run successfully
- [ ] `.env` file configured with API keys
- [ ] Sunnah.com API key obtained (free)
- [ ] Brave Search API key obtained (free)
- [ ] Tools integrated into at least one agent
- [ ] Tested end-to-end agent workflow
- [ ] Citation accuracy improved (measure before/after)
- [ ] Documentation reviewed by team

---

**🎉 Congratulations!** You now have a robust verification system that eliminates hallucinated citations and grounds your agents in real, verifiable sources.
