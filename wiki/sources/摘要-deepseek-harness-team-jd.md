---
title: "DeepSeek Harness 团队职位描述"
type: source
tags: [DeepSeek, Harness, 职位, 招聘, Agent, Agent_Harness]
sources: []
last_updated: 2026-07-15
---

# DeepSeek Harness 团队职位描述

> **来源**：DeepSeek 官方招聘信息（2026 年），由 Claude 对话获取并整理。
>
> **核心公式**：**Model + Harness = Agent**

---

## 团队使命

DeepSeek 正在以研究、工程、产品相结合的方式，把 DeepSeek 的模型能力转化为前沿的科研突破与领先的 Agent 产品。Harness 团队与研究员、工程师、产品经理紧密协作，探索 Harness 领域的研究、工程与产品前沿，定义 DeepSeek 对 Harness 的理解。

---

## 四个招聘方向

| 方向 | 角色定位 | 核心能力 |
|------|---------|---------|
| **Agent Harness 研究** | 探索 Agent Harness 研究方向的前沿 | 科研能力、实验迭代、Benchmark 设计、0→1 推动 |
| **Agent Harness 研发/工程** | 解决下一代 Agent Harness 的工程难题 | 技术架构、快速迭代、AI 辅助开发、开发者体验 |
| **Agent Harness 产品** | 探索和定义下一代 Agent 产品形态 | 产品路线图、UX/UI、数据驱动决策、社区运营 |
| **Agent Harness 项目经理**（实习） | 协助推动项目高效运转 | 沟通协调、进度跟踪、文档整理、执行力 |

---

## 技术知识要求（全方向共同）

### 基础机制层

| 知识领域 | 说明 | 对应 wiki 概念 |
|---------|------|---------------|
| **LLM API** | 模型调用接口、参数调优、Streaming、Function Calling | [[OpenAI_Compatible_API]] |
| **KV Cache** | 推理优化、上下文窗口管理、缓存策略 | — |
| **Agent Loop** | 思考-行动-观察循环（ReAct、Plan-Execute 等模式） | [[Agent_Loop]] |
| **Tool Use** | 工具定义、调用、结果回注、权限控制 | [[Tool_Calling]] |
| **Reasoning** | 思维链（CoT）、树状思维、反思机制 | [[Chain_of_Thought]] |
| **Planning** | 任务分解、子目标规划、动态重规划 | — |
| **Skills** | 可复用能力模块、技能的定义与加载 | [[Claude_Code_Skills]]、[[Skill_Factory]] |
| **MCP** | Model Context Protocol，模型-工具-数据的标准化协议 | [[MCP]] |
| **Memory** | 短期记忆（窗口内）、长期记忆（持久化）、结构化记忆 | [[Memory_Agent]] |
| **Subagent** | 子代理的生成、委派、监督、通信 | [[Claude_Code_Subagent]] |
| **Multi-Agent** | 多智能体协作、角色分工、共识机制、通信协议 | [[Multi_Agent_System]] |

### 三层工程模型

| 层级 | 知识要求 | 对应 wiki 概念 |
|------|---------|---------------|
| **Prompt Engineering** | 提示工程、指令优化、上下文注入 | [[Prompt_Engineering]] |
| **Context Engineering** | 上下文管理、RAG、窗口优化、KV Cache | [[Context_Engineering]] |
| **Harness Engineering** | 系统外围控制层（Loop/Retry/Sandbox/Observability） | [[Harness_Engineering]] |

### 进阶机制

| 知识领域 | 说明 |
|---------|------|
| **自进化 Agent** | Agent 从历史经验中自我改进、自动调优 |
| **超长程任务** | 数小时-数天的持续任务、状态持久化、断点续传 |
| **Sandbox / 沙箱执行** | 代码安全执行、容器化隔离、资源限制 |
| **Observability** | Agent 行为追踪、日志、监控、调试 |

---

## 各方向特色技能

### 研究方向

- **Benchmark 设计**：Agent 评测基准、任务设计、自动化评估
- **数据标注策略**：标注规范、质量控制、人机协作标注
- **实验设计**：A/B 测试、消融实验、统计显著性
- **真实世界反馈循环**：从用户行为数据到模型改进的闭环
- **0→1 研究能力**：快速将想法转化为可运行的原型

### 研发/工程方向

- **技术架构设计**：高可用、可扩展的 Harness 产品架构
- **一人公司（OPC）实践**：全栈能力、独立交付、最小可行产品思维
- **开发者体验（DX）**：API 设计、文档、SDK、开发者工具
- **用户社群维护**：理解用户反馈，维护产品社群

### 产品方向

- **UI/UX 设计**：原型设计、交互设计、设计系统
- **Vibe Coding**：用 AI 辅助表达产品意图
- **用户研究方法**：问卷设计、用户访谈、行为分析
- **数据驱动决策**：A/B 测试、灰度发布、指标定义、统计分析
- **开源社区运营**：社区沟通、Issue 管理、贡献者生态

### 项目经理方向（实习）

- **进度跟踪与风险管理**：识别延期风险、及时同步
- **会议与文档**：组织会议、撰写纪要、事项提醒
- **数据整理**：用户反馈整理、竞品资料收集
- **执行力**：对承诺的事情有交付到底的自觉

---

## 关键洞察

### 1. AI 辅助开发成为基础技能

JD 中每个技术方向都明确要求：

> **"熟练使用 AI Agent 工具进行软件开发。能够在 AI 辅助下，在没有直接经验的领域进行有质量保证的编程工作。"**

这意味着 AI 辅助开发已从"加分项"变为"基础能力"，不再是与传统编程并列的技能，而是**编程本身的新的实现方式**。

### 2. "高强度用户"门槛

JD 要求求职者**把 Agent 产品融入日常工作和生活**，包括：Claude Code、Cowork、Codex、Cursor、OpenCode、GitHub Copilot、Manus、OpenClaw、Hermes 等。这反映了 DeepSeek 对"模型行为品味"的重视——只有深度使用才能建立对 Agent 行为的直觉判断。

### 3. 三层工程模型作为面试基准

JD 在四个方向中都明确列出对 Prompt Engineering、Context Engineering、Harness Engineering 三层模型的理解要求，说明这三层模型已成为行业通用的能力评估标准。

### 4. 角色光谱（Research → Engineer → Product → PM）

四个方向构成了从**研究深度**到**执行宽度**的连续光谱：
- 研究：最深的科研能力要求，0→1 推动
- 工程：最广的技术架构视野，快速迭代
- 产品：用户理解与体验设计，连接技术与市场
- PM：项目管理与执行落地，让团队高效运转

---

## 关联连接

- [[DeepSeek]] — DeepSeek 公司实体页面，补充 Harness 团队信息
- [[Harness_Engineering]] — 核心概念，JD 中三层工程模型的最顶层
- [[Context_Engineering]] — 三层工程模型的中间层
- [[Prompt_Engineering]] — 三层工程模型的基础层
- [[Agent_Loop]] — Agent 核心运行机制
- [[MCP]] — 模型上下文协议
- [[Multi_Agent_System]] — 多智能体系统
- [[Memory_Agent]] — Agent 记忆系统
- [[Tool_Calling]] — 工具调用
- [[Claude_Code_Subagent]] — Subagent 机制
- [[Claude_Code_Skills]] — 技能系统
- [[Skill_Factory]] — 元技能/技能工厂
- [[Agent_Observability]] — Agent 可观测性
- [[Eval_Harness]] — 评估流水线
- [[Work_Boundary]] — Agent 工作边界
- [[API设计]] — 预留链接
