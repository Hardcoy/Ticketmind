# TicketMind 本地配置

以下命令在仓库根目录执行，适用于 Windows PowerShell。

## 1. 安装与环境变量

准备 Python 3.12、uv、Docker Desktop，以及 PostgreSQL（本机服务或下方容器）。

```powershell
uv sync --locked
if (-not (Test-Path .env)) { Copy-Item env.example .env }
```

编辑 `.env`：

| 配置 | 填写内容 |
| --- | --- |
| `TICKETMIND_DATABASE_URL` | `postgresql+psycopg://用户名:密码@主机:端口/数据库`；密码特殊字符需 URL 编码 |
| `DASHSCOPE_API_KEY` | 百炼 API Key |
| `DASHSCOPE_WORKSPACE_ID` | 与 Key 对应的北京地域业务空间 ID |
| `TICKETMIND_DECISION_MODEL` | 示例为 `qwen3.8-flash` |
| `TICKETMIND_JUDGE_MODEL` | 配置独立审核模型；示例为 `deepseek-v4.1-flash` |
| `TICKETMIND_MILVUS_URI` | 本地为 `http://127.0.0.1:19530` |
| `TICKETMIND_RETRIEVAL_MODE` | `hybrid`；Cases 使用 Dense + BM25，Top-K=5 |
| `TICKETMIND_RETRIEVAL_TOP_K` | `5`；candidate_k=20、RRF k=60 |
| `TICKETMIND_DOCS_DATASET` | `synthetic-phase7-docs-v1` |
| `TICKETMIND_DOCS_RETRIEVAL_MODE` | `bm25` |
| `TICKETMIND_AGENT_VERSION` | `ticketmind-tools-docs-v2` |

生成本地 operator / reviewer 登录令牌，不覆盖已有令牌：

```powershell
uv run --no-sync python scripts/configure_local_auth.py
```

`.env`、登录令牌和本地缓存不提交 Git。模型配置示例不代表调用授权；实际处理工单会调用模型并可能产生费用。

## 2. 启动 PostgreSQL 与 Milvus

已有 PostgreSQL 服务时，在 `.env` 填写其实际连接信息。使用仓库容器时执行：

```powershell
if (-not (Test-Path infra/postgres/.env)) { Copy-Item infra/postgres/env.example infra/postgres/.env }
# 编辑 infra/postgres/.env，设置 POSTGRES_PASSWORD
docker compose --project-directory infra/postgres up -d --wait
```

容器连接为 `localhost:5433`，用户 `ticketmind_app`，数据库 `ticketmind_dev`；根目录 `.env` 的密码须与 `POSTGRES_PASSWORD` 一致。

```powershell
docker compose --project-directory infra/milvus up -d --wait
uv run --no-sync alembic upgrade head
```

## 3. 初始化示例知识库

默认使用最后一次完整评测的 Phase 7 数据：120 条合成案例、8 篇产品文档。`.env` 中设置 `TICKETMIND_CORPUS_PATH=data/synthetic/phase7_v1/historical_cases.jsonl` 后执行以下命令，不调用模型或 Embedding：

```powershell
uv run --no-sync python scripts/knowledge.py seed
$dataset = 'synthetic-v2-9c0552c76c338a73e05990c3c0d7a588149d7b8471a3b0c9a8a648b8d06b488a'
uv run --no-sync python scripts/knowledge.py reconcile --dataset $dataset --limit 120
uv run --no-sync python -m ticketmind.documents.cli data/synthetic/phase7_v1/docs --version synthetic-phase7-docs-v1
```

在 `.env` 设置 `TICKETMIND_KNOWLEDGE_DATASET` 为上述 `$dataset` 的完整值。只有源数据时，上述命令先准备 BM25；完整 Hybrid 还要求同模型、空间和正文的文档向量缓存就绪，缺缓存不会自动付费生成。未准备向量时先设 `TICKETMIND_RETRIEVAL_MODE=bm25`。同步后确认案例 `active`、Dense 就绪及 Docs 索引就绪；详见 [知识库配置](docs/knowledge-writeback.md)。

## 4. 启动应用

读取 `.env` 中的配置：

```powershell
uv run --no-sync python scripts/start_local.py --skip-infra
```

也可使用对齐最终评测参数的兼容入口（保留旧文件名，配置已更新为 Phase 7 / Flash / Cases Hybrid / Docs BM25）：

```powershell
.\start_v2_flash.cmd --skip-infra
```

工作台：[http://127.0.0.1:8501](http://127.0.0.1:8501)；API 文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。从本地 `.env` 读取对应角色令牌登录。`Ctrl+C` 停止 API 和工作台，数据库与索引保留。

真实 Hybrid 处理任意新工单可能调用查询 Embedding；最后一次评测的 48 条固定查询缓存及批次费用额度不自动应用于日常工作台。

只演示界面与审核流程时，仅需 PostgreSQL，运行以下命令；该模式使用模型与检索替身，API 端口为 8010：

```powershell
uv run --no-sync python scripts/start_local.py --demo
```

演示令牌路径由终端输出。操作步骤见 [演示指南](docs/demo-guide.md)，其他维护资料见 [文档索引](docs/README.md)。
