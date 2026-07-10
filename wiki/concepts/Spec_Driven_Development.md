---
title: "Spec-driven Development（规范驱动开发）"
type: concept
tags: [agentic AI, 规范驱动, formal spec, DSPy, 结构化开发]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Spec-driven Development（规范驱动开发）

## 定义

Spec-driven Development 是一种 Agent Task 定义范式：**Agent 的任务由 Formal Spec（YAML / JSON Schema / DSPy Signature）定义，而非自由形式的 Prompt**。这使得 Agent 的行为可预测、可验证、可审计。

> Task 由 Formal Spec 定义、不是自由 Prompt。— 进阶 Agentic 概念地图

## 与传统 Prompt 的对比

| 维度 | 自由 Prompt | Spec-driven |
|------|-----------|-------------|
| 定义方式 | 自然语言描述 | 形式化 Schema |
| 可验证性 | 模糊、难量化 | 精确、可自动检查 |
| 可复用性 | 低（每次要重写） | 高（Spec 可共享） |
| Agent 自由度 | 高（易越界） | 低（Spec 约束边界） |

## 动到哪一层

- **Types（Spec = Code）** — Spec 本身是 Types 层的一部分

## 主要实现

- **[[DSPy]]** — Programming-not-Prompting 范式，用 Signature 定义 Module 的输入/输出
- **JSON Schema / Pydantic** — Structured Output 的工业标准
- **Anthropic Tools Schema** — `input_schema` 定义工具接口

## 关联连接

- [[Contract_Driven_Handoffs]] — Spec 是契约的延伸
- [[DSPy]] — Spec-driven 的核心框架实现
- [[Work_Boundary]] — Spec 是工作边界的精确定义
- [[Taste_Invariants]] — Spec 可视为 Invariants 的一种形式
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
