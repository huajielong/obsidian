---
title: "Taste Invariants（品味不变量）"
type: concept
tags: [harness engineering, lint, code quality, 架构约束, OpenAI]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Taste Invariants（品味不变量）

## 定义

Taste Invariants 是 OpenAI Harness Engineering 五原则之四，核心思想是将"工程美学"（可维护性、一致性、简洁度）转化为可自动执行的规则，用 Lint 工具强制 Agent 遵守，而不是靠 Promot 建议。

> "We enforce these rules with custom linters and structural tests, plus a small set of 'taste invariants.' ... By enforcing invariants, not micromanaging implementations, we let agents ship fast." — OpenAI

## 两个维度

### (a) Enforcing Architecture — 用物理边界框住 AI

| 实践 | 说明 |
|------|------|
| **单向依赖** | 底层 Types 绝对不能引用高层 Service，AI 偷渡 import 会被挡 |
| **刚性目录结构** | 特定 Code 必须待在特定目录（`models/` / `controllers/` / `schemas/`）|
| **自动化 Linter** | CI 自动拒绝违规 merge，逼 AI 重写 |

### (b) Enforcing Taste — 把工程美学变成规则

| 实践 | 说明 |
|------|------|
| **黄金准则列表** | "偏好 Composition 而非 Inheritance"、"函数短小"、"文件 < 500 行" |
| **代码风格统一** | 强制产出看起来像"同一个高阶工程师写的" |
| **拒绝 AI Slop** | AI 常生成冗余、"看起来正确"但无用的 Code，设定品味基准要求重构简化 |

## 核心精神

**定义边界、不细管实作** — 让 Agent 在划好的格子里自由冲，而不是每行都要人盯。

## 跨 Vendor 对照

| OpenAI | Anthropic 对应 |
|--------|---------------|
| Taste Invariants | Evaluator-optimizer loops + Tool "poka-yoke" |

## 关联连接

- [[Legibility]] — Invariants 确保命名一致性，支撑 Legibility
- [[Harness_Engineering]] — Invariants 是 OpenAI 五原则之四
- [[Eval_Harness]] — 自动评估流水线与 Invariants 配合
- [[Work_Boundary]] — Invariants 是工作边界的工程化实现手段
- [[摘要-openai-harness-engineering]] — OpenAI Harness Engineering 实验
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
