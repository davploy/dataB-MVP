import os
import json
import csv

# io = standard library module for handling input/output streams
import io
from pathlib import Path
from typing import Dict, Any, List

from anthropic import Anthropic
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

def _load_prompt() -> str:
    """Load the analysis prompt from base-prompt.md."""
    prompt_path = Path(__file__).parent / "prompts" / "base-prompt.md"
    with open(prompt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract the ANALYSIS_PROMPT constant from the file
    # Expecting format: ANALYSIS_PROMPT = """..."""
    if 'ANALYSIS_PROMPT = """' in content:
        start = content.index('ANALYSIS_PROMPT = """') + len('ANALYSIS_PROMPT = """')
        end = content.rindex('"""')
        return content[start:end]
    
    raise ValueError("Could not find ANALYSIS_PROMPT in base-prompt.md")