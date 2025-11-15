"""
Seedance Video Generation Service

Integrates with fal.ai to generate videos using ByteDance's Seedance 1.0 model.
"""

import os
import fal_client
from typing import Dict, Any, Optional
from pydantic import BaseModel


class VideoGenerationRequest(BaseModel):
    """Request model for video generation"""
    prompt: str
    duration: str = "5"  # Duration in seconds (5, 10, etc.)
    resolution: str = "1080p"  # 1080p for Pro, 720p for Lite
    aspect_ratio: str = "9:16"  # Vertical for TikTok/Reels


class VideoGenerationResponse(BaseModel):
    """Response model for video generation"""
    video_url: str
    request_id: str
    status: str
    metadata: Optional[Dict[str, Any]] = None


class SeedanceService:
    """Service for generating videos using Seedance API via fal.ai"""

    def __init__(self):
        """Initialize Seedance service with API credentials"""
        self.api_key = os.getenv("FAL_KEY")
        if not self.api_key:
            raise ValueError("FAL_KEY environment variable is required for Seedance API")

        # Configure fal client
        os.environ["FAL_KEY"] = self.api_key

    def generate_video(
        self,
        prompt: str,
        duration: str = "5",
        resolution: str = "1080p",
        aspect_ratio: str = "9:16",
        use_lite: bool = False
    ) -> VideoGenerationResponse:
        """
        Generate a video using Seedance model

        Args:
            prompt: Text description of the video to generate
            duration: Video duration in seconds (5, 10, etc.)
            resolution: Video resolution (1080p for Pro, 720p for Lite)
            aspect_ratio: Video aspect ratio (e.g., "9:16" for vertical, "16:9" for horizontal)
            use_lite: Use Lite model (faster, cheaper) vs Pro model (higher quality)

        Returns:
            VideoGenerationResponse with video URL and metadata
        """
        try:
            # Select model based on use_lite parameter
            model_id = "fal-ai/bytedance/seedance/v1/lite/text-to-video" if use_lite else "fal-ai/bytedance/seedance/v1/pro/text-to-video"

            # Prepare request arguments
            arguments = {
                "prompt": prompt,
                "duration": duration,
                "resolution": resolution,
                "aspect_ratio": aspect_ratio
            }

            print(f"[SEEDANCE] Generating video with model: {model_id}")
            print(f"[SEEDANCE] Arguments: {arguments}")

            # Submit video generation request
            # Using subscribe for synchronous processing (waits for completion)
            result = fal_client.subscribe(
                model_id,
                arguments=arguments,
                with_logs=True
            )

            print(f"[SEEDANCE] Generation completed: {result}")

            # Extract video URL from result
            video_url = result.get("video", {}).get("url") if isinstance(result.get("video"), dict) else result.get("video")

            if not video_url:
                raise ValueError(f"No video URL in response: {result}")

            return VideoGenerationResponse(
                video_url=video_url,
                request_id=result.get("request_id", "unknown"),
                status="completed",
                metadata={
                    "model": model_id,
                    "duration": duration,
                    "resolution": resolution,
                    "aspect_ratio": aspect_ratio,
                    "prompt": prompt
                }
            )

        except Exception as e:
            print(f"[SEEDANCE] Error generating video: {str(e)}")
            raise

    async def generate_video_async(
        self,
        prompt: str,
        duration: str = "5",
        resolution: str = "1080p",
        aspect_ratio: str = "9:16",
        use_lite: bool = False
    ) -> str:
        """
        Generate a video asynchronously and return a request_id for polling

        Args:
            prompt: Text description of the video to generate
            duration: Video duration in seconds
            resolution: Video resolution
            aspect_ratio: Video aspect ratio
            use_lite: Use Lite model vs Pro model

        Returns:
            request_id for polling the generation status
        """
        try:
            model_id = "fal-ai/bytedance/seedance/v1/lite/text-to-video" if use_lite else "fal-ai/bytedance/seedance/v1/pro/text-to-video"

            arguments = {
                "prompt": prompt,
                "duration": duration,
                "resolution": resolution,
                "aspect_ratio": aspect_ratio
            }

            print(f"[SEEDANCE] Starting async video generation with model: {model_id}")

            # Submit to queue for async processing
            handle = await fal_client.submit_async(
                model_id,
                arguments=arguments
            )

            request_id = handle.request_id
            print(f"[SEEDANCE] Async request submitted: {request_id}")

            return request_id

        except Exception as e:
            print(f"[SEEDANCE] Error submitting async video generation: {str(e)}")
            raise

    async def get_video_status(self, request_id: str) -> Dict[str, Any]:
        """
        Check the status of an async video generation request

        Args:
            request_id: The request ID returned from generate_video_async

        Returns:
            Status information including completion status and video URL if ready
        """
        try:
            status = await fal_client.status_async(request_id)

            print(f"[SEEDANCE] Status for {request_id}: {status}")

            return {
                "request_id": request_id,
                "status": status.get("status", "unknown"),
                "logs": status.get("logs", []),
                "result": status.get("result")
            }

        except Exception as e:
            print(f"[SEEDANCE] Error checking status: {str(e)}")
            raise

    async def get_video_result(self, request_id: str) -> VideoGenerationResponse:
        """
        Get the final result of an async video generation request

        Args:
            request_id: The request ID returned from generate_video_async

        Returns:
            VideoGenerationResponse with video URL and metadata
        """
        try:
            result = await fal_client.result_async(request_id)

            print(f"[SEEDANCE] Result for {request_id}: {result}")

            video_url = result.get("video", {}).get("url") if isinstance(result.get("video"), dict) else result.get("video")

            if not video_url:
                raise ValueError(f"No video URL in response: {result}")

            return VideoGenerationResponse(
                video_url=video_url,
                request_id=request_id,
                status="completed",
                metadata=result
            )

        except Exception as e:
            print(f"[SEEDANCE] Error getting result: {str(e)}")
            raise


# Global service instance
_seedance_service = None


def get_seedance_service() -> SeedanceService:
    """Get or create the global Seedance service instance"""
    global _seedance_service
    if _seedance_service is None:
        _seedance_service = SeedanceService()
    return _seedance_service
