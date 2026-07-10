---
title: "Autonomy Gradient（自主权梯度）"
type: concept
tags: [agentic AI, 安全, 权限控制, 治理, 自主权]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Autonomy Gradient（自主权梯度 / 信任层）

## 定义

Autonomy Gradient 是一种基于风险等级的 Agent 授权机制：不同任务赋予不同自主权，形成 **Suggest → Propose → Execute** 三段梯度。这是对 [[Work_Boundary]] 的具体实现——不是一刀切地授权或限制，而是根据任务危险性动态调整。

## 三段授权模型

| 层级 | 行为 | 适用场景 | 例子 |
|------|------|---------|------|
| **Suggest** | Agent 仅给出建议，等待人确认 | 高影响操作 | 删除生产数据库、修改核心架构 |
| **Propose** | Agent 提出方案+预览，人 approve 后执行 | 中等影响 | 改配置文件、调整部署参数 |
| **Execute** | Agent 直接执行，事后报告 | 低影响常规操作 | 格式化代码、运行常规测试 |

## 核心来源

- **Claude Code 权限系统** — 内建 permission prompt，破坏性操作需人确认
- **Cognition** — "Operator 自律不够，必须有 mechanical gate"
- **Replit Agent 2024 事故** — Production DB 被清空的根本原因就是没有设 autonomy gate

## 实作建议

1. **设好默认梯度**：新操作默认 Suggest（最安全），验证可信后逐步升级
2. **操作分类**：列出每个 Tool 的危险等级，对应不同的授权层级
3. **Gate 必须是 Mechanical** — 不能靠"Agent 自觉"，必须有代码层面的强制执行

## 关联连接

- [[Work_Boundary]] — Autonomy Gradient 是工作边界的细化实现
- [[Cost_Aware_Budget_Gates]] — 预算门控是另一维度的梯度控制
- [[Harness_Engineering]] — 属于 Harness Engineering 的 Config 层
- [[Graceful_Degradation]] — Frontier 模型挂掉时的回退也是一种梯度
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
