# 🌐 Deployment Guide - Share Your Academic Debate System

## 🚀 Option 1: Chainlit Cloud (Recommended - Easiest)

**Pros:**
- ✅ Free tier available
- ✅ No server management
- ✅ Automatic HTTPS
- ✅ Built-in authentication
- ✅ Deploy in 5 minutes

**Steps:**

1. **Install Chainlit CLI (if not already installed)**
   ```powershell
   pip install chainlit --upgrade
   ```

2. **Login to Chainlit Cloud**
   ```powershell
   chainlit login
   ```
   - Opens browser for authentication
   - Create free account at https://cloud.chainlit.io/

3. **Deploy Your App**
   ```powershell
   cd "D:\Academic debate"
   chainlit deploy
   ```
   - Follow prompts to configure deployment
   - Choose a unique subdomain (e.g., `academic-debate-council`)
   - Your app will be at: `https://academic-debate-council.chainlit.app`

4. **Set Environment Variables**
   After deployment, add your API keys via Chainlit Cloud dashboard:
   - Go to https://cloud.chainlit.io/
   - Select your project
   - Add environment variables:
     - `ANTHROPIC_API_KEY`
     - `HADITH_API_KEY` (optional)
     - `BRAVE_API_KEY` (optional)
     - `PERPLEXITY_API_KEY` (optional)

**Result:** Your app is live at `https://your-app-name.chainlit.app` 🎉

---

## 🔗 Option 2: ngrok (Temporary Public URL)

**Pros:**
- ✅ Instant public URL
- ✅ No deployment needed
- ✅ Free tier (8 hours/session)
- ✅ Great for demos

**Cons:**
- ❌ URL changes on restart
- ❌ Not for 24/7 hosting
- ❌ Limited to 40 connections/minute (free tier)

**Steps:**

1. **Install ngrok**
   ```powershell
   # Download from: https://ngrok.com/download
   # Or use chocolatey:
   choco install ngrok
   ```

2. **Sign up for free account**
   - Go to https://ngrok.com/
   - Get your auth token

3. **Configure ngrok**
   ```powershell
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

4. **Start Your Chainlit App**
   ```powershell
   cd "D:\Academic debate"
   chainlit run chainlit_app.py
   ```

5. **In Another Terminal, Start ngrok**
   ```powershell
   ngrok http 8000
   ```

6. **Share the URL**
   - ngrok will display: `Forwarding: https://abc123.ngrok.io -> localhost:8000`
   - Share the `https://abc123.ngrok.io` URL
   - Anyone can access it while ngrok is running

**Result:** Temporary public URL for demos and testing 🌐

---

## ☁️ Option 3: Hugging Face Spaces (Free Public Hosting)

**Pros:**
- ✅ Completely free
- ✅ Permanent hosting
- ✅ No credit card needed
- ✅ Great community

**Cons:**
- ❌ Slower cold starts
- ❌ Limited resources (free tier)

**Steps:**

1. **Create Hugging Face Account**
   - Go to https://huggingface.co/join

2. **Create New Space**
   - Click "New Space"
   - Choose "Docker" SDK
   - Set visibility to "Public"

3. **Prepare Deployment Files**

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 7860

# Run chainlit
CMD ["chainlit", "run", "chainlit_app.py", "--host", "0.0.0.0", "--port", "7860"]
```

Create `.env.example` (users will need to add their own keys):
```bash
ANTHROPIC_API_KEY=your_key_here
```

4. **Push to Space**
   ```powershell
   cd "D:\Academic debate"
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/academic-debate
   git push origin main
   ```

5. **Configure Secrets**
   - In Hugging Face Space settings
   - Add "Secrets" for API keys
   - These won't be publicly visible

**Result:** Free permanent hosting at `https://huggingface.co/spaces/YOUR_USERNAME/academic-debate` 🤗

---

## 🖥️ Option 4: Cloud VPS (Most Control)

**Pros:**
- ✅ Full control
- ✅ 24/7 uptime
- ✅ Custom domain
- ✅ No vendor lock-in

**Cons:**
- ❌ Requires server management
- ❌ Costs $5-10/month
- ❌ More setup complexity

**Providers:**
- DigitalOcean (Droplet - $6/month)
- Linode (Nanode - $5/month)
- AWS Lightsail ($5/month)
- Azure VM (B1s - $4/month)

**Quick Setup Example (Ubuntu Server):**

```bash
# 1. SSH into your server
ssh root@your-server-ip

# 2. Install Python and dependencies
apt update
apt install python3 python3-pip git -y

# 3. Clone your repository
git clone https://github.com/yourusername/academic-debate.git
cd academic-debate

# 4. Install requirements
pip3 install -r requirements.txt

# 5. Set up environment variables
nano .env
# Add your API keys

# 6. Install PM2 for process management
npm install -g pm2

# 7. Start app with PM2
pm2 start "chainlit run chainlit_app.py --host 0.0.0.0 --port 8000" --name academic-debate

# 8. Set up nginx reverse proxy
apt install nginx -y
nano /etc/nginx/sites-available/academic-debate

# Add nginx config (see below)

# 9. Enable site
ln -s /etc/nginx/sites-available/academic-debate /etc/nginx/sites-enabled/
systemctl restart nginx

# 10. Install SSL with Let's Encrypt
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com
```

**Nginx Config:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Result:** Your own server at `https://yourdomain.com` 🌐

---

## 📊 Comparison Table

| Feature | Chainlit Cloud | ngrok | Hugging Face | VPS |
|---------|----------------|-------|--------------|-----|
| **Setup Time** | 5 min | 2 min | 30 min | 2 hours |
| **Cost** | Free tier | Free tier | Free | $5-10/mo |
| **Uptime** | 24/7 | Session-based | 24/7 | 24/7 |
| **Custom Domain** | ✅ Premium | ❌ | ❌ | ✅ |
| **HTTPS** | ✅ | ✅ | ✅ | ✅ (manual) |
| **Best For** | Production | Demos | Public projects | Full control |

---

## 🎯 Recommendation Based on Use Case

### **For Quick Demos/Testing:**
👉 **Use ngrok** - Instant public URL, no deployment

### **For Production (Easy):**
👉 **Use Chainlit Cloud** - Professional, managed, easy

### **For Free Public Hosting:**
👉 **Use Hugging Face Spaces** - Free forever, community-friendly

### **For Enterprise/Custom Domain:**
👉 **Use VPS** - Full control, your infrastructure

---

## 🔐 Security Considerations

**IMPORTANT: Before making your app public:**

1. **Rate Limiting**
   - Add rate limits to prevent API abuse
   - Each user shares your API quota

2. **Authentication**
   - Consider adding user authentication
   - Chainlit Cloud has built-in auth

3. **API Key Protection**
   - NEVER commit `.env` to git
   - Use environment variables
   - Monitor API usage

4. **Cost Monitoring**
   - Set up billing alerts for Anthropic API
   - Each debate costs ~$0.10-0.30 in API calls
   - Consider adding user limits

**Example Rate Limiting (add to chainlit_app.py):**
```python
from collections import defaultdict
import time

# Simple rate limiter
user_requests = defaultdict(list)
MAX_REQUESTS_PER_HOUR = 5

@cl.on_message
async def main(message: cl.Message):
    user_id = cl.user_session.get("user").identifier
    current_time = time.time()
    
    # Clean old requests
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id]
        if current_time - req_time < 3600
    ]
    
    # Check limit
    if len(user_requests[user_id]) >= MAX_REQUESTS_PER_HOUR:
        await cl.Message(
            content="⚠️ Rate limit reached. Please try again in 1 hour."
        ).send()
        return
    
    user_requests[user_id].append(current_time)
    
    # Continue with normal processing...
```

---

## 📞 Support & Resources

**Chainlit Documentation:**
- https://docs.chainlit.io/deployment/overview

**ngrok Documentation:**
- https://ngrok.com/docs

**Hugging Face Spaces:**
- https://huggingface.co/docs/hub/spaces

**Community:**
- Chainlit Discord: https://discord.gg/chainlit
- Hugging Face Forums: https://discuss.huggingface.co/

---

## ✅ Quick Start Script

Save this as `deploy_quick.ps1`:

```powershell
# Quick deployment script for Chainlit Cloud

Write-Host "🚀 Academic Debate System - Quick Deploy" -ForegroundColor Cyan
Write-Host ""

# Check if logged in
Write-Host "📝 Checking Chainlit login status..." -ForegroundColor Yellow
chainlit auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not logged in. Opening login page..." -ForegroundColor Red
    chainlit login
} else {
    Write-Host "✅ Already logged in!" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Deploying application..." -ForegroundColor Yellow
chainlit deploy

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "📌 Your app is now live and accessible to anyone!" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Don't forget to add your API keys in the Chainlit Cloud dashboard!" -ForegroundColor Yellow
```

Run with:
```powershell
powershell -ExecutionPolicy Bypass -File deploy_quick.ps1
```

---

**Choose the option that best fits your needs and follow the steps above!** 🚀
