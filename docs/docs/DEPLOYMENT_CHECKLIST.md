# SmartNutri Complete Deployment Checklist

**Status**: Ready for Production  
**Date**: April 10, 2026  
**Total Steps**: 15  

---

## ✅ PRE-DEPLOYMENT VERIFICATION

### Frontend Configuration
- [x] Frontend API client configured (`src/api/index.js`)
- [x] Environment variables set up (`.env.local`, `.env.production`)
- [x] Vite build configuration ready
- [x] React Router configured
- [x] All components integrated

### Backend Configuration  
- [x] FastAPI backend ready
- [x] CORS middleware configured
- [x] MongoDB connection configured
- [x] JWT authentication ready
- [x] All 25+ endpoints implemented

### Local Connectivity
- [x] Backend runs on `http://localhost:3001`
- [x] Frontend runs on `http://localhost:5173`
- [x] CORS allows localhost origins
- [x] API client points to correct backend URL

---

## 🚀 DEPLOYMENT STEPS (15 minutes)

### STEP 1: Database Setup (MongoDB Atlas) - 5 mins
- [ ] Go to https://www.mongodb.com/cloud/atlas
- [ ] Create free account (no credit card required)
- [ ] Create free cluster (takes 2-3 mins)
- [ ] Create database user: `smartnutri_user`
- [ ] Save password securely
- [ ] Get connection string: `mongodb+srv://smartnutri_user:PASSWORD@cluster.mongodb.net/smartnutri?retryWrites=true&w=majority`
- [ ] Add IP whitelist: `0.0.0.0/0`
- [ ] **SAVE**: Database URL for later

### STEP 2: Backend Deployment (Render.com) - 5 mins
- [ ] Go to https://render.com
- [ ] Sign up with GitHub account
- [ ] Create "Web Service"
- [ ] Connect your GitHub repo: `smartnutri-vite`
- [ ] Configure service:
  - Name: `smartnutri-backend`
  - Environment: `Python 3`
  - Build command: `pip install -r smartnutri-backend/requirements.txt`
  - Start command: `cd smartnutri-backend && uvicorn main:app --host 0.0.0.0 --port 8000`
  - Region: Choose closest to you
  - Plan: Free
- [ ] Add environment variables:
  ```
  MONGO_URL=mongodb+srv://smartnutri_user:YOUR_PASSWORD@cluster.mongodb.net/smartnutri?retryWrites=true&w=majority
  SECRET_KEY=your-32-char-secret-key-here
  FRONTEND_URL=https://your-frontend.vercel.app
  ENV=production
  PORT=8000
  ```
- [ ] Click "Deploy"
- [ ] Wait for build to complete (2-3 mins)
- [ ] **SAVE**: Backend URL (e.g., `https://smartnutri-backend.onrender.com`)
- [ ] Test: Visit URL (first request takes 10-20 seconds to wake up)

### STEP 3: Frontend Deployment (Vercel) - 3 mins
- [ ] Go to https://vercel.com
- [ ] Sign up with GitHub
- [ ] Click "New Project"
- [ ] Import your GitHub repo: `smartnutri-vite`
- [ ] Configure project:
  - Framework Preset: `Vite`
  - Root Directory: `./smartnutri-vite`
  - Build Command: `npm run build`
  - Output Directory: `dist`
- [ ] Add environment variable:
  ```
  VITE_API_URL=https://smartnutri-backend.onrender.com
  ```
- [ ] Click "Deploy"
- [ ] Wait for deployment (2-3 mins)
- [ ] **SAVE**: Frontend URL (e.g., `https://smartnutri-web.vercel.app`)

### STEP 4: Update Backend CORS
- [ ] Go back to Render.com
- [ ] Edit environment variables
- [ ] Update `FRONTEND_URL=https://your-frontend.vercel.app`
- [ ] Redeploy backend

### STEP 5: Verify Production Connectivity
- [ ] Visit your frontend URL
- [ ] Attempt to register new user
- [ ] Check browser console for errors
- [ ] Check network tab for API calls
- [ ] Verify API returns 200+ responses

---

## 🔗 CONNECTIVITY VERIFICATION

### Local Development (Already Connected)
```
Frontend: http://localhost:5173
Backend: http://localhost:3001
Database: mongomock (local)
Status: ✅ Connected
```

### Production Deployment
```
Frontend: https://smartnutri-web.vercel.app
Backend: https://smartnutri-backend.onrender.com
Database: MongoDB Atlas (free tier)
Status: ⏳ Pending deployment
```

---

## 📋 CURRENT CONNECTION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │  Frontend (Vercel)        │
         │ https://...vercel.app     │
         │ - React 18                │
         │ - Vite build              │
         │ - API client              │
         └────────────┬──────────────┘
                      │
                      │ HTTPS Requests
                      │ (VITE_API_URL)
                      ▼
         ┌───────────────────────────┐
         │  Backend (Render)         │
         │ https://...onrender.com   │
         │ - FastAPI                 │
         │ - 25+ endpoints           │
         │ - JWT auth                │
         │ - CORS enabled            │
         └────────────┬──────────────┘
                      │
                      │ MongoDB Queries
                      ▼
         ┌───────────────────────────┐
         │  Database (MongoDB Atlas) │
         │ Free tier 512MB           │
         │ - Users Collection        │
         │ - Meals Collection        │
         │ - Cycles Collection       │
         │ - Progress Collection     │
         └───────────────────────────┘
```

---

## 🔐 ENVIRONMENT VARIABLES REQUIRED

### Frontend (.env.production)
```
VITE_API_URL=https://smartnutri-backend.onrender.com
```

### Backend (.env on Render)
```
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/smartnutri?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-min-32-chars
FRONTEND_URL=https://smartnutri-web.vercel.app
ENV=production
PORT=8000
```

---

## ✨ WHAT WORKS AFTER DEPLOYMENT

### User Features
✅ Register and verify email  
✅ Login with JWT token  
✅ Complete 5-step onboarding  
✅ Log meals and track nutrition  
✅ Search 42+ food database  
✅ Chat with AI nutrition coach  
✅ Track menstrual cycle  
✅ Log mood and symptoms  
✅ Get cycle predictions  
✅ Track progress metrics  
✅ View achievements  
✅ Full dashboard overview  

### Technical Features
✅ Persistent data in MongoDB  
✅ JWT token authentication  
✅ CORS enabled for production  
✅ Error handling and logging  
✅ Automatic retry on failed requests  
✅ React Query caching  

---

## 🆘 TROUBLESHOOTING

### Issue: CORS Error
**Solution:**
1. Check `FRONTEND_URL` environment variable on Render backend
2. Ensure frontend URL in browser matches `FRONTEND_URL`
3. Redeploy backend after updating CORS

### Issue: Backend takes 20 seconds to respond
**Solution:**
- Normal for free tier on Render (auto-sleeps after 15 min inactivity)
- First request wakes up the service
- Subsequent requests are fast

### Issue: 404 errors from API
**Solution:**
1. Check `VITE_API_URL` in frontend .env
2. Verify backend URL is correct (test in browser)
3. Check backend logs on Render for errors

### Issue: Cannot connect to MongoDB
**Solution:**
1. Verify connection string in `MONGO_URL`
2. Check database user and password
3. Verify IP whitelist includes `0.0.0.0/0`
4. Test connection: `mongosh "mongodb+srv://..."`

---

## 📊 DEPLOYMENT SUMMARY

| Component | Status | URL |
|-----------|--------|-----|
| Frontend | ⏳ Ready to deploy | vercel.app |
| Backend | ⏳ Ready to deploy | onrender.com |
| Database | ⏳ Ready to deploy | atlas.mongodb.com |
| **Total Setup Time** | **15 mins** | |
| **Total Cost** | **$0** | FREE |

---

## 🎯 NEXT STEPS AFTER DEPLOYMENT

1. ✅ Monitor backend logs on Render
2. ✅ Check frontend performance on Vercel
3. ✅ Test user registration flow
4. ✅ Load test with multiple concurrent users
5. ✅ Configure monitoring (Sentry optional)
6. ✅ Set up error alerts
7. ✅ Begin Phase 2 feature development

---

**Status: READY FOR DEPLOYMENT** ✅
All systems configured and tested locally.
Ready to launch production environment!
