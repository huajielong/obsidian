---
title: "Reflexion"
type: concept
tags: [reflexion, self-refine, agent loop, episodic memory, verbal reinforcement learning]
sources: [raw/01-articles/06-memory-rag.zh-Hans.md, raw/09-archive/awesome-agentic-ai-zh-stage-03-tool-use]
last_updated: 2026-07-10
---

# Reflexion（反思机制）

Reflexion 是一种让 Agent 通过反思自身过往成败来持续改进的机制。它的核心在于 **Verbal Reinforcement Learning**——Agent 尝试任务 → 失败 → 反思"为何失败"并保存 → 下次遇到类似任务时将过去的反思检索进 prompt，避免重蹈覆辙。

## Reflexion 完整版 vs Self-Refine

| 版本 | 会话内保留内容 | 跨 Session 保留 | 需要的 Memory 模式 |
|------|-------------|----------------|-------------------|
| **Self-Refine**（Madaan 2023） | 上一轮的 answer + critic feedback | ❌ 不保留 | 无需（Pattern 1 Buffer 即可） |
| **Reflexion 完整版**（Shinn 2023） | 同上 | ✅ 将过去 trial 的反思摘要存入 Episodic Memory | **需要** Pattern 3 Vector Store 或 Pattern 2 Summary |

> **关键区别**：Self-Refine 是单 session 内的 in-context 循环（无外部存储），Reflexion 完整版是跨 trial 的持久 Episodic Memory 存储 + 检索（从过往经验中学习）。

## 为什么需要持久 Memory

Reflexion paper 的核心贡献在于：Agent 跨 trial 累积教训——agent 失败后反思并保存，下次类似任务时将过去的反思检索进 prompt。这需要 **persistent episodic memory**，直接对应 [[Memory_Agent]] 中讨论的三种 Memory 模式。

**典型架构**：
```
Task → Actor（执行）→ Evaluator（评估）→ 反思失败原因 → 
存储到 Episodic Memory Store → 下次类似任务时检索教训 → 效果提升
```

## 论文与实现

**论文**：
- [Reflexion (Shinn et al. 2023)](https://arxiv.org/abs/2303.11366) — 完整版论文，Algorithm 1 详细说明了 memory buffer 的用法
- [Self-Refine (Madaan et al. 2023)](https://arxiv.org/abs/2303.17651) — 对比基线，无 episodic memory 的版本

**参考实现**：
- [noahshinn/reflexion](https://github.com/noahshinn/reflexion) — 论文第一作者的参考实现
- LangChain — LangGraph 版本的 Reflexion cookbook
- mem0 / Letta — 可作为 Reflexion 的 Episodic Store

## 与 Stage 3 的分工

- **理解"反思循环如何工作、单次如何运行"** → Stage 3 Agent Loop 基础反思
- **理解"反思如何跨 session 累积，Agent 如何从过往经验学习"** → 本节 Reflexion 完整版
- **看 Production Agent 内部如何使用反思** → [[Claude_Code]] Harness Internals

## 关联连接

- [[Memory_Agent]] — Reflexion 是 Episodic Memory 的典型应用，依赖持久 Memory Store
- [[Agent_Loop]] — ReAct 循环中 Evaluator 触发反思，Actor 利用反思结果
- [[RAG]] — 可与 RAG 结合：外部知识检索 + 内部经验反思
- [[DSPy]] — Path 3 自动优化框架，与 Reflexion 的 Path 1 思路互补
- [[摘要-awesome-agentic-ai-zh-memory-rag]] — 本概念的来源资料
