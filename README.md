# MoL-SQL

MoL-SQL evaluates Text-to-SQL when **question**, **schema**, and **value**
languages are controlled independently. Each logical instance is realized in
aligned language configurations and checked by execution.

- **MoL-Full**: 4,223 logical instances × 4 cells (English/Chinese question ×
  English/Chinese database) = 16,892 realizations
- **MoL-Cube**: 480 logical instances × 8 cells (independent Q × S × V) =
  3,840 realizations

Sources: Spider, BIRD mini-dev, BULL, EHRSQL, KaggleDBQA.

## Repository layout

```text
code/           Full/Cube builders, audit, Direct-ZS CLI
data/releases/  packaged MoL-Full and MoL-Cube
experiments/    Direct-ZS, Direct-FS, Baseline-CoT, Q-to-DB
migrate/        optional language-migration pipeline
```

## Setup

Python 3.10+. From the repository root:

```bash
pip install -e code/
pip install -r requirements.txt
cp .env.example .env
```

SQLite databases sit next to the BIRD-format packages. They are gitignored;
keep the local copies under `data/releases/` for execution evaluation.

## Run Cube baselines

Smoke (2 IDs, BIRD only):

```bash
bash experiments/bash/run_cube_direct_zs.sh qwen --source bird --limit-ids 2
```

Full Cube (480 × 8):

```bash
bash experiments/bash/run_cube_direct_zs.sh qwen --source all
bash experiments/bash/run_cube_direct_fs.sh qwen --source all
bash experiments/bash/run_cube_baseline_cot.sh qwen --source all
bash experiments/bash/run_cube_q_to_db_translate.sh qwen --source all
```

Direct-ZS through the package CLI:

```bash
PYTHONPATH=code/src python -m mol_sql.cli experiments run-direct-zs \
  --model qwen3.6-35b-a3b --api-profile dashscope --workers 2
```

See [experiments/README.md](experiments/README.md).

## Dataset files

BIRD-compatible packages:

```text
data/releases/full/mol-full-v0.1/bird_format/<source>/<Q--S--V>/
data/releases/cube/mol-cube-v0.1/bird_format/<source>/<Q--S--V>/
```

Each package has `dev.json`, `dev_gold.sql`, `tables.json`, and `database/`.

Optional rebuild (needs aligned four-cell seeds under `seeds/`):

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset build-full
PYTHONPATH=code/src python -m mol_sql.cli dataset build-cube \
  data/releases/full/mol-full-v0.1 \
  artifacts/paper_stats/dataset/provisional/mol-full-v0.1 \
  --allow-draft --overwrite
```

Language migration from upstream origin dumps: [migrate/README.md](migrate/README.md).

```bash
PYTHONPATH=code/src python -m unittest discover -s code/tests -v
```

## Licenses

| Source | License |
|--------|---------|
| Spider | Apache-2.0 |
| BIRD mini-dev | CC-BY-SA-4.0 |
| EHRSQL | CC-BY-4.0 |
| KaggleDBQA | CC-BY-SA-4.0 |
| BULL / FinSQL | no published license |

BULL databases are included in this local copy for research use. Do not
redistribute them until a license is obtained. See
[code/configs/dataset/PROVENANCE.md](code/configs/dataset/PROVENANCE.md).
