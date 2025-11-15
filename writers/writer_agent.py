"""Writer agent implementation."""

import yaml
import json
from pathlib import Path
from typing import Optional
from models import WriterConfig, StorySubmission
from llm_apis import LLMClientFactory, Message, ToolDefinition
from tools import PastWritingsTool, SubmitStoryTool, FeedbackIncorporationTool
from feedback_providers import FeedbackProvider


class WriterAgent:
    """An autonomous LLM-powered writer agent."""

    def __init__(self, config: WriterConfig, api_key: Optional[str] = None, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None, transcript_dir: Optional[str] = None):
        """
        Initialize a writer agent.

        Args:
            config: Writer configuration
            api_key: Optional API key for the LLM provider
            data_dir: Directory for storing data
            feedback_provider: Optional feedback provider (defaults to MockFeedbackProvider)
            transcript_dir: Directory for saving transcripts (defaults to ignore/transcripts)
        """
        self.config = config
        self.llm_client = LLMClientFactory.create_client(
            provider=config.llm_provider,
            config=config.llm_config,
            api_key=api_key,
        )

        # Store transcript directory
        self.transcript_dir = transcript_dir if transcript_dir else "ignore/transcripts"

        # Initialize tools
        self.past_writings_tool = PastWritingsTool(data_dir)
        self.submit_story_tool = SubmitStoryTool(data_dir, feedback_provider=feedback_provider)
        self.feedback_tool = FeedbackIncorporationTool(config.feedback_prompt_file) if config.enable_feedback_tool else None

        # Load and build the complete system prompt
        self.system_prompt = self._build_system_prompt()

        # Conversation history
        self.conversation_history: list[Message] = []

    @classmethod
    def from_yaml(cls, config_path: str, api_key: Optional[str] = None, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None, transcript_dir: Optional[str] = None) -> "WriterAgent":
        """
        Load a writer agent from a YAML configuration file.

        Args:
            config_path: Path to the YAML config file
            api_key: Optional API key for the LLM provider
            data_dir: Directory for storing data
            feedback_provider: Optional feedback provider (defaults to MockFeedbackProvider)
            transcript_dir: Directory for saving transcripts (defaults to ignore/transcripts)

        Returns:
            WriterAgent instance
        """
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)

        config = WriterConfig(**config_data)
        return cls(config, api_key, data_dir, feedback_provider, transcript_dir)

    def _build_system_prompt(self, round_num: int = 1) -> str:
        """
        Build the complete system prompt by combining the base system_prompt
        with content from prompt_file (round 1) or feedback_prompt_file (round 2+).
        
        Args:
            round_num: The current round number (default 1)
            
        Returns:
            Combined system prompt string
        """
        parts = []

        # Determine which prompt file to use based on round number
        prompt_file_to_use = None
        if round_num == 1:
            # Round 1: Use initial prompt file
            if self.config.prompt_file:
                prompt_file_to_use = self.config.prompt_file
        else:
            # Round 2+: Use feedback prompt file if available, otherwise fall back to prompt_file
            if self.config.feedback_prompt_file:
                prompt_file_to_use = self.config.feedback_prompt_file
            elif self.config.prompt_file:
                prompt_file_to_use = self.config.prompt_file

        # Load the selected prompt file
        if prompt_file_to_use:
            prompt_path = Path(prompt_file_to_use)

            # Try multiple locations for the prompt file
            if not prompt_path.exists():
                # Try prepending 'writers/' for when running from root directory
                alt_path = Path('writers') / prompt_file_to_use
                if alt_path.exists():
                    prompt_path = alt_path

            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    prompt_content = f.read()
                    parts.append(prompt_content)
            else:
                # Only warn, don't fail - system_prompt is still available
                pass  # Silently skip missing prompt files

        # Add the base system prompt
        if self.config.system_prompt:
            parts.append(self.config.system_prompt)

        # Combine with double newline separator
        return "\n\n".join(parts) if parts else ""

    def _get_tools(self) -> list[ToolDefinition]:
        """Get tool definitions for the LLM."""
        tools = [
            ToolDefinition(**self.past_writings_tool.get_tool_definition()),
            ToolDefinition(**self.submit_story_tool.get_tool_definition()),
        ]

        # Add feedback tool if enabled, but auto-disable if using round-based prompts
        # (when both prompt_file and feedback_prompt_file are specified, feedback is in system prompt instead)
        use_round_based_prompts = self.config.prompt_file and self.config.feedback_prompt_file
        if self.feedback_tool and not use_round_based_prompts:
            tools.append(ToolDefinition(**self.feedback_tool.get_tool_definition()))

        return tools

    def _build_round_prompt(self, round_num: int, tools_list: list[str]) -> str:
        """Build the initial round prompt with sequel-aware instructions."""

        # Base introduction
        prompt = f"You are {self.config.writer_name}, a creative writer. "

        # Add sequel context if enabled
        if self.config.should_write_sequel:
            if round_num == 1:
                prompt += (
                    f"You are beginning a {self.config.target_num_rounds}-part story series. "
                    f"This is Round {round_num} of {self.config.target_num_rounds}.\n\n"
                    f"IMPORTANT: You are writing the FIRST story in a connected series. "
                    f"Set up characters, world, and conflicts that will develop across {self.config.target_num_rounds} stories. "
                    f"End with hooks that make readers want to continue the series.\n\n"
                )
            elif round_num < self.config.target_num_rounds:
                prompt += (
                    f"You are continuing your {self.config.target_num_rounds}-part story series. "
                    f"This is Round {round_num} of {self.config.target_num_rounds}.\n\n"
                    f"IMPORTANT: This is a SEQUEL building on your previous stories. "
                    f"Continue character arcs, develop ongoing plot threads, and maintain consistency with established canon. "
                    f"You still have {self.config.target_num_rounds - round_num} more stories after this one.\n\n"
                )
            elif round_num == self.config.target_num_rounds:
                prompt += (
                    f"You are writing the FINAL story in your {self.config.target_num_rounds}-part series. "
                    f"This is Round {round_num} of {self.config.target_num_rounds}.\n\n"
                    f"IMPORTANT: This is the CONCLUSION of your story series. "
                    f"Resolve major plot threads, deliver satisfying character conclusions, and provide closure "
                    f"while staying true to everything you've established.\n\n"
                )
            else:  # Beyond target rounds
                prompt += (
                    f"You have completed your planned {self.config.target_num_rounds}-part series. "
                    f"This is Round {round_num} (BONUS CONTENT).\n\n"
                    f"IMPORTANT: Write additional content that expands the universe. This could be a spin-off, "
                    f"prequel, sequel, or side story that enriches the world you've built.\n\n"
                )
        else:
            # Standalone stories
            prompt += (
                f"It's now Round {round_num}. Your task is to write a short story synopsis.\n\n"
                f"Each story you write is STANDALONE - no need for continuity with previous rounds.\n\n"
            )

        # Add tools and process
        prompt += (
            f"You have access to the following tools:\n"
            f"{chr(10).join(tools_list)}\n\n"
            f"Process:\n"
            f"1. (Optional) Review your past writings to learn from feedback"
        )

        # Check if feedback tool is available (respects round-based prompt logic)
        use_round_based_prompts = self.config.prompt_file and self.config.feedback_prompt_file
        feedback_tool_available = self.feedback_tool and not use_round_based_prompts
        
        if feedback_tool_available:
            prompt += (
                f"\n2. (Optional) Access the feedback framework for strategic guidance on interpretation"
                f"\n3. Write your story"
                f"\n4. Submit your story using the submit_story tool\n\n"
            )
        else:
            prompt += (
                f"\n2. Write your story"
                f"\n3. Submit your story using the submit_story tool\n\n"
            )

        return prompt

    def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool call and return the result."""
        if tool_name == "get_past_writings":
            max_rounds = tool_input.get("max_rounds")
            return self.past_writings_tool.get_past_writings(
                writer_id=self.config.writer_id,
                max_rounds=max_rounds
            )
        elif tool_name == "submit_story":
            return self.submit_story_tool.submit_story(
                writer_id=self.config.writer_id,
                writer_name=self.config.writer_name,
                title=tool_input["title"],
                full_story=tool_input["full_story"],
                round=self._current_round,
                short_summary=tool_input.get("short_summary", ""),
                full_story_summary=tool_input.get("full_story_summary", ""),
                episode_summary=tool_input.get("episode_summary", ""),
                price=tool_input.get("price", 1.0),
            )
        elif tool_name == "get_feedback_framework":
            if self.feedback_tool:
                return self.feedback_tool.get_feedback_framework()
            else:
                return "Error: Feedback incorporation tool is not enabled for this writer."
        else:
            return f"Error: Unknown tool '{tool_name}'"

    def write_round(self, round_num: int, max_iterations: int = 10, save_transcript: bool = True) -> StorySubmission:
        """
        Execute a writing round.

        The agent will be prompted to write a story, can access past writings,
        and must submit the final story using the submit_story tool.

        Args:
            round_num: The current round number
            max_iterations: Maximum number of LLM calls to prevent infinite loops
            save_transcript: Whether to save the full conversation transcript

        Returns:
            The submitted story
        """
        self._current_round = round_num
        self.conversation_history = []
        self._iteration_log = []  # Track each iteration for debugging

        # Build round-specific system prompt
        round_system_prompt = self._build_system_prompt(round_num)

        # Initial prompt
        tools_list = [
            "1. get_past_writings - View your past stories and their performance",
            "2. submit_story - Submit your completed story and receive feedback"
        ]

        # Check if feedback tool is available (respects round-based prompt logic)
        use_round_based_prompts = self.config.prompt_file and self.config.feedback_prompt_file
        feedback_tool_available = self.feedback_tool and not use_round_based_prompts
        
        if feedback_tool_available:
            tools_list.insert(1, "2. get_feedback_framework - Access strategic guidance on incorporating market feedback")
            tools_list[2] = "3. submit_story - Submit your completed story and receive feedback"

        # Build sequel-aware prompt
        initial_prompt = self._build_round_prompt(round_num, tools_list)
        initial_prompt += "Begin writing!"

        self.conversation_history.append(Message(role="user", content=initial_prompt))

        submitted_story = None
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Log iteration start
            iteration_data = {
                "iteration": iteration,
                "input_messages": [{"role": m.role, "content": m.content} for m in self.conversation_history],
            }

            # Generate response using round-specific system prompt
            response = self.llm_client.generate(
                messages=self.conversation_history,
                tools=self._get_tools(),
                system=round_system_prompt,
            )

            # Log response
            iteration_data["response_content"] = response.content
            iteration_data["tool_calls"] = response.tool_calls if response.has_tool_calls() else []

            # Add assistant response to history
            if response.content:
                self.conversation_history.append(Message(role="assistant", content=response.content))

            # Handle tool calls
            iteration_data["tool_results"] = []
            if response.has_tool_calls():
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_input = tool_call["input"]

                    # Parse input if it's a JSON string (OpenAI format)
                    if isinstance(tool_input, str):
                        tool_input = json.loads(tool_input)

                    # Execute tool
                    tool_result = self._handle_tool_call(tool_name, tool_input)

                    # Log tool execution
                    iteration_data["tool_results"].append({
                        "tool_name": tool_name,
                        "tool_input": tool_input,
                        "tool_result": tool_result[:500] if len(tool_result) > 500 else tool_result  # Truncate long results
                    })

                    # Add tool result to conversation
                    self.conversation_history.append(
                        Message(role="user", content=f"Tool result: {tool_result}")
                    )

                    # Check if story was submitted
                    if tool_name == "submit_story":
                        # Load the submitted story from history
                        history = self.past_writings_tool._load_history(self.config.writer_id)
                        if history:
                            writing = history.get_round_writing(round_num)
                            if writing:
                                submitted_story = writing.submission
                                iteration_data["story_submitted"] = True
                                # Save iteration log before breaking
                                self._iteration_log.append(iteration_data)
                                break

                if submitted_story:
                    break
            else:
                # No tool calls and no submission - prompt to submit
                iteration_data["no_tool_calls"] = True
                self.conversation_history.append(
                    Message(role="user", content="Please submit your story using the submit_story tool.")
                )

            # Save iteration log (if not already saved)
            if not submitted_story:
                self._iteration_log.append(iteration_data)

        # Save transcript if requested
        if save_transcript:
            self._save_transcript(round_num, submitted_story is not None, round_system_prompt)

        if not submitted_story:
            raise RuntimeError(
                f"Writer {self.config.writer_name} failed to submit a story after {max_iterations} iterations"
            )

        return submitted_story

    def _save_transcript(self, round_num: int, success: bool, round_system_prompt: str):
        """Save the full conversation transcript for debugging."""
        from datetime import datetime

        transcript_dir = Path(self.transcript_dir) / self.config.writer_id
        transcript_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = "success" if success else "failed"
        transcript_file = transcript_dir / f"round_{round_num}_{status}_{timestamp}.json"

        transcript_data = {
            "writer_id": self.config.writer_id,
            "writer_name": self.config.writer_name,
            "round": round_num,
            "status": status,
            "timestamp": timestamp,
            "config": {
                "llm_provider": self.config.llm_provider.value,
                "model": self.config.llm_config.model,
                "temperature": self.config.llm_config.temperature,
                "prompt_file": self.config.prompt_file,
                "feedback_prompt_file": self.config.feedback_prompt_file,
            },
            "system_prompt": round_system_prompt,  # Save the round-specific prompt that was actually used
            "iterations": self._iteration_log,
            "final_conversation": [
                {"role": m.role, "content": m.content}
                for m in self.conversation_history
            ],
        }

        with open(transcript_file, 'w') as f:
            json.dump(transcript_data, f, indent=2, default=str)

        print(f"[DEBUG] Transcript saved to: {transcript_file}")

    def get_history(self):
        """Get the writer's complete history."""
        return self.past_writings_tool._load_history(self.config.writer_id)
