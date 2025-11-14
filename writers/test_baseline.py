"""Test script for baseline writers."""

from baseline_writer import BaselineWriter
from orchestrator import WriterOrchestrator


def test_baseline_writer_direct():
    """Test baseline writer directly."""
    print("\n" + "="*70)
    print("Test 1: Direct BaselineWriter Test")
    print("="*70 + "\n")

    writer = BaselineWriter(
        writer_id="test_baseline",
        writer_name="Test Baseline Writer",
        data_dir="data/test_writings"
    )

    # Test round 1
    print("Testing Round 1...")
    submission = writer.write_round(1)
    print(f"\nTitle: {submission.title}")
    print(f"Price: ${submission.price:.2f}")
    print(f"Summary: {submission.short_summary}")
    print(f"Story length: {len(submission.full_story)} characters")
    print(f"\nFirst 200 chars: {submission.full_story[:200]}...")

    # Test round 5
    print("\n" + "-"*70)
    print("Testing Round 5...")
    submission = writer.write_round(5)
    print(f"\nTitle: {submission.title}")
    print(f"Price: ${submission.price:.2f}")
    print(f"Summary: {submission.short_summary}")

    # Test round > 10 (should return empty template)
    print("\n" + "-"*70)
    print("Testing Round 11 (beyond available stories)...")
    submission = writer.write_round(11)
    print(f"\nTitle: {submission.title}")
    print(f"Price: ${submission.price:.2f}")
    print(f"Story: '{submission.full_story}'")
    print(f"Summary: '{submission.short_summary}'")


def test_baseline_writer_with_orchestrator():
    """Test baseline writer through orchestrator."""
    print("\n" + "="*70)
    print("Test 2: Orchestrator Integration Test")
    print("="*70 + "\n")

    orch = WriterOrchestrator(
        config_dir="config/writer_configs",
        baseline_config_dir="config/baseline_writers",
        data_dir="data/test_writings"
    )

    # Load only baseline writers
    orch.load_all_writers(load_baselines=True)

    # List all writers
    orch.list_writers()

    # Run round 1 for baseline writer
    if "baseline_001" in orch.writers:
        print("\nRunning Round 1 for baseline_001...")
        submission = orch.run_round("baseline_001", 1)
        print(f"Success! Submitted: {submission.title}")

        # Run round 2
        print("\nRunning Round 2 for baseline_001...")
        submission = orch.run_round("baseline_001", 2)
        print(f"Success! Submitted: {submission.title}")
    else:
        print("baseline_001 not loaded!")


if __name__ == "__main__":
    # Run tests
    test_baseline_writer_direct()
    test_baseline_writer_with_orchestrator()

    print("\n" + "="*70)
    print("All tests completed!")
    print("="*70 + "\n")
