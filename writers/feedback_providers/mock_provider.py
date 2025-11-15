"""Mock feedback provider for offline testing."""

import random
from models import FeedbackResponse, ReaderFeedback
from feedback_providers.base import FeedbackProvider


class MockFeedbackProvider(FeedbackProvider):
    """
    Mock feedback provider that generates random scores.

    Useful for unit testing and offline development without using LLMs.
    """

    def __init__(self, seed: int = None):
        """
        Initialize mock provider.

        Args:
            seed: Random seed for reproducibility (optional)
        """
        if seed is not None:
            random.seed(seed)

    def get_feedback(
        self,
        title: str,
        full_story: str,
        short_summary: str,
        price: float,
        timestep: int,
        writer_id: str,
        round_num: int
    ) -> FeedbackResponse:
        """Generate mock feedback with random scores."""

        # Generate random but somewhat correlated scores
        base_quality = random.uniform(0.3, 0.9)
        noise = 0.15

        return FeedbackResponse(
            sold_percentage=max(0.0, min(1.0, base_quality + random.uniform(-noise, noise))),
            aggregated_total_score=base_quality,
            aggregated_novelty_score=max(0.0, min(1.0, base_quality + random.uniform(-noise, noise))),
            aggregated_relevance_score=max(0.0, min(1.0, base_quality + random.uniform(-noise, noise))),
            aggregated_quality_score=max(0.0, min(1.0, base_quality + random.uniform(-noise, noise))),
            aggregated_qualitative_feedback=self._generate_mock_qualitative_feedback(base_quality),
            raw_feedback=[]  # Empty for mock provider
        )

    def _generate_mock_qualitative_feedback(self, score: float) -> str:
        """Generate mock qualitative feedback based on score."""
        if score > 0.8:
            templates = [
                "Exceptional work! The story is engaging and well-crafted.",
                "Outstanding! Readers loved the unique perspective.",
                "Brilliant storytelling with strong character development.",
            ]
        elif score > 0.6:
            templates = [
                "Good story with solid execution. Some areas could be improved.",
                "Engaging narrative, though pacing could be tightened.",
                "Interesting concept with room for deeper exploration.",
            ]
        else:
            templates = [
                "The concept has potential but needs more development.",
                "Story needs work on character motivation and plot coherence.",
                "Consider revising the narrative structure for better flow.",
            ]

        return random.choice(templates)
