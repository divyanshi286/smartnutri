# SmartNutri - 100% FREE Deployment Guide

**No Credit Card Required. Zero Cost. Fully Functional.**

---

## 🎯 Free Deployment Stack

| Component | Service | Cost | Specs |
|-----------|---------|------|-------|
| **Frontend** | Vercel | FREE | Unlimited deployments, 100GB bandwidth |
| **Backend** | Render.com | FREE | 0.5 CPU, 512MB RAM (auto-sleeps after 15min) |
| **Database** | MongoDB Atlas | FREE | 512MB storage, no credit card needed |
| **Analytics** | Plausible/Fathom | FREE | 10k free page views |
| **Monitoring** | Sentry | FREE | 10k free events/month |
| **Total Cost** | **$0** | **Forever Free Tier** | |

---

## 📋 Step-by-Step Setup (30 mins)

### Step 0: Prerequisites
```
You need:
✓ GitHub account (free at github.com)
✓ Email for MongoDB Atlas
✓ Your code in GitHub repo
```

---

### Step 1: Deploy Frontend to Vercel (5 mins)

**1. Go to vercel.com/signup**
```
- Sign up with GitHub
- Authorize Vercel to access your repos
- Skip the team creation
```

**2. Create new project**
```
- Click "New Project"
- Select your smartnutri-vite repo from GitHub
- Framework preset: Vite
- Root directory: ./smartnutri-vite
- Build command: npm run build
- Output directory: dist
- Environment variables: (skip for now)
```

**3. Deploy**
```
- Click Deploy
- Wait 2-3 minutes
- Get your URL: something.vercel.app
```

**Result:** Your frontend is live at no cost ✅

---

### Step 2: Database Setup (5 mins)

**1. Go to mongodb.com/cloud/atlas**
```
- Click "Start Free"
- Sign up with email
- NO CREDIT CARD REQUIRED
```

**2. Create cluster**
```
- Choose Free tier
- Select region closest to you
- Create cluster (takes 2-3 minutes)
```

**3. Get connection string**
```
- Click "Connect"
- Click "Create a database user"
- Username: smartnutri_user
- Password: (generate random strong)
- Click "Create User"
```

**4. Get connection URI**
```
- Click "Choose connection method"
- Select "Drivers"
- Copy the connection string
- Format: mongodb+srv://username:password@cluster.mongodb.net/smartnutri?retryWrites=true
```

**5. Whitelist IP**
```
- Go to Network Access
- Add IP address: 0.0.0.0/0 (allows all - for free tier only)
- Confirm
```

**Result:** Database is ready and free ✅

---

### Step 3: Deploy Backend to Render (10 mins)

**1. Go to render.com**
```
- Sign up with GitHub
- Authorize access
```

**2. Create Web Service**
```
- Click "New +"
- Select "Web Service"
- Connect your GitHub repo
- Choose smartnutri-vite repo
```

**3. Configure Service**
```
Name: smartnutri-backend
Environment: Python 3
Build command: pip install -r smartnutri-backend/requirements.txt
Start command: cd smartnutri-backend && uvicorn main:app --host 0.0.0.0 --port 8000
Region: Choose closest to you
Plan: Free
```

**4. Add Environment Variables**
```
In Environment tab, add:

MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/smartnutri?retryWrites=true&w=majority
OPENAI_API_KEY=sk-test (optional, fallback works)
JWT_SECRET=your-secret-key-here-min-32-chars
CORS_ORIGINS=https://yourname.vercel.app
NODE_ENV=production
```

**5. Deploy**
```
- Click "Create Web Service"
- Render starts building (2-3 minutes)
- Once built, get your URL: something.onrender.com
- First request wakes up service (might take 10-20 seconds)
```

**Result:** Backend is live and free ✅

---

### Step 4: Connect Frontend to Backend

**1. Update frontend API URL**
   
In `smartnutri-vite/src/api/index.js`, change:
```javascript
// Change from:
const API_BASE = 'http://localhost:3001/api'

// To:
const API_BASE = 'https://yourbackend.onrender.com/api'
```

**2. Redeploy frontend**
```
- Push changes to GitHub
- Vercel auto-deploys automatically
- Or manually redeploy in Vercel dashboard
```

**Result:** Frontend and backend connected ✅

---

## ✅ Testing Your Free Deployment

Run your E2E tests against production:

```bash
# In terminal, modify final_mvp_test.py:

# Change from:
BASE_URL = "http://localhost:3001"

# To:
BASE_URL = "https://yourbackend.onrender.com"

# Then run:
python final_mvp_test.py
```

Expected result: 14/14 tests passing ✅

---

## 🚨 Important Limitations (Free Tier)

### Render Backend (Free Tier)
```
❌ Sleeps after 15 minutes of inactivity
   └─ First request takes 20-30 seconds to wake up
   └─ Solution: Run a "keep alive" check every 10 minutes

❌ Limited to 0.5 CPU
   └─ Fine for MVP, not for production scale

❌ 512MB RAM
   └─ Enough for small user base (< 1000 users)

✅ Good for: MVP testing, beta launch
```

### MongoDB Atlas (Free Tier)
```
❌ Limited to 512MB storage
   └─ Fine for MVP (~ 50k meal logs, 1000 users)

❌ Shared cluster (slower)
   └─ Still acceptable for MVP usage

✅ Good for: Initial launch, testing
```

### Vercel (Free Tier)
```
✅ Unlimited deployments
✅ 100GB bandwidth (plenty)
✅ Fast CDN worldwide
✅ Good for: Production-grade frontend
```

---

## 🔧 Free Upgrade Paths (When You Need)

### Keep It Free
```
When to stick with free:
- < 100 daily active users
- MVP testing phase
- Beta launch
- Learning/development
```

### Upgrade to Paid (If Needed)
```
Render Backend: $7/month
  - Always-on instance
  - 2GB RAM
  - 1 CPU
  └─ Supports 1000-5000 concurrent users

MongoDB Atlas: $57/month
  - When you exceed 512MB
  - Better performance
  - Backup features
  └─ Supports 100M documents

Total: $64/month (when needed)
```

---

## 🛠️ Workaround: Prevent Backend Sleep

### Option 1: Uptime Robot (Free)
```
1. Go to uptimerobot.com
2. Sign up free
3. Create monitor for: https://yourbackend.onrender.com/health
4. Check every 5 minutes
5. Backend never sleeps
```

### Option 2: GitHub Actions (Free)
```
Create .github/workflows/keep-alive.yml:

name: Keep Backend Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Keep backend awake
        run: curl https://yourbackend.onrender.com/health
```

### Option 3: Vercel Cron (Free)
```
Add to vercel.json:
{
  "crons": [{
    "path": "/api/health",
    "schedule": "*/10 * * * *"
  }]
}
```

---

## 📊 Cost Breakdown (Forever Free)

| Service | Monthly Cost | Annual Cost |
|---------|--------------|-------------|
| Vercel | $0 | $0 |
| Render | $0 (free tier) | $0 |
| MongoDB | $0 (free tier) | $0 |
| Sentry | $0 (10k events) | $0 |
| Uptime Robot | $0 (free tier) | $0 |
| **TOTAL** | **$0** | **$0** |

---

## 🚀 Deployment Checklist (Free)

```
☐ GitHub account created
☐ Code pushed to GitHub repo
☐ Vercel account created
☐ Frontend deployed (vercel.app)
☐ MongoDB Atlas account (no CC)
☐ Database created & connection URL obtained
☐ Render account created
☐ Backend deployed (onrender.com)
☐ Environment variables set
☐ Frontend API URL updated to Render
☐ Redeploy frontend after changes
☐ Run E2E tests against production
☐ Test on mobile device
☐ Set up Uptime Robot to prevent sleep
```

---

## 🎯 Quick Reference URLs

After deployment, you'll have:

```
Frontend: https://smartnutri-frontend.vercel.app
Backend API: https://smartnutri-backend.onrender.com
Database: MongoDB Atlas cloud (no URL needed from client)
Dashboard: https://smartnutri-frontend.vercel.app/dashboard
```

---

## ⚡ Pro Tips (Free Tier)

### Optimize for Free Tier
```
1. Keep backend lightweight
   - No heavy image processing
   - No video encoding
   - Batch database operations

2. Cache aggressively
   - Use React Query's stale time
   - Cache API responses
   - Browser caching headers

3. Lazy load components
   - Code splitting in Vite
   - Lazy load routes
   - Lazy load images

4. Database optimization
   - Index frequently queried fields
   - Avoid N+1 queries
   - Limit returned fields
```

### Monitor Usage
```
Vercel Analytics: Free dashboard
  - See traffic patterns
  - Identify slow APIs

Render Metrics: Free in dashboard
  - Monitor CPU/RAM usage
  - Check response times

MongoDB Atlas Monitoring: Free
  - Check storage usage
  - Monitor query performance
```

---

## 🆘 Troubleshooting Free Tier

### Backend returns 503 / Slow response
```
✅ Solution: This is normal on free Render tier
- First request wakes up: 20-30 seconds
- Subsequent requests: < 2 seconds
- Use Uptime Robot to keep it alive
```

### "Database connection failed"
```
✅ Check:
- MongoDB connection string is correct
- IP whitelist includes 0.0.0.0/0
- Database user password is correct
- No special characters in password (or URL-encoded)

✅ Test with:
mongosh "mongodb+srv://user:password@cluster.mongodb.net/smartnutri"
```

### Frontend shows "Cannot reach API"
```
✅ Check:
- Backend is deployed and running
- API URL in frontend matches Render URL
- CORS is enabled in backend
- Frontend was redeployed after URL change
```

### Storage exceeded (MongoDB)
```
✅ Solutions:
- Delete test data
- Archive old data
- Upgrade to paid ($57/month)
- Use database compression
```

---

## 📱 Mobile Testing (Free)

```
After deployment:
1. Get your Vercel URL
2. Share: https://yourname.vercel.app
3. Open on phone (any device, any network)
4. Test all features
5. No installation needed

For production beta:
- Invite 50-100 beta users
- Monitor Sentry errors (free)
- Collect feedback in Discord/Slack (free)
```

---

## 🎉 You're LIVE! (For Free)

```
✅ Frontend deployed
✅ Backend running
✅ Database configured
✅ All 14 E2E tests passing
✅ $0/month cost
✅ Ready for beta launch
✅ No credit card required
```

Next steps:
1. Invite beta users
2. Monitor errors (Sentry)
3. Collect feedback
4. Iterate Phase 2 features
5. Upgrade when you need (optional)

---

## 💬 Support Channels (All Free)

```
📚 Documentation:
  - Render docs: render.com/docs
  - Vercel docs: vercel.com/docs
  - MongoDB docs: mongodb.com/docs

💬 Communities:
  - Reddit: r/webdev, r/learnprogramming
  - Stack Overflow: Free Q&A
  - Discord: Vercel, Render communities

🐛 Issues:
  - GitHub Issues: Free issue tracking
  - Render support: Free basic support
```

---

**Your MVP is now live. For free. Forever.** 🚀
