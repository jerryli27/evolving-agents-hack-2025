# Backend API - Story Evolution Sandbox

This directory contains the backend API for the Story Evolution Sandbox.

## Quick Start

Choose your preferred stack:

### Option 1: Python + FastAPI

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Option 2: Node.js + Express

```bash
npm install
npm run dev
```

## API Endpoints

- `GET /` - Health check
- `GET /api/writers` - Get all writer agents
- `GET /api/rounds` - Get all rounds data
- `GET /api/finalists?n=3` - Get top N finalists
- `POST /api/export-video` - Generate video blueprint (future)

## Environment Variables

Create a `.env` file:

```bash
PORT=8000
ANTHROPIC_API_KEY=your_api_key_here
FRONTEND_URL=http://localhost:3000
```

## Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed instructions on deploying to Render.

## Development

The backend should implement the data models defined in `frontend/types/index.ts`:
- Writer
- Story
- RoundData
- Finalist
- Score
- ReaderFeedback

Currently, the frontend uses mock data from `frontend/lib/mockData.ts`. Replace these with real API calls once the backend is ready.
