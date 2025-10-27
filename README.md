# 🎓 Academic Debate Council

**Multi-Agent AI System for Comprehensive Multi-Perspective Analysis**

A sophisticated ChatGPT-like interface where **7 AI expert agents** analyze ANY topic through comprehensive debate, providing spiritual, emotional, intellectual, physical, and social perspectives.

## 👨‍💻 Developer

**Salim AL-Barami**

## 🎯 Features

### Core Capabilities
- **7 Expert AI Agents** - Each with specialized knowledge and perspective
- **12 Sequential Tasks** - Structured debate across two rounds plus synthesis
- **Real-Time Streaming** - Watch each agent's analysis appear as they complete
- **ChatGPT-like Interface** - Professional, modern chat UI powered by Chainlit
- **Any Topic** - Analyze wellbeing, policy, lifestyle, or social issues

### 🔍 Research Integrity (NEW - Oct 2025)
- **Citation Verification** - Semantic Scholar API with bulk search & precise matching
- **Medical Verification** - PubMed database for health claims
- **Islamic Text Verification** - Authenticated Quranic verses and hadith
- **Fact Checking** - Multi-source verification with Brave Search & Perplexity AI
- **Honest Limitations** - System admits when sources cannot be verified

### 🚀 Deployment (NEW)
- **Multiple Options** - Hugging Face, Railway, Render, ngrok
- **Password Protection** - Private link-only access
- **One-Click Deploy** - Automated deployment scripts
- **Production Ready** - WebSocket stability, error handling, timeout protection

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `ANTHROPIC_API_KEY` into the `.env` file**

```bash
# .env file
ANTHROPIC_API_KEY=your_api_key_here
```

Install dependencies:

```bash
pip install -e .
```

### 🔍 Verification Tools Setup (NEW)

The system now includes API-based verification tools to eliminate hallucinated citations:

**Works Immediately (No API Keys):**
- ✅ Academic citation verification (Semantic Scholar)
- ✅ Medical research verification (PubMed)
- ✅ Quran verse verification (Quran.com)

**Get FREE API Keys for Full Features:**
```bash
# 1. Sunnah.com (for hadith verification)
#    Sign up: https://sunnah.api-docs.io/
SUNNAH_API_KEY=your_key

# 2. Brave Search (for fact-checking & Qatar stats)
#    Sign up: https://brave.com/search/api/
BRAVE_API_KEY=your_key
```

See **[QUICK_START_VERIFICATION.md](QUICK_START_VERIFICATION.md)** for 3-minute setup!

## 🚀 Running the Project

### **Option 1: Chainlit Interface (Recommended)**

Run the ChatGPT-like interface:

```bash
chainlit run chainlit_app.py
```

Then open: http://localhost:8000

### **Option 2: Streamlit Interface (Alternative)**

Run the data-focused interface:

```bash
streamlit run src/academic_debate_council/streamlit_app.py
```

Then open: http://localhost:8501

## 📱 Example Usage

1. Open the Chainlit interface
2. Type any question, for example:
   - "Should prayer breaks be enforced in workplaces?"
   - "Impact of social media on youth"
   - "Remote work policies in Gulf corporations"
3. Watch 7 AI experts debate through 12 sequential tasks
4. Get a comprehensive multi-perspective analysis

### 🧪 Test Verification Tools

```bash
# Run comprehensive test suite
python test_verification_tools.py

# Test individual tools
python src/academic_debate_council/tools/citation_verifier.py
python src/academic_debate_council/tools/islamic_texts.py
python src/academic_debate_council/tools/fact_checker.py
```

## 🤖 The Expert Agents

### **Round 1: Initial Analyses**

1. **🕌 Sheikh Dr. Ibrahim al-Tazkiyah** - Spiritual Pillar Expert
   - Provides Islamic foundation with Quranic verses and hadith
   - Analyzes through lens of Maqasid al-Shariah

2. **❤️ Dr. Layla al-Qalb** - Emotional Pillar Expert
   - Analyzes emotional landscape and wellbeing impact
   - Cites psychological research and Islamic emotional frameworks

3. **🧠 Dr. Hassan al-Hikmah** - Intellectual Pillar Expert
   - Provides philosophical and epistemological analysis
   - Challenges assumptions with critical questions

4. **💪 Dr. Fatima al-Jism** - Physical Pillar Expert
   - Evidence-based health impact analysis
   - Cites quantitative studies and Gulf epidemiology

5. **🤝 Dr. Aisha al-Mujtama'** - Social Pillar Expert
   - Analyzes social structure and power dynamics
   - Gulf context (expat-national, kafala, gender dynamics)

### **Moderation**

6. **⚖️ Dr. Yusuf al-Mudeer** - Debate Orchestrator
   - Identifies tensions between expert perspectives
   - Poses challenging questions to agents

### **Round 2: Expert Responses**

Agents 1-5 respond to orchestrator's challenges

### **Final Synthesis**

7. **📊 Dr. Amira al-Tawhid** - Synthesizer
   - Comprehensive integration of all perspectives
   - Balanced synthesis with actionable recommendations

## 🌐 Deployment

### Quick Start
```powershell
# Password-protected (private access)
START_PRIVATE.bat

# Deploy to cloud (one-click)
DEPLOY_NOW.bat
```

### Deployment Options

| Option | Cost | Setup Time | Best For |
|--------|------|------------|----------|
| **Hugging Face Spaces** | Free | 10 min | Public projects |
| **Railway.app** | $5/mo | 5 min | Simple paid hosting |
| **Render.com** | Free tier | 15 min | Professional |
| **ngrok** | Free | 2 min | Quick demos |

**See detailed guides:**
- 📘 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - All deployment options
- 🔐 [PRIVATE_DEPLOYMENT_GUIDE.md](PRIVATE_DEPLOYMENT_GUIDE.md) - Private access setup
- 🚀 [PERMANENT_DEPLOYMENT_STEPS.md](PERMANENT_DEPLOYMENT_STEPS.md) - Step-by-step guide

### What's New (October 2025)

✅ **WebSocket Stability** - No more "Could not reach the server" errors  
✅ **Citation Verifier Upgrade** - Bulk search, better queries, pagination  
✅ **Password Protection** - Private link-only access  
✅ **Comprehensive Docs** - Complete deployment and troubleshooting guides  

See [CHANGELOG.md](CHANGELOG.md) for full details.

## 📝 License

MIT License

## 👨‍💻 About the Developer

**Salim AL-Barami**

---

*Built with Anthropic Claude API, Chainlit, and Streamlit*
