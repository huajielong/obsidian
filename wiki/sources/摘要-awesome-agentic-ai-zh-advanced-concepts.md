---
title: "摘要-awesome-agentic-ai-zh-advanced-concepts"
type: source
tags: [agentic AI, 进阶概念, harness engineering, 工作边界, 概念地图]
sources:
  - https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/stages/07.5-advanced-agentic-concepts.zh-Hans.md
last_updated: 2026-07-10
---

# 摘要：进阶 Agentic 概念地图（Stage 7.5）

## 核心主旨

这份资料是 awesome-agentic-ai-zh 学习路线的 **Stage 7.5**，定位为 Production（Stage 7）之后的 **Frontier 概念地图**。它不是完整教学，而是帮助已能上线 Production Agent 的开发者定位业界前沿概念、理解每个概念解决什么问题、以及该读哪些 paper/blog。

## 来源信息

- **项目**: [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) — Agentic AI 中文系统性学习路线
- **作者**: Wenyu Chiou（TW 工程师，TRAE.ai @ 火山引擎）
- **前置条件**: 完成 Stage 4（Agent 框架）+ 6（Context Engineering）+ 7（Multi-Agent Production）

## 内容结构

资料分为 8 个区块：

### 1. 概念地图主轴：Types → Config → Repo → Service 四层工作边界

用工作边界作为主线，把 Agent 系统拆成 4 个层级：

| 层级 | 自主权 | 示例 |
|------|--------|------|
| **Types** | 只能符合既有契约，不能改 Schema | Codex 接 brief 后只能加 inline gloss |
| **Config** | 可以调 budget/policy，不能改 memory | Context-budget agent 改 max_cost_usd |
| **Repo** | 可以读写 memory/vector store，不能 redesign workflow | 数据操作 |
| **Service** | 可以重组整个 workflow，最高自主权 | 系统架构重组 |

三个公开记录的真实越界案例：
- **Cognition Flappy Bird** — Multi-agent subagent 各自看不到对方 context，风格对不上
- **Anthropic Speculative-leap** — Subagent 擅自加未验证推论
- **Replit Agent 2024** — Production DB 权限给太多，agent 执行破坏性 SQL

### 2. 12 个进阶概念 Skeleton

| # | 概念 | 动到哪一层 | 一句话定义 |
|---|------|-----------|-----------|
| 1 | **Work Boundary** | 跨所有层 | agent 只动 brief 指定的对象、不越界 |
| 2 | **Contract-driven Hand-offs** | Types + Service | 上游承诺 artifacts，下游验证已收到 |
| 3 | **Speculative/Parallel Exploration** | Service | 跑 N 条路径取最佳 |
| 4 | **Agent-as-Judge/Constitutional AI** | Service | 一个 agent 评另一个的输出 |
| 5 | **Plan-Act-Reflect Loop** | Service | Write plan → Execute → Critique → Revise |
| 6 | **Hierarchical Task Decomposition** | Service | Supervisor → Worker → Sub-worker |
| 7 | **Autonomy Gradients** | Config | 不同任务不同自主权（suggest/propose/execute）|
| 8 | **Cost-aware Budget Gates** | Config | 超过预算自动停或升级审核 |
| 9 | **Failure Injection/Chaos Eval** | Service | 故意给 broken input 看 agent 怎么处理 |
| 10 | **Self-organizing Teams** | Service | Agents 动态分工而非预先分配 |
| 11 | **Spec-driven Development** | Types | Task 由 formal spec 定义而非自由 prompt |
| 12 | **Graceful Degradation Paths** | Config | Frontier model 挂了回退到便宜 model |

### 3. 跨概念 Harness Engineering 原则（4 大类别）

整合 Anthropic / OpenAI / Cognition / Hamel Husain 多方来源：

| 类别 | 核心问题 | 原则 |
|------|---------|------|
| **① Context 管理** | 上下文不爆炸 | SoR / Memory Persistence / Progressive Disclosure |
| **② Interface/沟通** | agent 看得懂 codebase | Legibility / ACI / Transparency |
| **③ Quality/验证** | 不能 hallucinate | Taste Invariants / Evaluator-Optimizer / LLM-as-Judge |
| **④ Process 纪律** | scale + iterate 不爆 | Simplicity / Throughput Merge Philosophy |

展开 **OpenAI 5 原则**：Legibility / System of Record / Progressive Disclosure / Taste Invariants / Throughput Changes Merge Philosophy，并做了 Anthropic ↔ OpenAI cross-vendor 对照。

### 4. 其他关键内容

- **Dynamic Workflows（Opus 4.8）** — Agent 自生成 Workflow 脚本的编排机制，16 concurrent / 1000 total per run
- **Coding-agent harness vs 一般 tool-use agent** 的差异
- **Eval Rigor** — Benchmark 分数有一半是 harness 给的，不是 model 给的
- **Model-Harness-Fit 与 Bitter Lesson** — 今天搭的 harness 可能被下一代 model 淘汰
- **人 vs Agent 分工** — 你决定"要做什么"，agent 决定"怎么做"

### 5. Reading Path 与 Self-check

分 Foundation / Workflow patterns / Production-Harness / Frontier research 四层，每层 2-4 篇核心阅读。附自我检查列表。

## 关键见解

- **工作边界是根概念**：12 个概念中有 11 个最终回到"agent 的自主权到底到哪里为止"
- **Harness Engineering 原则跨 vendor 趋同**：Anthropic、OpenAI、Cognition 用不同词汇表达同一组设计约束
- **Eval Rigor 被严重低估**：同一 model 不同 scaffold 分数可以差一倍，benchmark 排名常误导
- **"Fail → Publish → Codify → Fix"** 是整个 Agentic 领域的进化机制

## 关联连接

- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — 此前 Stage 7，Harness 8 核心元件
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — Claude Code 生态 Stage 5
- [[摘要-openai-harness-engineering]] — OpenAI Harness Engineering 官方实验
- [[Work_Boundary]] — 工作边界概念
- [[Harness_Engineering]] — Harness Engineering 核心概念
- [[Claude_Code_Dynamic_Workflows]] — Dynamic Workflows 概念
