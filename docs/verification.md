# 验证与评测

在仓库根目录执行：

```powershell
# 默认离线测试：模型、检索和向量使用确定性替身
uv run --no-sync python scripts/verify_project.py
# 可选：真实 PostgreSQL，使用随机隔离 schema
uv run --no-sync python scripts/verify_project.py --db
# 可选：PostgreSQL + Milvus，要求已有冻结索引与查询缓存
uv run --no-sync python scripts/verify_project.py --db --milvus
```

结果保存在忽略提交的 `data/cache/verification/<批次>/`，包含日志、JUnit 和 summary。上述测试不新增真实模型或 Embedding 调用；不能把替身测试通过率写成模型准确率。Milvus 测试写入独立 UUID 集合，冻结历史集合只读。

模型效果评估与代码验证分别报告。当前应用测试按功能维护，范围见 [测试索引](../tests/README.md)；旧阶段生成、冻结、独立评测脚本的测试不再纳入默认回归。历史实验脚本与原始数据仍保留，入口见 [脚本索引](../scripts/README.md)和[数据索引](../data/README.md)。历史 Phase 7 校验依赖已移除的规则文件，不属于当前验收范围；含 live / execute 的实验可能调用付费服务，重新执行需另行准备材料并确认模型、接口、配置和额度，历史预算不复用为新授权。

历史测试数量、原始提案、费用台账和阶段报告保留在本机仓库外。本公开仓库不依赖这些日志，也不将未随仓库提供的历史成绩作为当前验收结果。复现某次历史实验需另备该批配置、缓存和原始记录。
