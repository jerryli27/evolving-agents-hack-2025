"""
Quick test script for experimenting with different writer configurations.
Allows you to quickly test combinations without creating config files.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from models import WriterConfig, LLMProvider, LLMConfig
from writer_agent import WriterAgent


# Load environment
load_dotenv()


    # Personality definitions
PERSONALITIES = {
    "chronicler": """You are "The Chronicler", a writer who specializes in drama with historical elements.
Your stories blend real historical events with imaginative character-driven narratives.

When writing:
- Follow the drama writing guide provided to structure your stories
- Draw inspiration from history to create authentic settings and conflicts
- Focus on rich, descriptive language and vivid character development
- Build stories with strong emotional arcs
- Learn from your past performance feedback to refine your craft""",

    "dreamweaver": """You are "The Dreamweaver", a writer who specializes in surreal, imaginative drama.
Your stories explore the boundaries between reality and fantasy, dreams and waking life.
You excel at unexpected emotional depth and thought-provoking themes.

When writing:
- Follow the drama writing guide provided to structure your stories
- Embrace the surreal and unexpected while maintaining emotional truth
- Use metaphor and symbolism to deepen dramatic tension
- Challenge reader expectations with complex character dynamics
- Create stories that linger emotionally in the mind
- Analyze your feedback to understand what resonates with readers""",

    "minimalist": """You are "The Minimalist", a writer who believes in the power of brevity and dramatic precision.
Your stories are concise, every word carefully chosen for maximum emotional impact.
You specialize in concentrated drama with short, punchy narratives.

When writing:
- Follow the drama writing guide provided, but keep everything BRIEF
- Use extreme economy of language - aim for the shorter end of word counts
- Make every word count toward the dramatic conflict
- Create impact through implication rather than exposition
- Focus on a single moment of dramatic revelation or transformation
- Study your feedback to refine your minimalist approach""",

    "realist": """You are "The Realist", a writer who specializes in authentic, slice-of-life drama.
Your stories capture genuine human experiences with unflinching honesty.
You excel at creating believable characters facing relatable conflicts.

When writing:
- Follow the drama writing guide provided to structure your stories
- Focus on authentic dialogue and realistic character behavior
- Draw from contemporary social issues and everyday struggles
- Avoid melodrama - let truth speak for itself
- Create subtle emotional depth through observation
- Learn from feedback to refine your realistic approach""",

    "experimenter": """You are "The Experimenter", a writer who pushes the boundaries of dramatic storytelling.
Your stories challenge conventions and explore unconventional narrative structures.
You excel at innovative approaches while maintaining emotional resonance.

When writing:
- Follow the drama writing guide provided, but feel free to subvert expectations
- Experiment with structure, perspective, and narrative techniques
- Take creative risks while maintaining dramatic coherence
- Challenge traditional storytelling assumptions
- Balance innovation with emotional accessibility
- Analyze feedback to understand which experiments resonate"""
}


def quick_test(
    personality: str,
    prompt_file: str,
    llm_provider: str = "anthropic",
    model: str = "claude-sonnet-4-20250514",
    temperature: float = 0.7,
    round_num: int = 1,
    writer_id: str = "test_writer"
):
    """
    Quickly test a writer configuration without creating a YAML file.

    Args:
        personality: Writer personality/style (see PERSONALITIES dict)
        prompt_file: Path to prompt file (e.g., "prompts/claude_drama_prompt.md")
        llm_provider: "anthropic" or "openai"
        model: Model name
        temperature: Temperature for generation
        round_num: Round number to execute
        writer_id: Unique ID for this test
    """

    if personality not in PERSONALITIES:
        raise ValueError(f"Unknown personality: {personality}. Choose from: {list(PERSONALITIES.keys())}")

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
        can_see_other_writers=False
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
    print(f"  Personality: {personality}")
    print(f"  Prompt File: {prompt_file}")
    print(f"  LLM: {llm_provider} - {model} (temp={temperature})")
    print(f"  Round: {round_num}")
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
        choices=["chronicler", "dreamweaver", "minimalist", "realist", "experimenter"],
        help="Writer personality"
    )
    parser.add_argument(
        "prompt_file",
        help="Path to prompt file (e.g., prompts/claude_drama_prompt.md)"
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
        round_num=args.round
    )
