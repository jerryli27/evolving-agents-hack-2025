# Video Generation Pipeline Implementation Guide

Complete guide to turning AI-generated scripts into actual videos.

---

## 🎯 Goal

Take a winning story script → Generate a professional short-form video (30-120 seconds) ready for TikTok/YouTube Shorts.

---

## 🎬 Option 1: Runway Gen-3 (Recommended for Hackathon)

### Why Runway?
- ✅ Best API documentation
- ✅ Fast generation (2-5 minutes)
- ✅ High quality cinematic output
- ✅ Text-to-video + image-to-video
- ✅ Good for demos

### Setup

**1. Get API Key**
- Sign up at https://runwayml.com
- Get API key from settings
- $10 credit for new users

**2. Install SDK**
```bash
cd frontend
npm install @runwayml/sdk
```

**3. Set Environment Variable**
```bash
# frontend/.env.local
NEXT_PUBLIC_RUNWAY_API_KEY=your_api_key_here
RUNWAY_API_KEY=your_api_key_here  # For server-side
```

### Implementation

**Create `frontend/lib/videoGeneration.ts`:**

```typescript
import RunwayML from '@runwayml/sdk';

const client = new RunwayML({
  apiKey: process.env.RUNWAY_API_KEY,
});

export interface VideoGenerationJob {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  videoUrl?: string;
  error?: string;
}

export async function generateVideoFromBlueprint(
  blueprint: VideoBlueprint
): Promise<VideoGenerationJob> {
  try {
    // Generate video for each beat in the beat sheet
    const sceneVideos = await Promise.all(
      blueprint.beat_sheet.map(async (beat) => {
        const task = await client.gen3.textToVideo.create({
          model: 'gen3a_turbo',
          promptText: `${beat.description}. ${beat.visual_cues}. ${beat.camera_angle}. ${beat.emotion} mood. ${blueprint.visual_style}`,
          duration: beat.duration_seconds || 5,
          ratio: blueprint.aspect_ratio, // '16:9', '9:16', etc.
        });

        // Poll for completion
        let result = await client.tasks.retrieve(task.id);
        while (result.status === 'PENDING' || result.status === 'RUNNING') {
          await new Promise(resolve => setTimeout(resolve, 2000));
          result = await client.tasks.retrieve(task.id);
        }

        return result.output?.[0];
      })
    );

    // Combine scenes into final video (using Runway's video-to-video)
    const finalVideo = await combineScenes(sceneVideos);

    return {
      id: finalVideo.id,
      status: 'completed',
      progress: 100,
      videoUrl: finalVideo.url,
    };
  } catch (error) {
    console.error('Video generation failed:', error);
    return {
      id: 'error',
      status: 'failed',
      progress: 0,
      error: error.message,
    };
  }
}

async function combineScenes(sceneUrls: string[]): Promise<any> {
  // Use Runway's video concatenation or external service
  // For hackathon, could just return first scene as MVP
  return { id: '123', url: sceneUrls[0] };
}
```

**Update `ExportVideoModal.tsx`:**

```typescript
import { generateVideoFromBlueprint } from '@/lib/videoGeneration';

function ExportVideoModal({ finalist, onClose }) {
  const [videoJob, setVideoJob] = useState<VideoGenerationJob | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerateVideo = async () => {
    setIsGenerating(true);

    // First generate blueprint
    const blueprint = await generateVideoBlueprint({
      story_id: finalist.story.story_id,
      title: finalist.story.title,
      script: finalist.story.full_script,
      target_length_seconds: videoLength,
      visual_style: visualStyle,
      aspect_ratio: aspectRatio,
    });

    // Then generate actual video
    const job = await generateVideoFromBlueprint(blueprint);
    setVideoJob(job);
    setIsGenerating(false);
  };

  return (
    <div>
      {/* ... existing blueprint UI ... */}

      {/* Video Generation Section */}
      <div className="border-t-2 border-black bg-white p-4">
        <button
          onClick={handleGenerateVideo}
          disabled={isGenerating || !blueprint}
          className="w-full py-4 px-6 bg-black text-white border-2 border-black font-bold text-sm uppercase tracking-wide"
        >
          {isGenerating ? (
            <span className="flex items-center justify-center gap-2">
              <LoadingSpinner />
              GENERATING VIDEO... {videoJob?.progress}%
            </span>
          ) : videoJob?.status === 'completed' ? (
            '✓ VIDEO READY - CLICK TO VIEW'
          ) : (
            '🎬 GENERATE VIDEO (COSTS ~$2)'
          )}
        </button>

        {videoJob?.videoUrl && (
          <div className="mt-4">
            <video
              src={videoJob.videoUrl}
              controls
              className="w-full border-2 border-black"
            />
            <a
              href={videoJob.videoUrl}
              download
              className="block mt-2 text-center text-xs uppercase"
            >
              Download Video
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
```

### Pricing
- **Gen-3 Turbo**: ~$0.05/second
- **60-second video**: ~$3
- **Budget accordingly**

---

## 🎨 Option 2: Pika Labs

### Why Pika?
- ✅ Great for stylized content (anime, cartoon)
- ✅ Good motion quality
- ✅ Similar pricing to Runway

### Setup

```bash
npm install pika-ai
```

```typescript
import Pika from 'pika-ai';

const pika = new Pika(process.env.PIKA_API_KEY);

const video = await pika.generate({
  prompt: beatDescription,
  style: visualStyle,
  duration: 3,
  aspectRatio: '9:16',
});
```

---

## 🆓 Option 3: Open Source (Free but Lower Quality)

### Stable Video Diffusion

**Pros:**
- ✅ Free
- ✅ Run locally or on modal.com

**Cons:**
- ❌ Lower quality than Runway/Pika
- ❌ Slower generation
- ❌ Requires GPU

```python
# backend/services/stable_video.py
from diffusers import StableVideoDiffusionPipeline
import torch

pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,
    variant="fp16"
)

def generate_video(prompt: str, image_path: str):
    frames = pipe(
        image=image_path,
        decode_chunk_size=8,
        num_frames=25,
    ).frames[0]

    # Export to video
    export_to_video(frames, "output.mp4", fps=7)
    return "output.mp4"
```

---

## 🎯 MVP Approach (For Demo)

If short on time, do this:

### Step 1: Pre-generate Sample Videos

```bash
# Use Runway to generate 3 sample videos ahead of time
# Save them as:
# - /public/videos/sample-winner-1.mp4
# - /public/videos/sample-winner-2.mp4
# - /public/videos/sample-winner-3.mp4
```

### Step 2: Mock the Generation Flow

```typescript
async function generateVideoFromBlueprint(blueprint: VideoBlueprint) {
  // Show loading for 3 seconds
  await new Promise(resolve => setTimeout(resolve, 3000));

  // Return pre-generated sample
  return {
    id: '123',
    status: 'completed',
    progress: 100,
    videoUrl: '/videos/sample-winner-1.mp4',
  };
}
```

### Step 3: Label It Clearly

```tsx
<div className="text-xs text-black opacity-60 text-center">
  Demo: Showing pre-generated sample. Live generation via Runway Gen-3 available in production.
</div>
```

**Effort:** 30 minutes + cost of generating samples

---

## 🔄 Backend Video Queue (Production)

For production, handle video generation on backend:

```python
# backend/services/video_queue.py
from celery import Celery
import runwayml

celery = Celery('video_tasks', broker='redis://localhost:6379')

@celery.task
def generate_video_async(blueprint_id: str, blueprint_data: dict):
    """Generate video in background queue"""
    client = runwayml.Client(api_key=os.getenv("RUNWAY_API_KEY"))

    # Generate video
    video = client.gen3.text_to_video.create(
        prompt=blueprint_data['beat_sheet'][0]['description'],
        duration=blueprint_data['target_length_seconds'],
    )

    # Save to storage
    video_url = upload_to_s3(video.url)

    # Update database
    update_video_job(blueprint_id, status='completed', url=video_url)

    return video_url


# API endpoint
@app.post("/api/videos/generate")
async def queue_video_generation(blueprint: VideoBlueprint):
    job = generate_video_async.delay(blueprint.story_id, blueprint.model_dump())
    return {"job_id": job.id, "status": "queued"}


@app.get("/api/videos/status/{job_id}")
async def get_video_status(job_id: str):
    job = celery.AsyncResult(job_id)
    return {
        "status": job.status,
        "result": job.result if job.ready() else None
    }
```

---

## 📊 Cost Estimation

For a hackathon with ~100 video generations:

| Service | Per Video | 100 Videos | Notes |
|---------|-----------|------------|-------|
| Runway Gen-3 | $3 | $300 | 60s @ $0.05/s |
| Pika Labs | $2.50 | $250 | Similar pricing |
| Stable Diffusion | Free | Free | Lower quality |
| Pre-generated samples | $10 | $10 | Generate 3-5 samples |

**Recommendation for hackathon:** Pre-generate samples + offer 1-2 live generations for judges

---

## 🎬 Video Export Formats

```typescript
export interface ExportedVideo {
  videoUrl: string;
  thumbnail: string;
  duration: number;
  size: number;
  formats: {
    tiktok: string;    // 9:16, 60s max
    youtube: string;   // 16:9 or 9:16
    instagram: string; // 4:5 or 9:16
  };
}
```

---

## ✅ Checklist

- [ ] Choose video generation service (Runway/Pika/Mock)
- [ ] Get API keys and credits
- [ ] Implement generation function
- [ ] Add to ExportVideoModal UI
- [ ] Test with 1-2 sample blueprints
- [ ] Add progress tracking
- [ ] Handle errors gracefully
- [ ] Add cost warnings
- [ ] Test different aspect ratios
- [ ] Optimize for demo day

---

## 🚀 Next Steps

1. **Quick Win (1 hour):** Pre-generate 3 sample videos, show in UI
2. **Medium (4 hours):** Integrate Runway Gen-3 API for live generation
3. **Advanced (8 hours):** Multi-scene stitching, background queue, progress tracking

Choose based on your timeline! 🎥
