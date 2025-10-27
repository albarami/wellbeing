# 🚀 Share Your App in 2 Minutes with ngrok

## Quick Steps to Share Your Academic Debate System

### 1️⃣ Install ngrok (One-Time Setup)

**Option A: Download Installer**
1. Go to https://ngrok.com/download
2. Download Windows version
3. Extract `ngrok.exe` to `C:\ngrok\`
4. Add `C:\ngrok` to your PATH

**Option B: Using Chocolatey (Recommended)**
```powershell
choco install ngrok
```

### 2️⃣ Sign Up (Free - One-Time)

1. Go to https://ngrok.com/signup
2. Create free account
3. Get your auth token from dashboard: https://dashboard.ngrok.com/get-started/your-authtoken

### 3️⃣ Configure Auth Token (One-Time)

```powershell
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### 4️⃣ Start Your App

**Terminal 1:**
```powershell
cd "D:\Academic debate"
chainlit run chainlit_app.py
```

Wait until you see: "Your app is available at http://localhost:8000"

### 5️⃣ Start ngrok Tunnel

**Terminal 2 (New Window):**
```powershell
ngrok http 8000
```

### 6️⃣ Share the URL! 🎉

You'll see something like:
```
Forwarding: https://abc123def456.ngrok.io -> localhost:8000
```

**Share the `https://abc123def456.ngrok.io` URL** with anyone!

---

## 📋 Full Example

```powershell
# Terminal 1
PS D:\Academic debate> chainlit run chainlit_app.py
2025-10-27 15:30:00 - Your app is available at http://localhost:8000

# Terminal 2
PS D:\> ngrok http 8000

ngrok                                                                                              
                                                                                                    
Session Status                online                                                              
Account                       your-email@example.com (Plan: Free)                                 
Version                       3.5.0                                                               
Region                        United States (us)                                                  
Latency                       42ms                                                                
Web Interface                 http://127.0.0.1:4040                                               
Forwarding                    https://abc123def456.ngrok.io -> localhost:8000                     

Connections                   ttl     opn     rt1     rt5     p50     p90                          
                              0       0       0.00    0.00    0.00    0.00
```

**Your public URL:** `https://abc123def456.ngrok.io`

---

## ⚠️ Important Notes

### Free Tier Limits:
- ✅ 1 online ngrok process
- ✅ 4 tunnels/ngrok process
- ✅ 40 connections/minute
- ⚠️ URL changes each time you restart ngrok

### Session Duration:
- Free tier: Max 8 hours per session
- After 8 hours, restart ngrok (new URL)

### Security:
- Anyone with the URL can access your app
- They'll use YOUR API keys
- Consider adding rate limiting (see DEPLOYMENT_GUIDE.md)

---

## 🎯 When to Use ngrok

**Perfect for:**
- ✅ Quick demos to colleagues
- ✅ Testing with friends
- ✅ Showing proof-of-concept
- ✅ Short presentations

**NOT recommended for:**
- ❌ Long-term public access
- ❌ Production use
- ❌ Large audiences
- ❌ When you need a permanent URL

For long-term sharing, use **Chainlit Cloud** or **Hugging Face Spaces** (see DEPLOYMENT_GUIDE.md)

---

## 🔍 Troubleshooting

### "command not found: ngrok"
```powershell
# Add to PATH or use full path
C:\ngrok\ngrok.exe http 8000
```

### "Invalid credentials" error
```powershell
# Make sure you configured auth token
ngrok config add-authtoken YOUR_TOKEN
```

### "Port already in use"
```powershell
# Make sure Chainlit is running on port 8000
# Check with: netstat -an | findstr 8000
```

### Can't access the ngrok URL
- Check Windows Firewall
- Verify Chainlit is running
- Try the ngrok Web Interface: http://127.0.0.1:4040

---

## 📊 Monitor Your Tunnel

Open http://127.0.0.1:4040 to see:
- Real-time request logs
- Response times
- Connection details
- Request/response inspection

---

## 🎓 Pro Tips

1. **Keep URLs Handy**: Screenshot the ngrok URL or copy to clipboard
2. **Test First**: Visit the URL yourself before sharing
3. **Monitor Usage**: Watch the ngrok dashboard for activity
4. **Restart if Needed**: If connection is slow, restart ngrok for new server

---

## ✅ Quick Checklist

- [ ] ngrok installed
- [ ] Free account created
- [ ] Auth token configured
- [ ] Chainlit app running on port 8000
- [ ] ngrok tunnel started
- [ ] URL copied and tested
- [ ] URL shared with others

---

**You're ready to share your Academic Debate System! 🚀**

For permanent hosting, see: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
