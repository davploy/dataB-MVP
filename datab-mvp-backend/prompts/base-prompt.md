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

For outlier detection:
- For each numerical column, calculate mean and standard deviation
- Flag any row where a value is >2 standard deviations from the mean as an outlier
- Include the row index (0-based) and the column name
- Provide reasoning for each outlier (e.g., "Row 3, column 'sales': 450 is 2.8σ above mean of 150")

Return a JSON object with this structure:
{{
    "schema": [{"name": "field1", "type": "string", "sample": "value"}, ...],
    "rows": [parsed data rows as objects],
    "issues": [{"row": N, "field": "name", "issue": "description", "severity": "error|warning"}],
    "outliers": {{
        "detected": [
            {{"row_index": 0, "column": "column_name", "value": actual_value, "z_score": 2.5, "reasoning": "explanation"}}
        ],
        "numerical_columns": ["column1", "column2"]
    }}
}}

Return ONLY valid JSON, no markdown formatting, no ```json markers, no preamble or explanation. Start directly with { and end with }."""