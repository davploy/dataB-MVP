import os
import json
import csv
import io
from pathlib import Path
from typing import Dict, Any, List

from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()

def _load_prompt() -> str:
    """Load the analysis prompt from base-prompt.md."""
    prompt_path = Path(__file__).parent / "prompts" / "base-prompt.md"
    with open(prompt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if 'ANALYSIS_PROMPT = """' in content:
        start = content.index('ANALYSIS_PROMPT = """') + len('ANALYSIS_PROMPT = """')
        end = content.rindex('"""')
        return content[start:end]
    
    raise ValueError("Could not find ANALYSIS_PROMPT in base-prompt.md")


class CSVAnalyzer:
    """Analyzes CSV data using Anthropic Claude API."""
    
    def __init__(self):
        """Initialize the CSV analyzer with API key and prompt."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.prompt_template = _load_prompt()
        
        schema_path = os.getenv("OUTPUT_SCHEMA")
        base_dir = Path(__file__).parent
        full_path = base_dir / schema_path
        
        with open(full_path, "r", encoding="utf-8") as f:
            self.output_schema = json.load(f)
    
    def _parse_csv(self, csv_text: str) -> tuple[List[str], List[Dict[str, Any]]]:
        """Parse CSV text into headers and rows."""
        reader = csv.DictReader(io.StringIO(csv_text))
        rows = list(reader)
        headers = list(rows[0].keys()) if rows else []
        return headers, rows
    
    def analyze(self, csv_text: str) -> Dict[str, Any]:
        """Analyze CSV data using Anthropic Claude and return structured JSON."""
        # Parse CSV
        headers, rows = self._parse_csv(csv_text)
        
        # Format prompt with reference schema and CSV text
        formatted_prompt = self.prompt_template.format(
            reference_schema=json.dumps(self.output_schema, indent=2),
            csv_text=csv_text
        )
        
        # Call Anthropic API
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": formatted_prompt}]
        )
        
        # Extract and parse response
        response_text = message.content[0].text
        result = json.loads(response_text)
        
        return result