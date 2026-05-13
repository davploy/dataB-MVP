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