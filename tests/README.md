# 当前版本测试

测试围绕当前应用行为组织，文件按功能命名。旧阶段独立验收脚本、M4 数据集打分、Phase 7 生成/冻结/批次校验以及早期图缓存探针的测试已移出本测试目录；它们不再是当前应用回归的要求。

| 测试范围 | 主要文件 |
| --- | --- |
| 默认启动配置 | `test_start_v2_flash.py`、`test_config.py` |
| Agent 状态、单图执行与恢复 | `test_agent_state.py`、`test_agent_durable.py`、`test_workflow_lifecycle.py`、`integration/test_agent_*_postgres.py` |
| 五动作、双只读工具与预算 | `test_agent_policy.py`、`test_tool_docs_graph.py`、`test_decision_*.py`、`test_call_budget.py`、`test_call_adapters.py` |
| Judge、提案与状态承诺 | `test_semantic_judge.py`、`test_proposals.py`、`test_reply_claims.py` |
| Cases / Docs / 知识索引 | `test_retrieval.py`、`test_documents.py`、`test_knowledge_index.py`、`integration/test_knowledge*.py` |
| API、审核、失败与事务 | `integration/test_ticket_api.py`、`test_reviews.py`、`test_runtime_reliability.py`、`test_run_*.py`、`test_reply_claims_http.py` |
| 工作台和可信身份 | `test_workbench_client.py`、`integration/test_workbench_http.py`、`test_knowledge_workbench.py` |

默认执行 `uv run --no-sync python scripts/verify_project.py`，使用确定性模型与检索替身。`--db` 验证随机隔离 PostgreSQL schema；`--db --milvus` 额外验证独立 Milvus 集合及已有冻结缓存。任何未启用的真实服务测试显示 skipped，不计为通过。

历史文件名中的阶段编号已从当前功能测试中去掉。兼容性断言只保留当前实现仍支持的缓存、审核检查点和预算台账行为；代码或配置改变时更新有实际业务含义的夹具与预期，不能只放宽断言来获得通过结果。
