"""
End-to-end simulation: Multiple writers, multiple rounds, with ReaderMarket feedback.

This script runs a complete writing competition:
- Multiple writer agents (LLM or baseline writers)
- Multiple rounds of writing (default: 5)
- ReaderMarket feedback (or mock for testing)
- Parallel execution of writers within each round
- Sequential rounds (writers wait for all feedback before next round)

Usage:
    # Full mock (no LLM costs - defaults to 5 baseline writers + mock feedback)
    python end_to_end_v0.1.py --mock

    # Baseline writers + real LLM readers (one-sided mock)
    python end_to_end_v0.1.py --mock-writers

    # Real LLM writers + mock readers (one-sided mock)
    python end_to_end_v0.1.py --mock --llm 4

    # Full real LLMs (writers + readers)
    python end_to_end_v0.1.py --llm 4

    # Mix of baseline and LLM writers with mock feedback
    python end_to_end_v0.1.py --mock --baseline 2 --llm 2
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add writers directory to path
sys.path.insert(0, str(Path(__file__).parent / "writers"))

from writers.orchestrator import WriterOrchestrator
from writers.feedback_providers import MockFeedbackProvider, ReaderMarketFeedbackProvider


def print_banner(text):
    """Print a formatted banner."""
    print("\n" + "="*80)
    print(f" {text}")
    print("="*80 + "\n")


def print_round_summary(round_num, submissions):
    """Print summary of round results."""
    print_banner(f"ROUND {round_num} SUMMARY")

    successful = sum(1 for s in submissions.values() if s is not None)
    print(f"Submissions: {successful}/{len(submissions)}")
    print()

    for writer_id, submission in submissions.items():
        if submission:
            print(f"  {writer_id}: '{submission.title}'")
            print(f"    Length: {len(submission.full_story)} chars")
            print(f"    Price: ${submission.price:.2f}")
        else:
            print(f"  {writer_id}: FAILED")
        print()


def print_final_results(orchestrator, num_rounds):
    """Print final results and standings."""
    print_banner("FINAL RESULTS")

    # Collect all writer histories
    results = []
    for writer_id, writer in orchestrator.writers.items():
        history = writer.get_history()
        if history and history.writings:
            # Calculate averages
            total_sales = sum(w.feedback.sold_percentage for w in history.writings if w.feedback)
            total_score = sum(w.feedback.aggregated_total_score for w in history.writings if w.feedback)
            count = len([w for w in history.writings if w.feedback])

            if count > 0:
                results.append({
                    'writer_id': writer_id,
                    'writer_name': history.writer_name,
                    'rounds': count,
                    'avg_sales': total_sales / count,
                    'avg_score': total_score / count
                })

    # Sort by average sales (descending)
    results.sort(key=lambda x: x['avg_sales'], reverse=True)

    # Print standings
    print(f"{'Rank':<6} {'Writer':<25} {'Avg Sales':<12} {'Avg Score':<12} {'Rounds'}")
    print("-" * 80)

    for i, result in enumerate(results, 1):
        print(f"{i:<6} {result['writer_name']:<25} "
              f"{result['avg_sales']*100:>6.1f}%     "
              f"{result['avg_score']:>6.2f}       "
              f"{result['rounds']}/{num_rounds}")

    print()

    # Print winner
    if results:
        winner = results[0]
        print(f"🏆 WINNER: {winner['writer_name']}")
        print(f"   Average Sales: {winner['avg_sales']*100:.1f}%")
        print(f"   Average Score: {winner['avg_score']:.2f}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Run end-to-end writer competition simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full mock (no LLM costs)
  python end_to_end_v0.1.py --mock

  # Baseline writers + real LLM readers (test reader behavior)
  python end_to_end_v0.1.py --mock-writers --baseline 5

  # Real LLM writers + mock readers (test writer behavior)
  python end_to_end_v0.1.py --mock-readers --llm 4

  # Full real LLMs (writers + readers)
  python end_to_end_v0.1.py --llm 4

  # Custom configuration with specific writers
  python end_to_end_v0.1.py --mock --rounds 3 --writers writer_001.yaml writer_002.yaml

  # Mix baseline and LLM writers
  python end_to_end_v0.1.py --mock --baseline 2 --llm 2
        """
    )

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock feedback instead of ReaderMarket (fast, no LLM costs)"
    )

    parser.add_argument(
        "--mock-writers",
        action="store_true",
        help="Use only baseline (non-LLM) writers (overrides --llm to 0)"
    )

    parser.add_argument(
        "--mock-readers",
        action="store_true",
        help="Use mock feedback instead of real ReaderMarket (same as --mock)"
    )

    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="Number of rounds to run (default: 5)"
    )

    parser.add_argument(
        "--baseline",
        type=int,
        default=0,
        help="Number of baseline (non-LLM) writers to include (default: 0)"
    )

    parser.add_argument(
        "--llm",
        type=int,
        default=4,
        help="Number of LLM writers to include (default: 4)"
    )

    parser.add_argument(
        "--writers",
        nargs="+",
        help="Specific writer config files to use (overrides --llm)"
    )

    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Run writers sequentially instead of in parallel"
    )

    parser.add_argument(
        "--data-dir",
        default="data/end_to_end_v0.1",
        help="Data directory for this run (default: data/end_to_end_v0.1)"
    )

    args = parser.parse_args()

    # Handle mock flags
    use_mock_readers = args.mock or args.mock_readers
    use_mock_writers = args.mock_writers or args.mock

    # If --mock or --mock-writers is set, override to use only baseline writers
    # unless user explicitly requested LLM writers with --llm
    if use_mock_writers:
        # Check if user explicitly set --llm (not just using default)
        llm_explicitly_set = '--llm' in sys.argv
        if not llm_explicitly_set:
            # Default to baseline writers only for full mock mode
            if args.baseline == 0:
                args.baseline = 5  # Default to 5 baseline writers
            args.llm = 0  # No LLM writers

    # Load environment
    load_dotenv()

    # Determine writer and reader types for display
    # Check actual writer counts after mock flag processing
    if args.baseline > 0 and args.llm > 0:
        writer_type = f"Mixed ({args.baseline} baseline + {args.llm} LLM)"
    elif args.baseline > 0 and args.llm == 0:
        writer_type = f"Baseline (non-LLM, {args.baseline} writers)"
    elif args.llm > 0:
        writer_type = f"LLM-based ({args.llm} writers)"
    else:
        writer_type = "No writers configured"

    reader_type = "Mock (instant, no LLM)" if use_mock_readers else "ReaderMarket (real LLM agents)"

    # Print configuration
    print_banner("END-TO-END SIMULATION v0.1")
    print(f"Configuration:")
    print(f"  Rounds: {args.rounds}")
    print(f"  Writers: {writer_type}")
    print(f"  Readers: {reader_type}")
    print(f"  Execution: {'Sequential' if args.sequential else 'Parallel'}")
    print(f"  Data Directory: {args.data_dir}")
    print()

    # Initialize feedback provider factory
    if use_mock_readers:
        print("Using MockFeedbackProvider (instant, offline)")
        feedback_provider_factory = lambda: MockFeedbackProvider(seed=42)
    else:
        # Check for OPENAI_API_KEY if ReaderMarket is requested
        openai_key = os.environ.get("OPENAI_API_KEY")
        if not openai_key:
            print("⚠ Warning: OPENAI_API_KEY not set, ReaderMarket may fail")
            print("  Set it with: export OPENAI_API_KEY='your-key'")
            print("  Or use mock readers: --mock-readers or --mock")
            print()

        print("Using ReaderMarketFeedbackProvider")
        print("(Each writer will get its own ReaderMarket instance with independent reader agents)")
        try:
            # Test that ReaderMarketFeedbackProvider can be instantiated
            test_provider = ReaderMarketFeedbackProvider()
            print("✓ ReaderMarketFeedbackProvider is available")
            del test_provider  # Clean up test instance
            feedback_provider_factory = ReaderMarketFeedbackProvider
        except Exception as e:
            print(f"✗ Error testing ReaderMarketFeedbackProvider: {e}")
            print("\nFalling back to MockFeedbackProvider")
            print("To use ReaderMarket, ensure:")
            print("  1. genagents is installed")
            print("  2. Reader agents are available")
            print("  3. OPENAI_API_KEY is set")
            feedback_provider_factory = lambda: MockFeedbackProvider(seed=42)

    print()

    # Check for API keys if LLM writers are requested
    if args.llm > 0 and not use_mock_writers:
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")

        if not anthropic_key and not openai_key:
            print("✗ Error: No LLM API keys set but LLM writers requested")
            print("\nAt least one of the following API keys must be set:")
            print("  - ANTHROPIC_API_KEY (for Claude writers)")
            print("  - OPENAI_API_KEY (for GPT writers)")
            print("\nOptions:")
            print("  1. Set API keys:")
            print("     export ANTHROPIC_API_KEY='your-key'")
            print("     export OPENAI_API_KEY='your-key'")
            print("  2. Use baseline writers instead: --baseline 4 --llm 0")
            print("  3. Use mock writers mode: --mock-writers")
            print()
            return
        elif not anthropic_key:
            print("⚠ Warning: ANTHROPIC_API_KEY not set, Claude writers will fail")
        elif not openai_key:
            print("⚠ Warning: OPENAI_API_KEY not set, OpenAI writers will fail")

    # Initialize orchestrator
    orchestrator = WriterOrchestrator(
        config_dir="writers/config/writer_configs",
        baseline_config_dir="writers/config/baseline_writers",
        data_dir=args.data_dir,
        feedback_provider_factory=feedback_provider_factory
    )

    # Load writers
    print("Loading writers...")

    if args.writers:
        # Load specific writers
        for writer_file in args.writers:
            try:
                api_key = os.environ.get("ANTHROPIC_API_KEY")
                orchestrator.load_writer(writer_file, api_key=api_key, is_baseline=False)
                print(f"  ✓ Loaded: {writer_file}")
            except Exception as e:
                print(f"  ✗ Failed to load {writer_file}: {e}")
    else:
        # Load mix of baseline and LLM writers
        from pathlib import Path

        # Load baseline writers
        if args.baseline > 0:
            baseline_dir = Path("writers/config/baseline_writers")
            if baseline_dir.exists():
                baseline_files = list(baseline_dir.glob("*.yaml"))[:args.baseline]
                if not baseline_files:
                    print(f"  ⚠ Warning: No baseline writer configs found in {baseline_dir}")
                for config_file in baseline_files:
                    try:
                        orchestrator.load_writer(config_file.name, is_baseline=True)
                        print(f"  ✓ Loaded baseline: {config_file.name}")
                    except Exception as e:
                        print(f"  ✗ Failed to load {config_file.name}: {e}")
            else:
                print(f"  ✗ Baseline config directory not found: {baseline_dir}")

        # Load LLM writers
        if args.llm > 0:
            llm_dir = Path("writers/config/writer_configs")
            if llm_dir.exists():
                llm_files = list(llm_dir.glob("*.yaml"))[:args.llm]
                if not llm_files:
                    print(f"  ⚠ Warning: No LLM writer configs found in {llm_dir}")
                for config_file in llm_files:
                    try:
                        # Determine which API key to use based on the provider in the config
                        import yaml
                        with open(config_file, 'r') as f:
                            config_data = yaml.safe_load(f)

                        provider = config_data.get('llm_provider', 'anthropic').lower()
                        if provider == 'openai':
                            api_key = os.environ.get("OPENAI_API_KEY")
                        else:  # anthropic or default
                            api_key = os.environ.get("ANTHROPIC_API_KEY")

                        orchestrator.load_writer(config_file.name, api_key=api_key, is_baseline=False)
                        print(f"  ✓ Loaded LLM: {config_file.name} (provider: {provider})")
                    except Exception as e:
                        print(f"  ✗ Failed to load {config_file.name}: {e}")
                        if "authentication" in str(e).lower() or "api_key" in str(e).lower():
                            # Try to determine which API key is needed
                            try:
                                with open(config_file, 'r') as f:
                                    config_data = yaml.safe_load(f)
                                provider = config_data.get('llm_provider', 'anthropic').lower()
                                key_name = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
                                print(f"     Hint: Make sure {key_name} is set in your environment")
                            except:
                                print(f"     Hint: Make sure the appropriate API key is set in your environment")
            else:
                print(f"  ✗ LLM config directory not found: {llm_dir}")

    print()
    orchestrator.list_writers()

    if not orchestrator.writers:
        print("\n" + "="*80)
        print("✗ ERROR: No writers loaded successfully")
        print("="*80)
        print("\nPossible solutions:")
        print("  1. For quick testing, use baseline writers:")
        print("     python end_to_end_v0.1.py --mock-writers")
        print()
        print("  2. For LLM writers, ensure ANTHROPIC_API_KEY is set:")
        print("     export ANTHROPIC_API_KEY='your-key'")
        print("     python end_to_end_v0.1.py --llm 4")
        print()
        print("  3. Check that config files exist:")
        print("     ls writers/config/writer_configs/")
        print("     ls writers/config/baseline_writers/")
        print()
        return

    # Run rounds
    for round_num in range(1, args.rounds + 1):
        print_banner(f"STARTING ROUND {round_num}/{args.rounds}")

        submissions = orchestrator.run_round_for_all(
            round_num=round_num,
            parallel=not args.sequential
        )

        print_round_summary(round_num, submissions)

        # Synchronization point: all writers have completed this round
        # and received feedback before starting the next round
        print(f"✓ All writers synchronized at end of Round {round_num}")
        print(f"  Writers can now access feedback from this round\n")

    # Print final results
    print_final_results(orchestrator, args.rounds)

    print_banner("SIMULATION COMPLETE")
    print(f"Data saved to: {args.data_dir}/")
    print(f"Writer histories: {args.data_dir}/*.json")
    print()


if __name__ == "__main__":
    main()
