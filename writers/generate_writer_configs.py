"""
Utility script to generate writer configurations by mixing and matching:
- Prompt files
- System prompts (writer personalities)
- LLM providers and models
"""

import yaml
from pathlib import Path
from itertools import product


# Define available prompt files
PROMPT_FILES = [
    "prompts/claude_drama_prompt.md",
    "prompts/chatgpt5.1_drama_prompt.md",
    "prompts/gpt2.5pro_drama_prompt.md",
]

# Define available feedback prompt files
FEEDBACK_PROMPT_FILES = [
    "feedback_prompts/claude_feedback_prompt.md",
    "feedback_prompts/gpt_feedback_prompt.md",
    "feedback_prompts/gpt2.5pro_feedback_prompt.md",
]

# Define writer personalities (system prompts)
PERSONALITIES = {
    "chronicler": {
        "name": "The Chronicler",
        "prompt": """You are "The Chronicler", a writer who specializes in drama with historical elements.
Your stories blend real historical events with imaginative character-driven narratives.

When writing:
- Follow the drama writing guide provided to structure your stories
- Draw inspiration from history to create authentic settings and conflicts
- Focus on rich, descriptive language and vivid character development
- Build stories with strong emotional arcs
- Learn from your past performance feedback to refine your craft"""
    },
    "dreamweaver": {
        "name": "The Dreamweaver",
        "prompt": """You are "The Dreamweaver", a writer who specializes in surreal, imaginative drama.
Your stories explore the boundaries between reality and fantasy, dreams and waking life.
You excel at unexpected emotional depth and thought-provoking themes.

When writing:
- Follow the drama writing guide provided to structure your stories
- Embrace the surreal and unexpected while maintaining emotional truth
- Use metaphor and symbolism to deepen dramatic tension
- Challenge reader expectations with complex character dynamics
- Create stories that linger emotionally in the mind
- Analyze your feedback to understand what resonates with readers"""
    },
    "minimalist": {
        "name": "The Minimalist",
        "prompt": """You are "The Minimalist", a writer who believes in the power of brevity and dramatic precision.
Your stories are concise, every word carefully chosen for maximum emotional impact.
You specialize in concentrated drama with short, punchy narratives.

When writing:
- Follow the drama writing guide provided, but keep everything BRIEF
- Use extreme economy of language - aim for the shorter end of word counts
- Make every word count toward the dramatic conflict
- Create impact through implication rather than exposition
- Focus on a single moment of dramatic revelation or transformation
- Study your feedback to refine your minimalist approach"""
    },
    "realist": {
        "name": "The Realist",
        "prompt": """You are "The Realist", a writer who specializes in authentic, slice-of-life drama.
Your stories capture genuine human experiences with unflinching honesty.
You excel at creating believable characters facing relatable conflicts.

When writing:
- Follow the drama writing guide provided to structure your stories
- Focus on authentic dialogue and realistic character behavior
- Draw from contemporary social issues and everyday struggles
- Avoid melodrama - let truth speak for itself
- Create subtle emotional depth through observation
- Learn from feedback to refine your realistic approach"""
    },
    "experimenter": {
        "name": "The Experimenter",
        "prompt": """You are "The Experimenter", a writer who pushes the boundaries of dramatic storytelling.
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
}

# Define LLM configurations
LLM_CONFIGS = {
    "anthropic_sonnet": {
        "provider": "anthropic",
        "config": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.7,
            "max_tokens": 4096,
            "extra_params": {}
        }
    },
    "anthropic_sonnet_creative": {
        "provider": "anthropic",
        "config": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.9,
            "max_tokens": 4096,
            "extra_params": {}
        }
    },
    "anthropic_sonnet_precise": {
        "provider": "anthropic",
        "config": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.5,
            "max_tokens": 4096,
            "extra_params": {}
        }
    },
    "openai_gpt4o": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o",
            "temperature": 0.7,
            "max_tokens": 4096,
            "extra_params": {}
        }
    },
    "openai_gpt4o_creative": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o",
            "temperature": 0.9,
            "max_tokens": 4096,
            "extra_params": {}
        }
    },
    "openai_gpt4o_precise": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o",
            "temperature": 0.5,
            "max_tokens": 4096,
            "extra_params": {}
        }
    }
}


def generate_writer_config(
    writer_id: str,
    personality_key: str,
    prompt_file: str,
    llm_key: str,
    output_dir: Path,
    feedback_prompt_file: str = None,
    enable_feedback_tool: bool = True
):
    """Generate a single writer configuration file."""

    personality = PERSONALITIES[personality_key]
    llm_config = LLM_CONFIGS[llm_key]

    config = {
        "writer_id": writer_id,
        "writer_name": personality["name"],
        "llm_provider": llm_config["provider"],
        "llm_config": llm_config["config"],
        "prompt_file": prompt_file,
        "system_prompt": personality["prompt"],
        "feedback_prompt_file": feedback_prompt_file,
        "enable_feedback_tool": enable_feedback_tool,
        "can_see_other_writers": False
    }

    output_path = output_dir / f"{writer_id}.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    return output_path


def generate_all_combinations(output_dir: str = "config/experiments", feedback_prompt_file: str = None):
    """Generate all possible combinations of personality, prompt, and LLM."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Use first feedback prompt as default if none specified
    if feedback_prompt_file is None:
        feedback_prompt_file = FEEDBACK_PROMPT_FILES[0]

    generated = []
    counter = 1

    for personality_key, prompt_file, llm_key in product(
        PERSONALITIES.keys(),
        PROMPT_FILES,
        LLM_CONFIGS.keys()
    ):
        writer_id = f"exp_{counter:03d}"

        config_path = generate_writer_config(
            writer_id=writer_id,
            personality_key=personality_key,
            prompt_file=prompt_file,
            llm_key=llm_key,
            output_dir=output_path,
            feedback_prompt_file=feedback_prompt_file
        )

        # Extract prompt filename for display
        prompt_name = Path(prompt_file).stem

        generated.append({
            "id": writer_id,
            "personality": personality_key,
            "prompt": prompt_name,
            "llm": llm_key,
            "path": str(config_path)
        })

        counter += 1

    # Generate index file
    index_path = output_path / "INDEX.md"
    with open(index_path, 'w') as f:
        f.write("# Generated Writer Configurations\n\n")
        f.write(f"Total combinations: {len(generated)}\n\n")
        f.write("| Writer ID | Personality | Prompt File | LLM Config | Path |\n")
        f.write("|-----------|-------------|-------------|------------|------|\n")

        for item in generated:
            f.write(
                f"| {item['id']} | {item['personality']} | "
                f"{item['prompt']} | {item['llm']} | {item['path']} |\n"
            )

    return generated, index_path


def generate_subset(
    personalities=None,
    prompt_files=None,
    llm_configs=None,
    output_dir: str = "config/experiments",
    feedback_prompt_file: str = None,
    enable_feedback_tool: bool = True
):
    """Generate a subset of combinations based on filters."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Use all if not specified
    personalities = personalities or list(PERSONALITIES.keys())
    prompt_files = prompt_files or PROMPT_FILES
    llm_configs = llm_configs or list(LLM_CONFIGS.keys())

    # Use first feedback prompt as default if none specified and tool is enabled
    if feedback_prompt_file is None and enable_feedback_tool:
        feedback_prompt_file = FEEDBACK_PROMPT_FILES[0]

    generated = []
    counter = 1

    for personality_key, prompt_file, llm_key in product(
        personalities,
        prompt_files,
        llm_configs
    ):
        writer_id = f"subset_{counter:03d}"

        config_path = generate_writer_config(
            writer_id=writer_id,
            personality_key=personality_key,
            prompt_file=prompt_file,
            llm_key=llm_key,
            output_dir=output_path,
            feedback_prompt_file=feedback_prompt_file,
            enable_feedback_tool=enable_feedback_tool
        )

        prompt_name = Path(prompt_file).stem

        generated.append({
            "id": writer_id,
            "personality": personality_key,
            "prompt": prompt_name,
            "llm": llm_key,
            "path": str(config_path)
        })

        counter += 1

    return generated


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate writer configurations by mixing personalities, prompts, and LLMs"
    )
    parser.add_argument(
        "--mode",
        choices=["all", "subset", "list"],
        default="list",
        help="Generation mode: all (all combinations), subset (filtered), list (show options)"
    )
    parser.add_argument(
        "--output",
        default="config/experiments",
        help="Output directory for generated configs"
    )
    parser.add_argument(
        "--personalities",
        nargs="+",
        choices=list(PERSONALITIES.keys()),
        help="Personality types to include"
    )
    parser.add_argument(
        "--prompts",
        nargs="+",
        choices=PROMPT_FILES,
        help="Prompt files to include"
    )
    parser.add_argument(
        "--llms",
        nargs="+",
        choices=list(LLM_CONFIGS.keys()),
        help="LLM configs to include"
    )
    parser.add_argument(
        "--feedback-prompt",
        choices=FEEDBACK_PROMPT_FILES,
        help="Feedback prompt file to use (default: first available)"
    )
    parser.add_argument(
        "--disable-feedback-tool",
        action="store_true",
        help="Disable the feedback incorporation tool for generated configs"
    )

    args = parser.parse_args()

    if args.mode == "list":
        print("\n=== Available Options ===\n")

        print("Personalities:")
        for key, value in PERSONALITIES.items():
            print(f"  - {key}: {value['name']}")

        print("\nPrompt Files:")
        for pf in PROMPT_FILES:
            print(f"  - {pf}")

        print("\nFeedback Prompt Files:")
        for fpf in FEEDBACK_PROMPT_FILES:
            print(f"  - {fpf}")

        print("\nLLM Configurations:")
        for key, value in LLM_CONFIGS.items():
            print(f"  - {key}: {value['provider']} - {value['config']['model']} (temp={value['config']['temperature']})")

        print(f"\nTotal possible combinations: {len(PERSONALITIES) * len(PROMPT_FILES) * len(LLM_CONFIGS)}")

        print("\nExample usage:")
        print("  # Generate all combinations")
        print("  python generate_writer_configs.py --mode all")
        print("\n  # Generate specific combinations")
        print("  python generate_writer_configs.py --mode subset --personalities chronicler minimalist --prompts prompts/claude_drama_prompt.md --llms anthropic_sonnet openai_gpt4o")

    elif args.mode == "all":
        print("Generating all combinations...")
        generated, index_path = generate_all_combinations(
            output_dir=args.output,
            feedback_prompt_file=args.feedback_prompt
        )
        print(f"\nGenerated {len(generated)} configurations in {args.output}/")
        print(f"Index file: {index_path}")

    elif args.mode == "subset":
        print("Generating subset...")
        generated = generate_subset(
            personalities=args.personalities,
            prompt_files=args.prompts,
            llm_configs=args.llms,
            output_dir=args.output,
            feedback_prompt_file=args.feedback_prompt,
            enable_feedback_tool=not args.disable_feedback_tool
        )
        print(f"\nGenerated {len(generated)} configurations in {args.output}/")
        for item in generated:
            print(f"  {item['id']}: {item['personality']} + {item['prompt']} + {item['llm']}")
