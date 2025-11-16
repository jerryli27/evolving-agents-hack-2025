#!/usr/bin/env python3
"""
Test different prompt variations to see which ones lead to better writer behavior.
"""

import os
import sys
from pathlib import Path

# Add writers directory to path
sys.path.insert(0, str(Path(__file__).parent / "writers"))

from writers.writer_agent import WriterAgent
from writers.feedback_providers.mock_provider import MockFeedbackProvider

# Test configurations
TEST_PROMPTS = {
    "test_1_direct_commands": {
        "prompt_file": "prompts/test_1_direct_commands.md",
        "description": "Direct, mandatory commands style"
    },
    "test_2_tool_forcing": {
        "prompt_file": "prompts/test_2_tool_forcing.md",
        "description": "Tool-based workflow emphasis"
    },
    "test_3_metacognitive": {
        "prompt_file": "prompts/test_3_metacognitive.md",
        "description": "Metacognitive 'think before acting' approach"
    },
    "test_4_minimal_explicit": {
        "prompt_file": "prompts/test_4_minimal_explicit.md",
        "description": "Ultra-minimal explicit steps"
    },
    "test_5_framework_driven": {
        "prompt_file": "prompts/test_5_framework_driven.md",
        "description": "References drama framework training"
    },
    "test_6_forced_iteration": {
        "prompt_file": "prompts/test_6_forced_iteration.md",
        "description": "Forces multiple drafts and revisions"
    },
    "chatgpt5_drama_iteration": {
        "prompt_file": "prompts/chatgpt5_drama_ITERATION.md",
        "description": "ChatGPT 5.1 8-step framework + forced iteration"
    },
    "claude_drama_iteration": {
        "prompt_file": "prompts/claude_drama_ITERATION.md",
        "description": "Claude 7-step framework + forced iteration"
    },
    "gpt25pro_drama_iteration": {
        "prompt_file": "prompts/gpt25pro_drama_ITERATION.md",
        "description": "GPT-2.5 Pro 5-step DNA framework + forced iteration"
    }
}

def run_single_test(prompt_name, prompt_config):
    """Run a single test with the given prompt configuration."""
    print(f"\n{'='*80}")
    print(f"Testing: {prompt_name}")
    print(f"Description: {prompt_config['description']}")
    print(f"{'='*80}\n")

    # Create a test config
    config_path = Path(__file__).parent / "writers" / "config" / "writer_configs" / "writer_004.yaml"

    # Load the config and override prompt_file
    import yaml
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)

    config_data['prompt_file'] = prompt_config['prompt_file']
    config_data['writer_id'] = f"test_{prompt_name}"

    # Save temporary config
    temp_config_path = Path(__file__).parent / "writers" / "config" / f"temp_{prompt_name}.yaml"
    with open(temp_config_path, 'w') as f:
        yaml.dump(config_data, f)

    try:
        # Initialize writer
        api_key = os.getenv("ANTHROPIC_API_KEY")
        data_dir = Path(__file__).parent / "data"
        transcript_dir = Path(__file__).parent / "test_transcripts"
        transcript_dir.mkdir(exist_ok=True)

        feedback_provider = MockFeedbackProvider()

        writer = WriterAgent.from_yaml(
            str(temp_config_path),
            api_key=api_key,
            data_dir=str(data_dir),
            feedback_provider=feedback_provider,
            transcript_dir=str(transcript_dir)
        )

        # Run one round
        print(f"Running round 1 for {prompt_name}...")
        story = writer.write_round(round_num=1, save_transcript=True)

        # Analyze the result from iteration log
        print(f"\n--- Results for {prompt_name} ---")
        print(f"Story submitted: {story.title if story else 'None'}")
        print(f"Number of iterations: {len(writer._iteration_log)}")

        # Check if they used get_past_writings
        used_past_writings = False
        used_feedback_framework = False

        for iteration in writer._iteration_log:
            tool_calls = iteration.get('tool_calls', [])
            for tool_call in tool_calls:
                if isinstance(tool_call, dict) and tool_call.get('name') == 'get_past_writings':
                    used_past_writings = True
                elif hasattr(tool_call, 'name') and tool_call.name == 'get_past_writings':
                    used_past_writings = True
                if isinstance(tool_call, dict) and tool_call.get('name') == 'get_feedback_framework':
                    used_feedback_framework = True
                elif hasattr(tool_call, 'name') and tool_call.name == 'get_feedback_framework':
                    used_feedback_framework = True

        print(f"Used get_past_writings: {used_past_writings}")
        print(f"Used get_feedback_framework: {used_feedback_framework}")

        # Show how many words of thinking before submit
        if len(writer._iteration_log) > 0:
            thinking_before_submit = []
            for iteration in writer._iteration_log:
                if iteration.get('tool_calls'):
                    submitted_in_this_iteration = False
                    for tool_call in iteration.get('tool_calls', []):
                        tool_name = tool_call.get('name') if isinstance(tool_call, dict) else getattr(tool_call, 'name', '')
                        if tool_name == 'submit_story':
                            submitted_in_this_iteration = True
                            break
                    if not submitted_in_this_iteration:
                        # No submit in this iteration, count the response
                        response = iteration.get('response_content', '')
                        thinking_before_submit.append(len(response.split()))

            if thinking_before_submit:
                print(f"Words of 'thinking' before submit: {sum(thinking_before_submit)}")
            else:
                print(f"Words of 'thinking' before submit: 0 (submitted immediately)")

        print(f"\nTranscript saved to: {transcript_dir}")

    finally:
        # Cleanup temp config
        if temp_config_path.exists():
            temp_config_path.unlink()

    return {"story": story, "iterations": len(writer._iteration_log)}

def main():
    """Run all test variations."""
    import argparse

    parser = argparse.ArgumentParser(description="Test different prompt variations")
    parser.add_argument("--test", "-t", help="Run specific test only", choices=list(TEST_PROMPTS.keys()))
    parser.add_argument("--all", "-a", action="store_true", help="Run all tests")

    args = parser.parse_args()

    if args.test:
        # Run single test
        prompt_config = TEST_PROMPTS[args.test]
        run_single_test(args.test, prompt_config)
    elif args.all:
        # Run all tests
        results = {}
        for prompt_name, prompt_config in TEST_PROMPTS.items():
            try:
                result = run_single_test(prompt_name, prompt_config)
                results[prompt_name] = result
            except Exception as e:
                print(f"ERROR in {prompt_name}: {e}")
                results[prompt_name] = {"error": str(e)}

        # Summary
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}\n")
        for prompt_name, result in results.items():
            if "error" in result:
                print(f"{prompt_name}: ERROR - {result['error']}")
            else:
                story = result.get('story')
                iterations = result.get('iterations', 0)
                print(f"{prompt_name}: {story.title if story else 'No story'}, {iterations} iterations")
    else:
        # Show available tests
        print("Available tests:")
        for prompt_name, prompt_config in TEST_PROMPTS.items():
            print(f"  {prompt_name}: {prompt_config['description']}")
        print("\nUsage:")
        print("  python test_prompt_variations.py --test <test_name>")
        print("  python test_prompt_variations.py --all")

if __name__ == "__main__":
    main()
