"""
Test LLM writer with ReaderMarket feedback for 3 rounds.
This uses actual LLMs for both the writer and the reader agents.
"""

import os
from dotenv import load_dotenv
from writer_agent import WriterAgent
from feedback_providers import ReaderMarketFeedbackProvider

load_dotenv()


def main():
    print("="*80)
    print("LLM WRITER + READERMARKET FEEDBACK TEST (3 ROUNDS)")
    print("="*80)
    print()
    print("This test uses:")
    print("  - WriterAgent: LLM-powered writer")
    print("  - ReaderMarketFeedbackProvider: Generative reader agents with memory")
    print()
    print("Note: This will take several minutes as it involves multiple LLM calls")
    print()

    # Initialize ReaderMarket feedback provider
    print("Initializing ReaderMarket...")
    print("(Loading reader agents - this may take a moment)")
    print()

    try:
        feedback_provider = ReaderMarketFeedbackProvider()
    except Exception as e:
        print(f"✗ Error initializing ReaderMarket: {e}")
        print()
        print("Requirements:")
        print("  1. genagents installed (pip install -r genagents/requirements.txt)")
        print("  2. Reader agents at genagents/agent_bank/populations/gss_agents/")
        print("  3. readers_parameters.py configured correctly")
        return

    print("✓ ReaderMarket initialized")
    print()

    # Load writer
    print("Loading LLM writer...")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("✗ Error: ANTHROPIC_API_KEY not found")
        return

    writer = WriterAgent.from_yaml(
        config_path="config/writer_configs/writer_001.yaml",
        api_key=api_key,
        data_dir="data/test_llm_readermarket",
        feedback_provider=feedback_provider
    )

    print(f"✓ Writer loaded: {writer.config.writer_name}")
    print()

    # Run 3 rounds
    for round_num in range(1, 4):
        print("="*80)
        print(f"ROUND {round_num}")
        print("="*80)
        print()

        if round_num > 1:
            print(f"Note: Readers remember stories from previous rounds")
            print()

        try:
            submission = writer.write_round(round_num)

            print()
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
            print(f"  Summary: {writing.submission.short_summary[:80]}...")
            if writing.feedback:
                print(f"  Sales: {writing.feedback.sold_percentage*100:.1f}%")
                print(f"  Total Score: {writing.feedback.aggregated_total_score:.2f}")
                print(f"  Novelty: {writing.feedback.aggregated_novelty_score:.2f}")
                print(f"  Relevance: {writing.feedback.aggregated_relevance_score:.2f}")
                print(f"  Quality: {writing.feedback.aggregated_quality_score:.2f}")
                print(f"  Individual readers: {len(writing.feedback.raw_feedback)}")
                print(f"  Feedback sample: {writing.feedback.aggregated_qualitative_feedback[:100]}...")
            print()

    print("="*80)
    print("TEST COMPLETE")
    print("="*80)
    print()
    print("✓ All 3 rounds completed with real LLMs")
    print("✓ Reader agents provided memory-aware feedback")
    print("✓ Each reader remembered previous stories")
    print()


if __name__ == "__main__":
    main()
