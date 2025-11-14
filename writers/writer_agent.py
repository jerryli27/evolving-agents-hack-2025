"""Writer agent implementation."""

import yaml
import json
from pathlib import Path
from typing import Optional
from models import WriterConfig, StorySubmission
from llm_apis import LLMClientFactory, Message, ToolDefinition
from tools import PastWritingsTool, SubmitStoryTool


class WriterAgent:
    """An autonomous LLM-powered writer agent."""

    def __init__(self, config: WriterConfig, api_key: Optional[str] = None, data_dir: str = "data/writings"):
        """
        Initialize a writer agent.

        Args:
            config: Writer configuration
            api_key: Optional API key for the LLM provider
            data_dir: Directory for storing data
        """
        self.config = config
        self.llm_client = LLMClientFactory.create_client(
            provider=config.llm_provider,
            config=config.llm_config,
            api_key=api_key,
        )

        # Initialize tools
        self.past_writings_tool = PastWritingsTool(data_dir)
        self.submit_story_tool = SubmitStoryTool(data_dir)

        # Load and build the complete system prompt
        self.system_prompt = self._build_system_prompt()

        # Conversation history
        self.conversation_history: list[Message] = []

    @classmethod
    def from_yaml(cls, config_path: str, api_key: Optional[str] = None, data_dir: str = "data/writings") -> "WriterAgent":
        """
        Load a writer agent from a YAML configuration file.

        Args:
            config_path: Path to the YAML config file
            api_key: Optional API key for the LLM provider
            data_dir: Directory for storing data

        Returns:
            WriterAgent instance
        """
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)

        config = WriterConfig(**config_data)
        return cls(config, api_key, data_dir)

    def _build_system_prompt(self) -> str:
        """
        Build the complete system prompt by combining the base system_prompt
        with content from prompt_file if specified.
        """
        parts = []

        # Add content from prompt file if specified
        if self.config.prompt_file:
            prompt_path = Path(self.config.prompt_file)
            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    prompt_content = f.read()
                    parts.append(prompt_content)
            else:
                print(f"Warning: prompt_file '{self.config.prompt_file}' not found. Skipping.")

        # Add the base system prompt
        if self.config.system_prompt:
            parts.append(self.config.system_prompt)

        # Combine with double newline separator
        return "\n\n".join(parts) if parts else ""

    def _get_tools(self) -> list[ToolDefinition]:
        """Get tool definitions for the LLM."""
        return [
            ToolDefinition(**self.past_writings_tool.get_tool_definition()),
            ToolDefinition(**self.submit_story_tool.get_tool_definition()),
        ]

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
                price=tool_input.get("price", 1.0),
            )
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

        # Initial prompt
        initial_prompt = (
            f"You are {self.config.writer_name}, a creative writer. "
            f"It's now Round {round_num}. Your task is to write a short story synopsis.\n\n"
            f"You have access to the following tools:\n"
            f"1. get_past_writings - View your past stories and their performance\n"
            f"2. submit_story - Submit your completed story and receive feedback\n\n"
            f"Process:\n"
            f"1. (Optional) Review your past writings to learn from feedback\n"
            f"2. Write your story\n"
            f"3. Submit your story using the submit_story tool\n\n"
            f"Begin writing!"
        )

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

            # Generate response
            response = self.llm_client.generate(
                messages=self.conversation_history,
                tools=self._get_tools(),
                system=self.system_prompt,
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
            self._save_transcript(round_num, submitted_story is not None)

        if not submitted_story:
            raise RuntimeError(
                f"Writer {self.config.writer_name} failed to submit a story after {max_iterations} iterations"
            )

        return submitted_story

    def _save_transcript(self, round_num: int, success: bool):
        """Save the full conversation transcript for debugging."""
        from datetime import datetime

        transcript_dir = Path("ignore/transcripts") / self.config.writer_id
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
            },
            "system_prompt": self.system_prompt[:500] + "..." if len(self.system_prompt) > 500 else self.system_prompt,
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
