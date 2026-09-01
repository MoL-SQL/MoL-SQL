"""
Prompt templates for database schema and content translation (EN ↔ CN).

Each category has an EN-to-CN and a CN-to-EN variant.
"""

import json

# ===========================================================================
# Schema translation — EN → CN
# ===========================================================================

SCHEMA_EN2CN_EXAMPLE_INPUT = json.dumps({
    "table_names": ["department", "instructor"],
    "column_names": [
        [-1, "*"],
        [0, "dept_name"], [0, "building"], [0, "budget"],
        [1, "ID"], [1, "name"], [1, "dept_name"], [1, "salary"]
    ]
}, ensure_ascii=False)

SCHEMA_EN2CN_EXAMPLE_OUTPUT = json.dumps({
    "table_names": ["学院", "讲师"],
    "column_names": [
        [-1, "*"],
        [0, "学院"], [0, "办公楼"], [0, "预算"],
        [1, "工号"], [1, "姓名"], [1, "学院"], [1, "薪资"]
    ]
}, ensure_ascii=False, indent=2)

SCHEMA_PROMPT_EN2CN = """
You are an expert database engineer and linguist. Your task is to translate an English SQL database schema into Chinese.

### Instructions:
1. Translate both 'table_names' and 'column_names' into professional Chinese database terminology.
2. Ensure the translations are natural-sounding and keep the original meaning as accurate as possible.
3. Consider the entire schema for related entities. 
- If exact same column name appears in different tables, you should translate them to the same name. For example, column "account_id" can be found in table "order", table "loan" and table "trans", you should always translate "account_id" to "账户编号". Also, if "name" appears in table "student" and table "teacher", you should always translate "name" to "姓名".
- If similar column but not exact same names appear in same table, you should translate them to different names. For example, column "name" can be translated to "姓名", but if column "lname" and "fname" are both present, you should translate them to "姓" and "名" respectively.
- If similar but not exact same column names appear in multiple tables, you should translate them to different names. For example, column "District" in table "City" （means "城市的一个行政区"） and column "Region" in table "Country" （means "国家的一个区域"）should be translated differently. "District" in "City" should be translated to "行政区", while "Region" in "Country" should be translated to "区域".
4. If an entity is a proper noun (e.g. a brand name or a specific abbreviation that usually keeps in English), you may keep it as is. For example, in football, "B365H" should be kept as is. Also, in airport code, "HKG" should be kept as is.
5. Maintain a 1:1 mapping structure so the results can be used to programmatically rename the schema.
6. Return ONLY a valid JSON object.

### Example Input:
{example_input}

### Example Output:
{example_output}

### Current INPUT:
{current_input}

### OUTPUT (JSON):
"""

CONTENT_PROMPT_EN2CN = """
You are a professional translator specializing in data localization. Translate the following unique values from the English database '{db_id}' into Chinese.

### Context:
- These values are shared across the following table(s) and column(s) (including primary/foreign keys):
{context_str}

### Instructions:
1. Provide a contextually accurate Chinese translation for each value.
2. CRITICAL: Each translated value must be unique — no two different original values should map to the same Chinese translation. If two values would naturally translate to the same Chinese term, keep the less common or ambiguous one in its original English form to preserve distinctness.
3. When to keep values without translation:
- If a value is a proper noun (like a brand or a specific technical/abbreviation term) that is commonly kept in English, you should keep it as is.  For example, in football, "B365H" should be kept as is. Also, as airport code, "HKG" should be kept as is.
- If a value appears to be corrupted, truncated, or garbled data (e.g., a meaningless fragment like "stoc", "le", "y", "norm" that looks like a partial/broken string rather than a real word), keep it as is without translating. Do NOT guess what the original word might have been.
- If a value is a single letter or a single number, keep it as is. For example, "A" should be kept as is; "1993" should be kept as is;
- If a value is a single color code, keep it as is. For example, "B, R, G" should be kept as it is.
- If a value is a single date or time, keep it as is. For example, "2026-04-15" or "12:00:00" should be kept as it is.
4. Return the result as a JSON dictionary where the keys are the original English values and the values are the Chinese translations.

### Values to Translate:
{values}

### OUTPUT (JSON):
"""

# ===========================================================================
# Schema translation — CN → EN
# ===========================================================================

SCHEMA_CN2EN_EXAMPLE_INPUT = json.dumps({
    "table_names": ["学院", "讲师"],
    "column_names": [
        [-1, "*"],
        [0, "学院"], [0, "办公楼"], [0, "预算"],
        [1, "工号"], [1, "姓名"], [1, "学院"], [1, "薪资"]
    ]
}, ensure_ascii=False)

SCHEMA_CN2EN_EXAMPLE_OUTPUT = json.dumps({
    "table_names": ["department", "instructor"],
    "column_names": [
        [-1, "*"],
        [0, "dept_name"], [0, "building"], [0, "budget"],
        [1, "ID"], [1, "name"], [1, "dept_name"], [1, "salary"]
    ]
}, ensure_ascii=False, indent=2)

SCHEMA_PROMPT_CN2EN = """
You are an expert database engineer and linguist. Your task is to translate a Chinese SQL database schema into English.

### Instructions:
1. Translate both 'table_names' and 'column_names' into professional English database terminology (lowercase_snake_case preferred).
2. Ensure the translations are natural-sounding and keep the original meaning as accurate as possible.
3. Consider the entire schema for related entities.
- If the exact same column name appears in different tables, you should translate them to the same name. For example, column "账户编号" can be found in table "订单", table "贷款" and table "交易", you should always translate "账户编号" to "account_id". Also, if "姓名" appears in table "学生" and table "教师", you should always translate "姓名" to "name".
- If similar but not exact same column names appear in the same table, you should translate them to different names. For example, column "姓名" can be translated to "name", but if column "姓" and "名" are both present, you should translate them to "lname" and "fname" respectively.
- If similar but not exact same column names appear in multiple tables, you should translate them to different names. For example, column "行政区" in table "城市" (means "a district within a city") and column "区域" in table "国家" (means "a region within a country") should be translated differently. "行政区" in "城市" should be translated to "district", while "区域" in "国家" should be translated to "region".
4. If an entity is already in English, is a well-known abbreviation, or is a proper noun that is commonly kept as is, keep it unchanged. For example, "B365H" should be kept as is. Also, airport code "HKG" should be kept as is.
5. Maintain a 1:1 mapping structure so the results can be used to programmatically rename the schema.
6. Return ONLY a valid JSON object.

### Example Input:
{example_input}

### Example Output:
{example_output}

### Current INPUT:
{current_input}

### OUTPUT (JSON):
"""

CONTENT_PROMPT_CN2EN = """
You are a professional translator specializing in data localization. Translate the following unique values from the Chinese database '{db_id}' into English.

### Context:
- These values are shared across the following table(s) and column(s) (including primary/foreign keys):
{context_str}

### Instructions:
1. Provide a contextually accurate English translation for each value.
2. CRITICAL: Each translated value must be unique — no two different original values should map to the same English translation. If two values would naturally translate to the same English term, keep the less common or ambiguous one in its original Chinese form to preserve distinctness.
3. When to keep values without translation:
- If a value is already in English or is a well-known proper noun / abbreviation, keep it as is. For example, "B365H" should be kept as is. Also, airport code "HKG" should be kept as is.
- If a value appears to be corrupted, truncated, or garbled data (e.g., a meaningless fragment that looks like a partial/broken string rather than a real word), keep it as is without translating. Do NOT guess what the original word might have been.
- If a value is a single letter or a single number, keep it as is. For example, "A" should be kept as is; "1993" should be kept as is.
- If a value is a single color code, keep it as is. For example, "B, R, G" should be kept as is.
- If a value is a single date or time, keep it as is. For example, "2026-04-15" or "12:00:00" should be kept as is.
4. Return the result as a JSON dictionary where the keys are the original Chinese values and the values are the English translations.

### Values to Translate:
{values}

### OUTPUT (JSON):
"""

# Backward-compatible aliases (old names used by other modules)
SCHEMA_PROMPT_TEMPLATE = SCHEMA_PROMPT_EN2CN
SCHEMA_EXAMPLE_INPUT = SCHEMA_EN2CN_EXAMPLE_INPUT
SCHEMA_EXAMPLE_OUTPUT = SCHEMA_EN2CN_EXAMPLE_OUTPUT
CONTENT_PROMPT_TEMPLATE = CONTENT_PROMPT_EN2CN


# ===========================================================================
# NL question translation (already bidirectional)
# ===========================================================================

EXAMPLE_EN2CN_NL = [
    {
        "input": {
            "original_sql": "SELECT T2.name , count(*) FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id GROUP BY T1.stadium_id",
            "original_question": "Show the stadium name and the number of concerts in each stadium.",
            "current_sql": "SELECT T2.`名称` , count(*) FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号` = T2.`体育场编号` GROUP BY T1.`体育场编号`",
        },
        "output": {"current_question": "显示每个体育场的名称及其每个体育场举办的音乐会数量。"},
    },
    {
        "input": {
            "original_sql": "SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat' OR T3.pettype = 'dog'",
            "original_question": "Find the first name of students who have cat or dog pet.",
            "current_sql": "SELECT DISTINCT T1.`名` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号` = T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号` = T2.`宠物编号` WHERE T3.`宠物类型` = '猫' OR T3.`宠物类型` = '狗'",
        },
        "output": {"current_question": "查找养猫或养狗的学生的名。"},
    },
    {
        "input": {
            "original_sql": "SELECT stuid FROM student EXCEPT SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat'",
            "original_question": "What are the ids of the students who do not own cats as pets?",
            "current_sql": "SELECT `学生编号` FROM `学生` EXCEPT SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号` = T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号` = T2.`宠物编号` WHERE T3.`宠物类型` = '猫'",
        },
        "output": {"current_question": "没有养猫作为宠物的学生编号有哪些？"},
    },
    {
        "input": {
            "original_sql": "SELECT Abbreviation FROM AIRLINES WHERE Airline = 'JetBlue Airways'",
            "original_question": "Which abbreviation corresponds to Jetblue Airways?",
            "current_sql": "SELECT `缩写` FROM `航空公司` WHERE `航空公司名称` = '捷蓝航空'",
        },
        "output": {"current_question": "哪家航空公司的缩写是捷蓝航空？"},
    },
]

EXAMPLE_CN2EN_NL = [
    {
        "input": {
            "original_sql": "SELECT T2.`名称` , count(*) FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号` = T2.`体育场编号` GROUP BY T1.`体育场编号`",
            "original_question": "显示每个体育场的名称及其每个体育场举办的音乐会数量。",
            "current_sql": "SELECT T2.name , count(*) FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id GROUP BY T1.stadium_id",
        },
        "output": {"current_question": "Show the name of each stadium and the number of concerts held in each stadium."},
    },
    {
        "input": {
            "original_sql": "SELECT DISTINCT T1.`名` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号` = T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号` = T2.`宠物编号` WHERE T3.`宠物类型` = '猫' OR T3.`宠物类型` = '狗'",
            "original_question": "查找养猫或养狗的学生的名。",
            "current_sql": "SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat' OR T3.pettype = 'dog'",
        },
        "output": {"current_question": "Find the first name of students who have a cat or a dog as a pet."},
    },
    {
        "input": {
            "original_sql": "SELECT `学生编号` FROM `学生` EXCEPT SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号` = T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号` = T2.`宠物编号` WHERE T3.`宠物类型` = '猫'",
            "original_question": "没有养猫作为宠物的学生编号有哪些？",
            "current_sql": "SELECT stuid FROM student EXCEPT SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat'",
        },
        "output": {"current_question": "What are the stuids of the students who do not own a cat as a pet?"},
    },
    {
        "input": {
            "original_sql": "SELECT `缩写` FROM `航空公司` WHERE `航空公司名称` = '捷蓝航空'",
            "original_question": "哪家航空公司的缩写是捷蓝航空？",
            "current_sql": "SELECT Abbreviation FROM AIRLINES WHERE Airline = 'JetBlue Airways'",
        },
        "output": {"current_question": "What is the Abbreviation of the airline JetBlue Airways?"},
    },
]

# ---------------------------------------------------------------------------
# Prompt headers. The full prompt (header + few-shot examples + current input)
# is assembled via ``build_nl_translate_prompt`` below so that the JSON braces
# in examples don't clash with ``str.format`` placeholders.
# ---------------------------------------------------------------------------

NL_TRANSLATE_EN2CN_HEADER = """You translate English natural-language questions into Chinese for a cross-language text-to-SQL setting.

Each item has three inputs:
- ``original_sql``: the English SQL written against an English schema.
- ``original_question``: the English question the user originally asked.
- ``current_sql``: the equivalent Chinese SQL written against the translated Chinese schema (table/column names are backtick-quoted and typically non-ASCII).

Your job is to produce ``current_question``: a natural Chinese question that matches the meaning of ``original_question`` but whose noun phrases align with the identifiers and literal values used in ``current_sql``.

### Instructions
1. Preserve the exact intent of the original question — do not add, drop, or re-interpret information. Especially if the original question is not clear comparing to the SQL, you should not add SQL-related information to the translated question.
2. Use fluent, natural Chinese. Prefer wording that a Chinese speaker would use when reading ``current_sql``.
3. Match the Chinese identifiers in ``current_sql`` for column/table phrases (e.g. if the SQL selects `` `名称` `` then say "名称", not "名字"; if it selects `` `名` `` distinguished from `` `姓` `` then say "名", not the generic "名字").
4. Match the Chinese literal values in ``current_sql`` (e.g. "捷蓝航空" instead of transliterating "JetBlue Airways" differently).
5. Keep proper nouns or codes (e.g. airport codes, stock tickers) unchanged when ``current_sql`` keeps them unchanged.
6. Return ONLY a JSON object of the form ``{"current_question": "<Chinese question>"}`` with no extra commentary, no markdown fences."""

NL_TRANSLATE_CN2EN_HEADER = """You translate Chinese natural-language questions into English for a cross-language text-to-SQL setting.

Each item has three inputs:
- ``original_sql``: the Chinese SQL written against a Chinese schema (backtick-quoted non-ASCII identifiers).
- ``original_question``: the Chinese question the user originally asked.
- ``current_sql``: the equivalent English SQL written against the translated English schema.

Your job is to produce ``current_question``: a natural English question that matches the meaning of ``original_question`` but whose noun phrases align with the identifiers and literal values used in ``current_sql``.

### Instructions
1. Preserve the exact intent of the original question — do not add, drop, or re-interpret information. Especially if the original question is not clear comparing to the SQL, you should not add SQL-related information to the translated question.
2. Use fluent, natural English. Prefer wording that an English speaker would use when reading ``current_sql``.
3. Match the English identifiers in ``current_sql`` for column/table phrases (e.g. if the SQL selects ``Fname`` distinguished from ``Lname`` then say "first name", not a generic "name"; if the SQL selects ``stuid`` then say "stuid" or "student id" consistently with the column).
4. Match the English literal values in ``current_sql`` (e.g. "JetBlue Airways" rather than re-translating "捷蓝航空").
5. Keep proper nouns or codes unchanged when ``current_sql`` keeps them unchanged.
6. Return ONLY a JSON object of the form ``{"current_question": "<English question>"}`` with no extra commentary, no markdown fences."""


NL_TRANSLATE_CN2EN_NO_SQL_HEADER = """You translate Chinese text2sql questions into English.

Each item has one input:
- ``original_question``: the Chinese text2sql question.

Your job is to produce ``current_question``: a natural English text2sql question.

### Instructions
1. Preserve the meaning of ``original_question`` as closely as possible. Do not add or drop constraints, entities, or conditions.
2. Keep the question fluent and natural in English.
3. Keep proper nouns, abbreviations, codes, numbers, and dates faithful to the original wording.
4. This is question-only translation. Do not mention SQL, schema, table names, column names, or any explanation.
5. Return ONLY a JSON object of the form ``{"current_question": "<English question>"}`` with no extra commentary, no markdown fences."""

NL_TRANSLATE_EN2CN_NO_SQL_HEADER = """You translate English text2sql questions into Chinese.

Each item has one input:
- ``original_question``: the English text2sql question.

Your job is to produce ``current_question``: a natural Chinese text2sql question.

### Instructions
1. Preserve the meaning of ``original_question`` as closely as possible. Do not add or drop constraints, entities, or conditions.
2. Keep the question fluent and natural in Chinese.
3. Keep proper nouns, abbreviations, codes, numbers, and dates faithful to the original wording.
4. This is question-only translation. Do not mention SQL, schema, table names, column names, or any explanation.
5. Return ONLY a JSON object of the form ``{"current_question": "<Chinese question>"}`` with no extra commentary, no markdown fences."""

EXAMPLE_CN2EN_NL_BULL = [
    {
        "input": {
            "original_question": "显示指标周期为\"一个月\"的基金收益为正的基金数目，按基金类别分组展示"
        },
        "output": {
            "current_question": "Show the number of funds with positive fund return and index cycle '一个月', grouped by fund type name."
        },
    },
    {
        "input": {
            "original_question": "北京银行股份有限公司托管了哪些基金管理人的基金？"
        },
        "output": {
            "current_question": "Which fund investment advisors have funds custodied by Beijing Bank Co., Ltd.?"
        },
    },
    {
        "input": {
            "original_question": "哪些股东2020年的持股数量在1千万以上，列出这些股东名称"
        },
        "output": {
            "current_question": "Which shareholders have a holding sum greater than 10000000 in 2020? List these shareholder names."
        },
    },
    {
        "input": {
            "original_question": "2010年至今，有哪些基金获得过\"中国证券报\"设立的奖项"
        },
        "output": {
            "current_question": "Which funds have received awards established by China Securities Journal from 2010 to present?"
        },
    },
]

EXAMPLE_CN2EN_NL_TACO = [
    {
        "input": {
            "original_question": "李明咨询，想了解2019年至2023年期间本市所有公交企业的信誉得分和检查记录，特别关注那些信誉得分低于60分且至少有两次检查记录不合格的企业。他希望通过这些数据来识别出合规性较差的企业，以便为即将到来的年度评估报告做好准备，并提出相应的改进建议，提升公交服务质量。"
        },
        "output": {
            "current_question": "Li Ming is inquiring about the credit scores and inspection records of all public transport companies in the city from 2019 to 2023. He is particularly focused on companies with scores below 60 and at least two failed inspections. His goal is to use this data to identify non-compliant operators, prepare for the upcoming annual assessment report, and propose improvements to enhance the quality of public transport services."
        },
    },
    {
        "input": {
            "original_question": "需要查询本市所有驾驶培训机构的完整名单及详细信息，包括机构名称、法定代表人、统一社会信用代码、办学地址和联系电话，确保数据全面准确，以便后续进行资质核查和行业管理。"
        },
        "output": {
            "current_question": "A comprehensive list and detailed information of all driving training institutions in the city are required, including the institution name, legal representative, Unified Social Credit Code, school address, and contact number. It is essential to ensure the data is complete and accurate to facilitate subsequent qualification verification and industry management."
        },
    },
    {
        "input": {
            "original_question": "我是市交通管理局的工作人员李明，今天需要一份最新的驾驶培训机构名单，包含所有在册的机构名称、法定代表人和训练场地地址，别漏了任何一家，我们要用这份资料来做年度资质复核和后续管理，麻烦帮忙尽快提供完整且最新的驾培机构基本信息，谢谢。"
        },
        "output": {
            "current_question": "I am Li Ming from the Municipal Bureau of Transportation. I require the latest list of all registered driving training institutions, including their names, legal representatives, and training site addresses. Please ensure no entities are omitted, as this data is essential for our annual qualification review and ongoing management. I would appreciate it if you could provide this complete and up-to-date information as soon as possible. Thank you."
        },
    },
]

EXAMPLE_EN2CN_NL_LOGICCAT = [
    {
        "input": {
            "original_question": "If a Robinson R-22 helicopter has a total rotor disc area of 46.2 square meters and a maximum rotor disc loading of 14 kilograms per square meter, what is its lift under maximum gross weight?"
        },
        "output": {
            "current_question": "如果一架罗宾逊 R-22 直升机的旋翼圆盘总面积为 46.2 平方米，且最大旋翼圆盘载荷为 14 千克/平方米，那么在最大总重下它的升力是多少？"
        },
    },
    {
        "input": {
            "original_question": "Assuming a Robinson R-22 aircraft has a maximum gross weight of 635 kg, a total rotor disc area of 46.2 square meters, and a maximum rotor disc loading of 14 kg/square meter. If the aircraft's weight increases by 20%, what is the new maximum rotor disc loading?"
        },
        "output": {
            "current_question": "假设一架罗宾逊 R-22 直升机的最大总重为 635 千克，旋翼圆盘总面积为 46.2 平方米，最大旋翼圆盘载荷为 14 千克/平方米。如果该航空器的重量增加 20%，那么新的最大旋翼圆盘载荷是多少？"
        },
    },
    {
        "input": {
            "original_question": "如果一架罗宾逊 R-22 航空器的最大总重为 635 千克，旋翼圆盘总面积为 46.2 平方米，且已知其最大圆盘载荷，那么该航空器是否适合在高原地区飞行？"
        },
        "output": {
            "current_question": "罗宾逊R-22飞机的最大旋翼载荷乘以总旋翼面积再乘以0.75后若小于最大起飞重量，则为不适宜，否则为适宜。该飞机是否适宜在高原地区飞行？"
        },
    },
]

EXAMPLE_EN2CN_NL_KAGGLE = [
    {
        "input": {
            "original_question": "Which country is Kaiga-4 built in?"
        },
        "output": {
            "current_question": "Kaiga-4 建于哪个国家？"
        },
    },
    {
        "input": {
            "original_question": "which pesticides are most used?"
        },
        "output": {
            "current_question": "哪些农药使用得最多？"
        },
    },
    {
        "input": {
            "original_question": "What are the top five states in descending order in terms of revenue provided to school districts?"
        },
        "output": {
            "current_question": "按提供给学区的收入降序排列，前五个州是哪些？"
        },
    },
]

EXAMPLE_EN2CN_NL_BIRD = [
    {
        "input": {
            "original_question": "What is the ratio of customers who pay in EUR against customers who pay in CZK?"
        },
        "output": {
            "current_question": "以欧元付款的客户数量与以捷克克朗付款的客户数量之比是多少？"
        },
    },
    {
        "input": {
            "original_question": "How many members attended the \"Women's Soccer\" event?"
        },
        "output": {
            "current_question": "有多少成员出席了\"Women's Soccer\"活动？"
        },
    },
    {
        "input": {
            "original_question": "Please list the names of the players whose volley score and dribbling score are over 70."
        },
        "output": {
            "current_question": "请列出凌空抽射得分和盘带得分均超过70的球员姓名。"
        },
    },
    {
        "input": {
            "original_question": "What is the complete address of the school with the lowest excellence rate? Indicate the Street, City, Zip and State."
        },
        "output": {
            "current_question": "卓越率最低的学校的完整地址是什么？请指出街道、城市、州和邮政编码。"
        },
    },
]

EXAMPLE_EN2CN_NL_SPIDER = [
    {
        "input": {
            "original_question": "How many singers do we have?"
        },
        "output": {
            "current_question": "我们有多少位歌手？"
        },
    },
    {
        "input": {
            "original_question": "Show name, country, age for all singers ordered by age from the oldest to the youngest."
        },
        "output": {
            "current_question": "显示所有歌手的姓名、国籍和年龄，并按年龄从大到小排序。"
        },
    },
    {
        "input": {
            "original_question": "Show location and name for all stadiums with a capacity between 5000 and 10000."
        },
        "output": {
            "current_question": "显示容量在5000到10000之间的所有体育场的所在地和名称。"
        },
    },
    {
        "input": {
            "original_question": "Return the name of the airport with code 'AKO'."
        },
        "output": {
            "current_question": "机场代码为'AKO'的机场名称是什么？"
        },
    },
]

EXAMPLE_EN2CN_NL_EHRSQL = [
    {
        "input": {
            "original_question": "Can you tell me the change in bedside glucose values for patient 027-136480 measured at 2105-12-31 10:58:09 compared to the value measured at 2105-12-30 16:58:09?"
        },
        "output": {
            "current_question": "患者027-136480在2105-12-31 10:58:09测得的床旁血糖值与2105-12-30 16:58:09测得的数值相比，变化是多少？"
        },
    },
    {
        "input": {
            "original_question": "What is the name of the drug that has been prescribed to patient 009-11591 two or more times?"
        },
        "output": {
            "current_question": "被开具给患者009-11591两次或以上的药物名称是什么？"
        },
    },
    {
        "input": {
            "original_question": "What is the name of the procedure that was performed two times in 12/2105 on patient 004-64091?"
        },
        "output": {
            "current_question": "在2105年12月对患者004-64091执行了两次的操作名称是什么？"
        },
    },
]


def _render_nl_example(example):
    return (
        "Input:\n"
        + json.dumps(example["input"], ensure_ascii=False, indent=2)
        + "\nOutput:\n"
        + json.dumps(example["output"], ensure_ascii=False, indent=2)
    )


def _to_question_only_examples(examples):
    """Convert full examples into question-only examples."""
    return [
        {
            "input": {"original_question": ex["input"]["original_question"]},
            "output": {"current_question": ex["output"]["current_question"]},
        }
        for ex in examples
    ]


def build_nl_translate_prompt(
    direction, original_sql, original_question, current_sql, prompt_style="default", no_sql=False,
):
    """Assemble the few-shot NL-translation prompt for the given direction.

    ``direction`` is either ``"en2cn"`` or ``"cn2en"``.
    """
    style = (prompt_style or "default").upper()
    if direction == "en2cn":
        if no_sql:
            header = NL_TRANSLATE_EN2CN_NO_SQL_HEADER
            if style == "LOGICCAT":
                examples = EXAMPLE_EN2CN_NL_LOGICCAT
            elif style == "KAGGLE":
                examples = EXAMPLE_EN2CN_NL_KAGGLE
            elif style == "EHRSQL":
                examples = EXAMPLE_EN2CN_NL_EHRSQL
            elif style == "SPIDER":
                examples = EXAMPLE_EN2CN_NL_SPIDER
            elif style == "BIRD":
                examples = EXAMPLE_EN2CN_NL_BIRD
            else:
                examples = _to_question_only_examples(EXAMPLE_EN2CN_NL)
            current_input_payload = {"original_question": original_question}
        else:
            header = NL_TRANSLATE_EN2CN_HEADER
            examples = EXAMPLE_EN2CN_NL
            current_input_payload = {
                "original_sql": original_sql,
                "original_question": original_question,
                "current_sql": current_sql,
            }
    elif direction == "cn2en":
        header = NL_TRANSLATE_CN2EN_NO_SQL_HEADER
        if no_sql and style == "TACO":
            examples = EXAMPLE_CN2EN_NL_TACO
        elif no_sql and style == "BULL":
            examples = EXAMPLE_CN2EN_NL_BULL
        else:
            examples = _to_question_only_examples(EXAMPLE_CN2EN_NL)
        current_input_payload = {"original_question": original_question}
    else:
        raise ValueError(f"Unknown direction '{direction}', expected 'en2cn' or 'cn2en'.")

    examples_block = "\n\n".join(_render_nl_example(ex) for ex in examples)
    current_input = json.dumps(
        current_input_payload,
        ensure_ascii=False,
        indent=2,
    )

    return (
        f"{header}\n\n"
        f"### Examples\n{examples_block}\n\n"
        f"### Current Input\n{current_input}\n\n"
        f"### Current Output (JSON only):\n"
    )


# ===========================================================================
# Evidence translation — EN-reference (existing, for EN-to-CN pipeline)
# ===========================================================================

EVIDENCE_EN_QUESTION_CN_SQL = """You adapt BIRD-style "evidence" hints for a **cross-language** text-to-SQL setting.

The **reference** (standard BIRD English) has an English question, English SQL, and English evidence that uses **English** table/column names.

The **target** has an **English** question and **Chinese** SQL (Chinese table/column identifiers, often backtick-quoted). Below are the **English** and **Chinese** database schemas and sample rows for the same logical database. Use them to map names: when the reference evidence mentions a table or column, express it in your output using the **Chinese** identifier as it appears in the target SQL / Chinese schema.

--- English database (schema + sample rows) ---
{en_schema_block}

--- Chinese database (schema + sample rows) ---
{cn_schema_block}

--- Reference (BIRD English) ---
Question: {ref_question}
SQL: {ref_sql}
Evidence (English): {ref_evidence}

--- Target context (English question, Chinese SQL) ---
Question: {target_question}
SQL: {target_sql}

Task: Rewrite the reference evidence into **natural English** for the target. Preserve structure (e.g. semicolons between clauses). Align table/column references with the **Chinese** schema / target SQL.

Output: English evidence only. No quotes around the whole answer, no preamble or explanation."""

EVIDENCE_CN_QUESTION_EN_SQL = """You adapt BIRD-style "evidence" hints for a **cross-language** text-to-SQL setting.

The **reference** (standard BIRD English) has an English question, English SQL, and English evidence using **English** table/column names.

The **target** has a **Chinese** question and **English** SQL (**English** table/column names as in standard BIRD). Below are the **English** and **Chinese** database schemas and sample rows for the same logical database. Map names between them: your output is in **Chinese**, but when you refer to tables or columns, use the **English** names exactly as in the target SQL / English schema (do not translate identifiers into Chinese).

--- English database (schema + sample rows) ---
{en_schema_block}

--- Chinese database (schema + sample rows) ---
{cn_schema_block}

--- Reference (BIRD English) ---
Question: {ref_question}
SQL: {ref_sql}
Evidence (English): {ref_evidence}

--- Target context (Chinese question, English SQL) ---
Question: {target_question}
SQL: {target_sql}

Task: Translate and adapt the reference evidence into **natural Chinese** for the target. Preserve structure (e.g. semicolons between clauses). Align table/column references with the **English** schema / target SQL.

Output: Chinese evidence only. No quotes around the whole answer, no preamble or explanation."""

EVIDENCE_FULL_CN = """You translate BIRD-style "evidence" hints from English to Chinese for a fully-Chinese text-to-SQL setting.

The **reference** (standard BIRD English) has an English question, English SQL, and English evidence using **English** table/column names.

The **target** has a **Chinese** question, **Chinese** SQL (Chinese table/column identifiers). Below are the **English** and **Chinese** database schemas and sample rows. When the evidence mentions a table or column, use the **Chinese** identifier.

--- English database (schema + sample rows) ---
{en_schema_block}

--- Chinese database (schema + sample rows) ---
{cn_schema_block}

--- Reference (BIRD English) ---
Question: {ref_question}
SQL: {ref_sql}
Evidence (English): {ref_evidence}

--- Target context (Chinese question, Chinese SQL) ---
Question: {target_question}
SQL: {target_sql}

Task: Translate the reference evidence into **natural Chinese** for the target. Align table/column references with the **Chinese** schema / target SQL. Preserve structure.

Output: Chinese evidence only. No quotes, no preamble or explanation."""


# ===========================================================================
# Evidence translation — CN-reference (for CN-to-EN pipeline)
# ===========================================================================

EVIDENCE_CN_REF_EN_QUESTION_EN_SQL = """You adapt "evidence" hints for a **cross-language** text-to-SQL setting.

The **reference** (Chinese-origin) has a Chinese question, Chinese SQL, and Chinese evidence that uses **Chinese** table/column names.

The **target** has an **English** question and **English** SQL (English table/column identifiers). Below are the **Chinese** and **English** database schemas and sample rows for the same logical database. Use them to map names: when the reference evidence mentions a table or column, express it in your output using the **English** identifier as it appears in the target SQL / English schema.

--- Chinese database (schema + sample rows) ---
{cn_schema_block}

--- English database (schema + sample rows) ---
{en_schema_block}

--- Reference (Chinese-origin) ---
Question: {ref_question}
SQL: {ref_sql}
Evidence (Chinese): {ref_evidence}

--- Target context (English question, English SQL) ---
Question: {target_question}
SQL: {target_sql}

Task: Translate and rewrite the reference evidence into **natural English** for the target. Preserve structure (e.g. semicolons between clauses). Align table/column references with the **English** schema / target SQL.

Output: English evidence only. No quotes around the whole answer, no preamble or explanation."""

EVIDENCE_CN_REF_CN_QUESTION_CN_SQL = """You adapt "evidence" hints for a **cross-language** text-to-SQL setting.

The **reference** (Chinese-origin) has a Chinese question, Chinese SQL, and Chinese evidence using **Chinese** table/column names.

The **target** has a **Chinese** question and **Chinese** SQL (Chinese table/column identifiers). Below are the **Chinese** and **English** database schemas and sample rows for the same logical database. The target SQL may use different Chinese identifiers from the reference; align your output accordingly.

--- Chinese database (schema + sample rows) ---
{cn_schema_block}

--- English database (schema + sample rows) ---
{en_schema_block}

--- Reference (Chinese-origin) ---
Question: {ref_question}
SQL: {ref_sql}
Evidence (Chinese): {ref_evidence}

--- Target context (Chinese question, Chinese SQL) ---
Question: {target_question}
SQL: {target_sql}

Task: Adapt the reference evidence for the target context. Keep the evidence in **natural Chinese**. Align table/column references with the target SQL / Chinese schema. Preserve structure.

Output: Chinese evidence only. No quotes, no preamble or explanation."""

EVIDENCE_CN_REF_EN_QUESTION_CN_SQL = """You adapt "evidence" hints for a **cross-language** text-to-SQL setting.

The **reference** (Chinese-origin) has a Chinese question, Chinese SQL, and Chinese evidence using **Chinese** table/column names.

The **target** has an **English** question and **Chinese** SQL (Chinese table/column identifiers, possibly different from the reference). Below are the **Chinese** and **English** database schemas and sample rows. Align table/column references with the target SQL / Chinese schema.

--- Chinese database (schema + sample rows) ---
{cn_schema_block}

--- English database (schema + sample rows) ---
{en_schema_block}

--- Reference (Chinese-origin) ---
Question: {ref_question}
SQL: {ref_sql}
Evidence (Chinese): {ref_evidence}

--- Target context (English question, Chinese SQL) ---
Question: {target_question}
SQL: {target_sql}

Task: Translate and adapt the reference evidence into **natural English** for the target. Preserve structure (e.g. semicolons between clauses). Align table/column references with the **Chinese** schema / target SQL.

Output: English evidence only. No quotes around the whole answer, no preamble or explanation."""

EVIDENCE_FULL_EN = """You translate "evidence" hints from Chinese to English for a fully-English text-to-SQL setting.

The **reference** (Chinese-origin) has a Chinese question, Chinese SQL, and Chinese evidence using **Chinese** table/column names.

The **target** has an **English** question, **English** SQL (English table/column identifiers). Below are the **Chinese** and **English** database schemas and sample rows. When the evidence mentions a table or column, use the **English** identifier.

--- Chinese database (schema + sample rows) ---
{cn_schema_block}

--- English database (schema + sample rows) ---
{en_schema_block}

--- Reference (Chinese-origin) ---
Question: {ref_question}
SQL: {ref_sql}
Evidence (Chinese): {ref_evidence}

--- Target context (English question, English SQL) ---
Question: {target_question}
SQL: {target_sql}

Task: Translate the reference evidence into **natural English** for the target. Align table/column references with the **English** schema / target SQL. Preserve structure.

Output: English evidence only. No quotes, no preamble or explanation."""
