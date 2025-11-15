# Seedance Video Generation Setup

This project now includes real AI video generation powered by **Seedance 1.0** from ByteDance, accessed via fal.ai.

## Overview

The Seedance integration allows you to:
- Generate high-quality AI videos (1080p) from story scripts
- Create vertical videos (9:16) perfect for TikTok/Reels or horizontal (16:9) for YouTube
- Choose between Pro model (highest quality) and Lite model (faster, cheaper)
- Download generated videos directly from the UI

## Prerequisites

1. **fal.ai Account**: You need an API key from fal.ai
2. **API Credits**: Seedance video generation consumes API credits

## Setup Instructions

### Step 1: Get a fal.ai API Key

1. Go to [fal.ai](https://fal.ai)
2. Sign up for an account (or log in if you already have one)
3. Navigate to your [Dashboard > API Keys](https://fal.ai/dashboard/keys)
4. Create a new API key
5. Copy the key (it starts with something like `fal_xxx...`)

### Step 2: Configure Backend

1. Navigate to the `backend/` directory
2. Open the `.env` file (or create it from `.env.example`)
3. Add your fal.ai API key:

```bash
FAL_KEY=your_fal_api_key_here
```

4. Save the file

### Step 3: Install Dependencies

The backend already includes `fal-client` in `requirements.txt`. If you haven't installed it yet:

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Run the Backend

```bash
cd backend
python main.py
```

The backend will start on port 8000 (or the PORT specified in your `.env` file).

### Step 5: Run the Frontend

In a separate terminal:

```bash
cd frontend
npm install  # if you haven't already
npm run dev
```

The frontend will start on port 3000.

## Usage

1. Navigate to the frontend (http://localhost:3000)
2. Click on any finalist story
3. Click "Export Video"
4. In the Export Video modal:
   - Configure your video settings (duration, aspect ratio, visual style)
   - Click "🎬 Generate Video with Seedance AI"
   - Wait for the video to generate (typically 30-60 seconds)
   - Preview the video in the player
   - Download the video or generate a new variation

## API Endpoints

### `POST /api/generate-video-seedance`

Synchronous video generation endpoint.

**Request Body:**
```json
{
  "story_id": "string",
  "title": "string",
  "script": "string",
  "prompt": "string (optional)",
  "duration": "5",
  "resolution": "1080p",
  "aspect_ratio": "9:16",
  "use_lite": false
}
```

**Response:**
```json
{
  "video_url": "https://...",
  "request_id": "...",
  "status": "completed",
  "metadata": { ... }
}
```

### `POST /api/generate-video-seedance/async`

Asynchronous video generation (returns request_id immediately).

### `GET /api/generate-video-seedance/status/{request_id}`

Check status of async request.

### `GET /api/generate-video-seedance/result/{request_id}`

Get final result of async request.

## Configuration Options

### Duration
Maps to Seedance duration in seconds:
- 30s → 5s video
- 60s → 10s video
- 90s → 10s video (max)
- 120s → 10s video (max)
- 180s → 10s video (max)

### Resolution
- `1080p` - Pro model (high quality)
- `720p` - Lite model (faster)

### Aspect Ratio
- `9:16` - Vertical (TikTok, Instagram Reels)
- `16:9` - Horizontal (YouTube)
- `1:1` - Square (Instagram Feed)
- `4:5` - Portrait (Instagram)

### Model Selection
- `use_lite: false` - Seedance 1.0 Pro (best quality, slower)
- `use_lite: true` - Seedance 1.0 Lite (faster, cheaper)

## Costs

Video generation costs depend on your fal.ai pricing plan:
- Check [fal.ai pricing](https://fal.ai/pricing) for current rates
- Pro model costs more than Lite model
- Longer videos cost more than shorter videos

## Troubleshooting

### Error: "FAL_KEY environment variable is required"
- Make sure you've added `FAL_KEY` to `backend/.env`
- Restart your backend server after adding the key

### Error: "Video generation failed"
- Check your fal.ai API key is valid
- Verify you have sufficient credits in your fal.ai account
- Check backend console logs for detailed error messages

### Video not playing
- Ensure your browser supports the video format
- Try downloading the video and playing it locally
- Check the browser console for errors

## Production Deployment

### Render (Backend)

1. Go to your Render dashboard
2. Navigate to your backend service
3. Go to **Environment** tab
4. Add a new environment variable:
   - **Key**: `FAL_KEY`
   - **Value**: Your fal.ai API key
5. Click "Save Changes"
6. Render will automatically redeploy

### Vercel (Frontend)

No additional configuration needed for the frontend. The frontend talks to the backend API which handles Seedance integration.

## Architecture

```
Frontend (React)
    ↓
    fetch /api/generate-video-seedance
    ↓
Backend (FastAPI)
    ↓
    SeedanceService (seedance_service.py)
    ↓
    fal_client library
    ↓
    fal.ai API
    ↓
    ByteDance Seedance 1.0 Model
    ↓
    Generated Video URL
```

## Files Changed

### Backend
- `backend/requirements.txt` - Added `fal-client==0.6.2`
- `backend/services/seedance_service.py` - New service for Seedance integration
- `backend/main.py` - Added 4 new endpoints for video generation
- `backend/.env.example` - Added `FAL_KEY` documentation
- `backend/.env` - Added `FAL_KEY` configuration

### Frontend
- `frontend/lib/api.ts` - Added `generateVideoWithSeedance()` function
- `frontend/components/ExportVideoModal.tsx` - Updated to use real Seedance API instead of mock

## Future Enhancements

- [ ] Async video generation with status polling UI
- [ ] Queue multiple videos for batch generation
- [ ] Save generated videos to cloud storage (S3, Cloudinary)
- [ ] Video editing features (trim, add music, effects)
- [ ] Support for image-to-video generation
- [ ] Custom prompt engineering UI for better video quality

## Support

For fal.ai specific issues:
- [fal.ai Documentation](https://docs.fal.ai)
- [fal.ai Discord Community](https://discord.gg/fal-ai)

For Seedance model information:
- [Seedance Model Page](https://fal.ai/models/fal-ai/bytedance/seedance)
- [Seedance Research Paper](https://arxiv.org/html/2506.09113v1)
