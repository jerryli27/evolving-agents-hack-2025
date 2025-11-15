"""Base interface for feedback providers."""

from abc import ABC, abstractmethod
from models import FeedbackResponse


class FeedbackProvider(ABC):
    """Abstract base class for feedback providers."""

    @abstractmethod
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
        """
        Get feedback for a story submission.

        Args:
            title: Story title
            full_story: Complete story text
            short_summary: Brief summary of the story
            price: Price of the story
            timestep: Current timestep (for memory-enabled providers)
            writer_id: ID of the writer
            round_num: Current round number

        Returns:
            FeedbackResponse with scores and qualitative feedback
        """
        pass
