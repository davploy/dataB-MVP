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

class CSVAnalyzer:
    """
    Analyzes CSV data using Anthropic Claude API.
    
    Validates data quality, interprets headers against a reference schema,
    detects semantic errors, and returns structured JSON response.
    """
    
    def __init__(self):
        """Initialize the CSV analyzer with API key and prompt."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise CSVAnalyzerError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=self.api_key)
        
        # Load the analysis prompt
        self.prompt_template = _load_prompt()
        
        # Load reference schema from env
        schema_json = os.getenv("OUTPUT_SCHEMA")
        if not schema_json:
            raise CSVAnalyzerError("OUTPUT_SCHEMA environment variable not set")
        
        try:
            self.reference_schema = json.loads(schema_json)
        except json.JSONDecodeError as e:
            raise CSVAnalyzerError(f"Invalid JSON in OUTPUT_SCHEMA: {e}")
    
    def _parse_csv(self, csv_text: str) -> tuple[List[str], List[Dict[str, Any]]]:
        """
        Parse CSV text into headers and rows.
        
        Args:
            csv_text: Raw CSV text content
            
        Returns:
            Tuple of (headers list, rows list of dicts)
            
        Raises:
            CSVParseError: If CSV parsing fails
        """
        try:
            lines = csv_text.strip().split('\n')
            if not lines:
                raise CSVParseError("Empty CSV data")
            
            # Use csv module for proper parsing
            reader = csv.DictReader(io.StringIO(csv_text))
            rows = list(reader)
            
            if not rows:
                raise CSVParseError("No data rows found in CSV")
            
            headers = list(rows[0].keys()) if rows else []
            
            return headers, rows
        
        except csv.Error as e:
            raise CSVParseError(f"CSV parsing failed: {e}")
        except Exception as e:
            raise CSVParseError(f"Unexpected error parsing CSV: {e}")
    
    def analyze(self, csv_text: str) -> Dict[str, Any]:
        """
        Analyze CSV data using Anthropic Claude.
        
        Args:
            csv_text: Raw CSV text to analyze
            
        Returns:
            Structured JSON response with schema, rows, and issues
            
        Raises:
            CSVParseError: If CSV parsing fails
            AnthropicError: If API call fails
        """
        # Validate and parse CSV
        try:
            headers, rows = self._parse_csv(csv_text)
        except CSVParseError:
            raise
        
        # Format the prompt with reference schema and CSV text
        formatted_prompt = self.prompt_template.format(
            reference_schema=json.dumps(self.reference_schema, indent=2),
            csv_text=csv_text
        )
        
        # Call Anthropic API
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": formatted_prompt}
                ]
            )
            
            # Extract response content
            response_text = message.content[0].text
            
        except Exception as e:
            raise AnthropicError(f"Anthropic API call failed: {e}")
        
        # Parse the JSON response
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as e:
            raise AnthropicError(f"Failed to parse Anthropic response as JSON: {e}")
        
        # Validate response structure
        required_keys = {"schema", "rows", "issues"}
        if not all(key in result for key in required_keys):
            raise AnthropicError(f"Response missing required keys: {required_keys}")
        
        return result
