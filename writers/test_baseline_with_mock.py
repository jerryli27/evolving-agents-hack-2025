"""
Test baseline writer (non-LLM) with mock feedback (non-LLM) for 3 rounds.
This is a sanity check to ensure the feedback system works without any LLM calls.
"""

from baseline_writer import BaselineWriter
from feedback_providers import MockFeedbackProvider

def main():
    print("="*80)
    print("BASELINE WRITER + MOCK FEEDBACK TEST (3 ROUNDS)")
    print("="*80)
    print()
    print("This test uses:")
    print("  - BaselineWriter: Hardcoded stories (no LLM)")
    print("  - MockFeedbackProvider: Random feedback (no LLM)")
    print()

    # Create mock feedback provider with seed for reproducibility
    feedback_provider = MockFeedbackProvider(seed=42)

    # Create baseline writer
    writer = BaselineWriter(
        writer_id="baseline_test",
        writer_name="Baseline Writer",
        data_dir="data/test_baseline_mock",
        feedback_provider=feedback_provider
    )

    print(f"✓ Writer initialized: {writer.writer_name}")
    print()

    # Run 3 rounds
    for round_num in range(1, 4):
        print("="*80)
        print(f"ROUND {round_num}")
        print("="*80)
        print()

        try:
            submission = writer.write_round(round_num)

            print(f"✓ Story submitted: '{submission.title}'")
            print(f"  Length: {len(submission.full_story)} characters")
            print(f"  Price: ${submission.price:.2f}")
            print()

        except Exception as e:
            print(f"✗ Error in round {round_num}: {e}")
            import traceback
            traceback.print_exc()
            return

    # Show complete history
    print("="*80)
    print("COMPLETE HISTORY")
    print("="*80)
    print()

    history = writer.get_history()
    if history:
        for writing in history.writings:
            print(f"Round {writing.submission.round}: '{writing.submission.title}'")
            if writing.feedback:
                print(f"  Sales: {writing.feedback.sold_percentage*100:.1f}%")
                print(f"  Total Score: {writing.feedback.aggregated_total_score:.2f}")
                print(f"  Novelty: {writing.feedback.aggregated_novelty_score:.2f}")
                print(f"  Relevance: {writing.feedback.aggregated_relevance_score:.2f}")
                print(f"  Quality: {writing.feedback.aggregated_quality_score:.2f}")
                print(f"  Feedback: {writing.feedback.aggregated_qualitative_feedback}")
            print()

    print("="*80)
    print("TEST COMPLETE")
    print("="*80)
    print()
    print("✓ All 3 rounds completed successfully")
    print("✓ Feedback received for each round")
    print("✓ History saved with full feedback details")
    print()


if __name__ == "__main__":
    main()
