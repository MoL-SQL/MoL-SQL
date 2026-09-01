import sys
import json
import argparse
import multiprocessing as mp
from func_timeout import func_timeout, FunctionTimedOut
from tqdm import tqdm
from evaluation_utils import (
    load_json,
    load_jsonl,
    execute_sql,
    package_sqls,
    sort_results,
    print_data,
)


_progress_bar = None


def result_callback(result):
    exec_result.append(result)
    if _progress_bar is not None:
        _progress_bar.update(1)


def calculate_ex(predicted_res, ground_truth_res):
    res = 0
    if set(predicted_res) == set(ground_truth_res):
        res = 1
    return res


def execute_model(
    predicted_sql, ground_truth, db_place, idx, meta_time_out, sql_dialect,
    question=None, evidence=None,
):
    try:
        res = func_timeout(
            meta_time_out,
            execute_sql,
            args=(predicted_sql, ground_truth, db_place, sql_dialect, calculate_ex,
                  idx, question, evidence),
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except FunctionTimedOut:
        res = {"match": 0, "pred_result": None, "gold_result": None, "error_info": "timeout"}
    except Exception as e:
        res = {"match": 0, "pred_result": None, "gold_result": None, "error_info": str(e)}

    return {
        "sql_idx": idx,
        "res": res.get("match", 0),
        "gold_sql": ground_truth,
        "pred_sql": predicted_sql,
        "gold_result": res.get("gold_result"),
        "pred_result": res.get("pred_result"),
        "error_info": res.get("error_info"),
    }


def run_sqls_parallel(
    sqls, db_places, num_cpus=1, meta_time_out=30.0, sql_dialect="SQLite",
    questions=None,
):
    global _progress_bar
    pool = mp.Pool(processes=num_cpus)
    futures = []
    _progress_bar = tqdm(total=len(sqls), desc="Exec SQL", unit="sql")
    try:
        for i, sql_pair in enumerate(sqls):
            predicted_sql, ground_truth = sql_pair
            item = questions[i] if questions and i < len(questions) else {}
            q = item.get("question", item.get("Question", "")) or None
            ev = item.get("evidence", item.get("Evidence", "")) or None
            f = pool.apply_async(
                execute_model,
                args=(
                    predicted_sql,
                    ground_truth,
                    db_places[i],
                    i,
                    meta_time_out,
                    sql_dialect,
                    q,
                    ev,
                ),
                callback=result_callback,
            )
            futures.append(f)
        for f in futures:
            f.get()
        pool.close()
        pool.join()
    finally:
        _progress_bar.close()
        _progress_bar = None


def compute_acc_by_diff(exec_results, diff_json_path):
    num_queries = len(exec_results)
    results = [res["res"] for res in exec_results]
    contents = load_jsonl(diff_json_path)
    simple_results, moderate_results, challenging_results = [], [], []

    for i, content in enumerate(contents):
        if content["difficulty"] == "simple":
            simple_results.append(exec_results[i])

        if content["difficulty"] == "moderate":
            moderate_results.append(exec_results[i])

        if content["difficulty"] == "challenging":
            try:
                challenging_results.append(exec_results[i])
            except:
                print(i)

    simple_acc = sum([res["res"] for res in simple_results]) / len(simple_results) if len(simple_results) > 0 else 0
    moderate_acc = sum([res["res"] for res in moderate_results]) / len(moderate_results) if len(moderate_results) > 0 else 0
    challenging_acc = sum([res["res"] for res in challenging_results]) / len(challenging_results) if len(challenging_results) > 0 else 0

    all_acc = sum(results) / num_queries
    count_lists = [
        len(simple_results),
        len(moderate_results),
        len(challenging_results),
        num_queries,
    ]
    return (
        simple_acc * 100,
        moderate_acc * 100,
        challenging_acc * 100,
        all_acc * 100,
        count_lists,
    )


def _build_statistic(exec_results, diff_json_path):
    """Build the per-level statistic dict keyed in order: total, simple, moderate, challenging.

    Each level stores `exec` (fraction, 0-1) and `count`.
    """
    contents = load_jsonl(diff_json_path)
    buckets = {"simple": [], "moderate": [], "challenging": []}
    for i, content in enumerate(tqdm(contents, desc="Build stats", unit="row")):
        lvl = content.get("difficulty", "simple")
        if lvl in buckets and i < len(exec_results):
            buckets[lvl].append(exec_results[i])

    total_n = len(exec_results)
    total_match = sum(r["res"] for r in exec_results)

    def _acc(rs):
        return (sum(r["res"] for r in rs) / len(rs)) if rs else 0.0

    stat = {}
    stat["total"] = {
        "exec": (total_match / total_n) if total_n else 0.0,
        "count": total_n,
    }
    for lvl in ("simple", "moderate", "challenging"):
        stat[lvl] = {
            "exec": _acc(buckets[lvl]),
            "count": len(buckets[lvl]),
        }
    return stat


def _build_errors(exec_results, diff_json_path, questions=None):
    """Collect one entry per execution error (res == 0).

    ``questions`` is the list loaded from ``--questions_json_path``; when
    present, the per-sample ``question`` text is copied into each error entry.
    """
    contents = load_jsonl(diff_json_path)
    errors = []
    for i, r in enumerate(tqdm(exec_results, desc="Collect errors", unit="row")):
        if r.get("res"):
            continue
        level = contents[i].get("difficulty", "simple") if i < len(contents) else None
        q = None
        if questions and i < len(questions):
            item = questions[i] or {}
            q = item.get("question", item.get("Question")) or None
        errors.append({
            "index": i,
            "level": level,
            "question": q,
            "gold sql": r.get("gold_sql"),
            "pred sql": r.get("pred_sql"),
            "gold result": r.get("gold_result"),
            "pred result": r.get("pred_result"),
            "error_info": r.get("error_info"),
        })
    return errors


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--predicted_sql_path", type=str, required=True, default=""
    )
    args_parser.add_argument("--ground_truth_path", type=str, required=True, default="")
    args_parser.add_argument("--db_root_path", type=str, required=True, default="")
    args_parser.add_argument("--num_cpus", type=int, default=1)
    args_parser.add_argument("--meta_time_out", type=float, default=30.0)
    args_parser.add_argument("--diff_json_path", type=str, default="")
    args_parser.add_argument("--questions_json_path", type=str, default="", help="Path to _sqlite.json with question field for each sample")
    args_parser.add_argument("--sql_dialect", type=str, default="SQLite")
    args_parser.add_argument("--output", type=str, default=None,
                             help='Path to save evaluation result JSON ({"statistic": ..., "errors": [...]}).')
    args = args_parser.parse_args()
    exec_result = []

    pred_queries, db_paths = package_sqls(
        args.predicted_sql_path,
        args.db_root_path,
        mode='pred'
    )
    # generate ground truth sqls:
    gt_queries, db_paths_gt = package_sqls(
        args.ground_truth_path,
        args.db_root_path,
        mode="gt",
    )

    query_pairs = list(zip(pred_queries, gt_queries))

    questions = []
    if args.questions_json_path:
        try:
            questions = load_json(args.questions_json_path)
            if not isinstance(questions, list):
                questions = []
            questions = questions[:len(query_pairs)]
        except Exception as e:
            print(f"Warning: could not load questions from {args.questions_json_path}: {e}", file=sys.stderr)

    run_sqls_parallel(
        query_pairs,
        db_places=db_paths_gt,
        num_cpus=args.num_cpus,
        meta_time_out=args.meta_time_out,
        sql_dialect=args.sql_dialect,
        questions=questions if questions else None,
    )
    exec_result = sort_results(exec_result)

    if args.output:
        statistic = _build_statistic(exec_result, args.diff_json_path)
        errors = _build_errors(exec_result, args.diff_json_path,
                               questions=questions if questions else None)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"statistic": statistic, "errors": errors}, f,
                      indent=2, default=str, ensure_ascii=False)

    print("start calculate EX")
    simple_acc, moderate_acc, challenging_acc, acc, count_lists = compute_acc_by_diff(
        exec_result, args.diff_json_path
    )
    score_lists = [simple_acc, moderate_acc, challenging_acc, acc] 
    print_data(score_lists, count_lists, metric="EX")
    print(
        "==========================================================================================="
    )
    print(f"Finished EX evaluation for {args.sql_dialect} on Mini Dev set")
    print("\n\n")
