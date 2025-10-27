# 🎓 Academic Debate Council - Usage Guide

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Features Overview](#features-overview)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install uv
uv pip install -e .
```

### 2. Set Up API Key
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 3. Run the Streamlit App
```bash
streamlit run src/academic_debate_council/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📦 Installation

### Prerequisites
- Python 3.10 - 3.13
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Step-by-Step Installation

1. **Install UV (recommended package manager)**
   ```bash
   pip install uv
   ```

2. **Install project dependencies**
   ```bash
   # Option 1: Using UV (recommended)
   uv pip install -e .
   
   # Option 2: Using pip
   pip install -e .
   ```

3. **Create environment file**
   ```bash
   copy .env.example .env
   ```

4. **Add your API key to `.env`**
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx
   ```

---

## 🎯 Running the Application

### Option 1: Streamlit Web Interface (Recommended)

**Best for:** Interactive analysis with real-time updates and beautiful UI

```bash
streamlit run src/academic_debate_council/streamlit_app.py
```

**Features:**
- ✅ Real-time streaming output
- ✅ Progress tracking across 12 tasks
- ✅ Organized display by debate rounds
- ✅ Download final report as markdown
- ✅ Language selection (English/Arabic)
- ✅ Beautiful, responsive UI

**How to use:**
1. Enter your wellbeing topic (e.g., "Social media usage among teenagers")
2. Select language (English or Arabic)
3. Click "Start Analysis"
4. Watch the 7 AI agents debate in real-time
5. Download the final comprehensive report

---

### Option 2: Command Line - Interactive Mode

**Best for:** Terminal users who want topic input

```bash
python src/academic_debate_council/main.py interactive
```

**What happens:**
1. Prompts you for a wellbeing topic
2. Runs the full 12-task debate process
3. Displays verbose console output
4. Shows final synthesis

---

### Option 3: Command Line - Pre-configured Topic

**Best for:** Testing or automation

```bash
python src/academic_debate_council/main.py run
```

This runs with the default sample topic defined in `main.py`.

---

### Option 4: Using CrewAI CLI

**Best for:** CrewAI users familiar with the framework

```bash
crewai run
```

---

## ⚙️ Configuration

### API Keys

Edit `.env`:
```env
# Required
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Optional (if using OpenAI models)
OPENAI_API_KEY=sk-your-openai-key-here
```

### Agent Configuration

All agents are configured in:
- **Agents:** `src/academic_debate_council/config/agents.yaml`
- **Tasks:** `src/academic_debate_council/config/tasks.yaml`

#### Current Agent Setup:
| Agent | Model | Temperature | Role |
|-------|-------|-------------|------|
| Sheikh al-Tazkiyah | Claude Opus 4 | 0.3 | Spiritual Expert |
| Dr. al-Qalb | Claude Sonnet 4.5 | 0.4 | Emotional Expert |
| Dr. al-Hikmah | Claude Sonnet 4.5 | 0.3 | Intellectual Expert |
| Dr. al-Jism | Claude Sonnet 4.5 | 0.3 | Physical Expert |
| Dr. al-Mujtama' | Claude Sonnet 4.5 | 0.4 | Social Expert |
| Dr. al-Mudeer | Claude Sonnet 4.5 | 0.4 | Debate Orchestrator |
| Dr. al-Tawhid | Claude Opus 4 | 0.2 | Synthesizer |

**To modify agents:**
- Edit `agents.yaml` to change roles, goals, backstories, or LLM settings
- No code changes needed - configuration is hot-reloadable

---

## 🎨 Features Overview

### Multi-Round Debate System

#### **Round 1: Initial Analyses** (5 tasks)
1. 🕌 Spiritual Analysis - Islamic framework and maqasid al-shariah
2. ❤️ Emotional Analysis - Psychology and emotion regulation
3. 🧠 Intellectual Analysis - Learning sciences and epistemology
4. 💪 Physical Analysis - Public health and bioethics
5. 🤝 Social Analysis - Sociology and power dynamics

#### **Debate Moderation** (1 task)
6. ⚖️ Orchestrator identifies 2-3 key tensions between experts

#### **Round 2: Expert Responses** (5 tasks)
7-11. Each expert defends their position with evidence

#### **Final Synthesis** (1 task)
12. 📊 Comprehensive 2000+ word integrated assessment

### Streamlit Interface Features

- **Progress Tracking:** Real-time progress bar (1/12, 2/12, etc.)
- **Categorized Output:** Organized by Round 1, Moderation, Round 2, Synthesis
- **Expandable Sections:** Click to expand/collapse each expert's analysis
- **Status Indicators:** Visual indicators (✅ ✓, 🔄, ❌)
- **Download Report:** Export final synthesis as markdown
- **Execution Time:** Track how long the full analysis takes
- **API Validation:** Checks for missing API keys before running

### Language Support

Both **English** and **Arabic** are fully supported:
- Experts respond in the language you select
- All 7 agents are multilingual
- Citations and references adapt to language

---

## 🔍 Example Topics

Try analyzing these wellbeing topics:

### General Wellbeing
- "Daily prayer practice in modern life"
- "Work-life balance for working parents"
- "Mindfulness meditation practices"

### Technology & Society
- "Social media usage among teenagers"
- "Remote work and mental health"
- "Screen time limits for children"

### Health & Lifestyle
- "Intermittent fasting from multiple perspectives"
- "Regular exercise routines for busy professionals"
- "Sleep hygiene and quality"

### Education
- "Homework policies in primary education"
- "Bilingual education benefits and challenges"
- "Exam stress management for students"

### Family & Community
- "Elderly care in modern society"
- "Community volunteer programs"
- "Raising children in multicultural environments"

---

## 🐛 Troubleshooting

### Issue: "Missing API Key" Error

**Solution:**
1. Ensure `.env` file exists in project root
2. Open `.env` and verify `ANTHROPIC_API_KEY=sk-ant-...`
3. Restart the application

---

### Issue: "Module not found" Error

**Solution:**
```bash
# Reinstall dependencies
uv pip install -e .

# Or with pip
pip install -e .
```

---

### Issue: Streamlit won't start

**Solution:**
```bash
# Install Streamlit explicitly
pip install streamlit>=1.28.0

# Try running with full path
streamlit run "d:\Academic debate\src\academic_debate_council\streamlit_app.py"
```

---

### Issue: CrewAI version conflicts

**Solution:**
```bash
# Uninstall and reinstall CrewAI
pip uninstall crewai
pip install "crewai[tools]>=0.203.0,<1.0.0"
```

---

### Issue: Agent responses are too slow

**Explanation:** This is normal. The system runs 12 sequential tasks with 7 different AI agents. Each task can take 30-90 seconds. A full analysis typically takes **10-20 minutes**.

**Tips:**
- Use the Streamlit interface to watch progress in real-time
- The verbose output shows which agent is currently working
- Consider analyzing shorter topics for faster results

---

### Issue: Output is in the wrong language

**Solution:** Ensure you select the correct language in the Streamlit dropdown before clicking "Start Analysis". The agents match the user's input language.

---

## 📊 Understanding the Output

### Score System

Each expert provides 3 quantified scores ranging from **-3 to +3**:

- **+3:** Very beneficial
- **+2:** Moderately beneficial  
- **+1:** Slightly beneficial
- **0:** Neutral
- **-1:** Slightly harmful
- **-2:** Moderately harmful
- **-3:** Very harmful

### Pillar-Specific Scores

| Expert | Score 1 | Score 2 | Score 3 |
|--------|---------|---------|---------|
| Spiritual | Connection to Allah | Purposeful Living | Inner Purification |
| Emotional | Balance (Tawazun) | Resilience (Sabr) | Transformation |
| Intellectual | Truth-Seeking | Wisdom (Hikmah) | Contemplation |
| Physical | Health | Strength | Prevention |
| Social | Care/Empathy | Cooperation | Responsibility |

### Final Synthesis Structure

The synthesizer produces a comprehensive report including:

1. **Executive Summary** (250 words) - Bottom line for decision-makers
2. **Round 1 Summary** - Each pillar's core findings
3. **Key Tensions** - Main debates the orchestrator identified
4. **Resolution Status** - How Round 2 addressed tensions
5. **Cross-Pillar Synergies** - Where experts strongly agreed
6. **Integrated Assessment** - Net impact and confidence level
7. **Recommendations** - For individuals, organizations, policymakers
8. **Conclusion** - Integration of all perspectives

---

## 💡 Pro Tips

1. **Be Specific:** More specific topics yield better analysis
   - ❌ "Exercise"
   - ✅ "Morning exercise routines for office workers over 40"

2. **Use Context:** Add relevant context to your topic
   - ❌ "Fasting"
   - ✅ "Ramadan fasting practices for people with diabetes"

3. **Watch the Debate:** The Round 2 responses often contain the most nuanced insights

4. **Save Your Reports:** Download the markdown file for future reference

5. **Experiment with Languages:** Try the same topic in English and Arabic to see how cultural framing differs

---

## 🤝 Support

For issues or questions:
- Check the [CrewAI Documentation](https://docs.crewai.com)
- Review `README.md` for project overview
- Examine `agents.yaml` and `tasks.yaml` for configuration details

---

## 📝 License

See the main `README.md` for license information.

---

**Happy Analyzing! 🎓**
