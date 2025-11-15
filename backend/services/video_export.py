"""
Video Export Service - Intelligent Beat Sheet Generation
Uses OpenAI GPT-4 to analyze scripts and generate professional video blueprints
"""

import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from pydantic import BaseModel, Field


class VideoBeatSheet(BaseModel):
    """Represents a single beat/scene in the video"""
    scene_number: int
    description: str
    characters: List[str]
    emotion: str
    visual_cues: str
    camera_angle: Optional[str] = None
    duration_seconds: Optional[float] = None


class VideoBlueprint(BaseModel):
    """Complete video blueprint for AI generation"""
    story_id: str
    title: str
    target_length_seconds: int
    visual_style: str
    aspect_ratio: str = "9:16"  # Default to TikTok/Reels
    beat_sheet: List[VideoBeatSheet]
    characters: List[str]
    overall_mood: str
    color_palette: Optional[str] = None
    music_suggestion: Optional[str] = None


class VideoExportService:
    """Service for generating video blueprints from story scripts"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=self.api_key)

    def extract_characters(self, script: str) -> List[str]:
        """Extract character names from script using GPT-4"""
        prompt = f"""Analyze this script and extract all character names. Return ONLY a JSON array of character names, nothing else.

Script:
{script[:2000]}

Return format: ["Character 1", "Character 2", ...]"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )

            response_text = response.choices[0].message.content.strip()
            # Try to parse as JSON
            characters = json.loads(response_text)
            return characters if isinstance(characters, list) else ["Main Character"]
        except Exception as e:
            print(f"Error extracting characters: {e}")
            return ["Main Character"]

    def generate_beat_sheet(
        self,
        script: str,
        title: str,
        target_length: int,
        visual_style: str,
        characters: List[str]
    ) -> List[VideoBeatSheet]:
        """Generate intelligent beat sheet using GPT-4"""

        # Determine number of beats based on video length
        num_beats = max(3, min(8, target_length // 15))

        prompt = f"""You are a professional video editor and cinematographer. Analyze this drama script and create a beat sheet for a {target_length}-second video.

**Script Title:** {title}
**Characters:** {', '.join(characters)}
**Visual Style:** {visual_style}
**Target Video Length:** {target_length} seconds
**Number of Beats:** {num_beats} (key dramatic moments)

**Script:**
{script}

Create a beat sheet with {num_beats} key scenes/moments. For each beat, provide:
1. scene_number (1 to {num_beats})
2. description (concise, 1-2 sentences describing what happens)
3. characters (list of characters in this scene)
4. emotion (primary emotion: joy, tension, sadness, surprise, anger, fear, love, mystery, etc.)
5. visual_cues (specific visual direction: lighting, setting, props, actions)
6. camera_angle (shot type: close-up, medium shot, wide shot, over-shoulder, POV, etc.)
7. duration_seconds (how long this beat should last)

Return ONLY a valid JSON array of beat objects. No markdown, no explanation, just the JSON array.

Example format:
[
  {{
    "scene_number": 1,
    "description": "Opening shot establishes the mood",
    "characters": ["Character A"],
    "emotion": "mystery",
    "visual_cues": "Dark, moody lighting. Rain on window.",
    "camera_angle": "wide shot",
    "duration_seconds": 8
  }}
]"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )

            response_text = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            # Parse JSON
            beat_data = json.loads(response_text)

            # Convert to Pydantic models
            beats = [VideoBeatSheet(**beat) for beat in beat_data]
            return beats

        except Exception as e:
            print(f"Error generating beat sheet: {e}")
            # Fallback to simple beat sheet
            return self._generate_fallback_beats(script, num_beats, characters)

    def _generate_fallback_beats(
        self,
        script: str,
        num_beats: int,
        characters: List[str]
    ) -> List[VideoBeatSheet]:
        """Generate simple beat sheet if AI generation fails"""
        scenes = [s.strip() for s in script.split('\n\n') if s.strip()]
        beats = []

        for i in range(num_beats):
            scene_idx = min(i * len(scenes) // num_beats, len(scenes) - 1)
            scene_text = scenes[scene_idx][:150]

            beats.append(VideoBeatSheet(
                scene_number=i + 1,
                description=scene_text,
                characters=characters[:1] if characters else ["Main Character"],
                emotion="dramatic" if i == num_beats - 1 else "tense",
                visual_cues="Medium shot with natural lighting",
                camera_angle="medium shot",
                duration_seconds=None
            ))

        return beats

    def analyze_mood_and_style(self, script: str, visual_style: str) -> Dict[str, str]:
        """Analyze script to determine overall mood, color palette, and music"""
        prompt = f"""Analyze this script and the requested visual style. Return ONLY a JSON object with these fields:
- overall_mood (one word: dark, romantic, suspenseful, uplifting, melancholic, etc.)
- color_palette (describe the color scheme: "warm oranges and reds", "cool blues and grays", etc.)
- music_suggestion (type of music: "tense piano score", "upbeat indie pop", "ambient electronic", etc.)

Visual Style: {visual_style}

Script:
{script[:1500]}

Return only JSON, no markdown:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.5
            )

            response_text = response.choices[0].message.content.strip()

            # Remove markdown if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            return json.loads(response_text)

        except Exception as e:
            print(f"Error analyzing mood: {e}")
            return {
                "overall_mood": "dramatic",
                "color_palette": "natural tones",
                "music_suggestion": "ambient score"
            }

    def generate_video_blueprint(
        self,
        story_id: str,
        title: str,
        script: str,
        target_length_seconds: int = 60,
        visual_style: str = "TikTok vertical drama",
        aspect_ratio: str = "9:16"
    ) -> VideoBlueprint:
        """Generate complete video blueprint from script"""

        # Extract characters
        characters = self.extract_characters(script)

        # Generate beat sheet
        beat_sheet = self.generate_beat_sheet(
            script=script,
            title=title,
            target_length=target_length_seconds,
            visual_style=visual_style,
            characters=characters
        )

        # Analyze mood and style
        style_data = self.analyze_mood_and_style(script, visual_style)

        # Create blueprint
        blueprint = VideoBlueprint(
            story_id=story_id,
            title=title,
            target_length_seconds=target_length_seconds,
            visual_style=visual_style,
            aspect_ratio=aspect_ratio,
            beat_sheet=beat_sheet,
            characters=characters,
            overall_mood=style_data.get("overall_mood", "dramatic"),
            color_palette=style_data.get("color_palette"),
            music_suggestion=style_data.get("music_suggestion")
        )

        return blueprint

    def export_for_runway(self, blueprint: VideoBlueprint) -> Dict[str, Any]:
        """Format blueprint for Runway Gen-3 API"""
        return {
            "model": "gen3a_turbo",
            "prompt": f"{blueprint.title}. {blueprint.overall_mood} mood. {blueprint.visual_style}.",
            "duration": blueprint.target_length_seconds,
            "aspect_ratio": blueprint.aspect_ratio,
            "scenes": [
                {
                    "prompt": f"{beat.description}. {beat.visual_cues}. {beat.camera_angle}. {beat.emotion} emotion.",
                    "duration": beat.duration_seconds or (blueprint.target_length_seconds / len(blueprint.beat_sheet))
                }
                for beat in blueprint.beat_sheet
            ]
        }

    def export_for_pika(self, blueprint: VideoBlueprint) -> Dict[str, Any]:
        """Format blueprint for Pika API"""
        return {
            "style": blueprint.visual_style,
            "aspect_ratio": blueprint.aspect_ratio,
            "duration": blueprint.target_length_seconds,
            "prompt": f"{blueprint.title}. {blueprint.overall_mood}. {blueprint.color_palette or 'cinematic colors'}.",
            "scenes": [
                f"Scene {beat.scene_number}: {beat.description} ({beat.visual_cues}, {beat.camera_angle})"
                for beat in blueprint.beat_sheet
            ]
        }

    def export_for_sora(self, blueprint: VideoBlueprint) -> str:
        """Format blueprint as text prompt for OpenAI Sora"""
        prompt_parts = [
            f"Title: {blueprint.title}",
            f"Duration: {blueprint.target_length_seconds} seconds",
            f"Style: {blueprint.visual_style}",
            f"Aspect Ratio: {blueprint.aspect_ratio}",
            f"Mood: {blueprint.overall_mood}",
            f"Color Palette: {blueprint.color_palette or 'cinematic'}",
            f"Music: {blueprint.music_suggestion or 'ambient'}",
            "",
            "Scene Breakdown:",
        ]

        for beat in blueprint.beat_sheet:
            duration = beat.duration_seconds or (blueprint.target_length_seconds / len(blueprint.beat_sheet))
            prompt_parts.append(
                f"\nScene {beat.scene_number} ({duration:.1f}s): {beat.description}"
            )
            prompt_parts.append(f"  Characters: {', '.join(beat.characters)}")
            prompt_parts.append(f"  Emotion: {beat.emotion}")
            prompt_parts.append(f"  Visual: {beat.visual_cues}")
            prompt_parts.append(f"  Camera: {beat.camera_angle}")

        return "\n".join(prompt_parts)
