---
title: "摘要-awesome-agentic-ai-zh-agent-frameworks"
type: source
tags: [agent框架, 学习路线, multi-agent, LangGraph, CrewAI, AutoGen, orchestration, LLM]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-10
---

## 核心摘要

该资料是 "awesome-agentic-ai-zh" Agentic AI 系统学习路线图的 **Stage 4——Agent 框架（Agent Frameworks）**，提供从单 Agent 到多 Agent 框架的系统化教程。核心涵盖：Workflow vs Agent 和 Single vs Multi 的 2x2 正交分类矩阵、5 种经典 Multi-agent 编排模式（Routing/Handoff、Sequential、Parallel、Supervisor-Worker、Debate/Society），以及 16 个主流 Agent 框架的分级对比与选型指南。同时深入讨论"何时不该用 Multi-agent"的决策框架（引用了 Anthropic Building Effective Agents 和 Cognition 的 Don't Build Multi-Agents），以及 Framework 提供的三种进阶 Tool Pattern（Dynamic Selection、Composition/Chaining、Augmented Retrieval）。

## 关键提炼

- **核心分类矩阵**：Workflow（固定 code path）vs Agent（LLM 动态决策）和 Single LLM vs Multi LLM 是两个正交维度，Multi-agent framework 主要服务于"Multi LLM + Agent"象限
- **90% 场景不该用 Multi-agent**：Anthropic 和 Cognition 两家前沿实验室明确表示，多数用例 simple workflow + single agent 就足够；硬上 Multi-agent 会付 3-10x Token 成本、Debug 痛苦、Context Fragmentation
- **四个需要 Multi-agent 的信号**：任务天然可分解、Token 爆炸（Single agent prompt 装不下）、角色冲突（同一 LLM 既当 writer 又当 critic）、并行加速需求
- **五大编排模式**：Routing/Handoff（1:1 交接）、Sequential/Planner-Executor（多步骤）、Parallel（并行聚合）、Supervisor-Worker（Hub-Spoke）、Debate/Society（多视角收敛）
- **Framework 的本质**：把 orchestration boilerplate（角色定义、Handoff、State 管理、Retry、Checkpoint、HITL pause）抽象出来，让开发者只写角色定义和任务描述
- **进阶 Tool Pattern**：Dynamic tool selection（>30 个工具时 embedding-based 路由）、Tool composition/chaining（A→B 无 LLM 中间叙事）、Tool-augmented retrieval（RAG 搜索再推理）
- **两条 Multi-agent 路线**：Framework 路线（跨 LLM provider、写 Python orchestration code）vs Claude Code Subagent 路线（只在 Claude Code runtime 内、写 markdown 不写 code、天生 context 隔离）
- **框架选型**：Production 用 LangGraph（有 checkpointing + time-travel debug），快速雏形用 CrewAI（~20 行写完），CodeAct 路线用 Smolagents，Type-safe 用 Pydantic AI

## 关联连接

- [[Agent_Loop]] — Stage 3 的 ReAct 循环是单 Agent 核心机制，本 Stage 扩展到多 Agent 协作
- [[Multi_Agent_System]] — Multi-agent 的核心概念与架构决策，何时该用、何时不该用
- [[Agent_Orchestration_Patterns]] — 本资料介绍的 5 种经典 Multi-agent 编排模式详解
- [[Chain_of_Thought]] — CoT 是单 Agent 内部推理范式（Stage 3），与本 Stage 的多 Agent 编排是正交的两个层
- [[摘要-awesome-agentic-ai-zh-tool-use]] — 本路线图 Stage 3，从零构建 ReAct Agent 的前置基础
- [[Anthropic]] — 本资料引用的 Building Effective Agents 出自 Anthropic
- [[OpenAI]] — OpenAI Agents SDK 和 Swarm 是 Routing/Handoff 模式的代表实现
- [[Claude_Code]] — 另一条 Multi-agent 路线（Subagent 机制）的宿主环境
- [[Harness_Engineering]] — Framework 提供的高级 Tool Pattern 是 Harness Engineering 的组成部分
- [[摘要-awesome-agentic-ai-zh-foundations]] — 本路线图 Stage 0
- [[摘要-awesome-agentic-ai-zh-llm-basics]] — 本路线图 Stage 1
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 本路线图 Stage 2
