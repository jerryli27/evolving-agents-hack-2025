from pathlib import Path

OPENAI_API_KEY = "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"
KEY_OWNER = "Yi"

DEBUG = False

MAX_CHUNK_SIZE = 4

LLM_VERS = "gpt-4o-mini"

BASE_DIR = f"{Path(__file__).resolve().parent.parent}"

POPULATIONS_DIR = f"{BASE_DIR}/agent_bank/populations"
LLM_PROMPT_DIR = f"{BASE_DIR}/simulation_engine/prompt_template"

