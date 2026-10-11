# 数据目录

所有 `synthetic` 数据都是虚构示例，不是真实客户工单或产品政策。目录按冻结版本保留，不按名称新旧删除。

| 目录 | 当前用途 |
| --- | --- |
| `synthetic/v2` | 默认 seed 和固定 v2 启动器的 12 条历史知识；旧评测基线 |
| `synthetic/docs` | 日常 Docs 工具的两篇合成产品文档 |
| `synthetic/phase7_v1` | 8 篇 Docs、120 条 Cases、48 条工单；当前独立评测入口使用的冻结数据、manifest、标签审批与离线报告 |
| `synthetic/m3` | 固定查询与诊断夹具；检索评测默认输入、M3 回归与 Phase 7 重复样本检查使用 |
| `synthetic/m4` | 历史评测回归、开发标签与 hash 复核记录；M4 脚本和 Phase 7 重复样本检查使用 |
| `synthetic/live_e2e_v1` / `live_e2e_v2` | 历史流程夹具；Phase 7 校验和测试使用，v2 验证器还与 v1 比较 |
| `cache` | 本机向量、提案缓存、调用台账、演示令牌与测试结果；已忽略提交 |

数据构建脚本和复核记录用于重建、内容 hash 审批与防止标签泄漏。`phase7_v1/offline_validation_report.json` 是冻结数据的校验快照，保留在版本内；一次性运行输出写入本地缓存或仓库外日志。

旧数据集保留是为了现有回归可复现，不能把它们当作未接触的盲测集。向量缓存与预算台账可能用于后续重放，不按缓存目录阶段名称清空。初始化见 [配置指南](../README.md)，数据契约见 [Phase 7 契约](../docs/phase7-data-contract.md)。
