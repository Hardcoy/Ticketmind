# 来源、复用与贡献说明

## 基线与本轮新增范围

本仓库 Git 可追溯的初始基线为 `28004d1`（Initial commit: TicketMind application）。该基线已有工单模型、FastAPI 基础入口、理解与 Dense 检索、合成语料及开发脚本。它们不能计为本轮 M0—M5 从零新增。后续能力按提交和模块核对：

| 阶段 | 可检查的实现 |
| --- | --- |
| M0/M1，467ace9 | 一致运行入口、精确缓存、可信身份、数据库快照处理、幂等及待审/失败落库 |
| M2，a827fa9 | 受控工具、不可变审核、PostgreSQL interrupt/resume、客户补充、人工回复、显式关闭、恢复验证 |
| M3，abe0749 | 版本化 BM25、Dense/BM25/Hybrid、RRF、统一证据及检索诊断 |
| M4，192f115 | 业务规则、开发标签 overlay、独立分组样本、评测入口、调用账本与实测报告 |
| M5，已纳入当前基线 | Streamlit HTTP 工作台、可信身份读取、审核原请求恢复、隔离演示、启动器及交付文档 |

开发使用 AI 辅助实现、调试和文档。用户参与需求、范围、预算和业务判定授权；M4 标签由用户委托 Agent 审查，不是独立人工标注。贡献说明应以可追溯提交和实际实现为准。

## 上游参考与依赖

原计划列出 [agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit) 作为参考。本地 Git 历史从上述初始提交开始，现有记录不足以确定初始基线是否包含逐文件复制；因此不声称“全部原创”，也不凭空给出复制比例。若后续确认有直接复制内容，应补对应文件、上游 commit 和许可证声明。本轮没有复制该项目代码。

以下能力由依赖提供：FastAPI 的路由和请求校验，SQLAlchemy/Alembic 的持久化和迁移，LangGraph 的图执行与持久化中断，Milvus 的向量/BM25 检索，Streamlit 的页面组件和 AppTest，模型服务的理解、向量和文本生成。项目新增工作是业务边界、受控编排、HTTP/数据集成、审查流程与验证证据；不能把框架原有能力作为自研算法。

参考入口：[LangGraph 中断](https://docs.langchain.com/oss/python/langgraph/interrupts)、[Milvus BM25](https://milvus.io/docs/full-text-search.md)、[Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest)。具体版本以 `uv.lock` 为准。
