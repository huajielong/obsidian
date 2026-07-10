---
title: "工作边界（Work Boundary）"
type: concept
tags: [agentic AI, 自主权, 安全边界, 治理, 编排]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# 工作边界（Work Boundary / Scope Discipline）

## 定义

工作边界是 Agentic AI 系统中**约束 Agent 自主权范围的核心纪律**。它要求 Agent 只操作 brief 指定的对象，不越界执行未经授权的操作。在四层工作边界模型（Types → Config → Repo → Service）中，每一层定义了一个不同的自主权层级。

## 四层工作边界模型

借用软件架构的 **Types → Config → Repo → Service** 分层，套用到 Agent 系统：

| 层级 | 自主权范围 | Agent 能做什么 | 实际例子 |
|------|-----------|---------------|---------|
| **Types** | 只能符合既有契约 | 不能改 Schema，只能加 inline gloss | Codex 接到 brief 后按指定格式输出 |
| **Config** | 可以调 budget/policy | 不能改 memory，可以调 max_cost_usd | Context-budget agent 调整成本上限 |
| **Repo** | 可以读写 memory/vector store | 不能 redesign workflow | 读写持久化数据 |
| **Service** | 可以重组整个 workflow | 最高自主权 | 系统架构重组、重新编排流程 |

## 真实越界案例

三个有公开记录的 Agent 越界事故：

| 案例 | 问题 | 教训 |
|------|------|------|
| **Cognition Flappy Bird**（2025-06） | Multi-agent subagent 各自看不到对方 context，管道风格与云朵对不上 | Subagent 需要 full parent context |
| **Anthropic Speculative-leap**（2025-06） | Subagent 被指派"研究主题"，却擅自加未验证推论 | 用 evaluator-optimizer loop 过滤 speculative 内容 |
| **Replit Agent 2024** | 用户给 production DB 权限，agent 执行破坏性 SQL | 必须有 mechanical gate（permission check / cost cap / destructive op confirm）|

## Failure-Mode Lifecycle

产业级 Agent 失败模式的演化循环：**发现 Incident → 公开文档化 → Encode 成 Framework Pattern → 自动消除**

| # | Incident | 文档化 | 变成什么 Pattern |
|---|----------|--------|-----------------|
| 1 | Multi-agent context drift | "Sub-agents don't share context" | **Single-thread principle** |
| 2 | Speculative leap | "Speculative hallucination via filling-in" | **Evaluator-optimizer loop** |
| 3 | Production permission drift | "Unbounded autonomy on destructive ops" | **Autonomy gradient** |
| 4 | AutoGPT 卡 loop | "Reflexion-less iteration" | **Plan-Act-Reflect loop** |
| 5 | Skill library corruption | "Untested skill commit" | **Pre-verify before commit** |

## 实作建议

1. **Work boundary 写进 brief** — 明确写"只能动 X，绝对不要动 Y"
2. **Enforce 在 acceptance gate** — 用 preset YAML 验证输出范围
3. **破坏性操作加 explicit gate** — 参考 [[Autonomy_Gradient]] 的 suggest/propose/execute 三段授权

## 关联连接

- [[Autonomy_Gradient]] — 基于自主权梯度的工作边界细化实现
- [[Harness_Engineering]] — Harness Engineering 包含边界控制机制
- [[Contract_Driven_Handoffs]] — 上下游 Agent 间的契约确保边界不被跨越
- [[Agent_As_Judge]] — 独立评审 Agent 验证输出是否在边界内
- [[Hierarchical_Task_Decomposition]] — 多层 Supervisor 天然形成边界控制
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
