"""Simple orchestrator for managing writer agents."""

from pathlib import Path
from typing import Optional
from writer_agent import WriterAgent
from models import WriterConfig


class WriterOrchestrator:
    """Simple orchestrator for running writer agents."""

    def __init__(self, config_dir: str = "config/writer_configs", data_dir: str = "data/writings"):
        """
        Initialize the orchestrator.

        Args:
            config_dir: Directory containing writer configuration files
            data_dir: Directory for storing writer data
        """
        self.config_dir = Path(config_dir)
        self.data_dir = Path(data_dir)
        self.writers: dict[str, WriterAgent] = {}

    def load_writer(self, config_filename: str, api_key: Optional[str] = None) -> WriterAgent:
        """
        Load a writer from a config file.

        Args:
            config_filename: Name of the config file (e.g., "writer_001.yaml")
            api_key: Optional API key for the LLM provider

        Returns:
            WriterAgent instance
        """
        config_path = self.config_dir / config_filename
        writer = WriterAgent.from_yaml(str(config_path), api_key=api_key, data_dir=str(self.data_dir))
        self.writers[writer.config.writer_id] = writer
        return writer

    def load_all_writers(self, api_key: Optional[str] = None):
        """
        Load all writers from the config directory.

        Args:
            api_key: Optional API key for the LLM provider
        """
        if not self.config_dir.exists():
            print(f"Config directory {self.config_dir} does not exist")
            return

        for config_file in self.config_dir.glob("*.yaml"):
            try:
                self.load_writer(config_file.name, api_key=api_key)
                print(f"Loaded writer from {config_file.name}")
            except Exception as e:
                print(f"Failed to load {config_file.name}: {e}")

    def run_round(self, writer_id: str, round_num: int):
        """
        Run a writing round for a specific writer.

        Args:
            writer_id: ID of the writer
            round_num: Round number to execute

        Returns:
            The submitted story
        """
        if writer_id not in self.writers:
            raise ValueError(f"Writer {writer_id} not loaded")

        writer = self.writers[writer_id]
        print(f"\n{'='*60}")
        print(f"Running Round {round_num} for {writer.config.writer_name} (ID: {writer_id})")
        print(f"{'='*60}\n")

        submission = writer.write_round(round_num)

        print(f"\n{'='*60}")
        print(f"Round {round_num} completed for {writer.config.writer_name}")
        print(f"Submitted: '{submission.title}'")
        print(f"{'='*60}\n")

        return submission

    def run_round_for_all(self, round_num: int):
        """
        Run a writing round for all loaded writers.

        Args:
            round_num: Round number to execute
        """
        if not self.writers:
            print("No writers loaded")
            return

        submissions = {}
        for writer_id in self.writers:
            try:
                submission = self.run_round(writer_id, round_num)
                submissions[writer_id] = submission
            except Exception as e:
                print(f"Error running round for {writer_id}: {e}")
                submissions[writer_id] = None

        return submissions

    def get_writer(self, writer_id: str) -> Optional[WriterAgent]:
        """Get a writer by ID."""
        return self.writers.get(writer_id)

    def list_writers(self):
        """List all loaded writers."""
        if not self.writers:
            print("No writers loaded")
            return

        print(f"\nLoaded Writers ({len(self.writers)}):")
        print("=" * 60)
        for writer_id, writer in self.writers.items():
            config = writer.config
            print(f"  ID: {writer_id}")
            print(f"  Name: {config.writer_name}")
            print(f"  Provider: {config.llm_provider.value}")
            print(f"  Model: {config.llm_config.model}")
            print("-" * 60)
