"""Example script demonstrating the LLM Writers System."""

import os
from dotenv import load_dotenv
from orchestrator import WriterOrchestrator


def main():
    """Run a simple example with one or more writers."""

    # Load environment variables from .env file
    load_dotenv()

    # Check for API keys
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not anthropic_key and not openai_key:
        print("WARNING: No API keys found in environment variables.")
        print("Please create a .env file with your API keys or set them directly:")
        print("\nOption 1 - Create .env file:")
        print("  ANTHROPIC_API_KEY=your-key-here")
        print("  OPENAI_API_KEY=your-key-here")
        print("\nOption 2 - Export directly:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        print("  export OPENAI_API_KEY='your-key-here'")
        return

    # Initialize orchestrator
    print("\n" + "="*60)
    print("LLM Writers System - Example")
    print("="*60 + "\n")

    orchestrator = WriterOrchestrator(
        config_dir="config/writer_configs",
        data_dir="data/writings"
    )

    # Load all available writers
    print("Loading writers...")
    orchestrator.load_all_writers(api_key=anthropic_key or openai_key)

    # List loaded writers
    orchestrator.list_writers()

    if not orchestrator.writers:
        print("\nNo writers loaded. Please create writer configs in config/writer_configs/")
        return

    # Run Round 1 for all writers
    print("\n" + "="*60)
    print("Starting Round 1")
    print("="*60 + "\n")

    submissions = orchestrator.run_round_for_all(round_num=1)

    # Display results
    print("\n" + "="*60)
    print("Round 1 Results")
    print("="*60 + "\n")

    for writer_id, submission in submissions.items():
        if submission:
            writer = orchestrator.get_writer(writer_id)
            print(f"Writer: {writer.config.writer_name} (ID: {writer_id})")
            print(f"Title: {submission.title}")
            print(f"Price: ${submission.price:.2f}")
            print(f"Story length: {len(submission.full_story)} characters")
            print(f"\nStory excerpt:")
            # Show first 200 characters
            excerpt = submission.full_story[:200]
            if len(submission.full_story) > 200:
                excerpt += "..."
            print(f"  {excerpt}")
            print("\n" + "-"*60 + "\n")

    # Show how to access history
    print("\n" + "="*60)
    print("Accessing Writer History")
    print("="*60 + "\n")

    first_writer_id = list(orchestrator.writers.keys())[0]
    first_writer = orchestrator.get_writer(first_writer_id)
    history = first_writer.get_history()

    if history:
        print(f"History for {history.writer_name}:")
        print(f"Total writings: {len(history.writings)}")
        if history.writings:
            last_writing = history.writings[-1]
            print(f"\nMost recent submission:")
            print(last_writing.performance_summary)

    print("\n" + "="*60)
    print("Example Complete!")
    print("="*60 + "\n")
    print("To run another round, simply call:")
    print("  orchestrator.run_round_for_all(round_num=2)")
    print("\nWriter histories are saved in data/writings/")
    print("Check USAGE.md for more details!")


if __name__ == "__main__":
    main()
