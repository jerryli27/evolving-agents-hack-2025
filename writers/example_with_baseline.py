"""Example demonstrating baseline writers alongside LLM writers."""

import os
from dotenv import load_dotenv
from orchestrator import WriterOrchestrator

# Load environment variables
load_dotenv()

def main():
    print("\n" + "="*70)
    print("Autonomous Writer System Demo - With Baseline Writers")
    print("="*70 + "\n")

    # Initialize orchestrator
    orch = WriterOrchestrator(
        config_dir="config/writer_configs",
        baseline_config_dir="config/baseline_writers",
        data_dir="data/writings"
    )

    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not found. Only baseline writers will be loaded.")

    # Load all writers (LLM + baseline)
    print("Loading writers...")
    orch.load_all_writers(api_key=api_key, load_baselines=True)

    # List loaded writers
    orch.list_writers()

    # Run Round 1 for all writers
    print("\n" + "="*70)
    print("Running Round 1 for all writers...")
    print("="*70 + "\n")

    submissions = orch.run_round_for_all(round_num=1)

    # Summary
    print("\n" + "="*70)
    print("Round 1 Summary")
    print("="*70 + "\n")

    for writer_id, submission in submissions.items():
        if submission:
            writer = orch.get_writer(writer_id)
            writer_type = "Baseline" if hasattr(writer, 'BASELINE_STORIES') else "LLM"
            print(f"[{writer_type:8}] {writer_id:15} - '{submission.title}'")
        else:
            print(f"[FAILED  ] {writer_id:15} - No submission")

    print("\n" + "="*70)
    print("Demo completed!")
    print("="*70 + "\n")

    # Show comparison
    print("Comparison Notes:")
    print("- Baseline writers return instantly (no API calls)")
    print("- LLM writers may take several seconds per round")
    print("- Both types use the same data format and feedback system")
    print("- Baseline stories are based on real fictional works")
    print("\nView writer histories in: data/writings/")
    print("View LLM transcripts in: ignore/transcripts/")


if __name__ == "__main__":
    main()
