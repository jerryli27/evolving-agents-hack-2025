"""
View and analyze writer transcripts from failed or successful runs.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def view_transcript(transcript_path: str, show_full: bool = False):
    """View a transcript file in a readable format."""

    with open(transcript_path, 'r') as f:
        data = json.load(f)

    print("\n" + "="*80)
    print(f"TRANSCRIPT: {data['writer_name']} (ID: {data['writer_id']})")
    print("="*80)
    print(f"Round: {data['round']}")
    print(f"Status: {data['status'].upper()}")
    print(f"Timestamp: {data['timestamp']}")
    print(f"\nConfig:")
    print(f"  Provider: {data['config']['llm_provider']}")
    print(f"  Model: {data['config']['model']}")
    print(f"  Temperature: {data['config']['temperature']}")
    print(f"  Prompt File: {data['config']['prompt_file']}")

    print(f"\n{'='*80}")
    print(f"ITERATIONS: {len(data['iterations'])}")
    print("="*80)

    for iter_data in data['iterations']:
        print(f"\n--- Iteration {iter_data['iteration']} ---")

        # Show response content (truncated unless full mode)
        if 'response_content' in iter_data:
            content = iter_data['response_content']
            if content:
                if show_full or len(content) < 500:
                    print(f"\nAssistant Response:\n{content}")
                else:
                    print(f"\nAssistant Response (first 500 chars):\n{content[:500]}...")

        # Show tool calls
        if iter_data.get('tool_calls'):
            print(f"\nTool Calls: {len(iter_data['tool_calls'])}")
            for tc in iter_data['tool_calls']:
                print(f"  - {tc['name']}")

        # Show tool results
        if iter_data.get('tool_results'):
            for tr in iter_data['tool_results']:
                print(f"\nTool: {tr['tool_name']}")

                # Special handling for submit_story to show the actual story
                if tr['tool_name'] == 'submit_story':
                    tool_input = tr['tool_input']
                    print(f"\nSubmitted Story:")
                    print(f"  Title: {tool_input.get('title', 'N/A')}")
                    print(f"  Price: ${tool_input.get('price', 1.0):.2f}")
                    if 'short_summary' in tool_input and tool_input['short_summary']:
                        print(f"  Summary: {tool_input['short_summary']}")

                    full_story = tool_input.get('full_story', '')
                    if full_story:
                        print(f"\n  Full Story ({len(full_story)} chars):")
                        if show_full:
                            print(f"  {full_story}")
                        else:
                            # Show first 300 chars
                            preview = full_story[:300]
                            if len(full_story) > 300:
                                preview += "..."
                            print(f"  {preview}")
                            print(f"\n  [Use --full to see complete story]")

                    print(f"\nFeedback Result:")
                    print(f"  {tr['tool_result']}")
                else:
                    print(f"Input: {tr['tool_input']}")
                    print(f"Result (truncated): {tr['tool_result']}")

        # Show flags
        if iter_data.get('no_tool_calls'):
            print("\n[!] No tool calls - prompted to use submit_story tool")

        if iter_data.get('story_submitted'):
            print("\n[✓] Story successfully submitted!")

        print()

    # Show final status
    print("="*80)
    if data['status'] == 'success':
        print("RESULT: ✓ Successfully submitted story")
    else:
        print("RESULT: ✗ Failed to submit story")
        print("\nPossible issues:")
        print("- Writer didn't call submit_story tool")
        print("- Tool call had incorrect parameters")
        print("- Hit max iteration limit")
        print("\nReview the iterations above to see what went wrong.")
    print("="*80)


def list_transcripts(writer_id: str = None, status: str = None):
    """List available transcripts."""

    transcript_dir = Path("ignore/transcripts")

    if not transcript_dir.exists():
        print("No transcripts found. Run some writers first!")
        return

    # Find all transcript files
    if writer_id:
        pattern = f"{writer_id}/**/*.json"
    else:
        pattern = "**/*.json"

    transcripts = list(transcript_dir.glob(pattern))

    if status:
        transcripts = [t for t in transcripts if status in t.name]

    if not transcripts:
        print("No matching transcripts found.")
        return

    print(f"\nFound {len(transcripts)} transcript(s):\n")

    for t in sorted(transcripts, key=lambda x: x.stat().st_mtime, reverse=True):
        # Parse filename
        parts = t.stem.split('_')
        try:
            with open(t, 'r') as f:
                data = json.load(f)

            print(f"[{data['status'].upper():7}] {data['writer_name']:20} Round {data['round']} - {data['timestamp']}")
            print(f"           {t}")
            print()
        except Exception as e:
            print(f"[ERROR] {t} - Could not parse: {e}\n")


def compare_transcripts(transcript_paths: list[str]):
    """Compare multiple transcripts side-by-side."""

    transcripts = []
    for path in transcript_paths:
        with open(path, 'r') as f:
            transcripts.append(json.load(f))

    print("\n" + "="*80)
    print(f"COMPARING {len(transcripts)} TRANSCRIPTS")
    print("="*80)

    for i, data in enumerate(transcripts, 1):
        print(f"\n[{i}] {data['writer_name']} - Round {data['round']} - {data['status'].upper()}")
        print(f"    Model: {data['config']['model']}, Temp: {data['config']['temperature']}")
        print(f"    Iterations: {len(data['iterations'])}")

        # Count tool calls
        total_tools = sum(len(iter_data.get('tool_calls', [])) for iter_data in data['iterations'])
        submit_calls = sum(
            1 for iter_data in data['iterations']
            for tr in iter_data.get('tool_results', [])
            if tr['tool_name'] == 'submit_story'
        )

        print(f"    Tool calls: {total_tools} (submit_story: {submit_calls})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="View and analyze writer transcripts"
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # View command
    view_parser = subparsers.add_parser('view', help='View a specific transcript')
    view_parser.add_argument('transcript', help='Path to transcript JSON file')
    view_parser.add_argument('--full', action='store_true', help='Show full content (no truncation)')

    # List command
    list_parser = subparsers.add_parser('list', help='List available transcripts')
    list_parser.add_argument('--writer', help='Filter by writer ID')
    list_parser.add_argument('--status', choices=['success', 'failed'], help='Filter by status')

    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare multiple transcripts')
    compare_parser.add_argument('transcripts', nargs='+', help='Paths to transcript files')

    # Latest command
    latest_parser = subparsers.add_parser('latest', help='View the most recent transcript')
    latest_parser.add_argument('--writer', help='Filter by writer ID')
    latest_parser.add_argument('--status', choices=['success', 'failed'], help='Filter by status')
    latest_parser.add_argument('--full', action='store_true', help='Show full content')

    args = parser.parse_args()

    if args.command == 'view':
        view_transcript(args.transcript, show_full=args.full)

    elif args.command == 'list':
        list_transcripts(writer_id=args.writer, status=args.status)

    elif args.command == 'compare':
        compare_transcripts(args.transcripts)

    elif args.command == 'latest':
        # Find latest transcript
        transcript_dir = Path("ignore/transcripts")
        pattern = f"{args.writer}/**/*.json" if args.writer else "**/*.json"
        transcripts = list(transcript_dir.glob(pattern))

        if args.status:
            transcripts = [t for t in transcripts if args.status in t.name]

        if not transcripts:
            print("No transcripts found.")
        else:
            latest = max(transcripts, key=lambda x: x.stat().st_mtime)
            print(f"\nViewing latest transcript: {latest}\n")
            view_transcript(str(latest), show_full=args.full)

    else:
        parser.print_help()
