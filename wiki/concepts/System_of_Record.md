---
title: "System of Record（知识权威来源）"
type: concept
tags: [harness engineering, 知识管理, SoR, context management, OpenAI]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# System of Record（知识权威来源）

## 定义

System of Record（SoR）是 OpenAI Harness Engineering 五原则之二，核心思想是**所有真实知识住外部 docs、不住 prompt，Agent 从 docs 动态拉取**。解决 LLM 容易忘事、容易脑补、不同 Agent 读到的版本对不上的问题。

> "The repository's knowledge base lives in a structured docs/ directory treated as the system of record." — OpenAI

## 核心实践

### (a) 知识住 docs、不住 prompt

| 实践 | 说明 |
|------|------|
| **100 行 Entry Map** | AGENTS.md / CLAUDE.md 只放"地图"（指向 `docs/` 各区的索引），不放实际内容 |
| **`docs/` 结构化** | 实际内容住 `docs/api/`、`docs/architecture/`、`docs/runbook/` |
| **Prompt 绝不重复 docs 内容** | 避免"prompt 讲一套、docs 讲另一套"的版本不一致 |

### (b) 跨 Session / 跨 Agent 持久化

- **共享记忆**：`.coord/memory.yml` — Subagent 跟 Supervisor 读同一份
- **Decisions Log**：重要决策写进 docs，新 Session 从读档开始
- **Versioned**：用 Git 管 docs，可追溯知识变更历史

## 核心精神

**唯一权威、单向同步** — Agent 从 SoR 拉、不从 Prompt 拉；SoR 改了，所有 Agent 下次跑都读新版本。

## 跨 Vendor 对照

| OpenAI | Anthropic 对应 |
|--------|---------------|
| System of Record | CLAUDE.md hierarchy + Memory persistence |

## 关联连接

- [[Legibility]] — SoR 需要 Legibility 确保 Agent 能读懂
- [[Progressive_Disclosure]] — SoR 提供目的地，PD 是导航机制，两者配对运作
- [[Harness_Engineering]] — SoR 是 OpenAI 五原则之二
- [[Claude_Code_Memory_System]] — Claude Code 的三层记忆机制
- [[AGENT_MD]] — AI Agent 行为规范入口文件
- [[摘要-openai-harness-engineering]] — OpenAI Harness Engineering 实验
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
