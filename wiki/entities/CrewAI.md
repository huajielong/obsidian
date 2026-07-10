---
title: "CrewAI"
type: entity
tags: [agent框架, multi-agent, orchestration, 快速雏形]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-10
---

# CrewAI

CrewAI 是角色驱动的 Multi-agent 框架，以极低的学习曲线实现 "researcher → writer → critic" 流水线。**本路线图 Stage 4 推荐 #2（快速雏形首选）。** ~20 行即可完成一个 Crew 的定义。

## 核心特性

- **角色驱动**：定义 Agent 角色（role）、目标（goal）、背景故事（backstory）
- **Task 委托**：Agent 之间自动传递任务结果（轻量 memory）
- **Sequential tasks**：线性流水线
- **Parallel tasks**：并行加速
- **学习曲线最低**：框架抽象程度高、代码量少

## 覆盖的编排模式

- [[Agent_Orchestration_Patterns#2 Sequential（Planner → Executor）|Sequential（Planner → Executor）]] — 最擅长的模式
- [[Agent_Orchestration_Patterns#3 Parallel（并行加速）|Parallel（并行加速）]]

## 适用场景

- 快速雏形和原型验证
- "researcher → writer → critic" 流水线
- 2-3 个 Agent 角色分配的任务
- 学习 Multi-agent 概念入门

## 不适合场景

- 长 Workflow（无 checkpointing）
- Production 级系统需要稽核轨迹（应选 [[LangGraph]]）

## 基本信息

- **Stars**: 50k+
- **License**: MIT
- **GitHub**: https://github.com/crewAIInc/crewAI

## 关联连接

- [[LangGraph]] — Production 级替代方案（有 checkpointing）
- [[Agent_Orchestration_Patterns]] — CrewAI 主要使用 Sequential 和 Parallel 模式
- [[Multi_Agent_System]] — CrewAI 是 Multi-agent 的轻量实现
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本实体的核心来源
