from pathlib import Path

OPENAI_API_KEY = "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"
KEY_OWNER = "Yi"

DEBUG = False

MAX_CHUNK_SIZE = 4

LLM_VERS = "gpt-4o-mini"

BASE_DIR = f"{Path(__file__).resolve().parent.parent}"

POPULATIONS_DIR = f"{BASE_DIR}/agent_bank/populations"
LLM_PROMPT_DIR = f"{BASE_DIR}/simulation_engine/prompt_template"

