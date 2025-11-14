# Deployment Guide

Complete instructions for deploying the Story Evolution Sandbox to production.

## Architecture

- **Frontend**: Vercel (Next.js optimized hosting)
- **Backend**: Render (Python/Node.js API hosting)

## Prerequisites

- GitHub account with this repository
- Vercel account (free tier available)
- Render account (free tier available)

---

## Part 1: Deploy Backend to Render

### Step 1: Prepare Backend for Deployment

Create a `backend` directory in your repository (if not already created):

```bash
mkdir -p backend
cd backend
```

#### For Python/FastAPI Backend:

Create `requirements.txt`:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
anthropic==0.7.0  # If using Claude API
```

Create `main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",  # Your Vercel deployment
        os.getenv("FRONTEND_URL", "")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Story Evolution Sandbox API"}

@app.get("/api/writers")
def get_writers():
    # Your writer data logic here
    return []

@app.get("/api/rounds")
def get_rounds():
    # Your rounds data logic here
    return []

@app.get("/api/finalists")
def get_finalists(n: int = 3):
    # Your finalists logic here
    return []

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

Create `render.yaml` (optional, for infrastructure as code):
```yaml
services:
  - type: web
    name: story-evolution-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: ANTHROPIC_API_KEY
        sync: false  # Add manually in Render dashboard
```

#### For Node.js/Express Backend:

Create `package.json`:
```json
{
  "name": "story-evolution-backend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  }
}
```

Create `server.js`:
```javascript
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors({
  origin: [
    'http://localhost:3000',
    /\.vercel\.app$/,
    process.env.FRONTEND_URL
  ].filter(Boolean)
}));
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Story Evolution Sandbox API' });
});

app.get('/api/writers', (req, res) => {
  // Your writer data logic
  res.json([]);
});

app.get('/api/rounds', (req, res) => {
  // Your rounds data logic
  res.json([]);
});

app.get('/api/finalists', (req, res) => {
  const n = parseInt(req.query.n) || 3;
  // Your finalists logic
  res.json([]);
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Step 2: Push Backend to GitHub

```bash
git add backend/
git commit -m "Add backend API for deployment"
git push
```

### Step 3: Deploy on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com/
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Select "Build and deploy from a Git repository"
   - Connect your GitHub account
   - Select `evolving-agents-hack-2025` repository

3. **Configure Service**
   - **Name**: `story-evolution-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your deployment branch)
   - **Root Directory**: `backend`
   - **Environment**: Python or Node
   - **Build Command**:
     - Python: `pip install -r requirements.txt`
     - Node: `npm install`
   - **Start Command**:
     - Python: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - Node: `npm start`
   - **Plan**: Free

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add variables:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     FRONTEND_URL=https://your-app.vercel.app
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://story-evolution-backend.onrender.com`

### Important Notes for Render:
- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Consider paid tier ($7/mo) for always-on service

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend Environment Variables

Create `frontend/.env.local` (for local development):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Create `frontend/.env.production` (gitignored, just for reference):
```bash
NEXT_PUBLIC_API_URL=https://story-evolution-backend.onrender.com
```

### Step 2: Update Frontend to Use API

Create `frontend/lib/api.ts`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchWriters() {
  const response = await fetch(`${API_URL}/api/writers`);
  if (!response.ok) throw new Error('Failed to fetch writers');
  return response.json();
}

export async function fetchRounds() {
  const response = await fetch(`${API_URL}/api/rounds`);
  if (!response.ok) throw new Error('Failed to fetch rounds');
  return response.json();
}

export async function fetchFinalists(n: number = 3) {
  const response = await fetch(`${API_URL}/api/finalists?n=${n}`);
  if (!response.ok) throw new Error('Failed to fetch finalists');
  return response.json();
}
```

### Step 3: Deploy to Vercel

#### Option A: Via Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? story-evolution-sandbox (or your choice)
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

#### Option B: Via Vercel Dashboard

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Click "Add New..." → "Project"

2. **Import Repository**
   - Click "Import Git Repository"
   - Select `evolving-agents-hack-2025`
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)
   - **Install Command**: `npm install` (auto-filled)

4. **Add Environment Variables**
   - Click "Environment Variables"
   - Add:
     ```
     Name: NEXT_PUBLIC_API_URL
     Value: https://story-evolution-backend.onrender.com
     ```
   - Select all environments (Production, Preview, Development)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app will be live at: `https://your-app.vercel.app`

### Step 4: Configure Custom Domain (Optional)

1. In Vercel Dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. SSL automatically provisioned

---

## Part 3: Connect Frontend and Backend

### Update Backend CORS

In your backend, update the CORS configuration to include your Vercel URL:

**Python (FastAPI)**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app",
        "https://*.vercel.app",  # For preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Node.js (Express)**:
```javascript
app.use(cors({
  origin: [
    'http://localhost:3000',
    'https://your-app.vercel.app',
    /\.vercel\.app$/
  ]
}));
```

Commit and push to trigger Render redeployment:
```bash
git add backend/
git commit -m "Update CORS for Vercel deployment"
git push
```

---

## Part 4: Verify Deployment

### Test Backend
```bash
curl https://story-evolution-backend.onrender.com/
curl https://story-evolution-backend.onrender.com/api/writers
```

### Test Frontend
1. Visit your Vercel URL
2. Open browser DevTools → Network tab
3. Verify API calls are successful
4. Check for CORS errors (should be none)

---

## Automatic Deployments

Both platforms support automatic deployments:

### Vercel
- **Production**: Deploys when you push to `main` branch
- **Preview**: Deploys for every pull request
- Configure in: Settings → Git

### Render
- **Auto-deploy**: Enabled by default on main branch
- Configure in: Settings → Build & Deploy

---

## Troubleshooting

### Frontend can't reach backend
- ✅ Check `NEXT_PUBLIC_API_URL` in Vercel environment variables
- ✅ Verify backend CORS includes your Vercel domain
- ✅ Check Render backend is running (free tier may spin down)

### Backend slow to respond
- ⚠️ Render free tier spins down after inactivity
- 💡 First request takes 30-60 seconds
- 💡 Consider implementing a "warming" endpoint or upgrade to paid tier

### CORS errors
- ✅ Ensure backend allows your Vercel domain
- ✅ Check protocol (https vs http)
- ✅ Verify credentials and headers in CORS config

### Environment variables not working
- ✅ Vercel: Must start with `NEXT_PUBLIC_` for client-side access
- ✅ Redeploy after adding new environment variables
- ✅ Check environment (Production vs Preview)

---

## Cost Estimate

### Free Tier (Both Platforms)
- **Vercel**: 100GB bandwidth, unlimited requests
- **Render**: 750 hours/month, 512MB RAM, auto-sleep
- **Total**: $0/month

### Paid Tier (For Production)
- **Vercel Pro**: $20/month (better performance, analytics)
- **Render Starter**: $7/month (always-on, 512MB RAM)
- **Total**: $27/month

---

## Quick Deployment Checklist

- [ ] Create backend directory with API code
- [ ] Add requirements.txt/package.json to backend
- [ ] Push backend to GitHub
- [ ] Create Render account and deploy backend
- [ ] Note backend URL from Render
- [ ] Create Vercel account
- [ ] Deploy frontend to Vercel via CLI or dashboard
- [ ] Add NEXT_PUBLIC_API_URL to Vercel environment variables
- [ ] Update backend CORS with Vercel URL
- [ ] Test complete flow
- [ ] Set up custom domain (optional)

---

## Support Links

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Next.js Deployment**: https://nextjs.org/docs/deployment
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

Happy deploying! 🚀
