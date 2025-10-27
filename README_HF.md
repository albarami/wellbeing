---
title: Academic Debate Council
emoji: ⚖️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# ⚖️ Academic Debate Council

A sophisticated multi-agent AI system that conducts scholarly debates from Islamic, intellectual, psychological, physiological, and social perspectives.

## 🎯 Features

- **7 Expert Agents** debate from different academic perspectives
- **Citation Verification** using Semantic Scholar & PubMed APIs
- **Islamic Text Verification** with Quran and Hadith databases
- **Fact Checking** with multiple verification tools
- **Real-time Streaming** responses with tool execution visibility

## 🚀 How to Use

1. Enter your question in the chat
2. The system will automatically:
   - Deploy 7 expert agents
   - Conduct 2 rounds of debate
   - Verify all citations and claims
   - Synthesize a comprehensive answer

## 🔑 API Keys Required

This Space requires the following API keys (set in Settings → Repository Secrets):

- `ANTHROPIC_API_KEY` (Required) - Get from https://console.anthropic.com/
- `HADITH_API_KEY` (Optional) - Get from https://hadithapi.com/
- `BRAVE_API_KEY` (Optional) - Get from https://brave.com/search/api/
- `PERPLEXITY_API_KEY` (Optional) - Get from https://www.perplexity.ai/settings/api

## 📚 Example Questions

- Should prayer breaks be enforced in workplaces?
- What does research say about meditation and stress?
- How does Islamic scholarship view modern technology?

## 🛠️ Technology Stack

- **Chainlit** - Interactive UI
- **Anthropic Claude** - LLM for agent intelligence
- **CrewAI** - Multi-agent orchestration
- **Python 3.11** - Backend

## 📖 Documentation

For full documentation and setup instructions, visit the [GitHub repository](https://github.com/yourusername/academic-debate).

## ⚠️ Note

This is a research demonstration. Debates take 10-15 minutes to complete as agents verify sources and construct arguments.

## 📄 License

MIT License - See LICENSE file for details
