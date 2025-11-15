"""
Example demonstrating writers with ReaderMarket feedback.

This example shows how to use the ReaderMarket feedback provider
with writer agents for realistic, LLM-based reader feedback.
"""

import os
from dotenv import load_dotenv
from writer_agent import WriterAgent
from feedback_providers import ReaderMarketFeedbackProvider

# Load environment
load_dotenv()

def main():
    """
    Run a writer with ReaderMarket feedback.

    This demonstrates:
    1. Initializing the ReaderMarket (with memory-enabled reader agents)
    2. Using it with a writer agent
    3. Running multiple rounds to show memory persistence
    """

    print("="*80)
    print("WRITER EXAMPLE WITH READERMARKET FEEDBACK")
    print("="*80)
    print()

    # Initialize the ReaderMarket feedback provider
    # This will initialize generative reader agents
    print("Initializing ReaderMarket feedback provider...")
    print("(This may take a moment as reader agents are loaded)")
    print()

    try:
        feedback_provider = ReaderMarketFeedbackProvider()
    except Exception as e:
        print(f"Error initializing ReaderMarket: {e}")
        print()
        print("Make sure:")
        print("  1. genagents is installed (see genagents/requirements.txt)")
        print("  2. Reader agents are available at genagents/agent_bank/populations/gss_agents/")
        print("  3. readers_parameters.py is configured correctly")
        return

    print()
    print("ReaderMarket initialized!")
    print()

    # Load a writer
    print("Loading writer agent...")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment")
        return

    writer = WriterAgent.from_yaml(
        config_path="config/writer_configs/writer_001.yaml",
        api_key=api_key,
        data_dir="data/test_writings",
        feedback_provider=feedback_provider
    )

    print(f"Writer loaded: {writer.config.writer_name}")
    print()

    # Run Round 1
    print("="*80)
    print("ROUND 1")
    print("="*80)
    print()

    submission1 = writer.write_round(round_num=1)

    print()
    print(f"Story submitted: '{submission1.title}'")
    print()

    # Run Round 2 (readers will remember stories from Round 1)
    print("="*80)
    print("ROUND 2")
    print("="*80)
    print()
    print("Note: Reader agents will remember the story from Round 1 when evaluating Round 2")
    print()

    submission2 = writer.write_round(round_num=2)

    print()
    print(f"Story submitted: '{submission2.title}'")
    print()

    # Show history
    print("="*80)
    print("WRITER HISTORY")
    print("="*80)
    print()

    history = writer.get_history()
    if history:
        for writing in history.writings:
            print(f"Round {writing.submission.round}: '{writing.submission.title}'")
            if writing.feedback:
                print(f"  Sales: {writing.feedback.sold_percentage*100:.1f}%")
                print(f"  Total Score: {writing.feedback.aggregated_total_score:.2f}")
                print(f"  Feedback: {writing.feedback.aggregated_qualitative_feedback[:100]}...")
            print()

    print("="*80)
    print("Example complete!")
    print()
    print("Key features demonstrated:")
    print("  ✓ ReaderMarket feedback with generative agents")
    print("  ✓ Reader memory across rounds")
    print("  ✓ Realistic feedback scores based on reader preferences")
    print("  ✓ Qualitative feedback from individual readers")
    print("="*80)


if __name__ == "__main__":
    main()
