import os
import json

base_dir = 'dataset/BULL-FinSQL/BULL-en-origin-date-reset'
with open(os.path.join(base_dir, 'dev.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

# Spider-style gold format expected by the evaluator and schema_linking.py:
#   <sql>\t<db_id>\n
with open(os.path.join(base_dir, 'dev_gold.sql'), 'w', encoding='utf-8') as out:
    for item in data:
        sql = (item.get('sql_query') or '').strip()
        db_id = (item.get('db_name') or item.get('db_id') or '').strip()
        if sql:
            out.write(f"{sql}\t{db_id}\n")