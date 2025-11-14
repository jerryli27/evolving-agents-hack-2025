# Quick Start Guide

Get the Story Evolution Sandbox running in 5 minutes!

## 🚀 Fastest Path: Frontend Only (Mock Data)

The frontend works standalone with mock data - perfect for demos and development.

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000 and explore:
- 5 writer agents evolving over 5 rounds
- Interactive charts and visualizations
- Full script viewing
- Video export functionality

**All features work with realistic mock data!**

---

## 🔧 Full Stack Setup (Frontend + Backend)

### Prerequisites
- Node.js 18+
- Python 3.11+ (for backend)

### Step 1: Start the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend API will run at http://localhost:8000

### Step 2: Start the Frontend

```bash
cd frontend
cp .env.example .env.local
# Edit .env.local to set: NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

Frontend will run at http://localhost:3000

---

## 📦 What's Included

### Frontend (`/frontend`)
- **Next.js 14** with TypeScript
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- Fully functional with mock data
- Ready for API integration

### Backend (`/backend`)
- **FastAPI** template with basic endpoints
- CORS configured for local development
- Ready to implement writer agent logic
- Structured for easy Render deployment

---

## 🎯 Next Steps

### For Development
1. Keep frontend using mock data while building backend
2. Implement writer agent logic in backend
3. Replace mock data with API calls when ready

### For Deployment
1. See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions
2. Deploy backend to Render (free tier available)
3. Deploy frontend to Vercel (free tier available)
4. Connect them with environment variables

---

## 📚 Key Files

- `frontend/app/page.tsx` - Main dashboard
- `frontend/lib/mockData.ts` - Sample data
- `frontend/lib/api.ts` - API client (with fallback)
- `backend/main.py` - Backend API template
- `DEPLOYMENT.md` - Full deployment guide

---

## 🆘 Troubleshooting

**Frontend won't start?**
- Run `npm install` in frontend directory
- Check Node.js version: `node --version` (need 18+)

**Backend won't start?**
- Run `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.11+)

**Want to use mock data only?**
- Don't set `NEXT_PUBLIC_API_URL` environment variable
- Frontend automatically uses mock data

---

## 💡 Tips

- Frontend works great without backend for demos
- Backend template is ready - just add your writer agent logic
- All TypeScript types are defined in `frontend/types/index.ts`
- Check `frontend/lib/mockData.ts` to see expected data structure

Happy coding! 🎉
