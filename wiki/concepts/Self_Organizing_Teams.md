---
title: "Self-organizing Teams（自组织团队）"
type: concept
tags: [agentic AI, 多Agent, 动态分工, 编排, 涌现]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Self-organizing Teams（自组织团队）

## 定义

Self-organizing Teams 是一种高级 Multi-Agent 编排模式：**Agents 不是预先分配固定 Role，而是根据当前任务动态协商分工**。这是对 [[Agent_Orchestration_Patterns]] 中预设编排的延伸——角色不是设计师定的，而是运行时涌现的。

## 与预设编排的对比

| 维度 | 预设编排（Static） | 自组织（Self-organizing） |
|------|-------------------|------------------------|
| 角色分配 | 设计时写死 | 运行时动态协商 |
| 灵活性 | 低（流程固定） | 高（可适应任务变化） |
| 可预测性 | 高 | 低 |
| 适用场景 | 流程明确的常规任务 | 开放式、不确定的探索任务 |

## 核心来源

- **CAMEL（Li 2023）** — Role-Playing 框架，Agents 通过对话协商分工
- **AutoGen GroupChat** — 通过对话路由动态决定谁来发言
- Anhtropic Multi-Agent Research — Subagents 根据任务特化分工

## 关联连接

- [[Agent_Orchestration_Patterns]] — 自组织是动态编排的极端形式
- [[Hierarchical_Task_Decomposition]] — 层级分解与自组织是两种互补策略
- [[Contract_Driven_Handoffs]] — 即使动态分工，契约仍然需要
- [[Work_Boundary]] — 自组织更需要明确的工作边界
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
