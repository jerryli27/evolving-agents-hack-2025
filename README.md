# Story Evolution Sandbox

> AI Story Market: Evolving Writer Agents for Short-Drama IP

A hackathon project where multiple AI writer agents compete to create the most engaging short drama scripts. Reader agents score and critique their work over multiple rounds, and the best stories evolve into production-ready video content.

![Story Evolution Sandbox](https://img.shields.io/badge/Next.js-14-black) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688) ![TypeScript](https://img.shields.io/badge/TypeScript-5-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Project Overview

**Working Title**: AI Story Market: Evolving Writer Agents for Short-Drama IP

**What it does**:
- 5 unique writer agents (each with different "style DNA") create short drama scripts
- Reader/critic agents score stories on alignment, novelty, and coherence
- Writers evolve their approach based on feedback over 5 rounds
- Top 3 scripts are packaged for AI video generation (Sora, Runway, etc.)

**Key Innovation**: Visualize the evolution process - see how each writer improves (or fails) round by round, not just final scores.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Vercel)                     │
│  Next.js Dashboard - Visualization & Export Interface   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ REST API
                     │
┌────────────────────┴────────────────────────────────────┐
│                   Backend (Render)                       │
│  Writer Agents │ Reader Agents │ Evolution Engine       │
└──────────────────────────────────────────────────────────┘
```

## ✨ Features

### Story Evolution Dashboard
- **Interactive Multi-Line Chart**: See 5 writers evolve over 5 rounds (nof1.ai style)
- **Dynamic Metrics**: Switch between composite score, reader alignment, novelty, and coherence
- **Writer Deep Dive**: Click any point to explore writer's full history
- **Finalists Showcase**: Top 3 performing stories with rankings

### Export to Video Pipeline
- Auto-generate beat sheets from scripts
- Configurable video length (30s/60s/90s/120s)
- Multiple visual style options
- Copy as JSON or text prompt for AI video tools

### Writer Agents (5 Unique Personalities)
1. **Melodrama Maven** - Emotional, character-driven romance
2. **Plot Twister** - Suspense master with shocking reveals
3. **Comedy Genius** - Witty rom-com specialist
4. **Dark Realist** - Gritty psychological dramas
5. **Fantasy Weaver** - Magical realism stories

## 🚀 Quick Start

### Fastest Path (Frontend Only)
```bash
cd frontend
npm install
npm run dev
```
Visit http://localhost:3000 - **fully functional with mock data!**

### Full Stack
See [QUICKSTART.md](./QUICKSTART.md) for complete setup instructions.

## 📁 Project Structure

```
evolving-agents-hack-2025/
├── frontend/              # Next.js dashboard
│   ├── app/              # Pages and layouts
│   ├── components/       # React components
│   ├── lib/              # API client and mock data
│   └── types/            # TypeScript definitions
├── backend/              # FastAPI server (template)
│   ├── main.py           # API endpoints
│   └── requirements.txt  # Python dependencies
├── DEPLOYMENT.md         # Vercel + Render deployment guide
├── QUICKSTART.md         # Development setup
└── README.md             # This file
```

## 🎨 Screenshots

### Evolution Trajectory
Interactive chart showing how each writer's scores evolve across rounds with hover tooltips and click-to-explore functionality.

### Writer Detail Panel
Deep dive into any writer's complete story history with round-by-round breakdowns, score trends, and reader feedback.

### Finalists & Export
Top 3 stories showcased with one-click export to video-ready beat sheets (JSON or text format).

## 🛠️ Tech Stack

**Frontend**
- [Next.js 14](https://nextjs.org/) - React framework
- [TypeScript](https://www.typescriptlang.org/) - Type safety
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [Recharts](https://recharts.org/) - Data visualization

**Backend** (Template)
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [Anthropic Claude](https://www.anthropic.com/) - AI writer agents
- [Pydantic](https://pydantic.dev/) - Data validation

**Deployment**
- [Vercel](https://vercel.com/) - Frontend hosting
- [Render](https://render.com/) - Backend hosting

## 📦 Deployment

### Frontend → Vercel
```bash
cd frontend
vercel --prod
```

### Backend → Render
1. Push code to GitHub
2. Create new Web Service on Render
3. Point to `/backend` directory
4. Add environment variables
5. Deploy!

**Full instructions**: See [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🔧 Development

### Prerequisites
- Node.js 18+
- Python 3.11+ (for backend)
- npm or yarn

### Local Development
```bash
# Frontend (with mock data)
cd frontend
npm install
npm run dev

# Backend (optional)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Environment Variables

**Frontend** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_USE_MOCK=true  # Force mock data
```

**Backend** (`.env`):
```bash
PORT=8000
ANTHROPIC_API_KEY=your_key_here
FRONTEND_URL=http://localhost:3000
```

## 🎯 Roadmap

### ✅ P0 - MVP (Complete)
- [x] Frontend dashboard with visualization
- [x] Writer detail panels
- [x] Finalists section
- [x] Export to video modal
- [x] Mock data system
- [x] Deployment setup

### 🔄 P1 - Backend Integration
- [ ] Implement writer agents
- [ ] Implement reader agents
- [ ] Evolution engine
- [ ] Real-time API integration
- [ ] LLM-powered beat sheet generation

### 🚀 P2 - Polish & Extensions
- [ ] Human judging system with voting
- [ ] Animation and micro-interactions
- [ ] Direct video model integration
- [ ] Multi-round tournament mode

## 🤝 Contributing

This is a hackathon project! Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Anthropic for Claude API
- Vercel for hosting
- Render for backend hosting
- The entire evolving agents hackathon team

## 📞 Contact

For questions or feedback about this project, please open an issue on GitHub.

---

**Built with ❤️ for the Evolving Agents Hackathon 2025**
