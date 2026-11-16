---
title: "摘要-The AI Engineering Skills Map（吴恩达）"
type: source
tags: [来源, 原始文件, AI工程, 技能图谱, 职业发展]
sources:
  - "raw/09-archive/The AI Engineering Skills Map 人工智能工程技能图谱.md"
last_updated: 2026-11-09
---

# The AI Engineering Skills Map（吴恩达）

## 核心摘要

2026-08-15，吴恩达（[[Andrew_Ng]]）发布 **The AI Engineering Skills Map（AI 工程技能图谱）**。该图谱基于 **10,000+ 条招聘信息分析、数十场与 AI 专家/招聘经理/招聘官的结构化访谈、问卷调查以及其他线上数据** 的综合，提炼出当下与近期最重要的四项 AI 工程技能：**构建与部署 AI 应用、软件工程基础、使用编程智能体、塑造构建方案**。吴恩达特别强调 "AI Engineering skills" 比 "AI Engineer" 岗位更宽泛——就像所有开发者都要会用云，但不是人人都叫 Cloud Engineer；全栈、数据、DevOps、ML、AI 工程师都需要这些技能。所有技能之上是**持续学习**的心态，因为 AI 变化太快，最佳实践需要不断更新。DeepLearning.AI 将陆续逐项展开这四项技能，并发布更详细的技能图谱。

## 原文信息

| 项 | 内容 |
|---|---|
| 作者 | Andrew Ng（[[Andrew_Ng]]） |
| 发布时间 | 2026-08-15 |
| 来源 | https://x.com/AndrewYNg/status/2088302050706686198 |
| 原文语言 | 英文（含中文对照） |

## 方法论

- 分析 **10,000+ 条招聘帖**
- 进行 **数十场结构化访谈**：AI 专家、招聘经理、招聘官
- **问卷调查**收集数据
- **综合其他线上数据**

吴恩达把这一过程比作"对海量职位与专家访谈数据做聚类"，以识别不仅当下重要、近期也将重要的技能。

## 四项核心技能

### 1. 构建与部署 AI 应用（Building and deploying AI applications）

AI 应用与非 AI 应用的关键区别是**输出不可预测**：提示 LLM 时不知道会得到什么，训练深度学习模型时不知道它会对新样本做出什么预测；传统软件则更具可预测性。

该技能要求：

- 理解 AI 的**基础积木**：LLM、[[Context_Engineering|上下文工程]]、[[RAG]]、Agentic Workflow、机器学习与深度学习
- 掌握**统计技术**来测量、引导和治理 AI 系统，使其行为更可预测
- 核心是**有纪律的 evals 与 error analysis 循环**（disciplined evals and error analysis loops），见 [[Eval_Harness]]

### 2. 软件工程基础（Software engineering fundamentals）

深入理解软件如何工作，才能更高效地构建。软件工程需要在**成本、可扩展性、可靠性、速度**之间做权衡，**安全与隐私**进一步增加复杂度。

- 理解软件基础原理，才能识别**存在哪些权衡**
- 从而在选择软件栈、设计系统架构、设计数据存储、测试等环节做出更好决策
- 相比缺乏经验的开发者"凭感觉 vibe coding"，理解权衡的人能**用软件工程的精确语言引导编码智能体**，取得更好的结果；而缺乏上下文与判断的 vibe coding 往往让 Agent 做出糟糕的权衡

### 3. 使用编程智能体（Using coding agents）

高效运用 Agentic Coding 已成为每位开发者的核心技能。掌握它意味着：

- **心智模型**：理解 Agent 如何工作、局限在哪、如何绕过
- **介入尺度**：知道何时该干预、何时该放手，构建健壮软件而不浪费时间和 token
- **上下文管理**：管理编码智能体的 context
- **规划 vs 执行**：在两者之间做权衡
- **自主闭环**：提供 verifier 或 eval，让 Agent 自主完成闭环
- **规范**：会写清晰的 spec，也知道何时不必写
- **多智能体编排**：协调多个 Agent 协同工作
- **风险边界**：避免 Agent 误操作生产数据库等事故
- **持续演进**：由于 Agentic Coding 演进极快，要建立持续尝试新工具、更新工作流的例行机制

详见 [[Agentic_Coding]] 与 [[Harness_Engineering]]。

### 4. 塑造构建方案（Shaping the build）

给定清晰规范后，编码智能体的交付能力正在快速提升。因此工程师的工作重心**转向决定规范中应包含什么**：

- 工程师不应再期待"拿到像素级完美的设计，只负责实现"
- 高效的 AI 工程需要**产品感**、理解**业务上下文与客户目标**，参与塑造和推动构建
- AI 也带来更大的 **ownership 与自主权**：识别有趣的问题与机会，并以负责任的方式执行
- 需要懂得如何推动项目：知道何时快速做 MVP 给用户测试，何时放慢节奏做更严谨的开发

详见 [[Spec_Driven_Development]]。

## 底层心态：持续学习

所有技能的核心是**持续学习的思维模式**。AI 持续快速变化，所有人都必须不断学习、更新技能以采用新兴最佳实践。

## 术语辨析

吴恩达使用 "AI Engineering skills" 而非 "AI Engineer" 岗位称谓，因为前者**范围宽得多**：

> 所有开发者今天都应该知道如何与云打交道，但只有较少的人拥有 "Cloud Engineer" 头衔。同样，所有开发者——全栈工程师、数据工程师、DevOps 工程师、机器学习工程师，以及 AI 工程师——都需要 AI 工程技能。

## 关联连接

- [[AI_Engineering_Skills]] — 由本文提炼的概念页（四项核心技能框架）
- [[Andrew_Ng]] — 作者
- [[Agentic_Coding]] — 技能 3「使用编程智能体」的范式页
- [[Eval_Harness]] — 技能 1 的核心方法：纪律化的 evals 与 error analysis
- [[Spec_Driven_Development]] — 技能 4「塑造构建方案」的规范视角
- [[Context_Engineering]] — 技能 1 的基础积木之一
- [[RAG]] — 技能 1 的基础积木之一
- [[Harness_Engineering]] — 技能 3 的工程控制层
- [[AI_SDLC]] — 组织级 AI 研发流程落地
