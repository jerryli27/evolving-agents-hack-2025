"""
Story Evolution Sandbox - Backend API (FastAPI)
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from dotenv import load_dotenv

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
    # TODO: Replace with real data from your writer agent system
    return [
        {
            "writer_id": "writer_1",
            "name": "Melodrama Maven",
            "description": "Specializes in emotional arcs and tearjerker moments",
            "style_dna": "high-emotion, character-driven, romantic tension",
            "total_score": 425,
            "color": "#3B82F6"
        }
    ]

@app.get("/api/rounds")
def get_rounds():
    """
    Get all rounds data with stories

    Returns:
        List of round objects containing stories with scores and feedback
    """
    # TODO: Replace with real rounds data
    return [
        {
            "round": 1,
            "stories": [
                {
                    "story_id": "story_1",
                    "writer_id": "writer_1",
                    "round": 1,
                    "title": "Sample Story",
                    "logline": "A compelling short drama",
                    "excerpt": "Opening scene...",
                    "full_script": "Full script content...",
                    "score": {
                        "composite": 85.0,
                        "reader_alignment": 82.0,
                        "novelty": 88.0,
                        "coherence": 86.0
                    },
                    "reader_feedback": {
                        "summary": "Strong emotional resonance",
                        "tags": ["emotional", "engaging"],
                        "detailed_comments": "Great character development"
                    }
                }
            ]
        }
    ]

@app.get("/api/finalists")
def get_finalists(n: int = Query(default=3, ge=1, le=10)):
    """
    Get top N finalist stories

    Args:
        n: Number of finalists to return (default: 3, max: 10)

    Returns:
        List of finalist objects with story and writer details
    """
    # TODO: Replace with real finalists logic
    return [
        {
            "story": {
                "story_id": "story_winner",
                "writer_id": "writer_1",
                "title": "The Winner",
                "logline": "An incredible story",
                "score": {"composite": 95.0}
            },
            "writer": {
                "writer_id": "writer_1",
                "name": "Champion Writer",
                "color": "#3B82F6"
            },
            "ranking": 1
        }
    ]

@app.post("/api/export-video")
def export_video(story_id: str):
    """
    Generate video blueprint for a story

    Args:
        story_id: ID of the story to export

    Returns:
        Video blueprint with beat sheet and metadata
    """
    # TODO: Implement video export logic
    return {
        "story_id": story_id,
        "title": "Story Title",
        "target_length_seconds": 60,
        "visual_style": "cinematic",
        "beat_sheet": []
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
