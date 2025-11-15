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

load_dotenv()

app = FastAPI(
    title="Story Evolution Sandbox API",
    description="API for writer agent evolution and story generation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", ""),
    ],
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
