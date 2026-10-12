# 脚本索引

日常使用从 `start_local.py`、`knowledge.py` 和 `verify_project.py` 开始。阶段名不代表脚本已废弃；下表逐项说明保留用途。

| 脚本 | 用途与依赖 |
| --- | --- |
| [start_local.py](start_local.py) | 通用启动；--demo 为隔离替身模式，真实模式可启动基础设施 |
| [start_v2_flash.py](start_v2_flash.py) | 兼容旧命令；固定最终评测的 Phase 7 / Flash / Cases Hybrid Top-5 / Docs BM25 配置 |
| [serve_m5_demo.py](serve_m5_demo.py) | 隔离演示服务；start_local 调用，不是过期 M5 产物 |
| [configure_local_auth.py](configure_local_auth.py) | 生成本地身份令牌；保留已有配置 |
| [knowledge.py](knowledge.py) | seed / 缓存导入 / 索引同步；默认 Embedding 预算为零 |
| [verify_project.py](verify_project.py) | 默认离线回归；--db / --milvus 启用隔离真实服务验证 |
| [check_database.py](check_database.py) | 当前数据库连接诊断；访问真实 PostgreSQL |
| [check_milvus.py](check_milvus.py) | Milvus 集合只读连通检查 |
| [check_corpus.py](check_corpus.py) | v2 合成案例格式检查；本地数据 |
| [validate_phase7.py](validate_phase7.py) | Phase 7 数据验收 CLI；本地冻结数据 |
| [phase7_offline.py](phase7_offline.py) | Phase 7 校验、manifest / 查询生成、审批绑定及预检实现；测试导入 |
| [pilot_phase7_live.py](pilot_phase7_live.py) | 有预算的真实模型预检；需原始缓存和明确授权 |
| [evaluate_phase7_live.py](evaluate_phase7_live.py) | 真实 E2E 评测；PostgreSQL / Milvus / 模型，需配置与预算授权 |
| [evaluate_phase7_retrieval.py](evaluate_phase7_retrieval.py) | 真实三模式检索实验；Milvus / Embedding，需额度授权 |
| [score_phase7_live.py](score_phase7_live.py) | 已有 Phase 7 结果的离线评分；不生成模型输出 |
| [evaluate_retrieval.py](evaluate_retrieval.py) | M3 固定查询检索评测；真实 Milvus，缺查询缓存时可能调用 Embedding |
| [evaluate_m4.py](evaluate_m4.py) | M4 历史评测与回归入口；可执行真实模型路径，预算受控 |
| [check_ticket_graph.py](check_ticket_graph.py) | 历史图缓存 / 预算诊断；test_graph_cache 直接加载 |
| [check_ticket_flow.py](check_ticket_flow.py) | HTTP / PG / Milvus 历史流程验证；依赖 check_ticket_graph |
| [check_m2_acceptance.py](check_m2_acceptance.py) | M2 审核验收适配器；多个单元与 HTTP 测试直接加载 |
| [check_m2_followup.py](check_m2_followup.py) | 客户补充回归；HTTP 测试直接加载，依赖 M2 验收 |
| [check_m2_recovery.py](check_m2_recovery.py) | 硬终止 / 恢复验证；真实 PG / HTTP，合成 Agent |
| [check_m3_flow.py](check_m3_flow.py) | 三模式流程回归；真实 PG / Milvus，合成模型决策 |
| [check_semantic_guardrail_live.py](check_semantic_guardrail_live.py) | 历史语义护栏诊断；真实调用需单独授权 |
| [init_case_collection.py](init_case_collection.py) | 旧冻结案例集合初始化；历史检索兼容，写 Milvus |
| [ingest_historical_cases.py](ingest_historical_cases.py) | 旧冻结案例索引导入；历史检索兼容，可能调用 Embedding |

真实模型或 Embedding 调用前确认模型、接口、配置和预算，不能以脚本默认值代替授权。旧集合导入仅用于复现冻结历史检索；当前正式知识使用 `knowledge.py`，不能用旧导入脚本覆盖生产集合。

Phase 7 live / 检索实验的输出限制在仓库父目录 `log/evaluation/` 下，脚本按仓库位置解析该目录；更换机器时需准备缓存、台账与输出目录。旧 M2/M4 实验同样依赖该批本地原始材料，默认离线测试与应用启动不要求这些历史记录。
