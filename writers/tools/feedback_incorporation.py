"""Tool for providing feedback incorporation framework to writers."""

from pathlib import Path
from typing import Optional


class FeedbackIncorporationTool:
    """Tool that provides writers with feedback incorporation guidance."""

    def __init__(self, feedback_prompt_file: Optional[str] = None):
        """
        Initialize the tool.

        Args:
            feedback_prompt_file: Path to the markdown file with feedback incorporation framework
        """
        self.feedback_prompt_file = feedback_prompt_file
        self._framework_content = None

        # Load framework content if file is provided
        if self.feedback_prompt_file:
            self._load_framework()

    def _load_framework(self):
        """Load the feedback incorporation framework from file."""
        if not self.feedback_prompt_file:
            return

        framework_path = Path(self.feedback_prompt_file)

        # Try multiple locations for the feedback prompt file
        if not framework_path.exists():
            # Try prepending 'writers/' for when running from root directory
            alt_path = Path('writers') / self.feedback_prompt_file
            if alt_path.exists():
                framework_path = alt_path

        if framework_path.exists():
            with open(framework_path, 'r', encoding='utf-8') as f:
                self._framework_content = f.read()
        else:
            # Silently skip missing feedback prompt files
            self._framework_content = None

    def get_feedback_framework(self) -> str:
        """
        Get the feedback incorporation framework.

        Returns:
            The feedback incorporation framework content as a string
        """
        if not self._framework_content:
            if not self.feedback_prompt_file:
                return (
                    "No feedback incorporation framework configured. "
                    "Consider analyzing your past feedback scores and qualitative comments "
                    "to identify patterns and areas for improvement."
                )
            else:
                return (
                    f"Error: Could not load feedback framework from '{self.feedback_prompt_file}'. "
                    "The file may not exist or may be inaccessible."
                )

        return self._framework_content

    @staticmethod
    def get_tool_definition():
        """Get the tool definition for use with LLM APIs."""
        return {
            "name": "get_feedback_framework",
            "description": (
                "Access a structured framework for understanding and incorporating market feedback. "
                "This tool provides strategic guidance on how to interpret feedback scores "
                "(engagement, conversion, novelty, relevance, quality) and make informed decisions "
                "about revising your writing approach. Use this when you want systematic guidance "
                "on how to respond to feedback patterns."
            ),
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
