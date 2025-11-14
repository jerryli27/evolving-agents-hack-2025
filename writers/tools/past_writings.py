"""Tool for accessing past writings."""

import json
from pathlib import Path
from typing import Optional
from models import WriterHistory, PastWriting


class PastWritingsTool:
    """Tool for writers to access their past writings and performance."""

    def __init__(self, data_dir: str = "data/writings"):
        """
        Initialize the tool.

        Args:
            data_dir: Directory where writer histories are stored
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_history_path(self, writer_id: str) -> Path:
        """Get the path to a writer's history file."""
        return self.data_dir / f"{writer_id}.json"

    def get_past_writings(
        self,
        writer_id: str,
        include_other_writers: bool = False,
        max_rounds: Optional[int] = None
    ) -> str:
        """
        Get past writings for a writer.

        Args:
            writer_id: ID of the writer requesting their history
            include_other_writers: Whether to include other writers' works (future feature)
            max_rounds: Maximum number of past rounds to return (None = all)

        Returns:
            Formatted string with past writings and performance
        """
        history = self._load_history(writer_id)

        if not history or not history.writings:
            return "No past writings found. This is your first round!"

        # Filter by max_rounds if specified
        writings = history.writings
        if max_rounds:
            writings = writings[-max_rounds:]

        # Format the response
        output = [f"Past writings for {history.writer_name} (ID: {history.writer_id})\n"]
        output.append("=" * 60)

        for writing in writings:
            output.append(f"\n{writing.performance_summary}")
            output.append("-" * 60)

        # TODO: Add other writers' works if include_other_writers is True
        if include_other_writers:
            output.append("\n[Other writers' works: Feature coming soon]")

        return "\n".join(output)

    def _load_history(self, writer_id: str) -> Optional[WriterHistory]:
        """Load writer history from disk."""
        history_path = self._get_history_path(writer_id)

        if not history_path.exists():
            return None

        with open(history_path, 'r') as f:
            data = json.load(f)
            return WriterHistory(**data)

    def save_history(self, history: WriterHistory):
        """Save writer history to disk."""
        history_path = self._get_history_path(history.writer_id)

        with open(history_path, 'w') as f:
            json.dump(history.model_dump(), f, indent=2, default=str)

    @staticmethod
    def get_tool_definition():
        """Get the tool definition for use with LLM APIs."""
        return {
            "name": "get_past_writings",
            "description": (
                "Access your past story submissions and their performance metrics. "
                "This includes your previous stories, titles, and feedback scores "
                "(sales percentage, novelty, relevance, quality, and qualitative feedback)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "max_rounds": {
                        "type": "integer",
                        "description": "Maximum number of past rounds to retrieve (optional, default is all)",
                        "minimum": 1
                    }
                },
                "required": []
            }
        }
