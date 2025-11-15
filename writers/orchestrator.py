"""Simple orchestrator for managing writer agents."""

import yaml
from pathlib import Path
from typing import Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from writer_agent import WriterAgent
from baseline_writer import BaselineWriter
from baseline_writer_002 import BaselineWriter002
from baseline_writer_003 import BaselineWriter003
from baseline_writer_004 import BaselineWriter004
from baseline_writer_005 import BaselineWriter005
from models import WriterConfig
from feedback_providers import FeedbackProvider


class WriterOrchestrator:
    """Simple orchestrator for running writer agents."""

    # Map baseline writer IDs to their classes
    BASELINE_WRITER_CLASSES = {
        "baseline_001": BaselineWriter,
        "baseline_002": BaselineWriter002,
        "baseline_003": BaselineWriter003,
        "baseline_004": BaselineWriter004,
        "baseline_005": BaselineWriter005,
    }

    def __init__(self, config_dir: str = "config/writer_configs", data_dir: str = "data/writings", baseline_config_dir: str = "config/baseline_writers", feedback_provider_factory=None):
        """
        Initialize the orchestrator.

        Args:
            config_dir: Directory containing writer configuration files
            data_dir: Directory for storing writer data
            baseline_config_dir: Directory containing baseline writer configuration files
            feedback_provider_factory: Callable that returns a new FeedbackProvider instance for each writer.
                                      Can be a class, function, or lambda. Defaults to MockFeedbackProvider.
        """
        self.config_dir = Path(config_dir)
        self.baseline_config_dir = Path(baseline_config_dir)
        self.data_dir = Path(data_dir)
        self.feedback_provider_factory = feedback_provider_factory
        self.writers: dict[str, Union[WriterAgent, BaselineWriter, BaselineWriter002, BaselineWriter003, BaselineWriter004, BaselineWriter005]] = {}

    def _create_feedback_provider_for_writer(self) -> FeedbackProvider:
        """
        Create a new feedback provider instance for a writer.

        Each writer gets its own feedback provider instance to avoid memory conflicts
        (e.g., ReaderMarket reader agents would otherwise confuse stories from different writers).

        Returns:
            A new feedback provider instance
        """
        if self.feedback_provider_factory is None:
            from feedback_providers import MockFeedbackProvider
            return MockFeedbackProvider()

        # Call the factory to create a new instance
        return self.feedback_provider_factory()

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
        # Create a separate feedback provider instance for each writer to avoid memory conflicts
        # This ensures reader agents don't confuse stories from different writers
        writer_feedback_provider = self._create_feedback_provider_for_writer()

        if is_baseline:
            config_path = self.baseline_config_dir / config_filename

            # Determine which baseline writer class to use based on the config file name
            writer_id = config_filename.replace('.yaml', '')
            writer_class = self.BASELINE_WRITER_CLASSES.get(writer_id, BaselineWriter)

            writer = writer_class.from_yaml(str(config_path), data_dir=str(self.data_dir), feedback_provider=writer_feedback_provider)
        else:
            config_path = self.config_dir / config_filename
            writer = WriterAgent.from_yaml(str(config_path), api_key=api_key, data_dir=str(self.data_dir), feedback_provider=writer_feedback_provider)

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
        # Check if it's any baseline writer class
        is_baseline = isinstance(writer, (BaselineWriter, BaselineWriter002, BaselineWriter003, BaselineWriter004, BaselineWriter005))
        writer_name = writer.writer_name if is_baseline else writer.config.writer_name
        writer_type = "Baseline" if is_baseline else "LLM"

        print(f"\n{'='*60}")
        print(f"Running Round {round_num} for {writer_name} (ID: {writer_id}) [{writer_type}]")
        print(f"{'='*60}\n")

        submission = writer.write_round(round_num)

        print(f"\n{'='*60}")
        print(f"Round {round_num} completed for {writer_name}")
        print(f"Submitted: '{submission.title}'")
        print(f"{'='*60}\n")

        return submission

    def run_round_for_all(self, round_num: int, parallel: bool = True, max_workers: Optional[int] = None):
        """
        Run a writing round for all loaded writers.

        Args:
            round_num: Round number to execute
            parallel: Whether to run writers in parallel (default: True)
            max_workers: Maximum number of parallel workers (default: None = number of CPUs)

        Returns:
            Dictionary mapping writer_id to submission
        """
        if not self.writers:
            print("No writers loaded")
            return {}

        print(f"\n{'='*70}")
        print(f"ROUND {round_num} - Running {len(self.writers)} writers")
        print(f"Mode: {'PARALLEL' if parallel else 'SEQUENTIAL'}")
        print(f"{'='*70}\n")

        if not parallel:
            # Sequential execution (original behavior)
            submissions = {}
            for writer_id in self.writers:
                try:
                    submission = self.run_round(writer_id, round_num)
                    submissions[writer_id] = submission
                except Exception as e:
                    print(f"Error running round for {writer_id}: {e}")
                    submissions[writer_id] = None
            return submissions

        # Parallel execution
        submissions = {}

        def run_writer(writer_id):
            """Helper function to run a single writer."""
            try:
                submission = self.run_round(writer_id, round_num)
                return writer_id, submission, None
            except Exception as e:
                print(f"Error running round for {writer_id}: {e}")
                import traceback
                return writer_id, None, str(e)

        # Execute writers in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all writers
            futures = {executor.submit(run_writer, writer_id): writer_id
                      for writer_id in self.writers}

            # Collect results as they complete
            for future in as_completed(futures):
                writer_id, submission, error = future.result()
                submissions[writer_id] = submission
                if error:
                    print(f"[ERROR] {writer_id}: {error}")

        print(f"\n{'='*70}")
        print(f"ROUND {round_num} COMPLETE")
        print(f"Submissions: {sum(1 for s in submissions.values() if s is not None)}/{len(self.writers)}")
        print(f"{'='*70}\n")

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
            # Check if it's a baseline writer (any of the baseline writer classes)
            is_baseline = isinstance(writer, (BaselineWriter, BaselineWriter002, BaselineWriter003, BaselineWriter004, BaselineWriter005))
            if is_baseline:
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
