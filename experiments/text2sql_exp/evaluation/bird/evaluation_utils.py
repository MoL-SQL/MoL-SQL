"""Helper utilities for the BIRD-style execution evaluator.

Adapted from BIRD mini_dev/evaluation/evaluation_utils.py with three changes
relative to upstream, noted inline:

1. ``psycopg2`` / ``pymysql`` imports are guarded so SQLite-only environments
   do not fail at module import time.
2. ``execute_sql`` returns a dict ``{"match", "pred_result", "gold_result",
   "error_info"}`` instead of an int, matching what ``execute_model`` in
   ``evaluation_ex.py`` expects (``res.get(...)``).
3. ``execute_sql`` drops the unused ``output_log_path`` parameter so
   ``execute_model``'s 8-positional call site (..., idx, question, evidence)
   binds to the right names.
"""

import json
import sqlite3

try:  # optional at runtime; only needed for --sql_dialect MySQL / PostgreSQL
    import psycopg2  # noqa: F401
except Exception:  # pragma: no cover
    psycopg2 = None

try:
    import pymysql  # noqa: F401
except Exception:  # pragma: no cover
    pymysql = None


def load_jsonl(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            data.append(json.loads(line))
    return data


def load_json(path):
    with open(path, "r", encoding="utf-8") as j:
        return json.loads(j.read())


# psycopg2   2.9.9
def connect_postgresql():
    if psycopg2 is None:
        raise RuntimeError("psycopg2 is not installed; cannot use --sql_dialect PostgreSQL")
    return psycopg2.connect(
        "dbname=bird user=postgres host=localhost password=li123911 port=5432"
    )


# PyMySQL  1.1.1
def connect_mysql():
    if pymysql is None:
        raise RuntimeError("pymysql is not installed; cannot use --sql_dialect MySQL")
    return pymysql.connect(
        host="localhost",
        user="root",
        password="li123911",
        database="BIRD",
        unix_socket="/var/run/mysqld/mysqld.sock",
    )


def connect_db(sql_dialect, db_path):
    if sql_dialect == "SQLite":
        return sqlite3.connect(db_path)
    if sql_dialect == "MySQL":
        return connect_mysql()
    if sql_dialect == "PostgreSQL":
        return connect_postgresql()
    raise ValueError(f"Unsupported SQL dialect: {sql_dialect}")


def execute_sql(predicted_sql, ground_truth, db_path, sql_dialect, calculate_func,
                idx, question=None, evidence=None):
    """Execute ``predicted_sql`` and ``ground_truth`` against ``db_path`` and
    compare their results via ``calculate_func``.

    Returns a dict (not an int, unlike upstream BIRD) so ``execute_model`` in
    ``evaluation_ex.py`` can pull out ``match``, ``pred_result``,
    ``gold_result`` and ``error_info`` uniformly::

        {
            "match":        0 | 1,
            "pred_result":  list[tuple] | None,
            "gold_result":  list[tuple] | None,
            "error_info":   str | None,
        }
    """
    # ``question`` / ``evidence`` are accepted for signature compatibility with
    # ``execute_model`` but not used here; the caller embeds them into the
    # per-sample error record instead.
    del question, evidence

    conn = connect_db(sql_dialect, db_path)
    cursor = conn.cursor()

    predicted_res = None
    try:
        cursor.execute(predicted_sql)
    except Exception as e:
        conn.close()
        return {
            "match": 0,
            "pred_result": None,
            "gold_result": None,
            "error_info": f"pred failed: {e}",
        }

    # ``cursor.description is None`` when the statement produced no result set
    # (e.g. empty string, ``-- Error: ...`` comment line, DDL/DML rather than
    # a query). Without this check, SQLite silently returns ``[]`` for such
    # predictions and any gold query whose result happens to be empty becomes
    # a false-positive match.
    if cursor.description is None:
        snippet = (predicted_sql or "").strip().replace("\n", " ")[:200]
        try:
            cursor.execute(ground_truth)
            gold_res = cursor.fetchall()
        except Exception:
            gold_res = None
        conn.close()
        return {
            "match": 0,
            "pred_result": None,
            "gold_result": gold_res,
            "error_info": f"pred returned no result set: {snippet or '(empty)'}",
        }
    predicted_res = cursor.fetchall()

    try:
        cursor.execute(ground_truth)
        ground_truth_res = cursor.fetchall()
    except Exception as e:
        conn.close()
        return {
            "match": 0,
            "pred_result": predicted_res,
            "gold_result": None,
            "error_info": f"gold failed: {e}",
        }

    conn.close()
    match = calculate_func(predicted_res, ground_truth_res)
    return {
        "match": int(match),
        "pred_result": predicted_res,
        "gold_result": ground_truth_res,
        "error_info": None if match else "execution result mismatch",
    }


def package_sqls(sql_path, db_root_path, mode="pred"):
    """Load SQL statements from ``sql_path``.

    - ``mode='pred'``: expects a JSON dict mapping ``str(idx) -> sql``,
      optionally with the BIRD-style ``"<sql>\\t----- bird -----\\t<db_id>"``
      suffix (stripped here). Returns ``(clean_sqls, [])``; gold mode
      provides the db path list for both pred and gold.
    - ``mode='gt'``: expects one ``"<sql>\\t<db_id>"`` line per sample.
      Returns ``(clean_sqls, db_path_list)``.
    """
    clean_sqls = []
    db_path_list = []
    if mode == "pred":
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_data = json.load(f)
        for _, sql_str in sql_data.items():
            if isinstance(sql_str, str):
                try:
                    sql, _db_name = sql_str.split("\t----- bird -----\t")
                except ValueError:
                    sql = sql_str.strip()
            else:
                sql = " "
            clean_sqls.append(sql)

    elif mode == "gt":
        with open(sql_path, "r", encoding="utf-8") as f:
            for sql_str in f:
                sql_str = sql_str.strip()
                if not sql_str:
                    continue
                if "\t" in sql_str:
                    sql, db_name = sql_str.split("\t", 1)
                else:
                    parts = sql_str.rsplit(None, 1)
                    if len(parts) != 2:
                        continue
                    sql, db_name = parts
                clean_sqls.append(sql)
                db_path_list.append(f"{db_root_path}{db_name}/{db_name}.sqlite")

    else:
        raise ValueError(f"Unknown package_sqls mode: {mode}")

    return clean_sqls, db_path_list


def sort_results(list_of_dicts):
    return sorted(list_of_dicts, key=lambda x: x["sql_idx"])


def print_data(score_lists, count_lists, metric="F1 Score", result_log_file=None):
    levels = ["simple", "moderate", "challenging", "total"]
    print("{:20} {:20} {:20} {:20} {:20}".format("", *levels))
    print("{:20} {:<20} {:<20} {:<20} {:<20}".format("count", *count_lists))
    print(f"======================================    {metric}    =====================================")
    print("{:20} {:<20.2f} {:<20.2f} {:<20.2f} {:<20.2f}".format(metric, *score_lists))

    if result_log_file is not None:
        with open(result_log_file, "a") as log_file:
            log_file.write(f"start calculate {metric}\n")
            log_file.write("{:20} {:20} {:20} {:20} {:20}\n".format("", *levels))
            log_file.write("{:20} {:<20} {:<20} {:<20} {:<20}\n".format("count", *count_lists))
            log_file.write(f"======================================    {metric}   =====================================\n")
            log_file.write("{:20} {:<20.2f} {:<20.2f} {:<20.2f} {:<20.2f}\n".format(metric, *score_lists))
            log_file.write("===========================================================================================\n")
            log_file.write(f"Finished {metric} evaluation for mini dev set\n\n")
