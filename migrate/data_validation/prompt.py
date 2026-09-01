NL2SQL_BUGS_PROMPT = """
You are a SQL expert. Your task is to evaluate whether a given SQL query correctly aligns with the natural language query (NL), evidence, and database schema. Additionally, if the SQL query is wrong, you need to identify the specific error type and subtype.

When analyzing SQL errors, please categorize them according to the following taxonomy:
### Error Types Description:
Note: In SQLite, attribute and table names are case-insensitive (e.g., `TableName` and `tablename`, `ColumnName` and `columnname` refer to the same table/column). Do not flag an Attribute Mismatch or Table Mismatch solely due to differing letter case.

1. Attribute-Related Errors:
- Attribute Mismatch: Wrong attribute selection
- Attribute Redundancy: Unnecessary attributes included
- Attribute Missing: Required attributes not included

2. Table-Related Errors:
- Table Mismatch: Wrong table selection
- Table Redundancy: Unnecessary tables included
- Table Missing: Required tables not included
- Join Condition Mismatch: The join condition between tables is incorrect, If the [attribute][operator][attribute] is incorrectly chosen,the error should be classified as a "Join Condition Mismatch" rather than an "Attribute Mismatch."
- Join Type Mismatch: Wrong join type (e.g., LEFT JOIN when INNER JOIN needed)

3. Value-Related Errors:
- Value Mismatch: Incorrect values in conditions
- Data Format Mismatch: Wrong data type or format

4. Operator-Related Errors:
- Comparison Operator Mismatch: Wrong operator (e.g., = when != needed) in comparison condition.
- Logical Operator Mismatch: The logical operator (e.g., AND when OR needed) or the logical operator precedence may be wrong(e.g., (A AND B) OR C is interpreted as (A OR C) AND (B OR C) instead of (A AND B) OR C).

5. Condition-Related Errors:
- Explicit Condition Missing: Required conditions not included
- Explicit Condition Mismatch: Wrong conditions (condition= [attribute] [operator] [value] only two of them are wrong, if only one is wrong, it is should be attribute or value or operator error)
- Explicit Condition Redundancy: Unnecessary conditions
- Implicit Condition Missing: Missing implicit conditions (e.g., IS NOT NULL)

6. Function-Related Errors:
- Aggregate Functions: Incorrect use of SUM, AVG, etc.
- Window Functions: Incorrect use of OVER, PARTITION BY, etc.
- Date/Time Functions: Incorrect use of JULIANDAY, strftime, etc.
- Conversion Functions: Incorrect use of CAST, etc.
- Math Functions: Incorrect use of ROUND, etc.
- String Functions: Incorrect use of SUBSTR, etc.
- Conditional Functions: Incorrect use of IIF, CASE WHEN, etc.

7. Clause-Related Errors:
- Clause Missing: Required clauses not included. (e.g., GROUP BY, ORDER BY, HAVING)
- Clause Redundancy: Unnecessary clauses included. (e.g., GROUP BY, ORDER BY, HAVING)

8. Subquery-Related Errors:
- Subquery Missing: Required subquery not included.
- Subquery Mismatch: Incorrect subquery logic
- Partial Query: The error SQL query is a partial query that contributes to the cor SQL query.

9. Other Errors:
- ASC/DESC: Incorrect sorting order
- DISTINCT: Incorrect use of DISTINCT
- Other: Major logical errors requiring complete rewrite

### Evaluation Criteria:
    1. Semantic Error Detection: Indicate if the SQL query is "True" (correct) or "False" (contains errors).
    2. Semantic Error Type Detection: If the query is incorrect, specify the main error type (e.g., Table-Related Errors) and subtype (e.g., Table Mismatch). If there are multiple errors, return all the errors in the "error_types" list.
    3. Provide a brief explanation for your decision, referencing the NL query, evidence, and database schema as needed.

### Reasoning Style (IMPORTANT):
    Keep the "reasoning" short, factual, and easy to follow. Follow these rules:
    - Limit it to at most 3 short sentences (roughly 60 words total).
    - Sentence 1: state the intent of the NL query in a few words.
    - Sentence 2+: name the concrete mismatch(es), citing the exact clause/column/value that is wrong and what it should be. If correct, say so in one sentence.
    - Do NOT think out loud, hedge, or go back and forth (no "but wait", "however, on the other hand", "let me reconsider"). State your final judgment directly.
    - Do NOT restate the taxonomy, repeat the case-insensitivity rule, or list every error type you ruled out. Only mention what is actually relevant.

### Revised SQL:
    Also return a "revised_sql" field:
    - If "result" is "False", provide a corrected SQL query that fixes every identified error and faithfully answers the NL query.
    - If "result" is "True", repeat the original SQL query unchanged.

### Input:
    - Database schema: {schema}
    - Natural language query: {nl}
    - Evidence: {evidence}
    - SQL query: {sql}
    - SQL execution result: {exec_result}

### Output:
    Please output the result in the following format and ensure that error_types strictly adhere to the definitions in the taxonomy:
    {{
        "reasoning": "<brief reasoning, at most 3 sentences>",
        "result": "<True or False>",
        "error_types": [
            {{
                "error_type": "<main error type>",
                "sub_error_type": "<sub error type>"
            }},
            {{
                "error_type": "<main error type>",
                "sub_error_type": "<sub error type>"
            }}
        ],
        "revised_sql": "<corrected SQL if result is False, otherwise the original SQL>"
    }}"""


REVISE_EMPTY_SQL_PROMPT = """
You are a SQL and data-annotation expert. The natural-language question (NL) below is paired with a gold SQL query, but executing that SQL against the database has an execution issue: {exec_issue}. Samples with execution errors or empty results are not useful for text-to-SQL evaluation.

Your task is to revise the QUESTION and the SQL TOGETHER so that:
1. The revised SQL returns a NON-EMPTY result (at least one row) when executed against this database.
2. The revised question and the revised SQL stay faithfully aligned with each other (the SQL must be a correct answer to the revised question).
3. The revision stays as close as possible to the original intent and structure. Prefer minimal edits: usually it is enough to change a literal value in a WHERE condition (e.g. a name, id, date, or category) to one that actually exists in the data, and update the question to match that value. Only restructure the query if no small value change can make it non-empty.
4. The revised question is fluent and natural in the SAME language as the original question (e.g. keep Chinese questions in Chinese).

Use the provided database schema and sample rows to pick literal values that genuinely exist in the tables so the revised SQL is guaranteed to return rows.

### Input:
    - Database schema (with sample rows): {schema}
    - Original natural language query: {nl}
    - Original SQL query: {sql}
    - Execution issue: {exec_issue}

### Output:
    Output ONLY a JSON object in the following format:
    {{
        "reasoning": "<at most 2 short sentences: why the original had an execution issue and what you changed>",
        "revised_question": "<the revised natural language question, in the original language>",
        "revised_sql": "<the revised SQL query that returns a non-empty result>"
    }}"""