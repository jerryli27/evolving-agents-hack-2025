# 🚀 Deployment Checklist

Quick reference for deploying to Vercel (frontend) and Render (backend).

## ✅ Pre-Deployment Checklist

- [ ] Code is committed and pushed to GitHub
- [ ] Frontend works locally (`cd frontend && npm run dev`)
- [ ] Backend template is ready (optional for MVP)
- [ ] You have accounts on Vercel and Render

---

## 📦 Frontend Deployment (Vercel)

### Option 1: Vercel CLI (Fastest)

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Login
vercel login

# Deploy to production
vercel --prod
```

### Option 2: Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import `evolving-agents-hack-2025` from GitHub
4. Configure:
   - **Framework**: Next.js
   - **Root Directory**: `frontend`
   - **Environment Variables**:
     ```
     NEXT_PUBLIC_API_URL = https://your-backend.onrender.com
     ```
5. Click "Deploy"
6. **Your frontend URL**: `https://your-app.vercel.app`

---

## 🔧 Backend Deployment (Render)

### Step-by-Step

1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect GitHub and select your repository
4. Configure:
   - **Name**: `story-evolution-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
5. Add Environment Variables:
   ```
   ANTHROPIC_API_KEY = sk-ant-...
   FRONTEND_URL = https://your-app.vercel.app
   ```
6. Click "Create Web Service"
7. **Your backend URL**: `https://story-evolution-backend.onrender.com`

---

## 🔗 Connect Frontend and Backend

### 1. Update Frontend Environment Variable

In Vercel Dashboard:
- Go to your project → Settings → Environment Variables
- Update `NEXT_PUBLIC_API_URL`:
  ```
  https://story-evolution-backend.onrender.com
  ```
- Redeploy: Deployments → ⋯ → Redeploy

### 2. Update Backend CORS

In `backend/main.py`, update:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Your actual Vercel URL
        "https://*.vercel.app",
        # ... rest of origins
    ],
    # ...
)
```

Commit and push to trigger auto-deploy on Render.

---

## 🧪 Verification

### Test Backend
```bash
curl https://story-evolution-backend.onrender.com/
curl https://story-evolution-backend.onrender.com/api/writers
```

### Test Frontend
1. Visit `https://your-app.vercel.app`
2. Open DevTools → Network tab
3. Verify API calls succeed (no CORS errors)
4. Interact with the dashboard

---

## ⚡ Quick Deploy Commands

```bash
# Frontend (one command)
cd frontend && vercel --prod

# Backend (automatic via git push)
git add backend/ && git commit -m "Update backend" && git push
```

---

## 🎯 URLs to Save

After deployment, save these:

- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://story-evolution-backend.onrender.com`
- **GitHub Repo**: `https://github.com/iamjustoutthere/evolving-agents-hack-2025`

---

## 🆘 Common Issues

### Frontend can't reach backend
- ✅ Check Vercel env var: `NEXT_PUBLIC_API_URL`
- ✅ Ensure backend CORS includes your Vercel domain
- ✅ Wait 30-60s for Render free tier to wake up

### Environment variables not working
- ✅ Must start with `NEXT_PUBLIC_` for client-side
- ✅ Redeploy after adding new variables
- ✅ Check correct environment (Production vs Preview)

### Build fails
- ✅ Verify `package.json` and `requirements.txt` are correct
- ✅ Check build logs in Vercel/Render dashboard
- ✅ Test build locally first: `npm run build`

---

## 💰 Cost

**Free Tier** (Perfect for hackathon/demo):
- Vercel: 100GB bandwidth, unlimited requests
- Render: 750 hours/month, auto-sleep after 15 min
- **Total: $0/month**

**Production** (If you want always-on):
- Vercel Pro: $20/month
- Render Starter: $7/month
- **Total: $27/month**

---

## 📚 Full Documentation

For detailed instructions, see:
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Complete deployment guide
- [QUICKSTART.md](./QUICKSTART.md) - Local development setup
- [README.md](./README.md) - Project overview

---

**Happy Deploying! 🎉**
