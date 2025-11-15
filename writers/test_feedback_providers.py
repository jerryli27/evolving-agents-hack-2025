"""
Test script to verify both feedback providers work correctly.
"""

import os
from dotenv import load_dotenv
from writer_agent import WriterAgent
from feedback_providers import MockFeedbackProvider, ReaderMarketFeedbackProvider

load_dotenv()


def test_mock_provider():
    """Test the mock feedback provider."""
    print("="*80)
    print("TEST 1: MOCK FEEDBACK PROVIDER")
    print("="*80)
    print()

    try:
        # Create mock provider with seed for reproducibility
        feedback_provider = MockFeedbackProvider(seed=42)

        # Load a writer
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY not found")
            return False

        writer = WriterAgent.from_yaml(
            config_path="config/writer_configs/writer_001.yaml",
            api_key=api_key,
            data_dir="data/test_mock",
            feedback_provider=feedback_provider
        )

        print(f"✓ Writer initialized: {writer.config.writer_name}")
        print(f"✓ Using MockFeedbackProvider")
        print()

        # Run one round
        print("Running Round 1...")
        submission = writer.write_round(round_num=1)

        print()
        print(f"✓ Story submitted: '{submission.title}'")

        # Verify history was saved
        history = writer.get_history()
        if history and len(history.writings) == 1:
            writing = history.writings[0]
            if writing.feedback:
                print(f"✓ Feedback received:")
                print(f"    Sales: {writing.feedback.sold_percentage*100:.1f}%")
                print(f"    Total Score: {writing.feedback.aggregated_total_score:.2f}")
                print(f"✓ Mock feedback provider works correctly!")
                print()
                return True
            else:
                print("✗ No feedback in history")
                return False
        else:
            print("✗ History not saved correctly")
            return False

    except Exception as e:
        print(f"✗ Error testing mock provider: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_reader_market_provider():
    """Test the ReaderMarket feedback provider."""
    print("="*80)
    print("TEST 2: READERMARKET FEEDBACK PROVIDER")
    print("="*80)
    print()

    try:
        # Initialize ReaderMarket provider
        print("Initializing ReaderMarket...")
        print("(This may take a moment)")
        print()

        feedback_provider = ReaderMarketFeedbackProvider()

        # Load a writer
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY not found")
            return False

        writer = WriterAgent.from_yaml(
            config_path="config/writer_configs/writer_001.yaml",
            api_key=api_key,
            data_dir="data/test_reader_market",
            feedback_provider=feedback_provider
        )

        print(f"✓ Writer initialized: {writer.config.writer_name}")
        print(f"✓ Using ReaderMarketFeedbackProvider")
        print()

        # Run one round
        print("Running Round 1 with real reader agents...")
        submission = writer.write_round(round_num=1)

        print()
        print(f"✓ Story submitted: '{submission.title}'")

        # Verify history was saved
        history = writer.get_history()
        if history and len(history.writings) == 1:
            writing = history.writings[0]
            if writing.feedback:
                print(f"✓ Feedback received from reader agents:")
                print(f"    Sales: {writing.feedback.sold_percentage*100:.1f}%")
                print(f"    Total Score: {writing.feedback.aggregated_total_score:.2f}")
                print(f"    Novelty: {writing.feedback.aggregated_novelty_score:.2f}")
                print(f"    Relevance: {writing.feedback.aggregated_relevance_score:.2f}")
                print(f"    Quality: {writing.feedback.aggregated_quality_score:.2f}")
                print(f"    Individual readers: {len(writing.feedback.raw_feedback)}")
                print(f"✓ ReaderMarket feedback provider works correctly!")
                print()
                return True
            else:
                print("✗ No feedback in history")
                return False
        else:
            print("✗ History not saved correctly")
            return False

    except Exception as e:
        print(f"✗ Error testing ReaderMarket provider: {e}")
        print()
        print("This is expected if:")
        print("  - genagents is not installed")
        print("  - Reader agents are not available")
        print("  - ReaderMarket configuration is incomplete")
        print()
        return False


if __name__ == "__main__":
    print()
    print("TESTING FEEDBACK PROVIDERS")
    print()

    # Test mock provider (should always work)
    mock_result = test_mock_provider()

    print()

    # Test ReaderMarket provider (may not be available)
    print("Note: ReaderMarket test requires genagents setup and may take several minutes")
    print("Skip this test? (y/n): ", end="")

    import sys
    response = input().strip().lower()

    if response != 'y':
        reader_market_result = test_reader_market_provider()
    else:
        print("Skipping ReaderMarket test")
        reader_market_result = None

    print()
    print("="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"MockFeedbackProvider:         {'✓ PASS' if mock_result else '✗ FAIL'}")
    if reader_market_result is not None:
        print(f"ReaderMarketFeedbackProvider: {'✓ PASS' if reader_market_result else '✗ FAIL'}")
    else:
        print(f"ReaderMarketFeedbackProvider: SKIPPED")
    print("="*80)
