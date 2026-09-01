# `dataset/adapters/`

将 Spider、BIRD、BULL、EHRSQL 和 KaggleDBQA 的不同目录、字段与 SQL 格式统一为 MoL-Full 构建器可消费的对象。

## 使用

adapter 通常由 `build-full` 根据 `source_family` 自动选择；也可在代码中调用：

```python
from mol_sql.dataset.adapters import adapter_for, load_source_specs
```

## 结构

- `base.py`：source/variant 配置模型、四格完整性检查、路径解析和通用加载；
- `spider.py`、`bird.py`、`bull.py`、`kaggledbqa.py`：复用通用 adapter；
- `ehrsql.py`：额外规范 EHRSQL 的 SQL 方言与时间表达式；
- `__init__.py`：维护 `source_family` 到 adapter 的显式映射。
