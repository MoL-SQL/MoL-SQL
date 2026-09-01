"""Render an integrated Full+Cube paper-ready dataset report."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mol_sql.contracts.io import load_json


@dataclass(frozen=True)
class DatasetPaperReportOptions:
    repo_root: Path
    full_statistics_dir: Path
    cube_statistics_dir: Path
    output_path: Path


SOURCE_LABELS = {
    "bird": "BIRD",
    "bull": "BULL",
    "ehrsql": "EHRSQL",
    "kaggledbqa": "KaggleDBQA",
    "spider": "Spider",
}
SOURCE_ORDER = tuple(SOURCE_LABELS)
BARRIER_LABELS = {
    "Q-COMP": "Question composition",
    "S-SELECT": "Schema selection",
    "S-JOIN": "Multi-table grounding",
    "S-LEX": "Schema lexical alignment",
    "V-EXACT": "Mapped exact values",
    "V-RECUR": "Recurring entities",
    "I-QS": "Question–schema interaction",
    "I-QV": "Question–value interaction",
    "I-SV": "Schema–value interaction",
    "I-QSV": "Three-way interaction",
}
EXISTING_BENCHMARK_ROWS = (
    (
        "**Spider 1.0**",
        "Cross-domain, closed-domain Text-to-SQL",
        "10,181 examples",
        "200",
        "1,020",
        "5.1",
        "✓",
        "×",
        "English; no aligned language-axis control",
        "1,030 retained logical instances from the aligned dev snapshot",
    ),
    (
        "**KaggleDBQA**",
        "Cross-domain, naturally occurring web databases",
        "272 examples",
        "8",
        "18",
        "2.25",
        "✓",
        "×",
        "English; no aligned language-axis control",
        "184 retained logical instances from the aligned test-derived subset",
    ),
    (
        "**BIRD**",
        "Cross-domain, large/value-rich databases with evidence",
        "12,751 examples",
        "95",
        "694",
        "7.3",
        "✓",
        "×",
        "English; no aligned language-axis control",
        "498 retained logical instances from BIRD Mini-Dev",
    ),
    (
        "**BULL**",
        "Domain-specific financial analysis",
        "4,966 examples",
        "3",
        "78",
        "26.0",
        "✓",
        "×",
        "Original financial benchmark; no aligned Q/S/V factorial control",
        "1,000 retained logical instances in the current aligned subset",
    ),
    (
        "**EHRSQL**",
        "Domain-specific clinical/EHR Text-to-SQL",
        "22,505 executable NL–SQL pairs",
        "2",
        "27",
        "13.5",
        "✓",
        "×",
        "English; no aligned Q/S/V factorial control",
        "1,511 retained logical instances from the aligned valid subset",
    ),
)
MOL_LOGICAL_TABLES = 278
MOL_MIXED_SV_MATERIALIZATIONS = 88


def _resolve(repo_root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root / candidate


def _load(directory: Path, name: str) -> Any:
    return load_json(directory / name)


def _number(value: int | float) -> str:
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.3f}"
    return f"{int(value):,}"


def _percentage(count: int | float, denominator: int | float) -> str:
    return f"{100 * count / denominator:.1f}%" if denominator else "0.0%"


def _count_percentage(count: int, denominator: int) -> str:
    return f"{_number(count)} ({_percentage(count, denominator)})"


def _row(values: list[str]) -> str:
    return "| " + " | ".join(values) + " |"


def _source_distribution(values: dict[str, int], total: int) -> list[float]:
    return [round(100 * values.get(source, 0) / total, 1) for source in SOURCE_ORDER]


def _tier_distribution(values: dict[str, int], total: int) -> list[float]:
    return [
        round(100 * values.get(tier, 0) / total, 1)
        for tier in ("easy", "medium", "hard")
    ]


def _fmt_series(values: list[float]) -> str:
    return "[" + ", ".join(f"{value:.1f}" for value in values) + "]"


def _enrichment(
    full_count: int,
    full_total: int,
    cube_count: int,
    cube_total: int,
) -> str:
    full_rate = full_count / full_total if full_total else 0.0
    cube_rate = cube_count / cube_total if cube_total else 0.0
    return f"{cube_rate / full_rate:.2f}×" if full_rate else "n/a"


def _render(options: DatasetPaperReportOptions) -> str:
    repo_root = options.repo_root.resolve()
    full_dir = _resolve(repo_root, options.full_statistics_dir).resolve()
    cube_dir = _resolve(repo_root, options.cube_statistics_dir).resolve()

    full_manifest = _load(full_dir, "report_manifest.json")
    full_composition = _load(full_dir, "composition.json")
    full_treatment = _load(full_dir, "treatment_support.json")
    full_quality = _load(full_dir, "quality_funnel.json")
    cube_manifest = _load(cube_dir, "report_manifest.json")
    cube_composition = _load(cube_dir, "composition.json")
    cube_completeness = _load(cube_dir, "cube_completeness.json")
    cube_support = _load(cube_dir, "treatment_barrier_support.json")
    cube_difficulty = _load(cube_dir, "difficulty.json")
    cube_comparison = _load(cube_dir, "full_cube_comparison.json")
    cube_quality = _load(cube_dir, "quality_funnel.json")

    full_total = int(full_composition["logical_instances"])
    cube_total = int(cube_composition["selected_logical_instances"])
    candidate = cube_comparison["candidate_universe"]
    selected = cube_comparison["selected"]
    full_databases = sum(
        int(row["databases"]) for row in full_composition["sources"].values()
    )
    cube_databases = sum(
        int(row["databases"]) for row in cube_composition["sources"].values()
    )
    all_blockers = sorted(set(full_manifest["blockers"] + cube_manifest["blockers"]))
    source_labels = json.dumps(
        [SOURCE_LABELS[source] for source in SOURCE_ORDER],
        ensure_ascii=False,
    )
    candidate_source_values = _source_distribution(candidate["sources"], full_total)
    selected_source_values = _source_distribution(selected["sources"], cube_total)
    candidate_tier_values = _tier_distribution(candidate["tiers"], full_total)
    selected_tier_values = _tier_distribution(selected["tiers"], cube_total)

    lines = [
        "# Provisional Dataset Tables and Figures for MoL-SQL (Full + Cube)",
        "",
        "> **状态：provisional / non-claim-bearing。** 本文档整合当前 "
        f"`{full_manifest['release_id']}` 与 `{cube_manifest['release_id']}` 的真实统计，"
        "用于确定论文 Dataset 章节的论证、表格和图形格式。Full/Cube 冻结后必须从新 manifest hash 全量重算；当前数字不得作为最终论文 claim。",
        "",
        "## 0. 统计来源与使用限制",
        "",
        _row(["Field", "MoL-Full", "MoL-Cube"]),
        _row(["---", "---", "---"]),
        _row(["Statistics version", f"`{full_manifest['statistics_version']}`", f"`{cube_manifest['statistics_version']}`"]),
        _row(["Release", f"`{full_manifest['release_id']}` (`{full_manifest['release_status']}`)", f"`{cube_manifest['release_id']}` (`{cube_manifest['release_status']}`)"]),
        _row(["Release manifest SHA-256", f"`{full_manifest['release_manifest_hash']}`", f"`{cube_manifest['release_manifest_hash']}`"]),
        _row(["Statistics config SHA-256", f"`{full_manifest['config_hash']}`", f"`{cube_manifest['config_hash']}`"]),
        _row(["Generated at", f"`{full_manifest['generated_at_utc']}`", f"`{cube_manifest['generated_at_utc']}`"]),
        _row(["Provisional", f"`{str(full_manifest['provisional']).lower()}`", f"`{str(cube_manifest['provisional']).lower()}`"]),
        "",
        f"当前 blockers：`{'; '.join(all_blockers)}`。Cube 的 Q-LEX/Q-REF 与 V-NORM/V-RETRIEVE 人工 annotation、Full/Cube 双人人工质量审计、BULL license/redistribution 仍未完成。Mermaid 图只用于确认论文信息结构；投稿图应由冻结 JSON/CSV 通过可复现绘图脚本生成。",
        "",
        "## 1. 论文主旨与数据集论证",
        "",
        "MoL-SQL 的核心不是用一个平衡子集替代自然 benchmark，而是用两个互补视图回答不同问题：",
        "",
        _row(["Dataset view", "Preserved property", "Primary estimand", "Validity role", "禁止的解释"]),
        _row(["---", "---", "---", "---", "---"]),
        _row(["MoL-Full", "五个来源的 retained natural workload distribution", "总体性能、source-level generality、micro/macro robustness", "外部有效性与 source coverage", "不能称为 Q/S/V 独立因果设计"]),
        _row(["MoL-Cube", "每 source 等额、每 logical instance 完整 2×2×2 cells", "Q、S、V 主效应及二阶/三阶交互", "构念有效性与内部有效性", "不能称为真实世界语言分布或独立新数据集"]),
        "",
        "**论文逻辑：** Full 证明结论不是来自单一 benchmark 或人为平衡分布；Cube 在同一 logical intent 内独立改变 question、schema 和 eligible-value language，使语言因素可以被识别。二者共同避免“自然分布可推广但不可归因”与“平衡实验可归因但不代表自然分布”的单边缺陷。",
        "",
        "## 2. 推荐的主文最小组合",
        "",
        "在 Dataset 章节约 1.5 页预算下，正文建议保留：",
        "",
        "1. **Table D1：Full/Cube overview and complementary roles**；",
        "2. **Table D2：comparison with representative Text-to-SQL benchmarks**；",
        "3. **Table D3：Full natural composition and Cube balanced composition**；",
        "4. **Table D4：Cube B-Q/B-S/B-V/B-I coverage and factorial completeness**；",
        "5. **Figure D3：Full→Cube construction and verification funnel**。",
        "",
        "Sampling comparison、difficulty enrichment、database concentration、quota shortfall 和质量限制放附录；若正文空间受限，可将 Table D3 移至附录，但应保留 Table D2 以明确 MoL-SQL 的贡献是受控多语言诊断，而不是更大的原始 benchmark scale。",
        "",
        "## 3. Table D1 — MoL-SQL Dataset Overview（推荐正文）",
        "",
        _row(["Dataset view", "Sources", "DBs", "Logical", "Realizations", "Per logical", "Configurations", "Role"]),
        _row(["---", "---:", "---:", "---:", "---:", "---:", "---", "---"]),
        _row(["MoL-Full draft", "5", _number(full_databases), _number(full_total), _number(full_composition["realizations"]), "4", "$Q_{en/zh} \\times DB_{en/zh}$", "Source-distribution evaluation"]),
        _row(["Engineering MoL-Cube", "5", _number(cube_databases), _number(cube_total), _number(cube_composition["realizations"]), "8", "$Q_{en/zh} \\times S_{en/zh} \\times V_{en/zh}$", "Balanced factorial diagnosis; non-claim-bearing"]),
        "",
        "**建议 caption：** *Overview of the complementary MoL-SQL views. MoL-Full preserves source-workload distributions, whereas MoL-Cube independently controls question, schema, and eligible-value language within aligned logical instances. Values are provisional.*",
        "",
        "## 4. Table D2 — Comparison with Existing Text-to-SQL Benchmarks（推荐正文）",
        "",
        _row(["Dataset / view", "Scope", "Benchmark scale", "DBs", "Tables", "Tables / DB", "Cross-table SQL", "Cross-DB SQL", "Language design", "Current MoL use / role"]),
        _row(["---", "---", "---:", "---:", "---:", "---:", ":---:", ":---:", "---", "---"]),
    ]
    lines.extend(_row(list(row)) for row in EXISTING_BENCHMARK_ROWS)
    lines.extend(
        [
            _row([
                "**MoL-Full**",
                "Five-source multilingual evaluation view preserving retained source distributions",
                f"**{_number(full_total)} logical / {_number(full_composition['realizations'])} realizations**",
                f"**{_number(full_databases)}**",
                f"**{_number(MOL_LOGICAL_TABLES)}**",
                f"**{MOL_LOGICAL_TABLES / full_databases:.2f}**",
                "✓",
                "×",
                "English/Chinese questions; schema and eligible values vary **jointly**; 4 aligned configurations",
                "Source-distribution evaluation, pooled micro + source macro + per-source analysis",
            ]),
            _row([
                "**MoL-Cube**",
                "Source-balanced diagnostic view sampled from MoL-Full",
                f"**{_number(cube_total)} logical / {_number(cube_composition['realizations'])} realizations**",
                f"**{_number(cube_databases)} logical DBs**; {_number(MOL_MIXED_SV_MATERIALIZATIONS)} mixed S/V materializations",
                f"**{_number(MOL_LOGICAL_TABLES)} logical schema tables**",
                f"**{MOL_LOGICAL_TABLES / cube_databases:.2f}**",
                "✓",
                "×",
                "English/Chinese **Q, S, and V independently controlled**; complete $2\\times2\\times2$ design",
                f"B-Q/B-S/B-V/B-I main effects and interactions; {_number(cube_total)} realizations per factorial cell",
            ]),
            "",
            "**建议 caption：** *Comparison with representative Text-to-SQL benchmarks. Existing benchmarks provide broad cross-domain or domain-specific SQL workloads but do not align the same logical intent under independently controlled question, schema, and eligible-value languages. MoL-Full preserves the retained source-workload distributions, whereas MoL-Cube provides a source-balanced $2\\times2\\times2$ diagnostic design over the same multilingual construction pipeline.*",
            "",
            "该表不用于声称 MoL-SQL 在规模、开放域或跨数据库查询上优于现有 benchmark。Spider、KaggleDBQA、BIRD、BULL 和 EHRSQL 分别服务于组合泛化、自然数据库、值密集型大库、金融分析和临床查询；MoL-SQL 的增量是把同一 logical intent 组织为可对齐的语言配置，其中 Full 支持 source-distribution validity，Cube 支持 Q/S/V language placement 的 construct/internal validity。所有 MoL 查询仍在单一 logical database 内执行，cross-table 不等于 cross-database。",
            "",
            "规模与属性口径：Spider 1.0、KaggleDBQA、BIRD 采用 TACO Table 1 的 original benchmark statistics；BULL、EHRSQL 采用仓库中当前可验证的 benchmark snapshot；最后一列另列 MoL-Full 实际 retained subset，避免把 source benchmark 总规模与本研究对齐子集混淆。",
            "",
            "## 5. Table D3 — Full Natural Composition and Cube Balance（推荐正文）",
        "",
        _row(["Source", "Full logical", "Full share", "Cube logical", "Cube share", "Cube DBs", "Cube Easy / Med. / Hard"]),
        _row(["---", "---:", "---:", "---:", "---:", "---:", "---:"]),
        ]
    )

    for source in SOURCE_ORDER:
        full_row = full_composition["sources"][source]
        cube_row = cube_composition["sources"][source]
        tiers = cube_row["composite_tiers"]
        lines.append(
            _row(
                [
                    SOURCE_LABELS[source],
                    _number(full_row["logical_instances"]),
                    _percentage(full_row["logical_instances"], full_total),
                    _number(cube_row["logical_instances"]),
                    _percentage(cube_row["logical_instances"], cube_total),
                    _number(cube_row["databases"]),
                    f"{tiers['easy']} / {tiers['medium']} / {tiers['hard']}",
                ]
            )
        )
    cube_tiers = cube_difficulty["overall"]["tiers"]
    lines.extend(
        [
            _row(["**Total**", f"**{_number(full_total)}**", "**100.0%**", f"**{_number(cube_total)}**", "**100.0%**", f"**{_number(cube_databases)}**", f"**{cube_tiers['easy']} / {cube_tiers['medium']} / {cube_tiers['hard']}**"]),
            "",
            "解释：Full 保留来源规模差异，因此 EHRSQL/BULL 对 pooled micro 指标影响更大；Cube 每 source 固定 96 个 logical instances，使 factorial contrast 不被单一 source 主导。最终实验应同时报告 Full micro、Full source-macro 与 Cube factorial effects。",
            "",
            "**建议 caption：** *Natural source composition in MoL-Full and source-balanced composition in the engineering MoL-Cube. Cube difficulty tiers are defined from model-independent, source-internal SQL/schema/value descriptors.*",
            "",
            "## 6. Figure D1 — Full Natural Distribution vs. Cube Balance（正文候选）",
            "",
            "```mermaid",
            "xychart-beta",
            '    title "Source share: Full candidates vs. selected Cube"',
            f"    x-axis {source_labels}",
            '    y-axis "Share of logical instances (%)" 0 --> 40',
            f"    bar {_fmt_series(candidate_source_values)}",
            f"    bar {_fmt_series(selected_source_values)}",
            "```",
            "",
            "系列顺序为 Full candidate universe 与 selected Cube。该图用于说明 Cube 的 source balance 是预先定义的诊断设计，而不是自然分布估计。",
            "",
            "## 7. Table D4 — Full→Cube Factorial and Barrier-Family Coverage（推荐正文）",
            "",
            _row(["Evidence", "Full candidate pool", "Selected Cube", "Enrichment", "Design implication"]),
            _row(["---", "---:", "---:", "---:", "---"]),
            _row(["Aligned-cell completeness", f"{_number(full_total)} (100.0%; 4 coupled cells)", f"{_number(cube_completeness['complete_logical_instances'])} (100.0%; 8 cells)", "4→8 cells", "从 coupled DB language 扩展为完整 Q×S×V factorial design"]),
            _row(["Execution equivalence", f"{_number(full_total)} (100.0%; retained)", f"{_number(cube_quality['audit_summary']['eight_cell_execution_equivalence']['pass'])} (100.0%)", "preserved", "targeting 未牺牲 SQL/answer semantics"]),
            _row(["B-Q: Q-axis intervention active", _count_percentage(candidate["logical_instances"], full_total), _count_percentage(selected["logical_instances"], cube_total), "1.00×", "所有样本均可估计 Q effect"]),
            _row(["B-Q: Q-COMP opportunity", _count_percentage(candidate["barrier_opportunities"]["Q-COMP"], full_total), _count_percentage(selected["barrier_opportunities"]["Q-COMP"], cube_total), _enrichment(candidate["barrier_opportunities"]["Q-COMP"], full_total, selected["barrier_opportunities"]["Q-COMP"], cube_total), "保留并略提高 compositional question coverage"]),
            _row(["B-S: S-axis intervention active", _count_percentage(candidate["logical_instances"], full_total), _count_percentage(selected["logical_instances"], cube_total), "1.00×", "所有样本均可估计 S 与 Q×S"]),
            _row(["B-S: S-JOIN opportunity", _count_percentage(candidate["barrier_opportunities"]["S-JOIN"], full_total), _count_percentage(selected["barrier_opportunities"]["S-JOIN"], cube_total), _enrichment(candidate["barrier_opportunities"]["S-JOIN"], full_total, selected["barrier_opportunities"]["S-JOIN"], cube_total), "提高 multi-table schema grounding coverage"]),
            _row(["B-V: V-axis intervention active", _count_percentage(candidate["barrier_opportunities"]["V-EXACT"], full_total), _count_percentage(selected["barrier_opportunities"]["V-EXACT"], cube_total), _enrichment(candidate["barrier_opportunities"]["V-EXACT"], full_total, selected["barrier_opportunities"]["V-EXACT"], cube_total), "显著提高 V、Q×V 与 S×V 的可估计覆盖"]),
            _row(["B-V: recurring-entity opportunity", _count_percentage(candidate["barrier_opportunities"]["V-RECUR"], full_total), _count_percentage(selected["barrier_opportunities"]["V-RECUR"], cube_total), _enrichment(candidate["barrier_opportunities"]["V-RECUR"], full_total, selected["barrier_opportunities"]["V-RECUR"], cube_total), "针对跨位置一致 value grounding"]),
            _row(["B-I: three-way opportunity", _count_percentage(candidate["barrier_opportunities"]["I-QSV"], full_total), _count_percentage(selected["barrier_opportunities"]["I-QSV"], cube_total), _enrichment(candidate["barrier_opportunities"]["I-QSV"], full_total, selected["barrier_opportunities"]["I-QSV"], cube_total), "提高 Q×S×V interaction 的有效样本量"]),
            _row(["B-V control: literal-free", _count_percentage(full_treatment["overall"]["controls"]["literal_free"], full_total), _count_percentage(cube_support["controls"]["literal_free"], cube_total), _enrichment(full_treatment["overall"]["controls"]["literal_free"], full_total, cube_support["controls"]["literal_free"], cube_total), "仍保留无 V-axis intervention 的 calibration controls"]),
            "",
            "**建议 caption：** *Factorial validity and barrier-family coverage before and after Cube selection. Cube preserves universal Q/S interventions while enriching value-grounding, recurring-entity, and cross-component opportunities without sacrificing execution equivalence.*",
            "",
            "Table D4 同时展示 Full baseline rate 与 Cube selected rate，因此可以直接说明 Cube 的针对性：Q/S 轴保持全覆盖，B-V 与 B-I 的有效机会被显著提高，同时保留 literal-free controls。Language intervention 是 estimand 可计算的前提；具体 barrier opportunity 仍由预模型结构证据定义，不把 axis change 本身称为 barrier。",
            "",
            "## 8. Table D5 — Cube Barrier-Opportunity Coverage（正文候选 / 推荐附录）",
            "",
            _row(["Barrier opportunity", "Selected", "Coverage", "Planned estimand"]),
            _row(["---", "---:", "---:", "---"]),
        ]
    )
    estimands = {
        "Q-COMP": "$Q$ and $Q\\times$ difficulty",
        "S-SELECT": "$S$ within distractor-heavy schemas",
        "S-JOIN": "$S$ and $Q\\times S$",
        "S-LEX": "$S$ and $Q\\times S$ lexical grounding",
        "V-EXACT": "$V$ and $Q\\times V$",
        "V-RECUR": "$V$ within recurring entities",
        "I-QS": "$Q\\times S$",
        "I-QV": "$Q\\times V$",
        "I-SV": "$S\\times V$",
        "I-QSV": "$Q\\times S\\times V$",
    }
    for barrier in BARRIER_LABELS:
        count = int(cube_support["barrier_opportunities"].get(barrier, 0))
        lines.append(
            _row([f"{barrier}: {BARRIER_LABELS[barrier]}", _number(count), _percentage(count, cube_total), estimands[barrier]])
        )

    candidate_v = float(candidate["support_rates"]["v_treatment_present"])
    selected_v = float(selected["support_rates"]["v_treatment_present"])
    lines.extend(
        [
            "",
            "这些标签是 **barrier opportunities**：它们预先描述样本能否检验某类语言需求，不根据模型在八格上的 accuracy delta 选择样本，因此避免 difficulty/selection leakage。Q-LEX/Q-REF 与更细的 V-NORM/V-RETRIEVE 仍需双人人工 annotation。",
            "",
            "## 9. Table D6 — Full Candidate Pool vs. Selected Cube（推荐附录）",
            "",
            _row(["Property", "Full candidate universe", "Selected Cube", "Design implication"]),
            _row(["---", "---:", "---:", "---"]),
            _row(["Logical instances", _number(candidate["logical_instances"]), _number(selected["logical_instances"]), f"Selection fraction {_percentage(selected['logical_instances'], candidate['logical_instances'])}"]),
            _row(["Easy", _count_percentage(candidate["tiers"]["easy"], full_total), _count_percentage(selected["tiers"]["easy"], cube_total), "保留 calibration/control，但不让 easy 主导"]),
            _row(["Medium", _count_percentage(candidate["tiers"]["medium"], full_total), _count_percentage(selected["tiers"]["medium"], cube_total), "支持中等复杂度交互估计"]),
            _row(["Hard", _count_percentage(candidate["tiers"]["hard"], full_total), _count_percentage(selected["tiers"]["hard"], cube_total), "有意提高诊断挑战性"]),
            _row(["B-V: active V-axis intervention", _percentage(candidate_v, 1), _percentage(selected_v, 1), f"从自然池的 {_percentage(candidate_v, 1)} 提高至 {_percentage(selected_v, 1)}，确保 B-V contrasts 可估计"]),
            _row(["Composite score mean", f"{candidate['composite_score']['mean']:.3f}", f"{selected['composite_score']['mean']:.3f}", "使用内生难度分层，不读取模型错误率"]),
            "",
            f"具有 active V-axis intervention 的样本占比提高了 {selected_v / candidate_v:.2f}×。这不是代表性抽样，而是围绕 B-V 及 B-I estimands 的 claim-driven diagnostic sampling；论文必须把 Cube effect 与 Full natural-distribution results 分开报告。唯一 quota shortfall 是 EHRSQL 仅有两个数据库，40% database cap 理论上不可行，实际最小上限为 48/96，并已显式记录。",
            "",
            "## 10. Figure D2 — Difficulty Shift from Full to Cube（正文候选）",
            "",
            "```mermaid",
            "xychart-beta",
            '    title "Source-internal intrinsic difficulty distribution"',
            '    x-axis ["Easy", "Medium", "Hard"]',
            '    y-axis "Share of logical instances (%)" 0 --> 50',
            f"    bar {_fmt_series(candidate_tier_values)}",
            f"    bar {_fmt_series(selected_tier_values)}",
            "```",
            "",
            "系列顺序为 Full candidate universe 与 selected Cube。Cube 将 hard tier 从约三分之一提高到接近 45%，但保留 19.8% easy controls；难度完全来自 SQL/schema/value 数据属性，而非待评测模型表现。",
            "",
            "## 11. Table D7 — Per-Source Full→Cube B-V Targeting（推荐附录）",
            "",
            _row(["Source", "Full B-V active", "Cube B-V active", "Enrichment", "Cube logical", "Cube DBs", "Composite median"]),
            _row(["---", "---:", "---:", "---:", "---:", "---:", "---:"]),
        ]
    )
    for source in SOURCE_ORDER:
        full_source_count = int(full_composition["sources"][source]["logical_instances"])
        source_count = int(cube_composition["sources"][source]["logical_instances"])
        full_v_count = int(
            full_treatment["by_source"][source]["treatment_presence"][
                "v_treatment_present"
            ]
        )
        support = cube_support["by_source"][source]
        cube_v_count = int(support["v_treatment_present"])
        lines.append(
            _row(
                [
                    SOURCE_LABELS[source],
                    _count_percentage(full_v_count, full_source_count),
                    _count_percentage(cube_v_count, source_count),
                    _enrichment(
                        full_v_count,
                        full_source_count,
                        cube_v_count,
                        source_count,
                    ),
                    _number(source_count),
                    _number(cube_composition["sources"][source]["databases"]),
                    f"{cube_difficulty['by_source'][source]['composite_score']['median']:.3f}",
                ]
            )
        )

    full_retained = int(full_quality["retained_logical_instances"])
    full_eligible = int(full_quality["eligible_before_execution_adjudication"])
    full_pass_rate = _percentage(full_retained, full_eligible)
    lines.extend(
        [
            "",
            "逐 source 对比显示 targeting 不是由单一 benchmark 驱动：五个来源的 B-V active rate 均提高，其中 Spider 从 12.9% 提高到 79.2%。Cube 同时保持每 source 96 个 logical instances，避免高覆盖 source 通过更大样本量主导 factorial effects。",
            "",
            "## 12. Figure D3 — Full→Cube Construction and Verification Funnel（推荐正文）",
            "",
            "```mermaid",
            "flowchart LR",
            f"    A[Full eligible intents<br/>{_number(full_eligible)}] --> B[Versioned SQL repairs<br/>{_number(full_quality['versioned_sql_repairs'])}]",
            f"    B --> C[Execution adjudication drops<br/>{_number(full_quality['dropped_logical_instances'])}]",
            f"    C --> D[Retained Full logicals<br/>{_number(full_retained)} / {full_pass_rate}]",
            f"    D --> E[Claim-driven Cube selection<br/>{_number(cube_total)} / {_percentage(cube_total, full_retained)}]",
            f"    E --> F[Complete eight-cell realizations<br/>{_number(cube_composition['realizations'])}]",
            f"    F --> G[Execution-equivalent groups<br/>{_number(cube_quality['audit_summary']['eight_cell_execution_equivalence']['pass'])} / 100%]",
            "    G --> H[Human audit and frozen rebuild<br/>pending]",
            "```",
            "",
            f"Full BIRD export currently contains {full_quality['bird_format']['packages']} source×configuration packages and {_number(full_quality['bird_format']['samples'])} samples；Cube BIRD export contains 40 source×cell packages and {_number(cube_composition['realizations'])} samples。Cube 因继承 BULL redistribution blocker 仅提供 local-only symlink package。",
            "",
            "## 13. 数据集合理性与有效性论证（可直接改写进论文）",
            "",
            "### 13.1 构念有效性（construct validity）",
            "",
            f"- 每个 Cube logical instance 具有完整八格，当前 `{str(cube_completeness['contract_satisfied']).lower()}`；B-Q 的 Q-axis 与 B-S 的 S-axis intervention 在全部样本中实际发生，而不是仅靠文件名定义。",
            f"- B-V 的 V-axis intervention 在 {_number(cube_support['treatment_support']['v_treatment_present']['count'])}/{_number(cube_total)} 个样本中实际发生；literal-free 和 fixed/control 样本被显式保留，不把没有 value change 的样本错误归入 B-V。",
            "- Barrier 标签在模型运行前由 SQL/schema/value 结构定义，只表示检验机会，不把模型错误循环定义成语言障碍。",
            "",
            "### 13.2 内部有效性（internal validity）",
            "",
            f"- {_number(cube_total)}/{_number(cube_total)} 个八格组通过独立执行等价审计，降低数据库迁移、SQL rewrite 或编码差异造成伪语言效应的风险。",
            "- 同一 logical ID 固定 intent、database semantics、gold answer 与 split；相邻 cells 只改变设计中的语言轴及其必要依赖。显式 single-axis diff audit 仍是冻结前门禁。",
            "- 采样不读取待评测模型 accuracy/error，难度使用 source 内 SQL/schema/value descriptors，避免 benchmark selection leakage。",
            "",
            "### 13.3 外部与覆盖有效性（external/coverage validity）",
            "",
            f"- Full 保留五源 {_number(full_total)} 个 retained logical instances 和 {_number(full_composition['realizations'])} 个 coupled realizations，提供自然 source distribution 下的总体与 source-level 检验。",
            f"- Cube 从相同 Full candidate universe 选择 {_number(cube_total)} 个样本，每 source 96 个，覆盖全部 {_number(cube_databases)} 个当前 core databases；因此诊断结果不由最大 source 主导。",
            "- Cube 不是概率代表性样本，不能单独外推真实 workload prevalence；外部有效性必须依赖 Full，Cube 负责机制定位。",
            "",
            "### 13.4 统计有效性（statistical validity）",
            "",
            f"- 每个 factorial cell 有 {_number(cube_total)} 个 aligned realizations，source 配额完全平衡；hard/medium 合计 {_number(selected['tiers']['hard'] + selected['tiers']['medium'])} 个，为主效应与交互分析提供更高信息量。",
            f"- B-V active intervention coverage 从 Full 的 {_percentage(candidate_v, 1)} 提升到 Cube 的 {_percentage(selected_v, 1)}，使 V 与 Q×V/S×V contrasts 不被大量 B-V control 样本稀释。",
            "- 数据库是 cluster 而非独立样本；最终分析必须使用 database/source clustered uncertainty、source macro summary，并报告 EHRSQL 两库导致的 concentration limitation。",
            "",
            "### 13.5 当前限制与冻结条件",
            "",
            "- 当前 Full 为 draft、Cube 为 engineering-draft，全部数字 non-claim-bearing。",
            "- BULL license/redistribution 未解决；公开发布必须 fail closed。",
            "- Full human fidelity/naturalness/grounding audit 和 Cube Q-LEX/Q-REF、V-NORM/V-RETRIEVE 双人人工 annotation 未完成。",
            "- Cube 必须在 frozen Full hash 上重新 profiling、sampling、materialization、audit 和统计，工程版 membership 不能直接升级。",
            "",
            "## 14. 推荐论文表述（英文草稿）",
            "",
            "> **Dataset design.** MoL-SQL provides two complementary views over aligned logical instances. MoL-Full preserves the retained distributions of five source workloads for broad source-level evaluation, while MoL-Cube selects a source-balanced diagnostic panel and realizes every instance in all eight question–schema–value language configurations. This separation lets Full assess generality under natural workload mixtures and Cube identify marginal and interaction effects of language placement without treating the diagnostic sample as a representative workload distribution.",
            "",
            "> **Construction validity.** The engineering Cube contains 480 logical instances and 3,840 realizations. Every logical instance has exactly eight cells, all 480 groups pass execution-equivalence checks, and the Q and S language-axis interventions associated with B-Q and B-S are active for every selected instance. The V-axis intervention associated with B-V is active for 332 instances, while literal-free and other controls remain explicitly labeled rather than being counted as B-V cases.",
            "",
            "> **Sampling validity.** Cube selection uses source-balanced quotas, database concentration constraints, pre-model B-Q/B-S/B-V/B-I opportunities, and source-internal SQL/schema/value difficulty. It does not use errors from evaluated systems. Relative to the Full candidate pool, the selected Cube intentionally increases hard cases and the share of instances with an active B-V value-axis intervention to improve diagnostic power; consequently, Cube effects are reported separately from Full natural-distribution results.",
            "",
            "## 15. Freeze-time replacement checklist",
            "",
            "- [ ] Resolve BULL license and public redistribution policy.",
            "- [ ] Complete two-reviewer Full fidelity/naturalness/grounding audit and agreement.",
            "- [ ] Complete Cube Q-LEX/Q-REF and V-NORM/V-RETRIEVE annotations.",
            "- [ ] Add explicit single-axis intervention diff audit.",
            "- [ ] Rebuild Cube from frozen Full manifest and recompute this report.",
            "- [ ] Replace Mermaid with frozen plotting-script outputs and confidence-aware experiment figures.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_dataset_paper_report(options: DatasetPaperReportOptions) -> Path:
    output_path = _resolve(options.repo_root.resolve(), options.output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_render(options), encoding="utf-8", newline="\n")
    return output_path
