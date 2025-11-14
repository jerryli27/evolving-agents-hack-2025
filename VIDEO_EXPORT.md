# AI-Powered Video Export Feature

Complete documentation for the Story Evolution Sandbox video export pipeline.

## Overview

The video export feature transforms AI-generated story scripts into professional video blueprints using Claude AI. It provides intelligent beat sheet generation, character extraction, mood analysis, and multi-platform export formats.

## Features

### 🎬 Intelligent Beat Sheet Generation
- **AI-Powered Analysis**: Claude analyzes your script and identifies key dramatic moments
- **Scene Breakdown**: Automatically divides stories into 3-8 key beats based on video length
- **Camera Directions**: Provides specific camera angles (close-up, wide shot, POV, etc.)
- **Visual Cues**: Generates detailed visual direction for each scene
- **Timing**: Calculates optimal duration for each beat

### 🎭 Character & Mood Analysis
- **Automatic Character Extraction**: AI identifies all characters from the script
- **Mood Detection**: Determines overall emotional tone (dramatic, romantic, suspenseful, etc.)
- **Color Palette Suggestions**: Recommends color schemes based on story mood
- **Music Suggestions**: Provides music style recommendations

### 📱 Multi-Platform Export
Export your video blueprint in formats optimized for:
- **Blueprint (JSON)**: Complete structured data with all metadata
- **Runway Gen-3**: Formatted for Runway's video generation API
- **Pika Labs**: Scene-based prompts for Pika's platform
- **OpenAI Sora**: Text prompt format for Sora video generation

### ⚙️ Customization Options
- **Duration**: 30s, 60s, 90s, 2min, 3min
- **Visual Style**: 8+ preset styles (TikTok, Cinematic, Film Noir, Anime, Horror, etc.)
- **Aspect Ratio**: 9:16 (TikTok/Reels), 16:9 (YouTube), 1:1 (Square), 4:5 (Instagram)

## Backend Architecture

### Video Export Service
**Location**: `backend/services/video_export.py`

```python
from services.video_export import VideoExportService

# Initialize service
service = VideoExportService(api_key="your-anthropic-api-key")

# Generate complete blueprint
blueprint = service.generate_video_blueprint(
    story_id="story_1",
    title="Your Story Title",
    script="Your full script...",
    target_length_seconds=60,
    visual_style="Cinematic widescreen",
    aspect_ratio="16:9"
)
```

### API Endpoints

#### 1. Generate Video Blueprint
```
POST /api/export-video
```

**Request Body**:
```json
{
  "story_id": "story_1",
  "title": "The Last Goodbye",
  "script": "Full script content here...",
  "target_length_seconds": 60,
  "visual_style": "Cinematic widescreen",
  "aspect_ratio": "16:9"
}
```

**Response**:
```json
{
  "story_id": "story_1",
  "title": "The Last Goodbye",
  "target_length_seconds": 60,
  "visual_style": "Cinematic widescreen",
  "aspect_ratio": "16:9",
  "characters": ["Emma", "David"],
  "overall_mood": "melancholic",
  "color_palette": "cool blues and warm oranges",
  "music_suggestion": "soft piano with strings",
  "beat_sheet": [
    {
      "scene_number": 1,
      "description": "Emma stands at the window, watching rain...",
      "characters": ["Emma"],
      "emotion": "sadness",
      "visual_cues": "Soft window light, rain bokeh in background",
      "camera_angle": "medium close-up",
      "duration_seconds": 12
    }
  ]
}
```

#### 2. Export to Specific Format
```
POST /api/export-video/format
```

**Request Body**:
```json
{
  "story_id": "story_1",
  "title": "The Last Goodbye",
  "script": "Full script...",
  "target_length_seconds": 60,
  "visual_style": "Cinematic widescreen",
  "aspect_ratio": "16:9",
  "format": "runway"
}
```

**Supported Formats**: `runway`, `pika`, `sora`, `blueprint`

## Frontend Implementation

### Using the Export Modal

```tsx
import ExportVideoModal from '@/components/ExportVideoModal';

// In your component
const [showExport, setShowExport] = useState(false);
const [selectedFinalist, setSelectedFinalist] = useState<Finalist | null>(null);

// Open modal
const handleExport = (finalist: Finalist) => {
  setSelectedFinalist(finalist);
  setShowExport(true);
};

// Render modal
{showExport && selectedFinalist && (
  <ExportVideoModal
    finalist={selectedFinalist}
    onClose={() => setShowExport(false)}
  />
)}
```

### API Functions

```typescript
import { generateVideoBlueprint, exportVideoFormat } from '@/lib/api';

// Generate blueprint
const blueprint = await generateVideoBlueprint({
  story_id: "story_1",
  title: "Your Story",
  script: "Full script...",
  target_length_seconds: 60,
  visual_style: "TikTok vertical drama",
  aspect_ratio: "9:16"
});

// Export specific format
const runwayExport = await exportVideoFormat({
  story_id: "story_1",
  title: "Your Story",
  script: "Full script...",
  target_length_seconds: 60,
  visual_style: "TikTok vertical drama",
  aspect_ratio: "9:16",
  format: "runway"
});
```

## Environment Setup

### Backend Requirements

1. **Install dependencies**:
```bash
pip install anthropic>=0.39.0
```

2. **Set environment variable**:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or create `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
```

### Frontend Configuration

Set API URL in Vercel or `.env.local`:
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

## Beat Sheet Structure

Each beat in the generated beat sheet contains:

```typescript
{
  scene_number: number;         // Sequential scene number (1, 2, 3...)
  description: string;          // 1-2 sentence description of what happens
  characters: string[];         // Characters present in this scene
  emotion: string;              // Primary emotion (joy, tension, sadness, etc.)
  visual_cues: string;          // Specific visual direction
  camera_angle: string;         // Shot type (close-up, wide shot, etc.)
  duration_seconds: number;     // Recommended duration for this beat
}
```

## Integration with Video Platforms

### Runway Gen-3
The Runway export format provides:
- Model specification (gen3a_turbo)
- Per-scene prompts with visual cues
- Duration for each scene
- Aspect ratio

### Pika Labs
The Pika export includes:
- Style and mood specifications
- Scene descriptions with visual details
- Character and emotion information

### OpenAI Sora
The Sora export generates a comprehensive text prompt:
- Full scene breakdown with timing
- Character and emotion details
- Visual and camera direction
- Music and color palette suggestions

## Example Use Cases

### 1. TikTok Drama Series
```typescript
{
  target_length_seconds: 60,
  visual_style: "TikTok vertical drama",
  aspect_ratio: "9:16"
}
```
→ Generates 4-5 quick beats, optimized for vertical viewing

### 2. YouTube Short Film
```typescript
{
  target_length_seconds: 180,
  visual_style: "Cinematic widescreen",
  aspect_ratio: "16:9"
}
```
→ Generates 7-8 detailed beats with cinematic direction

### 3. Instagram Reel
```typescript
{
  target_length_seconds: 30,
  visual_style: "Romantic soft lighting",
  aspect_ratio: "4:5"
}
```
→ Generates 3-4 quick romantic moments

## AI Prompting Strategy

The service uses carefully crafted prompts to ensure:
- **Consistency**: Same story always generates similar structure
- **Quality**: Professional cinematography terminology
- **Specificity**: Detailed visual and emotional direction
- **Adaptability**: Adjusts to different styles and lengths

## Error Handling

The service includes fallback mechanisms:
1. **Character Extraction Fails**: Defaults to "Main Character"
2. **Beat Sheet Generation Fails**: Falls back to simple scene splitting
3. **Mood Analysis Fails**: Uses generic "dramatic" mood

## Performance

- **Beat Sheet Generation**: 2-5 seconds (depending on script length)
- **Character Extraction**: 1-2 seconds
- **Mood Analysis**: 1-2 seconds
- **Total Time**: ~5-10 seconds for complete blueprint

## Testing

### Local Testing with Mock Data

The frontend automatically uses mock data when `NEXT_PUBLIC_API_URL` is not set:

```typescript
// Mock blueprint will be generated instantly
const blueprint = await generateVideoBlueprint({...});
```

### Testing with Backend

1. Start backend locally:
```bash
cd backend
uvicorn main:app --reload
```

2. Set frontend env:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Test video export feature from UI

## Future Enhancements

Potential improvements:
- [ ] Direct integration with Runway/Pika APIs for automatic generation
- [ ] Real-time preview of video composition
- [ ] Style transfer between different visual aesthetics
- [ ] Multi-language support for international markets
- [ ] Advanced cinematography options (shot list, storyboard export)
- [ ] Audio cue suggestions for sound design

## Troubleshooting

### "ANTHROPIC_API_KEY environment variable is required"
**Solution**: Set the API key in your `.env` file or environment variables

### Beat sheet generation is slow
**Solution**: Normal for first request. Claude API typically responds in 3-5 seconds

### Characters showing as "Main Character"
**Solution**: Ensure character names are clearly defined in the script

### Export buttons not working
**Solution**: Check that blueprint has been generated first (wait for loading to complete)

## Credits

- **AI Model**: Claude Sonnet 4.5 by Anthropic
- **Video Export Architecture**: Story Evolution Sandbox Team
- **Supported Platforms**: Runway, Pika Labs, OpenAI Sora

---

For questions or issues, please open an issue on the GitHub repository.
