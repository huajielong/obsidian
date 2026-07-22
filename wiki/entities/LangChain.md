---
title: "LangChain"
type: entity
tags: [LLM框架, Agent框架, Harness Engineering, 模型抽象, 工具编排, RAG]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-14
---

# LangChain

LangChain 是由 Harrison Chase 于 2022 年 10 月创立的 **LLM 应用开发框架**，本质上是 **Harness Engineering（工程层）** 的集大成者。它提供了一整套工具链来封装模型调用、构建 Agent 循环、管理记忆、实现 RAG 检索增强生成等，让开发者能高效地将 LLM 从"对话玩具"变为"生产级 Agent 系统"。

截至 2026 年，LangChain 已发展为包含 LangGraph（图编排）、LangSmith（可观测性）、LangMem（长期记忆）等子项目的完整生态系。

## 发展历程

| 年份 | 里程碑 | 意义 |
|------|--------|------|
| 2022.10 | Harrison Chase 创建 LangChain | 首个 LLM 应用开发框架诞生 |
| 2023 | 引入 Agent 概念与 ReAct 循环 | 使 LLM 具备自主工具调用能力 |
| 2023 | Plan-and-Execute 模式 | 将规划与执行分离，成为 [[Agent_Loop]] 演进的关键里程碑 |
| 2024 | 拆分出 LangGraph / LangSmith | 从链式走向图式编排，补充可观测性 [见 [[Agent_Observability]]] |
| 2025 | LangChain 1.0 发布 | 基于 LangGraph 重构核心，引入 `create_agent()`、中间件、状态机架构 |
| 2026 | Agent-first 范式成熟 | 教程体系从"Chain 优先"转向"Agent 优先"，重心全面转向 LangGraph 生产级编排 |

## 核心架构

### 1. 模型抽象层（Model Abstraction）

统一接口对接各大模型供应商，一行代码切换模型：

```python
from langchain.chat_models import init_chat_model
llm = init_chat_model("gpt-4o", model_provider="openai")
# llm = init_chat_model("claude-sonnet-4", model_provider="anthropic")
```

### 2. 工具系统（Tool System）

通过 `@tool` 装饰器将任意函数封装为模型可调用的工具，涵盖 API 调用、数据库查询、代码执行等。

### 3. Agent 循环（Agent Loop）

核心的 **ReAct 循环**模式：**推理 → 行动 → 观察 → 再推理**，模型自主决策何时调用哪个工具。参考 [[Agent_Loop]]。

### 4. RAG 流水线（Retrieval-Augmented Generation）

连接文档库 → 向量化 → 检索 → 生成，让模型基于私有知识回答。参考 [[RAG]] 和 [[Chunking]]。

### 5. 记忆管理（Memory）

支持短期对话记忆（Buffer）和长期持久化记忆（VectorStore-backed），参考 [[Memory_Agent]]。

## LangChain 生态全景

```
LangChain 生态系（2026）：
├── langchain-core          ← 核心抽象（LLM / Tools / Memory / Chains / LCEL）
├── langchain-community     ← 社区集成（向量数据库 / 嵌入模型 / 文档加载器）
├── langgraph               ← 图式 Agent 编排（生产级 Multi-agent）→ [[LangGraph]]
├── langsmith               ← 可观测性 / 调试 / 评测平台 → [[Agent_Observability]]
├── langserve               ← 部署服务化
├── langmem                 ← Agent 长期记忆系统 → [[Memory_Agent]]
├── langchain-cli           ← 命令行工具
└── langchain-text-splitters ← 文档分块（Chunking）策略 → [[Chunking]]
```

## 关键创新与贡献

### Plan-and-Execute（2023）
LangChain 首次将"规划（Plan）"与"执行（Execute）"两个步骤分离，这是 [[Agent_Loop]] 演进的关键里程碑。在此之前 Agent 循环基本只有 ReAct 模式，缺乏顶层规划能力。

### LCEL（LangChain Expression Language）
声明式链式调用语法，允许用 `|` 管道符将 Prompt、LLM、Parser 串接成可执行的 Chain，简化了基础流水线构建。

### Harness Engineering 的行业验证
在 [[Harness_Engineering]] 的行业验证表中，**LangChain 仅优化 Harness、不改变模型**，Terminal Bench 2.0 分数从 52.8% 提升至 66.5%（Top30 → Top5），是 Harness 工程的经典实践案例。

## 2026 年典型应用场景

| 场景 | 实现方式 |
|------|----------|
| **智能客服** | RAG 检索知识库 + Agent 动态路由到不同专家 Agent |
| **代码审查流水线** | 多 Agent 串联（Context → Analysis → Review） |
| **自动化测试** | Agent 自主编排：登录 → 操作 → 断言 → 截图 |
| **数据分析助手** | 自动清洗数据 → 探索分析 → 生成可视化报告 |
| **自动化运维** | 异常检测 → 根因分析 → 执行修复脚本 |
| **贷款审批** | 文件收集 → 风险评估（检查点）→ 人工审批 → 最终决策 |

## 最佳实践原则

1. **Agent-first**：先想 Agent 架构，再想 Chain 细节
2. **LangGraph 做外层编排**：多步工作流用有状态图，单步推理用 LCEL 链
3. **结构化输出是必选项**：所有 LLM 调用加 `with_structured_output()`，避免解析错误
4. **Traces 是新的真理源**：LangSmith 全链路追踪，出问题先看轨迹
5. **加人工审批节点**：重要操作（付款、删库、发邮件）加 Human-in-the-loop

## 基本信息

- **创建者**: Harrison Chase
- **License**: MIT
- **语言**: Python + TypeScript
- **GitHub**: https://github.com/langchain-ai/langchain
- **官方网站**: https://langchain.com

## 关联连接

- [[LangGraph]] — LangChain 团队的图式 Agent 编排框架，生产级 Multi-agent 首选
- [[Harness_Engineering]] — LangChain 是 Harness 工程化的集大成者和行业验证典范
- [[Agent_Loop]] — LangChain 贡献了 Plan-and-Execute 模式，是 Agent 循环演进的里程碑
- [[Agent_Observability]] — LangSmith（LangChain 生态）提供全链路可观测性
- [[Memory_Agent]] — LangMem 是 LangChain-native 的记忆系统
- [[RAG]] — LangChain 提供完整 RAG 流水线实现
- [[Chunking]] — LangChain 的 `RecursiveCharacterTextSplitter` 是从 Chunking 起步的推荐方案
- [[Reflexion]] — LangChain 提供了 LangGraph 版本的 Reflexion cookbook
- [[CrewAI]] — 同属 Agent 框架，LangChain 是底层基础设施，CrewAI 是角色驱动编排
- [[Dify]] — 开源 LLM 应用开发平台，LangChain 的可视化低代码替代方案
- [[AutoGen]] — 同属 Agent 框架，Microsoft 的对话式 Multi-agent 框架
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — Agent 框架全览来源
- [[摘要-agent-loop-guide]] — Agent Loop 指南中提及 LangChain 的 Plan-and-Execute
