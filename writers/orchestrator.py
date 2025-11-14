"""Simple orchestrator for managing writer agents."""

import yaml
from pathlib import Path
from typing import Optional, Union
from writer_agent import WriterAgent
from baseline_writer import BaselineWriter
from models import WriterConfig


class WriterOrchestrator:
    """Simple orchestrator for running writer agents."""

    def __init__(self, config_dir: str = "config/writer_configs", data_dir: str = "data/writings", baseline_config_dir: str = "config/baseline_writers"):
        """
        Initialize the orchestrator.

        Args:
            config_dir: Directory containing writer configuration files
            data_dir: Directory for storing writer data
            baseline_config_dir: Directory containing baseline writer configuration files
        """
        self.config_dir = Path(config_dir)
        self.baseline_config_dir = Path(baseline_config_dir)
        self.data_dir = Path(data_dir)
        self.writers: dict[str, Union[WriterAgent, BaselineWriter]] = {}

    def load_writer(self, config_filename: str, api_key: Optional[str] = None, is_baseline: bool = False) -> Union[WriterAgent, BaselineWriter]:
        """
        Load a writer from a config file.

        Args:
            config_filename: Name of the config file (e.g., "writer_001.yaml")
            api_key: Optional API key for the LLM provider
            is_baseline: Whether this is a baseline writer (non-LLM)

        Returns:
            WriterAgent or BaselineWriter instance
        """
        if is_baseline:
            config_path = self.baseline_config_dir / config_filename
            writer = BaselineWriter.from_yaml(str(config_path), data_dir=str(self.data_dir))
        else:
            config_path = self.config_dir / config_filename
            writer = WriterAgent.from_yaml(str(config_path), api_key=api_key, data_dir=str(self.data_dir))

        writer_id = writer.writer_id if is_baseline else writer.config.writer_id
        self.writers[writer_id] = writer
        return writer

    def load_all_writers(self, api_key: Optional[str] = None, load_baselines: bool = True):
        """
        Load all writers from the config directories.

        Args:
            api_key: Optional API key for the LLM provider
            load_baselines: Whether to also load baseline writers
        """
        # Load LLM-based writers
        if self.config_dir.exists():
            for config_file in self.config_dir.glob("*.yaml"):
                try:
                    self.load_writer(config_file.name, api_key=api_key, is_baseline=False)
                    print(f"Loaded LLM writer from {config_file.name}")
                except Exception as e:
                    print(f"Failed to load {config_file.name}: {e}")
        else:
            print(f"Config directory {self.config_dir} does not exist")

        # Load baseline writers
        if load_baselines and self.baseline_config_dir.exists():
            for config_file in self.baseline_config_dir.glob("*.yaml"):
                try:
                    self.load_writer(config_file.name, api_key=None, is_baseline=True)
                    print(f"Loaded baseline writer from {config_file.name}")
                except Exception as e:
                    print(f"Failed to load baseline {config_file.name}: {e}")
        elif load_baselines:
            print(f"Baseline config directory {self.baseline_config_dir} does not exist")

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
        writer_name = writer.writer_name if isinstance(writer, BaselineWriter) else writer.config.writer_name
        writer_type = "Baseline" if isinstance(writer, BaselineWriter) else "LLM"

        print(f"\n{'='*60}")
        print(f"Running Round {round_num} for {writer_name} (ID: {writer_id}) [{writer_type}]")
        print(f"{'='*60}\n")

        submission = writer.write_round(round_num)

        print(f"\n{'='*60}")
        print(f"Round {round_num} completed for {writer_name}")
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

    def get_writer(self, writer_id: str) -> Optional[Union[WriterAgent, BaselineWriter]]:
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
            print(f"  ID: {writer_id}")
            if isinstance(writer, BaselineWriter):
                print(f"  Name: {writer.writer_name}")
                print(f"  Type: Baseline (non-LLM)")
                print(f"  Stories: 10 hardcoded submissions")
            else:
                config = writer.config
                print(f"  Name: {config.writer_name}")
                print(f"  Type: LLM-based")
                print(f"  Provider: {config.llm_provider.value}")
                print(f"  Model: {config.llm_config.model}")
            print("-" * 60)
