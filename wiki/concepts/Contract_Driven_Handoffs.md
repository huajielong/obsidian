---
title: "契约驱动的 Agent 交接（Contract-driven Hand-offs）"
type: concept
tags: [agentic AI, 编排, 多Agent, 契约, 验证]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# 契约驱动的 Agent 交接（Contract-driven Hand-offs）

## 定义

Contract-driven Hand-offs 是一种 Agent 间协作模式：上游 Agent 承诺产出特定格式的 Artifacts，下游 Agent 必须验证自己真的收到了预期内容。其核心是 **Types 层的契约 + Service 层的验证**，广泛应用于 Anthropic 的 Routing pattern 和 LangGraph 的 State Schema。

> 类似软件工程中的 Interface Contract——上游承诺输出格式，下游依赖该格式，中间用 Schema 验证。

## 动到哪一层

| 层级 | 角色 |
|------|------|
| **Types** | 契约定义：Artifact 的 Schema / 接口格式 |
| **Service** | 验证执行：下游检查是否真的收到预期内容 |

## 关键实践

- **Structured Output Schema** — 用 JSON Schema / Pydantic 定义契约
- **接受度 Gate** — 下游拿到后验证 Schema，不符则触发 Retry 或 Escalate
- **Evaluator-Optimizer Loop** — 上游产出 → 下游验证 → 不符则修正 → 重新提交

## 关联连接

- [[Work_Boundary]] — 契约是工作边界的工程化定义
- [[Agent_Orchestration_Patterns]] — Handoff 是五大编排模式之一
- [[Spec_Driven_Development]] — 延伸：整个 Task 都由 Formal Spec 定义
- [[Hierarchical_Task_Decomposition]] — 多层交接需要更严格的契约
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
