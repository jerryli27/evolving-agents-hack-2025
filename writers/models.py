"""Core data models for the LLM writers system."""

from enum import Enum
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    # Future providers can be added here:
    # GEMINI = "gemini"
    # GROK = "grok"
    # DEEPSEEK = "deepseek"


class LLMConfig(BaseModel):
    """Configuration for an LLM provider."""
    model: str
    temperature: float = 0.7
    max_tokens: int = 4096
    # Additional provider-specific config can go here
    extra_params: dict[str, Any] = Field(default_factory=dict)


class WriterConfig(BaseModel):
    """Configuration for a writer agent."""
    writer_id: str
    writer_name: str
    llm_provider: LLMProvider
    llm_config: LLMConfig
    system_prompt: str = ""
    # Optional: Path to a markdown file containing additional prompt instructions
    prompt_file: Optional[str] = None
    # Optional: Path to a markdown file with feedback incorporation framework
    feedback_prompt_file: Optional[str] = None
    # Optional: Enable/disable the feedback incorporation tool
    enable_feedback_tool: bool = True
    # Optional: control which past writings the writer can see
    can_see_other_writers: bool = False


class StorySubmission(BaseModel):
    """Format for submitting a story."""
    writer_name: str
    title: str
    full_story: str
    round: int
    short_summary: str = ''
    price: float = 1.0
    # Metadata
    submitted_at: datetime = Field(default_factory=datetime.now)
    writer_id: str = ""


class ReaderFeedback(BaseModel):
    """Individual reader feedback (TBD - placeholder structure)."""
    reader_id: str = ""
    rating: float = 0.0
    comment: str = ""
    # More fields TBD


class FeedbackResponse(BaseModel):
    """Feedback received after submitting a story."""
    sold_percentage: float = Field(ge=0.0, le=1.0)  # 0.0 - 1.0
    aggregated_total_score: float = Field(ge=0.0, le=1.0)  # 0.0 - 1.0
    aggregated_novelty_score: float = Field(ge=0.0, le=1.0)  # 0.0 - 1.0
    aggregated_relevance_score: float = Field(ge=0.0, le=1.0)  # 0.0 - 1.0
    aggregated_quality_score: float = Field(ge=0.0, le=1.0)  # 0.0 - 1.0
    aggregated_qualitative_feedback: str
    raw_feedback: list[ReaderFeedback] = Field(default_factory=list)


class PastWriting(BaseModel):
    """A past writing with its metadata and feedback."""
    submission: StorySubmission
    feedback: Optional[FeedbackResponse] = None

    @property
    def performance_summary(self) -> str:
        """Get a human-readable summary of performance."""
        if not self.feedback:
            return "No feedback yet"

        fb = self.feedback
        return (
            f"Round {self.submission.round}: '{self.submission.title}'\n"
            f"  Sold: {fb.sold_percentage*100:.1f}%\n"
            f"  Total Score: {fb.aggregated_total_score:.2f}\n"
            f"  Novelty: {fb.aggregated_novelty_score:.2f}\n"
            f"  Relevance: {fb.aggregated_relevance_score:.2f}\n"
            f"  Quality: {fb.aggregated_quality_score:.2f}\n"
            f"  Feedback: {fb.aggregated_qualitative_feedback}"
        )


class WriterHistory(BaseModel):
    """Complete history for a writer."""
    writer_id: str
    writer_name: str
    writings: list[PastWriting] = Field(default_factory=list)

    def add_writing(self, submission: StorySubmission, feedback: Optional[FeedbackResponse] = None):
        """Add a new writing to history."""
        self.writings.append(PastWriting(submission=submission, feedback=feedback))

    def get_round_writing(self, round_num: int) -> Optional[PastWriting]:
        """Get writing for a specific round."""
        for writing in self.writings:
            if writing.submission.round == round_num:
                return writing
        return None
