"""
Story Evolution Sandbox - Backend API (FastAPI)
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from services.video_export import VideoExportService, VideoBlueprint
from services.data_loader import get_loader
from services.seedance_service import get_seedance_service, VideoGenerationRequest

load_dotenv()

app = FastAPI(
    title="Story Evolution Sandbox API",
    description="API for writer agent evolution and story generation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now - can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "Story Evolution Sandbox API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/writers")
def get_writers():
    """
    Get all writer agents

    Returns:
        List of writer objects with id, name, description, style_dna, etc.
    """
    try:
        loader = get_loader()
        return loader.load_writers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading writers: {str(e)}")

@app.get("/api/rounds")
def get_rounds():
    """
    Get all rounds data with stories

    Returns:
        List of round objects containing stories with scores and feedback
    """
    try:
        loader = get_loader()
        return loader.load_rounds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading rounds: {str(e)}")

@app.get("/api/finalists")
def get_finalists(n: int = Query(default=3, ge=1, le=10)):
    """
    Get top N finalist stories

    Args:
        n: Number of finalists to return (default: 3, max: 10)

    Returns:
        List of finalist objects with story and writer details
    """
    try:
        loader = get_loader()
        return loader.load_finalists(n=n)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading finalists: {str(e)}")

class VideoExportRequest(BaseModel):
    """Request model for video export"""
    story_id: str
    title: str
    script: str
    target_length_seconds: int = 60
    visual_style: str = "TikTok vertical drama"
    aspect_ratio: str = "9:16"


class ExportFormatRequest(BaseModel):
    """Request model for specific export formats"""
    story_id: str
    title: str
    script: str
    target_length_seconds: int = 60
    visual_style: str = "TikTok vertical drama"
    aspect_ratio: str = "9:16"
    format: str = "runway"  # runway, pika, sora, or blueprint


@app.post("/api/export-video")
async def export_video(request: VideoExportRequest):
    """
    Generate intelligent video blueprint for a story using Claude AI

    Args:
        request: VideoExportRequest with story details

    Returns:
        Video blueprint with AI-generated beat sheet, character analysis, and metadata
    """
    try:
        # Initialize video export service
        service = VideoExportService()

        # Generate comprehensive video blueprint
        blueprint = service.generate_video_blueprint(
            story_id=request.story_id,
            title=request.title,
            script=request.script,
            target_length_seconds=request.target_length_seconds,
            visual_style=request.visual_style,
            aspect_ratio=request.aspect_ratio
        )

        return blueprint.model_dump()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating video blueprint: {str(e)}")


@app.post("/api/export-video/format")
async def export_video_format(request: ExportFormatRequest):
    """
    Export video blueprint in specific format (Runway, Pika, Sora)

    Args:
        request: ExportFormatRequest with story details and desired format

    Returns:
        Formatted export for the specified video generation platform
    """
    try:
        service = VideoExportService()

        # Generate blueprint first
        blueprint = service.generate_video_blueprint(
            story_id=request.story_id,
            title=request.title,
            script=request.script,
            target_length_seconds=request.target_length_seconds,
            visual_style=request.visual_style,
            aspect_ratio=request.aspect_ratio
        )

        # Format for specific platform
        format_lower = request.format.lower()
        if format_lower == "runway":
            return service.export_for_runway(blueprint)
        elif format_lower == "pika":
            return service.export_for_pika(blueprint)
        elif format_lower == "sora":
            return {"prompt": service.export_for_sora(blueprint)}
        elif format_lower == "blueprint":
            return blueprint.model_dump()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown format: {request.format}. Use 'runway', 'pika', 'sora', or 'blueprint'"
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting video: {str(e)}")


# ==================== Seedance Video Generation Endpoints ====================

class SeedanceVideoRequest(BaseModel):
    """Request model for Seedance video generation"""
    story_id: str
    title: str
    script: str
    prompt: Optional[str] = None  # Custom prompt, or auto-generated from script
    duration: str = "5"
    resolution: str = "1080p"
    aspect_ratio: str = "9:16"
    use_lite: bool = False  # Use Lite model (faster) vs Pro model (higher quality)


@app.post("/api/generate-video-seedance")
def generate_video_seedance(request: SeedanceVideoRequest):
    """
    Generate a video using Seedance (ByteDance) AI model

    This endpoint generates videos synchronously - it waits for the video to complete
    before returning. For longer videos, consider using the async endpoint.

    Args:
        request: SeedanceVideoRequest with story details and generation parameters

    Returns:
        Video URL and metadata
    """
    try:
        seedance = get_seedance_service()

        # If no custom prompt provided, use the script as the prompt
        # In production, you might want to use the VideoExportService to create
        # a more structured prompt/beat sheet
        prompt = request.prompt or request.script[:1000]  # Limit to 1000 chars

        print(f"[API] Generating video for story {request.story_id}")
        print(f"[API] Prompt length: {len(prompt)} chars")

        result = seedance.generate_video(
            prompt=prompt,
            duration=request.duration,
            resolution=request.resolution,
            aspect_ratio=request.aspect_ratio,
            use_lite=request.use_lite
        )

        return {
            "video_url": result.video_url,
            "request_id": result.request_id,
            "status": result.status,
            "metadata": result.metadata,
            "story_id": request.story_id,
            "title": request.title
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating video: {str(e)}")


@app.post("/api/generate-video-seedance/async")
async def generate_video_seedance_async(request: SeedanceVideoRequest):
    """
    Start async video generation using Seedance

    This endpoint starts video generation and immediately returns a request_id.
    Use the /status or /result endpoints to check progress and get the final video.

    Args:
        request: SeedanceVideoRequest with story details

    Returns:
        request_id for polling status
    """
    try:
        seedance = get_seedance_service()

        prompt = request.prompt or request.script[:1000]

        print(f"[API] Starting async video generation for story {request.story_id}")

        request_id = await seedance.generate_video_async(
            prompt=prompt,
            duration=request.duration,
            resolution=request.resolution,
            aspect_ratio=request.aspect_ratio,
            use_lite=request.use_lite
        )

        return {
            "request_id": request_id,
            "status": "processing",
            "story_id": request.story_id,
            "title": request.title
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting video generation: {str(e)}")


@app.get("/api/generate-video-seedance/status/{request_id}")
async def get_video_status_seedance(request_id: str):
    """
    Check the status of an async video generation request

    Args:
        request_id: The request ID returned from the async endpoint

    Returns:
        Status information
    """
    try:
        seedance = get_seedance_service()
        status = await seedance.get_video_status(request_id)
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking status: {str(e)}")


@app.get("/api/generate-video-seedance/result/{request_id}")
async def get_video_result_seedance(request_id: str):
    """
    Get the result of an async video generation request

    Args:
        request_id: The request ID returned from the async endpoint

    Returns:
        Video URL and metadata if ready, or error if still processing
    """
    try:
        seedance = get_seedance_service()
        result = await seedance.get_video_result(request_id)

        return {
            "video_url": result.video_url,
            "request_id": result.request_id,
            "status": result.status,
            "metadata": result.metadata
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting result: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
