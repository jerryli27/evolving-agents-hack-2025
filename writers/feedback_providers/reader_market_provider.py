"""ReaderMarket-based feedback provider using generative agents."""

import sys
import os
from typing import Optional

# Add parent directory to path to import ReaderMarket
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models import FeedbackResponse, ReaderFeedback
from feedback_providers.base import FeedbackProvider


class ReaderMarketFeedbackProvider(FeedbackProvider):
    """
    Feedback provider that uses ReaderMarket with generative reader agents.

    This provider maintains memory across rounds through the underlying
    GenerativeAgent instances. Each reader agent remembers the stories
    they've read and uses that context in future feedback.
    """

    def __init__(self, reader_market_instance=None):
        """
        Initialize the ReaderMarket feedback provider.

        Args:
            reader_market_instance: Optional pre-initialized ReaderMarket instance.
                                   If None, will create a new instance when first needed.
        """
        self._reader_market = reader_market_instance
        self._initialized = reader_market_instance is not None

    def _ensure_initialized(self):
        """Lazy initialization of ReaderMarket."""
        if not self._initialized:
            try:
                # Change to parent directory for ReaderMarket imports
                import os
                original_cwd = os.getcwd()
                # Go to parent directory if we're in writers/
                if os.path.basename(original_cwd) == 'writers':
                    os.chdir('..')

                try:
                    from ReaderMarket import ReaderMarket
                    print("Initializing ReaderMarket (this may take a moment)...")
                    self._reader_market = ReaderMarket()
                    self._initialized = True
                    print("ReaderMarket initialized successfully.")
                finally:
                    # Always restore original directory
                    os.chdir(original_cwd)

            except Exception as e:
                raise RuntimeError(
                    f"Failed to initialize ReaderMarket: {e}\n"
                    "Make sure genagents is properly installed and reader agents are available."
                )

    def get_feedback(
        self,
        title: str,
        full_story: str,
        short_summary: str,
        price: float,
        timestep: int,
        writer_id: str,
        round_num: int,
        full_story_summary: str = "",
        episode_summary: str = ""
    ) -> FeedbackResponse:
        """
        Get feedback from ReaderMarket generative agents.

        The timestep parameter is important for memory tracking - each reader
        agent remembers stories they've read at specific timesteps and can
        reference them in future feedback.
        """
        self._ensure_initialized()

        # Use the new parameters if provided, otherwise fall back to short_summary for backward compatibility
        _full_story_summary = full_story_summary if full_story_summary else short_summary
        _episode_summary = episode_summary if episode_summary else short_summary

        # Get feedback from ReaderMarket
        aggregated_feedback = self._reader_market.get_reader_feedback(
            title=title,
            full_story_summary=_full_story_summary,
            episode_story=full_story,
            episode_summary=_episode_summary,
            timestep=timestep,
            price=price
        )

        # Convert raw_feedback to ReaderFeedback objects
        raw_feedback = []
        for feedback in aggregated_feedback.get('raw_feedback', []):
            reader_feedback = ReaderFeedback(
                reader_id=feedback['reader_agent'],
                total_score=feedback['total_score'],
                novelty=feedback['novelty'],
                relevance=feedback['relevance'],
                quality=feedback['quality'],
                qualitative_feedback=feedback['qualitative_feedback'],
                prediction_for_next_episode=feedback.get('prediction_for_next_episode', '')
            )
            raw_feedback.append(reader_feedback)

        # Create FeedbackResponse compatible with the existing system
        return FeedbackResponse(
            sold_percentage=aggregated_feedback['sold_percentage'],
            aggregated_total_score=aggregated_feedback['aggregated_total_score'],
            aggregated_novelty_score=aggregated_feedback['aggregated_novelty_score'],
            aggregated_relevance_score=aggregated_feedback['aggregated_relevance_score'],
            aggregated_quality_score=aggregated_feedback['aggregated_quality_score'],
            aggregated_qualitative_feedback=self._format_qualitative_feedback(aggregated_feedback['raw_feedback']),
            aggregated_prediction_for_next_episode=aggregated_feedback.get('aggregated_prediction_for_next_episode', ''),
            raw_feedback=raw_feedback
        )

    def _format_qualitative_feedback(self, raw_feedback_list: list) -> str:
        """
        Format qualitative feedback from multiple readers into a single string.

        Args:
            raw_feedback_list: List of individual feedback dictionaries

        Returns:
            Formatted string summarizing key themes from all readers
        """
        if not raw_feedback_list:
            return "No detailed feedback available."

        # Collect all feedback
        all_feedback = []
        for feedback in raw_feedback_list:
            reader_name = feedback['reader_agent']
            all_feedback.append(f"{reader_name}: {feedback['qualitative_feedback']}")

        # Return first few as a sample, or all if there are only a few
        if len(all_feedback) <= 3:
            return " | ".join(all_feedback)
        else:
            return " | ".join(all_feedback[:3]) + f" (and {len(all_feedback) - 3} more readers)"
