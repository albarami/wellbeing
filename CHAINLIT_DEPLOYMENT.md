# 🚀 Deploying Academic Debate Council to Chainlit Cloud

## Option A: Chainlit Cloud (Recommended)

### Prerequisites
- Chainlit Cloud account: https://cloud.chainlit.io
- GitHub account
- Anthropic API key

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
```bash
git init
git add .
git commit -m "Initial commit - Academic Debate Council"
```

2. **Push to GitHub**:
```bash
# Create a new repository on GitHub
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/academic-debate-council.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Chainlit Cloud

1. **Visit:** https://cloud.chainlit.io

2. **Sign Up/Login** with GitHub

3. **Create New App:**
   - Click "New App"
   - Name: `academic-debate-council`
   - Connect your GitHub repository
   - Select branch: `main`

4. **Configure Settings:**
   - **Entry Point:** `chainlit_app.py`
   - **Python Version:** 3.11
   
5. **Environment Variables:**
   - Add `ANTHROPIC_API_KEY` with your API key
   - Click "Add Variable"

6. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes for build

7. **Get Your URL:**
   - Your app will be at: `https://academic-debate.chainlit.io`
   - Or custom subdomain: `https://your-subdomain.chainlit.io`

### Step 3: Share the Link!

✅ **Share this URL with anyone:**
- `https://your-app.chainlit.io`
- No installation required
- Works on all devices
- Professional ChatGPT-like interface

---

## Option B: Hugging Face Spaces (FREE Forever)

### Step 1: Create Space

1. **Visit:** https://huggingface.co/spaces
2. **Click:** "Create new Space"
3. **Settings:**
   - Space name: `academic-debate-council`
   - License: Apache 2.0
   - SDK: Docker
   - Visibility: Public

### Step 2: Create Dockerfile

Create `Dockerfile` in your project:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 7860

# Set environment variable for Hugging Face
ENV CHAINLIT_HOST=0.0.0.0
ENV CHAINLIT_PORT=7860

# Run Chainlit
CMD ["chainlit", "run", "chainlit_app.py", "--host", "0.0.0.0", "--port", "7860"]
```

### Step 3: Create README.md

Create `README.md` for Hugging Face:

```markdown
---
title: Academic Debate Council
emoji: 🎓
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Academic Debate Council

Multi-agent AI system for comprehensive wellbeing analysis through expert debate.
```

### Step 4: Push to Hugging Face

```bash
# Add Hugging Face as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/academic-debate-council

# Push
git push hf main
```

### Step 5: Configure Secrets

1. Go to your Space settings
2. Add Secret: `ANTHROPIC_API_KEY`
3. Paste your API key

### Your URL:
✅ `https://huggingface.co/spaces/YOUR_USERNAME/academic-debate-council`

---

## Option C: Self-Host (Railway/Render)

### Railway Deployment

1. **Visit:** https://railway.app
2. **New Project** → "Deploy from GitHub repo"
3. **Select** your repository
4. **Add Variables:**
   - `ANTHROPIC_API_KEY`
   - `PORT=8000`
5. **Deploy**
6. **Get domain:** `your-app.railway.app`

### Cost: $5-10/month

---

## Pricing Comparison

| Platform | Free Tier | Paid | Custom Domain | Best For |
|----------|-----------|------|---------------|----------|
| **Chainlit Cloud** | 100 users/month | $50/month | Yes | Quick start |
| **Hugging Face** | Unlimited | Free | No | Free forever |
| **Railway** | $5 credit | ~$10/month | Yes | Full control |

---

## 🎯 Recommended: Start with Chainlit Cloud

**Why?**
- ✅ Fastest deployment (5 minutes)
- ✅ Professional subdomain
- ✅ Easy to manage
- ✅ Built for Chainlit apps
- ✅ Free tier to test

**Later migrate to:**
- Hugging Face (if you want free forever)
- Self-host (if you need custom domain)

---

## 📱 Testing Your Deployment

Once deployed, test with:

1. **Visit your URL**
2. **Wait for welcome message**
3. **Ask a question:** "Prayer breaks in workplace"
4. **Watch agents appear** one by one!

---

## 🔧 Troubleshooting

### API Key Issues
- Make sure `ANTHROPIC_API_KEY` is set in environment variables
- Check the secret is spelled correctly (case-sensitive)

### Build Failures
- Check `requirements.txt` has all dependencies
- Ensure Python version is 3.11
- Check logs in deployment dashboard

### App Not Loading
- Wait 2-3 minutes after deployment
- Check if environment variables are set
- Look at deployment logs

---

## 📊 After Deployment

**Share your link:**
- ✅ Send to colleagues: `https://your-app.chainlit.io`
- ✅ Post on social media
- ✅ Embed in website (iframe support)
- ✅ QR code for mobile access

**Monitor usage:**
- Check Chainlit Cloud dashboard
- View conversation logs
- Track API usage

---

## 🎉 You're Done!

Your Academic Debate Council is now **live and shareable**!

Anyone can:
- Visit the link
- Ask questions
- Get AI expert debate analysis
- No installation needed
- Works on all devices

**Professional, shareable, and looks like ChatGPT!** 🚀
