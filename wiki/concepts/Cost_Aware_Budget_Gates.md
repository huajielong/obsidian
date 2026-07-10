---
title: "Cost-aware Budget Gates（成本感知预算门控）"
type: concept
tags: [agentic AI, 成本控制, 预算, 生产部署, 治理]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Cost-aware Budget Gates（成本感知预算门控）

## 定义

Cost-aware Budget Gates 是一种基于成本的风险控制机制：当 Agent 运行超过预设的 $ 预算时，自动停止或升级到人工审核。它与 Token 上限不同——关注的是**实际金钱成本**而非 Token 数量。

> "超过 $ 预算就自动停或升级审核（不只是 token 上限）" — OpenAI Harness Engineering

## 与传统 Token 上限的区别

| 维度 | Token 上限 | Budget Gate |
|------|-----------|-------------|
| 衡量单位 | Token 数量 | 实际金钱成本（$） |
| 触发条件 | Context 窗口满了 | 预算消耗完了 |
| 响应方式 | 截断或压缩 | 停止、回退或升级审核 |
| 考虑因素 | 模型能力限制 | 业务成本控制 |

## 动到哪一层

- **Config**（Cost Policy）— 属于配置层的成本策略

## 关联连接

- [[Cost_Optimization]] — 成本优化的整体框架
- [[Autonomy_Gradient]] — Budget Gate 是自主权梯度的 Cost 维度
- [[Graceful_Degradation]] — 超过预算后的回退机制
- [[Harness_Engineering]] — 属于 Harness Engineering 的 Cost/Latency 元件
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
