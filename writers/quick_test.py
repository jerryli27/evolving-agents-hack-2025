"""
Quick test script for experimenting with different writer configurations.
Allows you to quickly test combinations without creating config files.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Union
from models import WriterConfig, LLMProvider, LLMConfig
from writer_agent import WriterAgent
from baseline_writer import BaselineWriter


# Load environment
load_dotenv()


    # Personality definitions
PERSONALITIES = {
    "chronicler": """You are Elena Martinez, a writer who specializes in drama with historical elements.
Your stories blend real historical events with imaginative character-driven narratives.

When writing:
- Follow the drama writing guide provided to structure your stories
- Draw inspiration from history to create authentic settings and conflicts
- Focus on rich, descriptive language and vivid character development
- Build stories with strong emotional arcs
- Learn from your past performance feedback to refine your craft""",

    "dreamweaver": """You are Maya Chen, a writer who specializes in surreal, imaginative drama.
Your stories explore the boundaries between reality and fantasy, dreams and waking life.
You excel at unexpected emotional depth and thought-provoking themes.

When writing:
- Follow the drama writing guide provided to structure your stories
- Embrace the surreal and unexpected while maintaining emotional truth
- Use metaphor and symbolism to deepen dramatic tension
- Challenge reader expectations with complex character dynamics
- Create stories that linger emotionally in the mind
- Analyze your feedback to understand what resonates with readers""",

    "minimalist": """You are James Park, a writer who believes in the power of brevity and dramatic precision.
Your stories are concise, every word carefully chosen for maximum emotional impact.
You specialize in concentrated drama with short, punchy narratives.

When writing:
- Follow the drama writing guide provided, but keep everything BRIEF
- Use extreme economy of language - aim for the shorter end of word counts
- Make every word count toward the dramatic conflict
- Create impact through implication rather than exposition
- Focus on a single moment of dramatic revelation or transformation
- Study your feedback to refine your minimalist approach""",

    "realist": """You are Sofia Rodriguez, a writer who specializes in authentic, slice-of-life drama.
Your stories capture genuine human experiences with unflinching honesty.
You excel at creating believable characters facing relatable conflicts.

When writing:
- Follow the drama writing guide provided to structure your stories
- Focus on authentic dialogue and realistic character behavior
- Draw from contemporary social issues and everyday struggles
- Avoid melodrama - let truth speak for itself
- Create subtle emotional depth through observation
- Learn from feedback to refine your realistic approach""",

    "experimenter": """You are Alex Taylor, a writer who pushes the boundaries of dramatic storytelling.
Your stories challenge conventions and explore unconventional narrative structures.
You excel at innovative approaches while maintaining emotional resonance.

When writing:
- Follow the drama writing guide provided, but feel free to subvert expectations
- Experiment with structure, perspective, and narrative techniques
- Take creative risks while maintaining dramatic coherence
- Challenge traditional storytelling assumptions
- Balance innovation with emotional accessibility
- Analyze feedback to understand which experiments resonate""",

    "baseline": "baseline"  # Special marker for baseline writers
}


def quick_test(
    personality: str,
    prompt_file: str = None,
    llm_provider: str = "anthropic",
    model: str = "claude-sonnet-4-20250514",
    temperature: float = 0.7,
    round_num: int = 1,
    writer_id: str = "test_writer",
    feedback_prompt_file: str = None,
    enable_feedback_tool: bool = True,
    target_num_rounds: int = 5,
    should_write_sequel: bool = True
) -> Union[WriterAgent, BaselineWriter]:
    """
    Quickly test a writer configuration without creating a YAML file.

    Args:
        personality: Writer personality/style (see PERSONALITIES dict) or "baseline"
        prompt_file: Path to prompt file (e.g., "prompts/claude_drama_prompt.md") - not used for baseline
        llm_provider: "anthropic" or "openai" - not used for baseline
        model: Model name - not used for baseline
        temperature: Temperature for generation - not used for baseline
        round_num: Round number to execute
        writer_id: Unique ID for this test
        feedback_prompt_file: Path to feedback prompt file (e.g., "feedback_prompts/claude_feedback_prompt.md")
        enable_feedback_tool: Whether to enable the feedback incorporation tool
    """

    if personality not in PERSONALITIES:
        raise ValueError(f"Unknown personality: {personality}. Choose from: {list(PERSONALITIES.keys())}")

    # Check if this is a baseline writer
    if personality == "baseline":
        print(f"\n{'='*70}")
        print(f"Testing Configuration:")
        print(f"  Type: Baseline (non-LLM)")
        print(f"  Writer ID: {writer_id}")
        print(f"  Round: {round_num}")
        print(f"{'='*70}\n")

        writer = BaselineWriter(
            writer_id=writer_id,
            writer_name="Baseline Writer",
            data_dir="data/test_writings"
        )
    else:
        # LLM-based writer
        if not prompt_file:
            raise ValueError("prompt_file is required for non-baseline writers")

        # Create configuration
        config = WriterConfig(
            writer_id=writer_id,
            writer_name=personality.title(),
            llm_provider=LLMProvider(llm_provider),
            llm_config=LLMConfig(
                model=model,
                temperature=temperature,
                max_tokens=4096
            ),
            prompt_file=prompt_file,
            system_prompt=PERSONALITIES[personality],
            feedback_prompt_file=feedback_prompt_file,
            enable_feedback_tool=enable_feedback_tool,
            can_see_other_writers=False,
            target_num_rounds=target_num_rounds,
            should_write_sequel=should_write_sequel
        )

        # Get API key
        api_key = None
        if llm_provider == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        elif llm_provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(f"No API key found for {llm_provider}. Set {llm_provider.upper()}_API_KEY in .env")

        # Create and run writer
        print(f"\n{'='*70}")
        print(f"Testing Configuration:")
        print(f"  Type: LLM")
        print(f"  Personality: {personality}")
        print(f"  Prompt File: {prompt_file}")
        print(f"  Feedback Prompt: {feedback_prompt_file if enable_feedback_tool else 'Disabled'}")
        print(f"  LLM: {llm_provider} - {model} (temp={temperature})")
        print(f"  Round: {round_num}")
        if should_write_sequel:
            print(f"  Series: {target_num_rounds}-part sequel series")
        else:
            print(f"  Series: Standalone stories")
        print(f"{'='*70}\n")

        writer = WriterAgent(config, api_key=api_key, data_dir="data/test_writings")

    try:
        submission = writer.write_round(round_num)

        print(f"\n{'='*70}")
        print(f"RESULT:")
        print(f"{'='*70}")
        print(f"Title: {submission.title}")
        print(f"Price: ${submission.price:.2f}")
        print(f"Length: {len(submission.full_story)} characters")
        print(f"\nStory:\n{submission.full_story}")
        print(f"\n{'='*70}\n")

        return submission

    except Exception as e:
        print(f"\nError during writing: {e}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Quick test for writer configurations"
    )
    parser.add_argument(
        "personality",
        choices=["chronicler", "dreamweaver", "minimalist", "realist", "experimenter", "baseline"],
        help="Writer personality (use 'baseline' for non-LLM baseline writer)"
    )
    parser.add_argument(
        "prompt_file",
        nargs="?",
        help="Path to prompt file (e.g., prompts/claude_drama_prompt.md) - not needed for baseline"
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai"],
        default="anthropic",
        help="LLM provider"
    )
    parser.add_argument(
        "--model",
        help="Model name (default: claude-sonnet-4-20250514 for Anthropic, gpt-4o for OpenAI)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature (0.0-1.0)"
    )
    parser.add_argument(
        "--round",
        type=int,
        default=1,
        help="Round number"
    )
    parser.add_argument(
        "--feedback-prompt",
        help="Path to feedback prompt file (e.g., feedback_prompts/claude_feedback_prompt.md)"
    )
    parser.add_argument(
        "--disable-feedback-tool",
        action="store_true",
        help="Disable the feedback incorporation tool"
    )
    parser.add_argument(
        "--target-rounds",
        type=int,
        default=5,
        help="Number of rounds/stories in the series (default: 5)"
    )
    parser.add_argument(
        "--standalone",
        action="store_true",
        help="Write standalone stories instead of sequels"
    )

    args = parser.parse_args()

    # Set default model based on provider
    if args.model is None:
        args.model = "claude-sonnet-4-20250514" if args.provider == "anthropic" else "gpt-4o"

    quick_test(
        personality=args.personality,
        prompt_file=args.prompt_file,
        llm_provider=args.provider,
        model=args.model,
        temperature=args.temperature,
        round_num=args.round,
        feedback_prompt_file=args.feedback_prompt,
        enable_feedback_tool=not args.disable_feedback_tool,
        target_num_rounds=args.target_rounds,
        should_write_sequel=not args.standalone
    )
