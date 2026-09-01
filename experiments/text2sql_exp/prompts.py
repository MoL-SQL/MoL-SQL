"""
Prompt template for Text2SQL experiments.

Unified from Spider (generic SQLite), BIRD (IIF/SUBSTR + evidence + Chinese),
and BULL (generic SQLite) variants.  Dataset-specific few-shot examples are
loaded from external JSON files; defaults below cover the common case.
"""

from typing import Any, List, Optional, Tuple, Union

# A few-shot example is either ``(question, sql)`` or ``(question, sql, knowledge)``
# where ``knowledge`` is an optional string (BIRD-style evidence / a short hint).
FewShotExample = Union[Tuple[str, str], Tuple[str, str, Optional[str]]]


def _split_example(ex: Any) -> Tuple[str, str, Optional[str]]:
    """Normalize a few-shot example to ``(question, sql, knowledge|None)``."""
    if isinstance(ex, dict):
        q = ex.get("question", "")
        sql = ex.get("sql") or ex.get("query") or ex.get("sql_query") or ""
        k = ex.get("knowledge") or ex.get("evidence")
        return q, sql, (k or None)
    if isinstance(ex, (list, tuple)):
        if len(ex) >= 3:
            q, sql, k = ex[0], ex[1], ex[2]
            return q, sql, (k or None)
        if len(ex) == 2:
            return ex[0], ex[1], None
    return "", "", None


# ---------------------------------------------------------------------------
# Default few-shot examples (Spider-style generic + BIRD SQLite dialect)
# ---------------------------------------------------------------------------

DEFAULT_FEW_SHOT_SPIDER: List[Tuple[str, str]] = [
    ("How many singers do we have?", "SELECT count(*) FROM singer"),
    (
        "Show name, country, age for all singers ordered by age from the oldest to the youngest.",
        "SELECT name, country, age FROM singer ORDER BY age DESC",
    ),
    (
        "What are the names of all singers who have a song with more than 20 words?",
        "SELECT DISTINCT T2.name FROM song AS T1 JOIN singer AS T2 ON T1.singer_id = T2.singer_id WHERE T1.word_count > 20",
    ),
    (
        "What is the average age of singers by country?",
        "SELECT country, AVG(age) FROM singer GROUP BY country",
    ),
    (
        "List the name of the singer who has the most songs.",
        "SELECT name FROM singer WHERE singer_id = (SELECT singer_id FROM song GROUP BY singer_id ORDER BY count(*) DESC LIMIT 1)",
    ),
]

DEFAULT_FEW_SHOT_BIRD: List[Tuple[str, str]] = [
    (
        "What is the ratio of customers who pay in EUR against customers who pay in CZK?",
        "SELECT CAST(SUM(IIF(Currency = 'EUR', 1, 0)) AS FLOAT) / SUM(IIF(Currency = 'CZK', 1, 0)) AS ratio FROM customers",
    ),
    (
        "In 2012, who had the least consumption in LAM?",
        "SELECT T1.CustomerID FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment = 'LAM' AND SUBSTR(T2.Date, 1, 4) = '2012' GROUP BY T1.CustomerID ORDER BY SUM(T2.Consumption) ASC LIMIT 1",
    ),
    (
        "What was the average monthly consumption of customers in SME for the year 2013?",
        "SELECT AVG(T2.Consumption) / 12 FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE SUBSTR(T2.Date, 1, 4) = '2013' AND T1.Segment = 'SME'",
    ),
]

# Fallback for any dataset
DEFAULT_FEW_SHOT_EXAMPLES = DEFAULT_FEW_SHOT_SPIDER


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def build_text2sql_prompt(
    question: str,
    schema_desc: str,
    candidate_values: Optional[List[Tuple[str, str]]] = None,
    db_id: str = "",
    use_cot: bool = False,
    few_shot_examples: Optional[List[FewShotExample]] = None,
    evidence: Optional[str] = None,
    chinese_prompt: bool = False,
    prompt_mode: str = "none",
    output_style: str = "label",
    retrieved_values_text: Optional[str] = None,
) -> str:
    """Build the user prompt for Text2SQL.

    Parameters
    ----------
    question : str
        Natural-language question.
    schema_desc : str
        SQL-style CREATE TABLE schema + sample rows.
    candidate_values : list, optional
        Unused; kept for API compatibility.
    db_id : str, optional
        Database identifier (informational).
    use_cot : bool
        If *True*, request analysis before SQL. Ignored in ``output_style='xml'``
        because xml style always asks for both ``<cot>`` and ``<sql>`` blocks.
    few_shot_examples : list, optional
        Few-shot demonstration items. Each item may be a ``(question, sql)``
        tuple, a ``(question, sql, knowledge)`` tuple, or a dict with the
        ``question`` / ``sql`` (or ``query``/``sql_query``) / ``knowledge``
        (or ``evidence``) keys.
    evidence : str, optional
        BIRD-style evidence/rationale for the question.
    chinese_prompt : bool
        Use Chinese instruction text.
    prompt_mode : str
        Optional dataset-specific prompt note mode. ``"q_to_db"`` asks the
        model to rewrite the question into the schema/value language before
        emitting SQL. ``"baseline_cot"`` is Direct-ZS plus
        ``Please think step by step`` and ``<thinking>`` then ``<sql>``.
    output_style : str
        Response format: ``"label"`` (legacy ``Analysis:/SQL:`` / bare SQL) or
        ``"xml"`` (model responds with ``<sql>single-line SQL</sql>``; few-shots
        and the live question are wrapped in ``<question>``, optional
        ``<knowledge>``, ``<sql>`` tags). ``prompt_mode="baseline_cot"`` asks
        for ``<thinking>`` then ``<sql>``. ``prompt_mode="q_to_db"`` in xml
        style also asks for ``<rewritten_question>``. Generic ``<cot>`` is
        only added when ``use_cot=True``.
    retrieved_values_text : str, optional
        Preformatted target-database value-retrieval block inserted after
        the schema. Must not contain gold SQL or gold literals.
    """
    xml_mode = output_style == "xml"
    q_to_db_mode = prompt_mode == "q_to_db"
    baseline_cot_mode = prompt_mode == "baseline_cot"
    # Q-to-DB and Baseline-CoT use their own reasoning steps instead of
    # generic entity/filter CoT. XML controls the output tags.
    effective_use_cot = use_cot and not q_to_db_mode and not baseline_cot_mode
    if chinese_prompt:
        parts = [
            "请根据下面的问题生成一条 SQLite SQL 查询语句。",
            "注意：使用 SQLite 方言，例如 IIF（替代 IF）、SUBSTR、CAST 等。",
            "",
            "规则：",
            "- 对中文或包含非 ASCII 字符的表名/列名请使用反引号 `...` 包裹。",
            "- SQLite 中请使用 IIF(a,b,c) 替代 IF；使用 SUBSTR(str,start,len) 截取子串。",
            "",
        ]
    else:
        parts = [
            "Generate a SQLite SQL query for the following question.",
            "",
            "Rules:",
            "- Use backticks around table and column names that are Chinese or contain non-ASCII characters, e.g. `名称`, `歌手`, `年龄`.",
            "- Example: SELECT `姓名`, `年龄` FROM `歌手` WHERE `国籍` = 'France' ORDER BY `年龄` DESC",
            "- For SQLite: use IIF(a,b,c) instead of IF; SUBSTR(str,start,len) for substring.",
            "",
        ]

    if effective_use_cot:
        if chinese_prompt:
            parts.extend([
                "在编写 SQL 之前，请先简要分析：(1) 涉及的实体与表，(2) 约束/过滤条件，(3) 是否需要聚合或排序。然后再输出 SQL。",
                "",
            ])
        else:
            parts.extend([
                "Before writing SQL, briefly analyze: (1) entities and tables involved, (2) constraints/filters, (3) aggregation or ordering needed. Then output the SQL.",
                "",
            ])

    if q_to_db_mode:
        if chinese_prompt:
            parts.extend([
                "在编写 SQL 之前，请先把问题改写成与当前数据库一致的表述：",
                "- 实体/属性用词对齐 schema 中的表名和列名语言。",
                "- 字面值用词对齐样例行中的存储值语言。",
                "- 保持原问题意图不变，不要增删或改写约束。",
                "- 若问题已经与 schema 和取值语言一致，则原样抄写。",
                "然后根据改写后的问题写出一条 SQLite 查询。",
                "",
            ])
        else:
            parts.extend([
                "Before writing SQL, first rewrite the question into the language of this database:",
                "- Align entity and attribute wording with the table and column names in the schema.",
                "- Align literal wording with the stored values shown in the sample rows.",
                "- Keep the original intent unchanged; do not add, drop, or reinterpret constraints.",
                "- If the question is already aligned with the schema and values, copy it unchanged.",
                "Then write one SQLite query from the rewritten question.",
                "",
            ])

    if baseline_cot_mode:
        if chinese_prompt:
            parts.extend(["请一步一步思考。", ""])
        else:
            parts.extend(["Please think step by step.", ""])

    if few_shot_examples:
        parts.append("## 示例" if chinese_prompt else "## Examples")
        for ex in few_shot_examples:
            q, sql, knowledge = _split_example(ex)
            if xml_mode:
                parts.append(f"<question>{q}</question>")
                if knowledge:
                    parts.append(f"<knowledge>{knowledge}</knowledge>")
                parts.append(f"<sql>{sql}</sql>")
                parts.append("")
            elif chinese_prompt:
                parts.append(f"问题: {q}")
                if knowledge:
                    parts.append(f"知识: {knowledge}")
                parts.extend([f"SQL: {sql}", ""])
            else:
                parts.append(f"Question: {q}")
                if knowledge:
                    parts.append(f"Knowledge: {knowledge}")
                parts.extend([f"SQL: {sql}", ""])
        parts.append("")

    parts.extend([
        "## 数据库结构与样例数据" if chinese_prompt else "## Database schema and sample data",
        schema_desc.strip(),
        "",
    ])

    if retrieved_values_text:
        parts.extend([retrieved_values_text.strip(), ""])

    if prompt_mode == "bull":
        if chinese_prompt:
            parts.extend([
                "## BULL 专用提示",
                "- 涉及基金或股票时，如存在简称字段（例如 SecuAbbr、证券简称、所属基金/股票简称），优先使用简称；除非问题明确要求全称。",
                "- 涉及公司名称时，如存在简称字段（例如 ChiNameAbbr、中文名称缩写），优先使用简称；除非问题明确要求全称。",
                "",
            ])
        else:
            parts.extend([
                "## BULL-specific note",
                "- For funds and stocks, use abbreviation columns when available, such as SecuAbbr, 证券简称, or 所属基金/股票简称, unless the question explicitly asks for the full name.",
                "- For companies, use abbreviation columns when available, such as ChiNameAbbr or 中文名称缩写, unless the question explicitly asks for the full name.",
                "",
            ])

    parts.append("## 问题" if chinese_prompt else "## Question")
    if xml_mode:
        parts.append(f"<question>{question.strip()}</question>")
        if evidence:
            parts.append(f"<knowledge>{evidence.strip()}</knowledge>")
        parts.append("")
    else:
        parts.extend([question.strip(), ""])
        if evidence:
            parts.extend([
                "## 该问题的证据" if chinese_prompt else "## Evidence for this question",
                evidence.strip(),
                "",
            ])

    if q_to_db_mode and xml_mode:
        if chinese_prompt:
            parts.extend([
                "## 你的回复",
                "请严格按以下 XML 标签输出（不要使用 markdown 代码块，标签外不要有其它内容）：",
                "<rewritten_question>改写后的问题，对齐 schema 与取值语言</rewritten_question>",
                "<sql>单行 SQL</sql>",
                "",
            ])
        else:
            parts.extend([
                "## Your response",
                "Respond using exactly the following XML tags (no markdown fences, no extra text outside the tags):",
                "<rewritten_question>question rewritten into the schema and value language</rewritten_question>",
                "<sql>single-line SQL</sql>",
                "",
            ])
    elif q_to_db_mode:
        if chinese_prompt:
            parts.extend([
                "## 你的回复",
                "先改写问题，再输出单行 SQL。",
                "格式：",
                "RewrittenQuestion: ...",
                "SQL: <single line SQL>",
                "",
            ])
        else:
            parts.extend([
                "## Your response",
                "First rewrite the question, then output the SQL on a single line.",
                "Format:",
                "RewrittenQuestion: ...",
                "SQL: <single line SQL>",
                "",
            ])
    elif baseline_cot_mode:
        if chinese_prompt:
            parts.extend([
                "## 你的回复",
                "请严格按以下 XML 标签输出（不要使用 markdown 代码块，标签外不要有其它内容）：",
                "<thinking>...</thinking>",
                "<sql>单行 SQL</sql>",
                "",
            ])
        else:
            parts.extend([
                "## Your response",
                "Respond using exactly the following XML tags (no markdown fences, no extra text outside the tags):",
                "<thinking>...</thinking>",
                "<sql>single-line SQL</sql>",
                "",
            ])
    elif xml_mode:
        if chinese_prompt:
            response = [
                "## 你的回复",
                "请严格按以下 XML 标签输出（不要使用 markdown 代码块，标签外不要有其它内容）：",
            ]
            if use_cot:
                response.append("<cot>简短分析：实体/表、约束/过滤、聚合或排序。</cot>")
            response.extend(["<sql>单行 SQL</sql>", ""])
            parts.extend(response)
        else:
            response = [
                "## Your response",
                "Respond using exactly the following XML tags (no markdown fences, no extra text outside the tags):",
            ]
            if use_cot:
                response.append(
                    "<cot>Short analysis: entities/tables, constraints/filters, aggregation or ordering.</cot>"
                )
            response.extend(["<sql>single-line SQL</sql>", ""])
            parts.extend(response)
    elif use_cot:
        if chinese_prompt:
            parts.extend([
                "## 你的回复",
                "先给出简短分析（实体、约束、逻辑），再输出单行 SQL。",
                "格式：", "Analysis: ...", "SQL: <single line SQL>", "",
            ])
        else:
            parts.extend([
                "## Your response",
                "First give a short analysis (entities, constraints, logic), then output the SQL on a single line.",
                "Format:", "Analysis: ...", "SQL: <single line SQL>", "",
            ])
    else:
        parts.extend([
            "## SQL（单行、不要 markdown；中文/非 ASCII 标识符用反引号）"
            if chinese_prompt
            else "## SQL (single line, no markdown; quote Chinese/non-ASCII identifiers with backticks)",
            "",
        ])

    return "\n".join(parts)
