"""
Compare multiple writer configurations side-by-side.
Run the same round with different configs and display results for easy comparison.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from quick_test import quick_test
import time


load_dotenv()


def compare_configurations(configs: list[dict], round_num: int = 1, save_results: bool = True):
    """
    Run multiple configurations and compare results.

    Args:
        configs: List of config dicts with keys: personality, prompt_file, provider, temperature
        round_num: Round number to test
        save_results: Whether to save comparison to a file
    """

    results = []

    print(f"\n{'='*80}")
    print(f"COMPARING {len(configs)} CONFIGURATIONS")
    print(f"{'='*80}\n")

    for i, config in enumerate(configs, 1):
        print(f"\n[{i}/{len(configs)}] Testing: {config.get('name', f'Config {i}')}")
        print("-" * 80)

        try:
            # Use unique writer_id for each test
            writer_id = f"compare_{i:03d}"

            # Check if this is a baseline writer
            if config["personality"] == "baseline":
                submission = quick_test(
                    personality="baseline",
                    prompt_file=None,
                    round_num=round_num,
                    writer_id=writer_id
                )
            else:
                # Get model with proper default based on provider
                provider = config.get("provider", "anthropic")
                model = config.get("model")
                if model is None:
                    model = "claude-sonnet-4-20250514" if provider == "anthropic" else "gpt-4o"

                submission = quick_test(
                    personality=config["personality"],
                    prompt_file=config["prompt_file"],
                    llm_provider=provider,
                    model=model,
                    temperature=config.get("temperature", 0.7),
                    round_num=round_num,
                    writer_id=writer_id
                )

            results.append({
                "config": config,
                "submission": submission,
                "success": True,
                "error": None
            })

        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                "config": config,
                "submission": None,
                "success": False,
                "error": str(e)
            })

        # Brief pause between requests
        if i < len(configs):
            time.sleep(2)

    # Display comparison
    print(f"\n\n{'='*80}")
    print("COMPARISON RESULTS")
    print(f"{'='*80}\n")

    for i, result in enumerate(results, 1):
        config = result["config"]
        name = config.get("name", f"Config {i}")

        print(f"\n{'='*80}")
        print(f"[{i}] {name}")
        print(f"{'='*80}")
        print(f"Personality: {config['personality']}")

        if config["personality"] == "baseline":
            print(f"Type: Baseline (non-LLM)")
        else:
            print(f"Prompt: {Path(config['prompt_file']).stem}")
            print(f"Provider: {config.get('provider', 'anthropic')}")
            print(f"Temperature: {config.get('temperature', 0.7)}")

        if result["success"]:
            sub = result["submission"]
            print(f"\nTitle: {sub.title}")
            print(f"Price: ${sub.price:.2f}")
            print(f"Length: {len(sub.full_story)} characters")
            print(f"Words: ~{len(sub.full_story.split())} words")
            print(f"\nStory Preview (first 200 chars):")
            print(f"{sub.full_story[:200]}...")
        else:
            print(f"\nFAILED: {result['error']}")

        print()

    # Save results if requested
    if save_results:
        output_dir = Path("ignore/comparison_results")
        output_dir.mkdir(exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"comparison_{timestamp}.md"

        with open(output_file, 'w') as f:
            f.write("# Writer Configuration Comparison\n\n")
            f.write(f"Round: {round_num}\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for i, result in enumerate(results, 1):
                config = result["config"]
                name = config.get("name", f"Config {i}")

                f.write(f"\n## [{i}] {name}\n\n")
                f.write(f"**Configuration:**\n")
                f.write(f"- Personality: {config['personality']}\n")

                if config["personality"] == "baseline":
                    f.write(f"- Type: Baseline (non-LLM)\n\n")
                else:
                    f.write(f"- Prompt: {Path(config['prompt_file']).stem}\n")
                    f.write(f"- Provider: {config.get('provider', 'anthropic')}\n")
                    f.write(f"- Temperature: {config.get('temperature', 0.7)}\n\n")

                if result["success"]:
                    sub = result["submission"]
                    f.write(f"**Results:**\n")
                    f.write(f"- Title: {sub.title}\n")
                    f.write(f"- Price: ${sub.price:.2f}\n")
                    f.write(f"- Length: {len(sub.full_story)} characters\n")
                    f.write(f"- Words: ~{len(sub.full_story.split())} words\n\n")
                    f.write(f"**Full Story:**\n\n{sub.full_story}\n\n")
                else:
                    f.write(f"**FAILED:** {result['error']}\n\n")

                f.write("---\n\n")

        print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Compare multiple writer configurations"
    )
    parser.add_argument(
        "--configs",
        type=str,
        help="JSON file with configuration list"
    )
    parser.add_argument(
        "--preset",
        choices=["quick", "temperature", "prompts", "providers", "personalities", "baseline_vs_llm"],
        help="Use a preset comparison"
    )
    parser.add_argument(
        "--round",
        type=int,
        default=1,
        help="Round number to test"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to file"
    )

    args = parser.parse_args()

    if args.configs:
        # Load from JSON file
        with open(args.configs) as f:
            configs = json.load(f)

    elif args.preset == "quick":
        # Quick comparison of different personalities with same prompt
        configs = [
            {
                "name": "Chronicler (Historical)",
                "personality": "chronicler",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "Minimalist (Brief)",
                "personality": "minimalist",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "Dreamweaver (Surreal)",
                "personality": "dreamweaver",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            }
        ]

    elif args.preset == "temperature":
        # Compare temperature variations
        configs = [
            {
                "name": "Low Temperature (0.5)",
                "personality": "chronicler",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.5
            },
            {
                "name": "Medium Temperature (0.7)",
                "personality": "chronicler",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "High Temperature (0.9)",
                "personality": "chronicler",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.9
            }
        ]

    elif args.preset == "prompts":
        # Compare different prompts with same personality
        configs = [
            {
                "name": "Claude Prompt",
                "personality": "minimalist",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "ChatGPT Prompt",
                "personality": "minimalist",
                "prompt_file": "prompts/chatgpt5.1_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "GPT2.5 Prompt",
                "personality": "minimalist",
                "prompt_file": "prompts/gpt2.5pro_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            }
        ]

    elif args.preset == "providers":
        # Compare Anthropic vs OpenAI
        configs = [
            {
                "name": "Anthropic Claude",
                "personality": "chronicler",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "OpenAI GPT-4o",
                "personality": "chronicler",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "openai",
                "temperature": 0.7
            }
        ]

    elif args.preset == "personalities":
        # Compare all personalities
        configs = [
            {
                "name": "Chronicler",
                "personality": "chronicler",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "Dreamweaver",
                "personality": "dreamweaver",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "Minimalist",
                "personality": "minimalist",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "Realist",
                "personality": "realist",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "Experimenter",
                "personality": "experimenter",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            }
        ]

    elif args.preset == "baseline_vs_llm":
        # Compare baseline writer vs LLM writers
        configs = [
            {
                "name": "Baseline (Hardcoded)",
                "personality": "baseline",
                "prompt_file": None
            },
            {
                "name": "Chronicler (LLM)",
                "personality": "chronicler",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            },
            {
                "name": "Minimalist (LLM)",
                "personality": "minimalist",
                "prompt_file": "prompts/claude_drama_prompt.md",
                "provider": "anthropic",
                "temperature": 0.7
            }
        ]

    else:
        print("Error: Must specify --configs file or --preset")
        print("\nAvailable presets:")
        print("  quick - Compare 3 personalities")
        print("  temperature - Compare temperature variations")
        print("  prompts - Compare different prompt files")
        print("  providers - Compare Anthropic vs OpenAI")
        print("  personalities - Compare all 5 personalities")
        print("  baseline_vs_llm - Compare baseline vs LLM writers")
        exit(1)

    compare_configurations(configs, round_num=args.round, save_results=not args.no_save)
