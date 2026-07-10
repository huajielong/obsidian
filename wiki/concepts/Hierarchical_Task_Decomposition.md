---
title: "Hierarchical Task Decomposition（层级任务分解）"
type: concept
tags: [agentic AI, 编排, 任务分解, 多层监督, supervisor]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Hierarchical Task Decomposition（层级任务分解）

## 定义

Hierarchical Task Decomposition 是一种 Multi-Agent 编排模式：通过 **Supervisor → Worker → Sub-worker** 的多层递归结构，将复杂任务逐层分解为可执行的子任务。这是 [[Agent_Orchestration_Patterns]] 中 Supervisor-Worker 模式的深层变体。

## 核心特征

| 特征 | 说明 |
|------|------|
| **至少 2 层 Recursion** | Supervisor → Worker 还不够，需要 Worker → Sub-worker |
| **逐层 Scope 缩减** | 每下一层任务范围更窄、Context 更聚焦 |
| **结果向上汇总** | Sub-worker → Worker → Supervisor 逐层合并 |

## 解决的问题

- **Context 爆炸**：单 Agent 无法处理超长任务
- **责任模糊**：没有清晰的任务边界导致 Agent 越界
- **评审困难**：大型任务难以一次性验证正确性

## 主要实现

- [[AutoGen]] — GroupChat 支持多层对话
- [[LangGraph]] — 图式编排天然支持层级分解
- Claude Code Subagent — Dynamic Workflows 中的 Orchestrator-Workers 模式

## 关联连接

- [[Agent_Orchestration_Patterns]] — 五大编排模式中的 Supervisor-Worker
- [[Contract_Driven_Handoffs]] — 层级间的契约确保信息正确传递
- [[Work_Boundary]] — 每层有自己的工作边界
- [[Claude_Code_Dynamic_Workflows]] — 在 Dynamic Workflows 中自动分解
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
