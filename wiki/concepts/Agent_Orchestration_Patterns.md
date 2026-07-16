---
title: "Agent_Orchestration_Patterns"
type: concept
tags: [orchestration, multi-agent, pattern, agent框架, LLM系统设计]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-10
---

# Agent Orchestration Patterns

Multi-agent 系统中多个 Agent 之间的协作编排模式。这些模式与 [[Chain_of_Thought]]、[[Agent_Loop|ReAct]] 等单 Agent 内部推理范式是正交的两个层——前者管"多个 Agent 之间怎么协作"，后者管"单个 Agent 内部怎么思考"。

## 五大编排模式（按复杂度排序）

### 1. Routing / Handoff ⭐

Agent 之间 1:1 handoff，无中央 orchestrator。

- **经典场景**：客户支持路由、context switch
- **代表实现**：[[OpenAI]] Swarm、OpenAI Agents SDK
- **关键特性**：轻量、去中心化、适合明确分工的场景

### 2. Sequential（Planner → Executor）⭐⭐

Planner 规划多步骤 + Executor 执行。

- **经典场景**：多步骤自动化、code generation
- **代表实现**：LangGraph、ChatDev paper
- **关键特性**：步骤依赖明确、适合流水线式任务

### 3. Parallel（并行加速）⭐⭐⭐

N 个 Agent 同时跑、结果 aggregate。

- **经典场景**：research / map-reduce 任务、wall-clock 1/N
- **代表实现**：LangGraph parallel branches、CrewAI parallel tasks
- **关键特性**：省 wall-clock 时间、需处理 async coordination + partial failure + state merge
- **⚠️ 坑点**：并行协调、部分失败处理、状态合并一致性

### 4. Supervisor-Worker（Hub-Spoke）⭐⭐⭐

1 个主 Agent + N 个 Worker，主分配 + 整合。

- **经典场景**：任务拆解、报告整合
- **代表实现**：LangGraph、AutoGen GroupChat
- **关键特性**：中央控制、适合复杂任务拆解

### 5. Debate / Society（多视角收敛）⭐⭐⭐⭐

2+ Agent 互相 critique 或角色扮演。

- **经典场景**：research、judgment task、social simulation
- **代表实现**：AutoGen GroupChat、CAMEL paper、Generative Agents paper
- **关键特性**：最复杂模式、适合需要多元视角的任务

## 进阶 Tool Patterns

Framework 提供的三个进阶 Tool Pattern，需 Framework 抽象层才写得干净：

| Pattern | 解决的问题 | 代表实现 |
|---|---|---|
| **Dynamic tool selection** | >30 个工具时 prompt 塞不下 | [[LlamaIndex]] tool router（embedding-based 路由）|
| **Tool composition / chaining** | A→B 无 LLM 中间叙事（省 token + latency） | LangGraph state graph、CrewAI sequential tasks、Pydantic AI |
| **Tool-augmented retrieval** | RAG 搜索 → 再 reason | LangGraph 把 retriever 包成 tool node |

## Claude Code 的 Subagent 编排模式

除了 LangGraph/CrewAI 等 Framework 路线，Claude Code 通过 [[Claude_Code_Subagent]] 提供原生 Subagent 编排：

| 模式 | Claude Code 实现 | Framework 对应 |
|------|-----------------|---------------|
| **Subagent Dispatch** | `.claude/agents/<name>.md` + Task Tool | Supervisor-Worker |
| **Agent Team** | 多 Agent 互相沟通/Debate（需 Opt-in）| Debate / Peer Review |
| **Background Agent** | `claude --bg` + Agent View 监控 | 无直接对应（Claude Code 特有）|
| **Dynamic Workflows** | Opus 4.8+ 自生成 Workflow 脚本 | 无直接对应（Claude Code 特有）|

## 如何选择

1. 先确认真的需要 [[Multi_Agent_System]]（90% 场景不需要）
2. 按复杂度从低到高选择：Routing → Sequential → Parallel → Supervisor-Worker → Debate
3. Framework 优先选 [[LangGraph]]（Production）或 [[CrewAI]]（快速雏形）
4. 简单场景可以自己写 dict + for loop，不需要 Framework

## 关联连接

- [[Multi_Agent_System]] — Multi-agent 的核心概念与决策框架
- [[Claude_Code_Subagent]] — Claude Code 原生 Subagent 编排模式
- [[Claude_Code_Dynamic_Workflows]] — Opus 4.8+ 动态 Workflow 编排
- [[Agent_Loop]] — Single-agent ReAct 循环（与编排模式是正交的两个层）
- [[Chain_of_Thought]] — 单 Agent 内部推理范式
- [[LangGraph]] — 图式编排框架，覆盖所有 5 种模式
- [[CrewAI]] — 角色驱动框架，擅长 Sequential 和 Parallel 模式
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本概念的核心来源
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — Subagent 编排的深度来源
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — Production 化视角的补充来源（Stage 7）
- [[Eval_Harness]] — 编排模式的质量评估
- [[Agent_Observability]] — 编排模式的运行时观测
- [[Cost_Optimization]] — Multi-agent 编排的成本控制
- [[Self_Organizing_Teams]] — Agent 运行时动态协商分工的高级编排模式
- [[Multi_Agent_System]] — Production 化注意事项
