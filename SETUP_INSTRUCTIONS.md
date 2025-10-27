# 🚀 Setup Instructions - Verification Tools

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Project Dependencies

The verification tools require the main project dependencies including CrewAI:

```bash
# Install the project in development mode
pip install -e .
```

This will install:
- `crewai[tools]` - Core framework
- `requests` - For API calls
- `beautifulsoup4` - For web scraping
- And all other project dependencies

### Step 2: Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key (required):
```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Step 3: Test Tools That Work Immediately

These tools work WITHOUT any additional API keys:

```bash
# Test citation verification
python src/academic_debate_council/tools/citation_verifier.py

# Test Quran retrieval
python src/academic_debate_council/tools/islamic_texts.py

# Run full test suite
python test_verification_tools.py
```

**Expected output**: Tools will verify citations and retrieve Quran verses successfully.

---

## 🔑 Get FREE API Keys (Optional, 5 Minutes)

### Sunnah.com API (for Hadith Verification)

**FREE - Highly Recommended**

1. Visit: https://sunnah.api-docs.io/
2. Click "Get API Key"  
3. Sign up with email
4. Copy your API key
5. Add to `.env`:
   ```bash
   SUNNAH_API_KEY=your_sunnah_key_here
   ```

### Brave Search API (for Fact-Checking)

**FREE - 2000 searches/month**

1. Visit: https://brave.com/search/api/
2. Sign up for free account
3. Navigate to API section
4. Copy your API key
5. Add to `.env`:
   ```bash
   BRAVE_API_KEY=your_brave_key_here
   ```

### Perplexity AI (Optional - Advanced Fact-Checking)

**PAID - $5 credit = ~1000 searches**

1. Visit: https://www.perplexity.ai/settings/api
2. Add payment method
3. Generate API key
4. Add to `.env`:
   ```bash
   PERPLEXITY_API_KEY=your_perplexity_key_here
   ```

---

## ✅ Verification Checklist

Run through this checklist to ensure everything is set up:

### Basic Setup
- [ ] Project installed: `pip install -e .` completed successfully
- [ ] `.env` file created with `ANTHROPIC_API_KEY`
- [ ] Can import tools: `python -c "from academic_debate_council.tools import CitationVerifierTool"`
- [ ] Citation test passes: `python src/academic_debate_council/tools/citation_verifier.py`
- [ ] Quran test passes: `python src/academic_debate_council/tools/islamic_texts.py`

### API Keys (Optional)
- [ ] Sunnah.com API key obtained and added to `.env`
- [ ] Brave Search API key obtained and added to `.env`
- [ ] Perplexity API key obtained (if desired) and added to `.env`
- [ ] All tests pass: `python test_verification_tools.py`

### Integration Ready
- [ ] Read `VERIFICATION_TOOLS_GUIDE.md`
- [ ] Reviewed `examples/agent_integration_example.py`
- [ ] Ready to integrate tools with agents

---

## 🧪 Testing

### Test Individual Tools

```bash
# Citation verification (works without API keys)
python src/academic_debate_council/tools/citation_verifier.py

# Islamic texts (Quran works without API key, Hadith needs key)
python src/academic_debate_council/tools/islamic_texts.py

# Fact-checking (requires Brave/Perplexity API keys)
python src/academic_debate_council/tools/fact_checker.py
```

### Test Full Suite

```bash
python test_verification_tools.py
```

This will:
- ✅ Test tools that work without API keys
- ⏭️  Skip tools that need API keys (with instructions)
- 📊 Show summary of what's working

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'crewai'"

**Problem**: Project dependencies not installed.

**Solution**:
```bash
pip install -e .
```

### "ModuleNotFoundError: No module named 'requests'"

**Problem**: Missing API dependencies.

**Solution**:
```bash
pip install requests beautifulsoup4
```

### "API key not configured"

**Problem**: Tool needs an API key that's not in `.env`.

**Solution**:
1. Check `.env` file exists in project root
2. Verify key is on correct line: `SUNNAH_API_KEY=actual_key_value`
3. No quotes around the value
4. Restart Python/terminal after adding keys

### Tools import error

**Problem**: Tools can't be imported.

**Solution**:
```bash
# Reinstall project
pip install -e .

# Verify tools directory is found
python -c "import sys; print(sys.path)"
```

### "Semantic Scholar API" or "PubMed" not working

**Problem**: Network/API issue.

**Solution**:
- Check internet connection
- These APIs don't require keys, so errors are temporary
- Try again in a few minutes
- Check API status pages

---

## 📖 Next Steps

### 1. Read Documentation
- [ ] `QUICK_START_VERIFICATION.md` - 3-minute overview
- [ ] `VERIFICATION_TOOLS_GUIDE.md` - Comprehensive guide
- [ ] `IMPLEMENTATION_COMPLETE.md` - What was built

### 2. Try Examples
- [ ] Run example integration: `python examples/agent_integration_example.py`
- [ ] Review agent integration patterns
- [ ] Understand verification protocols

### 3. Integrate with Your Agents
- [ ] Choose which agents need which tools
- [ ] Add tools to agent configurations
- [ ] Update agent prompts with verification protocols
- [ ] Test with sample topics

### 4. Measure Impact
- [ ] Run analysis before and after
- [ ] Count hallucinated vs verified citations
- [ ] Track user trust feedback
- [ ] Monitor API usage costs

---

## 📊 What Each Tool Does

### Citation Verifier
- **verify_citation**: Check if academic paper exists
- **verify_medical_claim**: Search PubMed for medical research
- **Use for**: Physical, Emotional, Intellectual agents

### Islamic Texts
- **search_hadith**: Find authenticated hadith
- **get_quran_verse**: Retrieve Quranic verses
- **Use for**: Spiritual agent

### Fact Checker
- **brave_search**: Web search with academic filtering
- **perplexity_fact_check**: AI-powered fact-checking
- **get_qatar_statistics**: Qatar-specific data
- **Use for**: Social agent, fact-checking any claims

---

## 💡 Pro Tips

1. **Start simple**: Use citation & Quran tools first (no API keys needed)
2. **Get Sunnah key**: Takes 2 minutes, huge impact for spiritual agent
3. **Get Brave key**: Free tier is generous, enables fact-checking
4. **Skip Perplexity**: Start without it, add later if needed
5. **Test standalone first**: Run each tool's test script individually
6. **Integrate gradually**: One agent at a time
7. **Monitor usage**: Stay within free tiers

---

## 🎯 Success Criteria

You'll know setup is successful when:

✅ `pip install -e .` completes without errors  
✅ Can import tools: `from academic_debate_council.tools import CitationVerifierTool`  
✅ Citation verification works (test with real paper)  
✅ Quran retrieval works (test with Surah 2, Ayah 177)  
✅ At least 2 FREE API keys obtained and configured  
✅ Full test suite runs with some tests passing  
✅ Ready to integrate with agents  

---

## 📞 Need Help?

### Documentation Files
- **This file**: Setup instructions
- **QUICK_START_VERIFICATION.md**: Quick reference
- **VERIFICATION_TOOLS_GUIDE.md**: Comprehensive guide
- **IMPLEMENTATION_COMPLETE.md**: What was implemented
- **.env.example**: API key configuration template

### Test Scripts
- **test_verification_tools.py**: Full test suite
- **examples/agent_integration_example.py**: Integration examples
- Individual tool files have `if __name__ == "__main__"` test sections

### Common Questions

**Q: Do I need ALL the API keys?**  
A: No! Citation and Quran tools work WITHOUT any API keys. Get Sunnah + Brave keys for full features.

**Q: Are these APIs free?**  
A: Yes! Semantic Scholar, PubMed, Quran.com, Sunnah.com, and Brave Search (2000/month) are all free.

**Q: How do I know if it's working?**  
A: Run `python test_verification_tools.py`. You should see at least 3 tests pass immediately.

**Q: Can I use this in production?**  
A: Yes! All tools have error handling, rate limiting, and graceful degradation.

**Q: What if verification fails?**  
A: Tools tell agents to reframe claims without specific citations. No hallucinations!

---

**Ready to eliminate hallucinated citations? Start with Step 1 above! 🚀**
