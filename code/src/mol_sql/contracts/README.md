# `contracts/`

定义贯穿数据构建、审计和 release 的稳定数据协议，防止不同阶段使用隐式或不兼容字段。

## 使用

```python
from mol_sql.contracts import LogicalInstance, Realization, ReleaseManifest
from mol_sql.contracts.io import load_jsonl, write_jsonl
```

## 结构

- `models.py`：Pydantic v2 严格模型及四格/冻结约束；
- `ids.py`：基于规范化输入生成稳定 ID；
- `hashing.py`：文件和 canonical JSON 的 SHA-256；
- `io.py`：确定性 JSON/JSONL 读写。

当前 contract 版本为 `mol-sql-contract-v0.1`，未知字段会被拒绝。
