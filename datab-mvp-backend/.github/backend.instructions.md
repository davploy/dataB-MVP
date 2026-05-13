---
name: datab-backend-python
description: "Use when writing Python code for the DataB MVP backend. Covers Flask API setup, Anthropic LLM integration, environment configuration, and dependency management with pipenv."
applyTo: "**/*.py"
---

# DataB MVP Backend Python Instructions

## Project Setup & Dependencies

This is a Flask-based backend that analyzes CSV data using Anthropic's Claude API. All dependencies are managed via **pipenv**.

### Running Python Scripts
Always use:
```bash
pipenv run python <script_name>
```

### Key Dependencies
- **anthropic==0.34.2** — Anthropic API client for Claude models
- **flask==3.0.0** — Web framework for API endpoints
- **python-dotenv==1.0.0** — Load environment variables from `.env`
- **flask-cors==6.0.2** — Cross-origin request handling for frontend integration
- **Python 3.14.\*** — Target version (set in Pipfile)

## Environment Configuration

The project requires a `.env` file at the project root with:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OUTPUT_SCHEMA=assets/schema.json
```

Always load environment variables early using:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Project Structure

- **`llm.py`** — Core `CSVAnalyzer` class for LLM interactions with Anthropic API
- **`inputs.py`** — Flask app (`app`) with `/input` and `/analyze` endpoints
- **`prompts/base-prompt.md`** — Contains `ANALYSIS_PROMPT` template (loaded dynamically)
- **`assets/schema.json`** — JSON schema for structured output validation

## Code Patterns

### File Handling
Use `pathlib.Path` for file operations:
```python
from pathlib import Path
prompt_path = Path(__file__).parent / "prompts" / "base-prompt.md"
```

### API Responses
All Flask endpoints return JSON with a consistent structure:
```python
return {'status': 'success', 'result': data}
return {'status': 'error', 'message': str(e)}, 500
```

### Environment-Based Configuration
Load paths relative to the base directory:
```python
base_dir = Path(__file__).parent
full_path = base_dir / os.getenv("OUTPUT_SCHEMA")
```

### CSV Processing
Use `csv.DictReader` with `io.StringIO` for in-memory CSV parsing:
```python
reader = csv.DictReader(io.StringIO(csv_text))
rows = list(reader)
```

## CORS Configuration

Flask-CORS is configured to allow requests from:
- `http://localhost:5000` (backend)
- `http://localhost:5173` (frontend dev server)

Modify the `CORS(app, resources={...})` configuration in `inputs.py` if adding new frontend origins.

## Anthropic LLM Integration

The `CSVAnalyzer` class:
1. Loads the prompt template from `prompts/base-prompt.md`
2. Loads the output schema from the path specified in `.env`
3. Formats the prompt with schema and CSV data
4. Sends to Claude API and returns structured JSON

When modifying LLM interactions, ensure:
- Prompts are loaded from files, not hardcoded
- Schema is always loaded and passed to the API
- Responses are validated against the schema structure

## Testing API Endpoints

**Debug endpoint** — echo CSV data:
```bash
curl -X POST http://localhost:5000/input --data-binary @file.csv
```

**Analysis endpoint** — analyze CSV with Claude:
```bash
curl -X POST http://localhost:5000/analyze --data-binary @file.csv
```

## Frontend Integration

The backend runs on port **5000** and expects CSV data as request body (binary). The frontend (at `http://localhost:5173`) sends POST requests to `/analyze` and receives `{'status': 'success', 'result': {...}}` responses.
