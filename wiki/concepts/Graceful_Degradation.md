---
title: "Graceful Degradation（优雅降级）"
type: concept
tags: [agentic AI, 容错, fallback, 韧性, 生产部署]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Graceful Degradation（优雅降级路径）

## 定义

Graceful Degradation 是一种系统韧性策略：**当 Frontier Model 不可用或超预算时，自动回退到更便宜的 Model 并降低预期，而不是直接 Crash**。这是 [[Harness_Engineering]] 中韧性与容错的核心实践。

> "Frontier model 挂掉时、回退到便宜 model 并降低预期、而不是直接 crash。"

## 降级阶梯

| 层级 | Model | 成本 | 预期质量 | 触发条件 |
|------|-------|------|---------|---------|
| **L1** | Frontier Model（Claude Opus / GPT-5） | $$$ | 最高质量 | 默认 |
| **L2** | Mid-range Model（Claude Sonnet / GPT-4o） | $$ | 中等质量 | L1 不可用或超预算 |
| **L3** | Small Model（Claude Haiku / GPT-4o-mini） | $ | 基本功能 | L2 不可用 |
| **L4** | Cached Response / Rule-based Fallback | $ | 最简功能 | L3 不可用 |

## 动到哪一层

- **Config（Fallback Policy）** — 属于配置层的回退策略

## 主要实现

- [[Anthropic]] Model Fallback — Claude 系列模型的降级路径
- [[OpenRouter]] Routing — 自动 Model Routing 与 Fallback

## 关联连接

- [[Cost_Aware_Budget_Gates]] — 超过预算后的降级触发
- [[Failure_Injection_Chaos_Eval]] — 故障注入测试的就是降级路径
- [[Autonomy_Gradient]] — 降级时自主权也应相应降低
- [[Harness_Engineering]] — 属于 Harness Engineering 韧性策略
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
