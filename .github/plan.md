# Plan: Anthropic CSV Analysis Component

## TL;DR

Create a Python module (`llm.py`) that uses the Anthropic SDK to validate, parse, and structure CSV data. Integrate via a new `/analyze` endpoint in `inputs.py`. The component validates CSV data quality, interprets headers against a fixed reference schema (from env config), detects semantic errors (type mismatches, invalid formats, inconsistent patterns), and returns structured JSON (`{schema, rows, issues}`) or 400 on validation failure.

## Steps

### Phase 1: Setup & Dependencies

1. Install Anthropic SDK: `pip install anthropic`
2. Create `datab-mvp-backend/llm.py` with:
   - `CSVAnalyzer` class that initializes Anthropic client from `ANTHROPIC_API_KEY` env var
   - Load reference schema from env var (e.g., `REFERENCE_SCHEMA` as JSON string)
   - Helper to parse reference schema safely

### Phase 2: Core Analysis Logic

3. Define static prompt constant in `llm.py`:
   ```python
   ANALYSIS_PROMPT = """Analyze the following CSV data and return a structured JSON response.

   Your task:
   1. Validate data quality
   2. Fix unit/symbol errors (e.g., "5kg" → 5, unit: "kg")
   3. Interpret mismatched headers against the reference schema
   4. Detect semantic errors (type mismatches, invalid formats, outliers, inconsistent patterns)
   
   Reference Schema:
   {reference_schema}
   
   CSV Data:
   {csv_text}
   
   Return a JSON object with this structure:
   {{
     "schema": [{"name": "field1", "type": "string", "sample": "value"}, ...],
     "rows": [parsed data rows as objects],
     "issues": [{"row": N, "field": "name", "issue": "description", "severity": "error|warning"}]
   }}
   
   Only return valid JSON, no other text."""
   ```

4. Implement `CSVAnalyzer.analyze(csv_text)` method that:
   - Parses CSV text into rows (validate UTF-8, detect headers)
   - Formats static prompt with reference schema and CSV text
   - Calls `anthropic.messages.create()` with the prompt
   - Parses Anthropic response as JSON → `{schema: [...], rows: [...], issues: [...]}`

4. Implement error detection & reporting:
   - Handle Anthropic API errors (rate limits, auth, timeouts) → return structured error
   - Handle malformed CSV (invalid UTF-8, unparseable rows) → 400
   - Handle semantic validation issues from Anthropic → include in `issues` array (don't auto-fix)

### Phase 3: Integration & Flask Route

5. Create `/analyze` endpoint in `inputs.py`:
   - Accept POST with raw CSV body (same as `/input`)
   - Instantiate `CSVAnalyzer` (or reuse singleton)
   - Call `analyzer.analyze(csv_text)`
   - Return 200 with `{status: 'success', data: {...}}` on success
   - Return 400 with `{status: 'error', message: '...', details: {...}}` on failure

6. Update `/input` endpoint (optional):
   - Decide: does `/input` stay as-is (simple echo), or delegate to `/analyze`?
   - If delegating, clear scope boundary in comments

### Phase 4: Testing & Validation

7. Manual test:
   - Create sample CSV files (valid, malformed, type mismatches, missing values, etc.)
   - Test `/analyze` endpoint locally with `curl` or frontend
   - Verify response structure matches `{schema, rows, issues}`

8. Document:
   - Comment code with docstrings (what, why, error handling)
   - Add env var reference to README or `.env.example`

## Relevant Files

- `datab-mvp-backend/llm.py` — new file, contains `CSVAnalyzer` class with:
  - Static prompt constant (hardcoded in code)
  - `__init__(api_key, reference_schema)` — initialize Anthropic client and load reference
  - `analyze(csv_text)` → returns `{schema, rows, issues}` or raises exception
  - Helper methods: `_parse_reference_schema()`, `_parse_csv()`, `_parse_response()`
  - Error handling: custom exceptions for validation, API errors

- `datab-mvp-backend/inputs.py` — modify:
  - Import `CSVAnalyzer` from `llm`
  - Create new `POST /analyze` endpoint (mirrors `/input` but calls analyzer)
  - Optional: decide if `/input` should call `/analyze` or remain as-is

## Verification

1. **Unit validation**:
   - Anthropic client initializes with API key from env
   - Reference schema loads and parses correctly
   - CSV parser handles edge cases (empty file, missing headers, Unicode)

2. **Integration test**:
   - POST valid CSV to `/analyze` → 200 with correct structure
   - POST invalid CSV → 400 with error details
   - POST malformed UTF-8 → 400 with decode error
   - POST CSV with semantic issues (type mismatches, etc.) → 200 with issues in response

3. **Manual smoke test**:
   - Test with frontend `UploadComponent` (update to POST to `/analyze` instead of `/input`)
   - Verify frontend receives and displays response correctly

## Decisions

- **Separate `/analyze` endpoint**: Keep `/input` as-is for flexibility; let `/analyze` be the new analysis pipeline. Either `/input` stays as a debug echo, or it delegates to `/analyze` with a note.
- **Model choice (flexible)**: Start with `claude-sonnet-4-20250514` (balanced cost/capability for CSV validation). Can switch to Opus if validation complexity grows, or Haiku if cost is critical.
- **Streaming**: Process all CSV at once (no chunking). If CSVs exceed API limits (~200k tokens), revisit with batching strategy.
- **Reference schema**: Fixed in env var (e.g., `REFERENCE_SCHEMA='{"name": "string", "email": "email", ...}'`). If schema needs to be per-request, modify endpoint to accept schema in POST body.
- **No auto-fix**: Anthropic flags issues but doesn't auto-correct. User reviews and decides action.

## Further Considerations

1. **Reference schema format**: How should it be structured? E.g., `{fieldName: type, ...}` or `{fields: [{name, type, required}, ...]}`. Recommend the simpler flat map unless you need more metadata.

2. **Static prompt**: The prompt is hardcoded in the code as a constant. If you need to adjust the prompt instructions or output format, update the constant directly.

3. **Future scaling**: If CSV files grow large (100k+ rows), consider:
   - Streaming rows to Anthropic in chunks
   - Sampling strategy (analyze 1st N rows + random sample)
   - Async processing (background job queue)

