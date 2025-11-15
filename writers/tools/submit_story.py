"""Tool for submitting stories and receiving feedback."""

import random
from typing import Optional
from models import StorySubmission, FeedbackResponse, WriterHistory, PastWriting
from tools.past_writings import PastWritingsTool
from feedback_providers import FeedbackProvider, MockFeedbackProvider


class SubmitStoryTool:
    """Tool for writers to submit their stories and receive feedback."""

    def __init__(self, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None):
        """
        Initialize the tool.

        Args:
            data_dir: Directory where writer histories are stored
            feedback_provider: Feedback provider instance (defaults to MockFeedbackProvider)
        """
        self.past_writings_tool = PastWritingsTool(data_dir)
        self.feedback_provider = feedback_provider if feedback_provider is not None else MockFeedbackProvider()
        self._current_timestep = 0  # Track timestep for memory-enabled providers

    def submit_story(
        self,
        writer_id: str,
        writer_name: str,
        title: str,
        full_story: str,
        round: int,
        short_summary: str = "",
        price: float = 1.0,
        max_words: int = 350,
    ) -> str:
        """
        Submit a story and receive feedback.

        Args:
            writer_id: ID of the writer
            writer_name: Name of the writer
            title: Story title
            full_story: Full story text
            round: Current round number
            short_summary: Short summary of the story
            price: Price to charge for the story
            max_words: Maximum allowed word count (default: 350)

        Returns:
            Formatted feedback string or error message if word limit exceeded
        """
        # Check word count
        word_count = len(full_story.split())
        if word_count > max_words:
            return (
                f"ERROR: Story submission REJECTED!\n"
                f"\n"
                f"Reason: Story exceeds word limit\n"
                f"  Your story: {word_count} words\n"
                f"  Maximum allowed: {max_words} words\n"
                f"  Excess: {word_count - max_words} words\n"
                f"\n"
                f"Please revise your story to be within {max_words} words and resubmit.\n"
                f"Tip: Focus on the most essential elements of your narrative."
            )

        # Create submission
        submission = StorySubmission(
            writer_name=writer_name,
            title=title,
            full_story=full_story,
            round=round,
            short_summary=short_summary,
            price=price,
            writer_id=writer_id,
        )

        # Get feedback from the configured provider
        self._current_timestep += 1
        feedback = self.feedback_provider.get_feedback(
            title=title,
            full_story=full_story,
            short_summary=short_summary,
            price=price,
            timestep=self._current_timestep,
            writer_id=writer_id,
            round_num=round
        )

        # Load or create writer history
        history = self.past_writings_tool._load_history(writer_id)
        if not history:
            history = WriterHistory(writer_id=writer_id, writer_name=writer_name)

        # Add to history
        history.add_writing(submission, feedback)

        # Save updated history
        self.past_writings_tool.save_history(history)

        # Format feedback response
        return self._format_feedback(submission, feedback)

    def _format_feedback(self, submission: StorySubmission, feedback: FeedbackResponse) -> str:
        """Format feedback into a readable string."""
        output = [
            f"Story submitted successfully!",
            f"",
            f"Title: {submission.title}",
            f"Round: {submission.round}",
            f"Price: ${submission.price:.2f}",
            f"",
            f"=== FEEDBACK ===",
            f"",
            f"Sales Performance: {feedback.sold_percentage*100:.1f}% of readers purchased",
            f"",
            f"Quality Scores:",
            f"  Overall:   {feedback.aggregated_total_score:.2f}/1.00",
            f"  Novelty:   {feedback.aggregated_novelty_score:.2f}/1.00",
            f"  Relevance: {feedback.aggregated_relevance_score:.2f}/1.00",
            f"  Quality:   {feedback.aggregated_quality_score:.2f}/1.00",
            f"",
            f"Qualitative Feedback:",
            f"  {feedback.aggregated_qualitative_feedback}",
        ]

        # Only add mock feedback note if using MockFeedbackProvider
        if isinstance(self.feedback_provider, MockFeedbackProvider):
            output.append(f"")
            output.append(f"Note: This is mock feedback. Real reader feedback will be available soon.")

        return "\n".join(output)

    @staticmethod
    def get_tool_definition():
        """Get the tool definition for use with LLM APIs."""
        return {
            "name": "submit_story",
            "description": (
                "Submit your completed story for the current round. IMPORTANT: Stories must be 350 words or fewer. "
                "Submissions exceeding this limit will be REJECTED. You will receive feedback "
                "including sales percentage, quality scores (novelty, relevance, quality), and "
                "qualitative feedback from readers. Use this when you have finished writing your story."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of your story"
                    },
                    "full_story": {
                        "type": "string",
                        "description": "The complete story text (must be 350 words or fewer)"
                    },
                    "short_summary": {
                        "type": "string",
                        "description": "A brief summary of your story (optional)"
                    },
                    "price": {
                        "type": "number",
                        "description": "Price to charge for the story in dollars (default: 1.0)",
                        "minimum": 0.0
                    }
                },
                "required": ["title", "full_story"]
            }
        }
