---
title: "LangGraph"
type: entity
tags: [agent框架, multi-agent, orchestration, LangChain, production]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-10
---

# LangGraph

LangGraph 是 LangChain 团队推出的图式 Agent 编排框架，专注于 Production 级 Multi-agent 系统的构建。支持图式 orchestration + checkpointing + time-travel debug，企业广泛采用。**本路线图 Stage 4 推荐 #1（Production 级首选）。**

## 核心特性

- **图式编排**：以 state graph 为核心，节点（Node）是 Agent 或工具、边（Edge）是条件路由
- **Checkpointing**：状态持久化，支持 rollback / replay
- **Time-travel debug**：回溯任意历史状态
- **Multi-agent 架构**：支持 Supervisor / Swarm / Hierarchical 三种架构（[官方文档](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)）
- **Tool Node**：直接把 retriever 包成 tool node
- 与 LangSmith 搭配做 observability

## 覆盖的编排模式

- [[Agent_Orchestration_Patterns#2 Sequential（Planner → Executor）|Sequential（Planner → Executor）]]
- [[Agent_Orchestration_Patterns#3 Parallel（并行加速）|Parallel（并行加速）]]
- [[Agent_Orchestration_Patterns#4 Supervisor-Worker（Hub-Spoke）|Supervisor-Worker]]
- 条件路由（Conditional Edge）可同时视为 Workflow routing 和 Agent 动态决策

## 适用场景

- Production 级 Multi-agent 需要稽核轨迹
- 需要 checkpoint / rollback / replay
- 长 Workflow 需要状态持久化
- 复杂条件分支逻辑

## 不适合场景

- 快速雏形（学习曲线较高）
- 简单线性任务（overkill）

## 基本信息

- **Stars**: 34k+
- **License**: MIT
- **语言**: Python + TypeScript
- **GitHub**: https://github.com/langchain-ai/langgraph

## 关联连接

- [[Agent_Orchestration_Patterns]] — LangGraph 覆盖所有 5 种编排模式
- [[Multi_Agent_System]] — LangGraph 是 Multi-agent 的主要 Framework 实现
- [[CrewAI]] — 同属 Agent Framework，LangGraph 更适合 Production、CrewAI 更适合雏形
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本实体的核心来源
- [[Chain_of_Thought]] — LangGraph 可编排 CoT 推理流程
- [[Harness_Engineering]] — LangGraph 的 checkpointing 是 Harness 的一部分
