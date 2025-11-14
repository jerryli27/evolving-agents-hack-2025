"""Tool for submitting stories and receiving feedback."""

import random
from typing import Optional
from models import StorySubmission, FeedbackResponse, WriterHistory, PastWriting
from tools.past_writings import PastWritingsTool


class SubmitStoryTool:
    """Tool for writers to submit their stories and receive feedback."""

    def __init__(self, data_dir: str = "data/writings"):
        """
        Initialize the tool.

        Args:
            data_dir: Directory where writer histories are stored
        """
        self.past_writings_tool = PastWritingsTool(data_dir)

    def submit_story(
        self,
        writer_id: str,
        writer_name: str,
        title: str,
        full_story: str,
        round: int,
        short_summary: str = "",
        price: float = 1.0,
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

        Returns:
            Formatted feedback string
        """
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

        # Generate mock feedback (placeholder until real feedback system is implemented)
        feedback = self._generate_mock_feedback()

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

    def _generate_mock_feedback(self) -> FeedbackResponse:
        """
        Generate mock feedback with random scores.

        TODO: Replace this with actual feedback system when implemented.
        """
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
            raw_feedback=[]  # Empty for now
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
            f"",
            f"Note: This is mock feedback. Real reader feedback will be available soon.",
        ]

        return "\n".join(output)

    @staticmethod
    def get_tool_definition():
        """Get the tool definition for use with LLM APIs."""
        return {
            "name": "submit_story",
            "description": (
                "Submit your completed story for the current round. You will receive feedback "
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
                        "description": "The complete story text"
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
