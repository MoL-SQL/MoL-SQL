# Direct-ZS Protocol

## 论文角色

Direct-ZS 是 model-controlled 的最低复杂度基线，用于测量同一模型在 Q/S/V 语言配置变化下的
端到端性能。它不是 schema-linking 方法，也不应混入按 source 调优的知识、translation、
retrieval 或 oracle 信息。

## 冻结输入

- 单条 `user` message；无 `system` message；
- 所有语言 cell 使用同一套英文 instruction；
- SQLite 方言；
- 展示数据库全部 user tables 的原始 `CREATE TABLE`；
- 展示 SQLite foreign keys；
- 每张表按数据库自然返回顺序展示前 3 行，不随机采样；
- 展示问题，不展示 gold SQL 或 BIRD evidence；
- zero-shot，无 demonstration、CoT、schema linking、translation 或 English pivot；
- 要求单行 SQL，并提醒中文/非 ASCII identifier 使用反引号。

## 冻结输出与预算

- 每个 realization 只生成 1 个候选；
- `temperature=0.0`，默认 `max_tokens=4096`；
- Qwen3 非流式请求设置 `enable_thinking=false`；
- parser 兼容 bare SQL、`SQL:` label、Markdown fence 和 `<sql>`，仅用于抵抗格式偏差，
  不增加候选预算；
- execution mismatch、invalid SQL 和错误答案不调用模型修复；只有 request-level API failure、
  empty response 或无法提取 SQL 的响应可在重启同一 run 后重试。

## 必须保留与可改进项

必须保留的是信息可见性和推理预算：full schema、first-3 values、统一英文 instruction、
zero-shot、无 evidence、单候选、无 reasoning/revision。否则实验行不再是同一个 Direct-ZS。

可以改进但必须记录的是工程调度：worker 数、429 退避、checkpoint 格式、token/latency 记录、
失败恢复和 manifest 完整性。这些变化不向模型增加信息或候选，因此不改变论文方法定义。

反引号和 SQLite 函数提醒应保留。它们不是针对某个语言 cell 的性能 trick，而是跨语言 SQL
可执行性的最低方言约束。BULL-specific abbreviation note、evidence、中文 instruction、CoT 和
schema selection 均不属于当前 Direct-ZS 主表协议；若加入，应作为独立 ablation/method variant。
