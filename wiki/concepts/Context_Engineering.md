---
title: "Context_Engineering"
type: concept
tags: [上下文工程, RAG, memory, agent loop, context window, chunking]
sources: [raw/01-articles/awesome-agentic-ai-zh-stage-02-prompt-engineering.md, raw/01-articles/06-memory-rag.zh-Hans.md]
last_updated: 2026-07-10
---

# Context Engineering（上下文工程）

Context Engineering（上下文工程）是 **LLM-powered system 三层工程堆栈的第二层**，工程对象是 **每次 LLM 调用时上下文窗口中填充的信息**——包括 RAG 检索结果、对话历史、工具定义（Tool Definitions）、长期记忆等。

> Karpathy 2025-06 原推文：Context Engineering 是"把 **刚好对下一步有用的信息** 填进 context window 的精细艺术。"

## 三层工程堆栈

由 [[Andrej_Karpathy]]（2025-06）与 Simon Willison / Addy Osmani 等人共同推进的分类框架：

| 层次 | 工程对象 | 典型技术 | 在哪学习 |
|------|---------|---------|---------|
| **1. [[Prompt_Engineering]]** | 送进 LLM 的字符串本身 | System prompt、Few-shot、CoT、格式控制 | Stage 2 |
| **2. Context Engineering** | 上下文窗口的信息组装 | RAG、Memory、Chunking、Tool defs、对话历史拼接 | **Stage 6（本 stage）** |
| **3. [[Harness_Engineering]]** | 模型外围的执行与控制 | Agent loop、Retry、Sandbox、Observability | Stage 7 |

## 四个 Sub-problem（Lance Martin 2025 框架）

Context Engineering 拆解为四个正交的子问题：

| Sub-problem | 解决什么 | 具体例子 | 对应技术 |
|------------|---------|---------|---------|
| **Select** | 要把 **哪些** 外部信息捞进窗口 | 从 Yelp DB 捞 3 家评分高的 → 塞进 prompt | [[RAG]]（基础 + 进阶） |
| **Write** | 要把 **哪些** 互动/教训写进长期记忆 | 用户"吃纯素" → 写进 memory，下次检索避免推肉食 | [[Memory_Agent]] |
| **Compress** | 对话太长怎么压 | 50 轮超 200k token → 摘要前 40 轮，保留后 10 轮原文 | [[Memory_Agent]] Pattern 2 |
| **Isolate** | 多 agent 各自窗口怎么分 | Supervisor 看全局，Worker 只看自己那段 | [[Multi_Agent_System]] Stage 7 |

## 核心区别

三层的区分不在于"调用次数"，而在于工程对象不同：

- 一次调用但做了 RAG 检索 → 在做 Context Engineering（重点是组 context）
- 五十次调用但未做检索 → 仍只是在做 Prompt Engineering
- 加了重试/沙盒/监控 → 在做 Harness Engineering

## 关键能力

Agent 需要两种 Context 能力：

1. **Retrieval**（通过 [[RAG]] 实现）— 从外部知识库找出和当前任务相关的资料
2. **Memory**（通过 [[Memory_Agent]] 实现）— 保留跨对话、跨 session、跨任务的状态、偏好与经验

两者互补而非替代：RAG 处理外部知识，Memory 记录自身与用户的交互历史。Production Agent 通常**两者都需要**。

## 相关概念体系

| 技术 | 解决哪个 Sub-problem | 核心挑战 |
|------|-------------------|---------|
| [[RAG]] | Select | Chunk 粒度、Embedding 选型、top-k 调优 |
| [[Memory_Agent]] | Write + Compress | 3 种 Pattern 选型、CoALA 四层覆盖 |
| [[Chunking]] | Select 的前置步骤 | 分块策略选择（固定/递归/语义） |
| [[Reflexion]] | Write（Episodic Memory） | 持久化反思、跨 trial 累积教训 |
| [[DSPy]] | 自动优化 Select + Write | 编译器代替手动调 Prompt/Retriever |

## 关联连接

- [[Prompt_Engineering]] — 三层堆栈的底层基础
- [[Harness_Engineering]] — 三层堆栈的最外层
- [[RAG]] — Context Engineering 的核心 Sub-problem（Select）
- [[Memory_Agent]] — Context Engineering 的核心 Sub-problem（Write + Compress）
- [[Chunking]] — 影响 Context 组装质量的技术细节
- [[Reflexion]] — Episodic Memory 的典型应用
- [[DSPy]] — 自动优化 Context Engineering 各环节的工具
- [[Chain_of_Thought]] — 推理链的上下文组织
- [[Context_Window]] — Context Engineering 的物理约束边界
- [[Agent_Loop]] — Context Engineering 的执行载体
- [[Multi_Agent_System]] — Stage 7 涉及 Isolate Sub-problem
- [[Andrej_Karpathy]] — Context Engineering 概念的共同推动者
- [[Claude_Code_Memory_System]] — Claude Code 中的 Memory 实现
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 来源资料（Stage 2）
- [[摘要-awesome-agentic-ai-zh-memory-rag]] — 来源资料（Stage 6）
