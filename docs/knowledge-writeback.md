# 知识库配置与维护

PostgreSQL 保存权威正文、来源、版本、审核和状态；Milvus 保存可重建索引。运行检索按来源 ID 从 PostgreSQL 读取正文并核对状态与 hash，索引命中本身不代表证据可信。

## 初始化与运维命令

在仓库根目录运行，连接配置读取 `.env`：

```powershell
uv run --no-sync alembic upgrade head
uv run --no-sync python scripts/knowledge.py seed
# 已有精确匹配向量缓存时可选；缺缓存不会自动生成
uv run --no-sync python scripts/knowledge.py import-cache
```

`seed` 使用 `TICKETMIND_CORPUS_PATH`（默认 `data/synthetic/v2/historical_cases.jsonl`），冻结数据集由内容 hash 标识。重复导入相同内容不重复插入，也不重新激活停用案例。

```powershell
$dataset = 'synthetic-v2-e5b5a59a7e1481ad3b095d518772354155d891e51ad2a367cf5f7be26540228f'
uv run --no-sync python scripts/knowledge.py reconcile --dataset $dataset
```

BM25 不要求文档向量；`active` 表示文本索引就绪，Dense 就绪单独记录。缺向量时默认不调用 Embedding，Dense 保持未就绪。使用 Dense 需准备匹配当前 provider / region / workspace / model / dimension / 正文的向量缓存并同步；Hybrid 可通过关键词通道召回无向量知识。查询向量在真实 Dense / Hybrid 运行中仍可能调用 Embedding。

生产知识使用独立 `production-v1`。选择它时在 `.env` 设置 `TICKETMIND_KNOWLEDGE_DATASET=production-v1` 并重启服务；固定 v2 启动器会覆盖该选择，须改用 `scripts/start_local.py`。

## 人工发布与索引修复

1. reviewer 明确关闭已解决工单。
2. 在工作台核对会话，填写问题、适用条件、处理步骤和验证结果。
3. 确认发布请求；系统先保存批准记录与知识正文，再同步索引。
4. 查看文本 / Dense 状态；失败时显式重试，不把待审草稿当知识。

所有写入校验角色、版本和幂等键。同一工单只发布一条知识，正文不支持原地编辑；停用保留 PostgreSQL 历史记录，立即禁止正常检索使用该来源。索引删除失败可再次清理。

```powershell
uv run --no-sync python scripts/knowledge.py reconcile --dataset production-v1
uv run --no-sync python scripts/knowledge.py reconcile --dataset production-v1 --repair-active
uv run --no-sync python scripts/knowledge.py reconcile --dataset production-v1 --source-id TICKET-实际UUID
```

同步按数据库 / schema / dataset 使用 advisory lock，网络期间不持有业务事务。Milvus 写入后核对 ID/hash；失败保留诊断，成功的向量缓存可复用。`--repair-active` 检查已激活但缺失的索引；reconcile 也清理索引中不存在于 PostgreSQL 的孤儿来源。

默认 `--embedding-budget=0`。确需新向量时，先确认模型、接口、配置与额度，再指定正预算及持久化 `--ledger`；失败请求也计入预算，不删除台账重置额度。HTTP 发布与重试没有隐式付费开关。

## 产品 Docs

```powershell
uv run --no-sync python -m ticketmind.documents.cli data/synthetic/docs --version synthetic-product-docs-v1
```

设置 `TICKETMIND_DOCS_DATASET=synthetic-product-docs-v1`、`TICKETMIND_DOCS_RETRIEVAL_MODE=bm25`、`TICKETMIND_AGENT_VERSION=ticketmind-tools-docs-v2`。导入与分块可重复执行，使用 `--no-index` 时索引未就绪。Docs 为独立 PostgreSQL chunk 存储和 BM25 集合，当前 Hybrid 配置显式降级到 BM25。导入目录中的每个 Markdown 都被作为产品文档，因此不能放工程 README、标签或面试资料。

Phase 7 产品文档是另一冻结版本；导入及验收条件见 [数据集说明](../data/synthetic/phase7_v1/README.md)。演示模式的索引替身不能当作真实 Milvus 验证。架构与接口见 [架构说明](architecture.md)，验证见 [验证指南](verification.md)。
