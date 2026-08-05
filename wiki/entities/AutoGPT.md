---
title: "AutoGPT"
type: entity
tags: [agent, 开源, 自主agent, 2023, LLM应用]
sources:
  - wiki/sources/摘要-hung-yi-lee-ai-agent-原理.md
last_updated: 2026-08-04
---

## 定义

AutoGPT 是 2023 年春季爆红的开源自主 AI Agent 项目，以 GPT-4 等 LLM 为驱动，将用户目标自动分解为一系列子任务并循环执行（规划 → 执行 → 反思）。它是 2023 年第一波 AI Agent 热潮的标志性代表。

## 关键信息

- **兴起**：ChatGPT 于 2022 年底爆红后，2023 年春出现第一波 AI Agent 热潮，AutoGPT 是其中最著名的项目。
- **运作方式**：给 LLM 一个目标，让它自主拆解步骤、调用工具/写代码、检查结果并继续，直到达成目标。
- **热潮消退**：初期被大量"网红"宣传，实际试下去发现能力远没有宣传的强，热潮随之消退——这是对 LLM 驱动 Agent 能力边界的早期祛魅。

## 关联连接

- [[Agent_Loop]] — AutoGPT 是"自主循环执行"的典型实现
- [[Agent_First_Engineering]] — Agent 优先工程方法论的开端
- [[Agent_Memory_Architecture]] — 自主长任务依赖记忆架构
- [[摘要-hung-yi-lee-ai-agent-原理]] — 本实体的来源
