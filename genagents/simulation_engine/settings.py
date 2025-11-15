from pathlib import Path

OPENAI_API_KEY = "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"
KEY_OWNER = "Yi"

DEBUG = False

MAX_CHUNK_SIZE = 4

LLM_VERS = "gpt-4o-mini"

BASE_DIR = f"{Path(__file__).resolve().parent.parent}"

POPULATIONS_DIR = f"{BASE_DIR}/agent_bank/populations"
LLM_PROMPT_DIR = f"{BASE_DIR}/simulation_engine/prompt_template"

