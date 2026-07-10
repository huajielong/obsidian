---
title: "Legibility（Agent 可读性）"
type: concept
tags: [harness engineering, ACI, codebase design, agent-friendly, OpenAI]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Legibility（Agent 可读性）

## 定义

Legibility 是 OpenAI Harness Engineering 五原则之首，核心思想是**为 Agent 优化 Codebase 和工具的可读性**，而非为人类优化。人类读代码有 IDE 高亮、跳转、目录树等视觉辅助；Agent 只看纯文字 + 工具回传值，因此需要特别的优化。

> "Because the repository is entirely agent-generated, it's optimized first for Codex's legibility." — OpenAI

## 两个维度

### (a) Codebase 对 Agent 友善

| 实践 | 说明 | 为什么 |
|------|------|--------|
| **一致 Schema 命名** | `get_user_by_id` 永远用这个格式，不混用 | Agent 靠 pattern matching 推论，规律不一致会推错 |
| **文件大小限制** | 文件 < 500 行，Agent 一次能完整读进 Context | >500 行 Agent 会跳读、漏看关键逻辑 |
| **`docs/` 阶层结构** | `docs/api/` / `docs/architecture/` / `docs/runbook/` 分区清晰 | Agent 才知道去哪找特定信息 |

### (b) Tool / API 对 Agent 友善（ACI）

Agent-Computer Interface（ACI）的设计目标：

- **清楚的 Tool Description** — 每个 Tool 一行讲"干什么"，不只写 function signature
- **Poka-yoke 工具设计** — 把易出错的设计拿掉（如强制 absolute path、强制 ISO 日期）
- **Schema 标注** — 每个字段有 type + 简述 + 范例值

## 跨 Vendor 对照

| OpenAI | Anthropic 对应 |
|--------|---------------|
| Legibility | ACI（Agent-Computer Interface）+ Tool Documentation |

## 关联连接

- [[Harness_Engineering]] — Legibility 是 OpenAI 五原则之首
- [[System_of_Record]] — SoR 提供知识目的地，Legibility 确保 Agent 能读到
- [[Progressive_Disclosure]] — 渐进式披露 + Legibility 让 Agent 高效导航
- [[Taste_Invariants]] — Invariants 确保命名一致性，支撑 Legibility
- [[摘要-openai-harness-engineering]] — OpenAI Harness Engineering 实验
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
