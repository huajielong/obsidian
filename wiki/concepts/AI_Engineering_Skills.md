---
title: "AI Engineering Skills（AI 工程技能图谱）"
type: concept
tags: [AI工程, 技能图谱, 职业发展, 工程能力]
sources:
  - "raw/09-archive/The AI Engineering Skills Map 人工智能工程技能图谱.md"
last_updated: 2026-11-09
---

# AI Engineering Skills（AI 工程技能图谱）

## 定义

**AI Engineering Skills Map** 是 [[Andrew_Ng]] 与团队于 2026-08-15 发布的 AI 工程技能框架。它基于 **10,000+ 条招聘信息、数十场结构化访谈（AI 专家/招聘经理/招聘官）、问卷调查与线上数据** 的综合分析，提炼出当前与近期最重要的四项 AI 工程技能：

| # | 技能 | 一句话概括 |
|---|------|-----------|
| 1 | 构建与部署 AI 应用 | 掌握 AI 积木，并用统计方法让输出不可预测的系统变得可测量、可引导、可治理 |
| 2 | 软件工程基础 | 理解成本/扩展性/可靠性/速度等权衡，才能做出好的架构、选型与 Agent 引导 |
| 3 | 使用编程智能体 | 理解 Agent 的心智模型与局限，知道何时介入、何时放手 |
| 4 | 塑造构建方案 | 从"实现设计"转向"定义规范"，用产品感与业务上下文决定做什么 |

所有技能之上是**持续学习**的心态。该框架的用途是双向的：帮助开发者**优先学什么**，也帮助雇主**招聘什么样的开发者**。

## 四项技能详解

### 1. 构建与部署 AI 应用

AI 应用与传统软件的分水岭是**输出不可预测**。因此这项技能不是"会用 API"，而是：

- 掌握 AI 基础积木：LLM、[[Context_Engineering|上下文工程]]、[[RAG]]、Agentic Workflow、机器学习/深度学习
- 用**统计技术**测量、引导、治理 AI 系统
- 核心动作是**有纪律的 evals 与 error analysis 循环**，见 [[Eval_Harness]]

### 2. 软件工程基础

软件工程本质是**权衡**：成本、可扩展性、可靠性、速度，外加安全与隐私。理解基础原理的价值在于：

- 能识别"存在哪些权衡"，从而在技术栈、系统架构、数据存储、测试策略上做出更好决策
- 能用**软件工程的精确语言**引导编码智能体；而缺乏判断的 vibe coding 会让 Agent 替你做出糟糕的权衡

### 3. 使用编程智能体

见 [[Agentic_Coding]]。该技能包含九个要素：

1. **心智模型** — 理解 Agent 如何工作、局限在哪、如何绕过
2. **介入尺度** — 知道何时干预、何时放手，不浪费时间和 token
3. **上下文管理** — 管理 Agent 的 context
4. **规划 vs 执行** — 在两者间做权衡
5. **自主闭环** — 提供 verifier / eval 让 Agent 自主完成循环
6. **规范** — 会写清晰 spec，也知道何时不必写
7. **多智能体编排** — 协调多个 Agent 协同工作
8. **风险边界** — 避免 Agent 误操作生产数据库等事故
9. **持续演进** — 建立例行机制持续尝试新工具、更新工作流

### 4. 塑造构建方案

当规范清晰时，编码智能体的交付能力已足够强，工程师的价值重心因此上移：

- 决定**规范里应该写什么**，而不是只负责实现像素级设计
- 需要**产品感**、业务上下文与客户目标的理解
- 承担更大的 **ownership 与 agency**，推动项目前进（何时做 MVP、何时慢工出细活）
- 与 [[Spec_Driven_Development]] 的"用 Spec 定义任务"形成上下游关系

## 术语辨析：技能 ≠ 岗位

吴恩达强调 "AI Engineering skills" 比 "AI Engineer" 岗位宽泛：

> 所有开发者今天都应该知道如何与云打交道，但只有较少的人拥有 "Cloud Engineer" 头衔。同样，全栈工程师、数据工程师、DevOps 工程师、机器学习工程师，以及 AI 工程师，都需要 AI 工程技能。

## 与知识库三层工程模型的关系

> 以下对应关系为本知识库的解读，非原文表述。

| 图谱技能 | 对应知识库层 |
|---|---|
| 1 构建与部署 AI 应用 | [[Context_Engineering]]（RAG/上下文/Memory 等 AI 积木）+ [[Eval_Harness]]（评测纪律） |
| 2 软件工程基础 | 三层共同的底座：权衡判断决定了 Prompt/Context/Harness 的设计质量 |
| 3 使用编程智能体 | [[Harness_Engineering]]（Loop/Retry/Sandbox/Observability/编排） |
| 4 塑造构建方案 | [[AI_SDLC]] 的目标层：intent/spec 决定整个研发闭环的方向 |

## 关联连接

- [[摘要-ai-engineering-skills-map]] — 来源摘要
- [[Andrew_Ng]] — 框架提出者
- [[Agentic_Coding]] — 技能 3 的范式定义与工具生态
- [[Eval_Harness]] — 技能 1 的核心方法论
- [[Context_Engineering]] — 技能 1 的基础积木
- [[RAG]] — 技能 1 的基础积木
- [[Spec_Driven_Development]] — 技能 4 的规范实践
- [[Harness_Engineering]] — 技能 3 的工程控制层
- [[AI_SDLC]] — 组织级 AI 研发流程落地
- [[AI_Mastery_Compass]] — 个人能力进阶路线视角
- [[AI_Project_Workflow]] — 传统 ML 项目工作流，与技能 1 的部署视角互补
