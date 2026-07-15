---
title: "Harness Engineering"
type: concept
tags: [AI编码, 驾驭工程, 软件工程, 智能体, 系统工程]
sources: 
  - https://openai.com/zh-Hans-CN/index/harness-engineering/
  - raw/01-articles/07-multi-agent-production.zh-Hans.md
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Harness Engineering（驾驭工程）

## 定义

Harness Engineering（驾驭工程）是由 **Mitchell Hashimoto**（HashiCorp 联合创始人）于 2026 年 2 月 5 日首次提出，并由 **OpenAI** 于 2026 年 2 月 11 日正式推广的软件工程范式。

其核心哲学是：

> **人类掌舵，智能体执行。**

Harness（马具/缰绳）的本意是控制马匹的器具。驾驭工程的本质是：**为 AI 智能体设计并构建约束机制、反馈回路、工作流控制和持续改进循环的系统工程实践。**

> **Simon Willison 2025**："coding agent = LLM + harness"；harness = 所有**不是 model 本身**的代码。
>
> **OpenAI 2026**：也正式使用 "Harness Engineering" 这个说法（2026-02 发布）。

### 三层工程分工定位 (awesome-agentic-ai-zh)

在具体的 Agent 工程实践中，Harness Engineering 是三层工程堆栈的最顶层：

| 层级 | 工程对象 | 核心问题 | 对应 Stage |
|------|---------|---------|-----------|
| **1. Prompt Engineering** | 送进 LLM 的**字符串**（system prompt / few-shot / 格式） | "这一次要怎么问？" | Stage 2 |
| **2. Context Engineering** | 窗口里装的**信息**（RAG / memory / tool defs / history 组装） | "这次该给模型哪些信息？" | Stage 6 |
| **3. Harness Engineering** | 模型**外围的执行与控制层**（loop / retry / sandbox / observability / 部署） | "整个流程怎么跑起来？" | **本概念** |

> 🔁 **下一层：Loop Engineering（循环工程）**：2026 浮现的第四层是"设计 agent 的迭代循环本身"——目标、可用工具、context 管理、**终止条件**、错误处理，让 agent 跑数百步、跨 session 仍可靠。

**怎么分辨自己在做哪一层？问自己**：
1. 改的是**字符串本身**？→ Prompt engineering
2. 改的是**塞进窗口的信息**？→ Context engineering
3. 改的是**调用模型的外围程序**？→ Harness engineering

它不优化模型本身，而是**优化模型运行的环境和系统**。

## 历史定位

驾驭工程被视为继以下范式之后的 **第三次重心转移**：

1. **提示词工程（Prompt Engineering）** — 优化输入给模型的指令
2. **上下文工程（Context Engineering）** — 优化模型可访问的信息范围
3. **Harness Engineering（驾驭工程）** — 优化模型运行的系统与环境

## 核心公式

> **Agent = Model + Harness**

模型能力趋同的背景下，决定 AI 产业落地效果的核心变量已从"模型中心论"转向"系统工程论"。

## 核心模块

### OpenAI 的五模块框架

| 模块 | 说明 |
|------|------|
| **按需索引** | 使用 AGENTS.md 等索引文件让 Agent 按需读取信息，而非一次性加载全部上下文 |
| **硬约束/代码拦截** | 用 Lint 工具、结构化测试脚本等确定性工具限制 Agent 行为，而非用 Prompt"建议" |
| **三层自动质检** | L1 硬性规则 → L2 执行测试 → L3 高推理模型质检，形成自动化反馈闭环 |
| **数据探针** | 为 Agent 开放 UI 测试工具、日志系统、性能指标等感知通道 |
| **垃圾回收** | 定期运行的清理 Agent 自动扫描偏差、修复技术债，防止 Agent 指数级放大坏模式 |

### 生产级 Agent Runtime 的 8 个核心元件（awesome-agentic-ai-zh）

一个可部署的 Agent Runtime 包含以下 8 个核心元件。前 6 个是 Runtime 内建，第 7 个 Eval 是外挂工具，第 8 个 Cost/Latency 是跨层议题：

| #   | 元件                            | 做什么                                                                  | 对应练习                       |
| --- | ----------------------------- | -------------------------------------------------------------------- | -------------------------- |
| 1   | **Agent Loop**                | "LLM → Tool → Result → LLM" 循环、稳定处理多轮                                | 练习 1 Multi-Agent 辩论        |
| 2   | **Tool Registry**             | 动态 tool dispatch、permission gate、sandboxing                          | 在每个 Framework/SDK 都有       |
| 3   | **Context Manager**           | message history 管理、context window 控制、auto-compact                    | 练习 4 SDK 进阶                |
| 4   | **Safety Layer**              | permission prompts、sandboxed exec、destructive op 拦截                  | SDK 可自定义                   |
| 5   | **Retry / Recovery**          | tool fail 怎么处理（exception vs LLM 自己看 error 反思）                        | 练习 4 SDK 进阶                |
| 6   | **Telemetry / Observability** | metrics、logging、token counting、trace export                          | **练习 3 Observability**     |
| 7   | **Eval Harness**              | regression test、quality gate、A/B test                                | **练习 2 Eval**              |
| 8   | **Cost / Latency** ⭐          | prompt caching、model routing、thinking budget、batching、semantic cache | **练习 6 Cost Optimization** |

> **Framework vs Harness 关键差别**：Framework（Agent 框架）规范 **API**——你调用的接口长什么样；Harness 规范 **Runtime**——怎么跑、怎么 recovery、怎么观测。

### 反馈循环：Agent 进步的真正机制

Agent 变强靠的是**把反馈送回循环**，不是把开头那段提示写得更完美。反馈可以在四个时机进来：

| 时机             | 白话                        | 工程上长什么样                                       |
| -------------- | ------------------------- | --------------------------------------------- |
| **1. 工具返回值**   | 工具吐回的那段话本身就是写给 Agent 看的反馈 | 把错误信息、提示、下一步建议"写清楚"，别只丢一个 stack trace         |
| **2. 执行中插话**   | 在 Agent 两次思考之间塞一句话调整方向    | 中途注入消息（steering），不用等它整轮跑完才修正                  |
| **3. 单轮结束的验收** | 一轮做完，由"另一个人"对着目标检查        | 用独立的验收者（Evaluator）比对目标，而不是让 Agent 自己打分        |
| **4. 外层 Loop** | 对着同一个目标反复叫 Agent，直到完成     | 目标导向的重跑（如 OpenAI Codex 的 `/goal`、或 cron 定时重跑） |

> 📌 **为什么第 3 个（独立验收）特别重要**：Anthropic 实验发现，叫 Agent 检查自己的成品几乎都会"自我称赞"。把"做东西的 Agent"和"验收的 Agent"拆开，比让同一个 Agent"对自己更严格"容易得多。

## "推理三明治"结构

```
┌─────────────────────────────┐
│  顶层：高推理模型（规划拆解）  │  ← o1/R1 级别
├─────────────────────────────┤
│  中层：低推理模型（批量执行）  │  ← GPT-4o-mini 级别
├─────────────────────────────┤
│  底层：高推理模型（按需质检）  │  ← 仅对高风险变更
└─────────────────────────────┘
```

## Cost / Latency 优化（Production 必修）

Production Agent 跑久了，**Cost / Latency 两条线会吃掉大半预算与用户体验**。2024-2026 前沿模型已把成本优化作为 First-class API Feature，**会用 = 省 50-90% Cost / Latency**。

### 技术总览

| 技巧 | 节省机制 | 2026 状态 | 省多少 |
|------|---------|-----------|-------|
| **Prompt Caching** | 重复 prefix 一次计费、后续 cache hit 折扣 | Anthropic / OpenAI / Gemini 全支持 | ~90% |
| **Model Routing / Cascade** | 简单 query → 小 model、难 query → frontier model | RouteLLM / OpenRouter production 内建 | 50-90% |
| **Thinking Budget** | reasoning model 可控 thinking token 上限 | Claude / Gemini API 参数 | 可控 |
| **Speculative Decoding** | 小 model 预测 N token、大 model 一次验证 | vLLM / TGI 内建 | 2-3× 速度 |
| **Batching** | 多 query 并行处理、GPU 利用率高 | vLLM、production inference layer | 高吞吐 |
| **Semantic Caching** | 相似 query 共享回答（不只 exact match）| GPTCache / Helicone 内建 | 不定 |

> 💡 详见 [[Cost_Optimization]] 概念页的完整分层实践路径。

### 参考实现

想看实际在 Production 跑的 Harness 长什么样：
- **Claude Code 整个 Runtime** — Reference Harness 实现（[[Claude_Code_Harness]] 解剖 main loop + 前 6 个 runtime 元件位置）
- **`anthropics/claude-agent-sdk-python`** — 同 Claude Code 的 Python SDK 版

## OpenAI 实验验证

详见 [[摘要-openai-harness-engineering]]，核心结论：

- 3-7 人团队，5 个月构建 100 万行代码，效率提升约 10 倍
- 禁止人类手动编写任何代码
- 关键瓶颈从"代码生产速度"变为"人类 QA 注意力"

## 行业验证

| 组织 | 实践 | 效果 |
|------|------|------|
| **LangChain** | 仅优化 Harness，不改变模型 | Terminal Bench 2.0：52.8% → 66.5%（Top30 → Top5） |
| **Anthropic** | 三阶段 Harness（planner → generator → evaluator）| 连续跑数小时做出完整音乐制作 App（2026-03） |
| **Stripe** | Minions Agent 体系 | 每周自动合并 1300+ 个 AI 编写的 PR |
| **斯坦福大学** | 论文《Meta-Harness》 | 让 AI 自动设计 Harness（2026年3月） |
| **中国信通院** | Harness Engineering 研究报告 | 2026年4月启动编制工作 |
| **阿里云** | HiClaw 开源项目 | 探索群体智能场景下的 Harness 实践 |
| **DeepSeek** | Harness 团队设置四个方向 | 以研究、工程、产品结合的方式推进 Agent 落地 |

### 行业视角：DeepSeek

DeepSeek（深度求索）是首个**以完整团队建制**系统化投入 Agent Harness 的中国 AI 公司。其 Harness 团队设置四个方向，覆盖从科研到交付的全链路：

> **团队使命** — 以研究、工程、产品相结合的方式，把 DeepSeek 的模型能力转化为前沿的科研突破与领先的 Agent 产品。

**核心公式**：`Model + Harness = Agent`

**四个角色方向**：

| 方向 | 核心问题 | 输出 |
|------|---------|------|
| **Agent Harness 研究** | "不确定能不能做，前沿在哪？" | 论文、Benchmark、实验数据、新机制原型 |
| **Agent Harness 研发/工程** | "怎么做得可靠、可扩展、可维护？" | 产品架构、技术实现、开发者工具 |
| **Agent Harness 产品** | "用户真正需要什么？" | 产品定义、路线图、体验设计、社区 |
| **Agent Harness 项目经理**（实习）| "团队怎么跑得顺？" | 进度追踪、风险识别、流程优化 |

> 💡 这构成了 Agent Harness 行业的第一份**公开角色光谱**——从研究深度到执行宽度的连续体。

**知识要求全角色共享**：DeepSeek 要求所有方向成员掌握 LLM 及 Agent 的基础机制（Agent Loop、Tool Use、Reasoning、Planning、Skills、MCP、Memory、Subagent、Multi-Agent、KV Cache），并深入理解三层工程模型（[[Prompt_Engineering]] / [[Context_Engineering]] / [[Harness_Engineering]]）。

详见 [[摘要-deepseek-harness-team-jd]] — 完整职位描述与技术知识图谱。

#### 服务端工程团队：Harness 的工程实现层

DeepSeek 的服务端工程团队承担与 Harness 团队**互补**的角色——将 Agent 运行时设计落地为可量产的在线服务。其团队使命体现了工程的艺术性：

> **使命**：与智能共演化，让工程即作品。

| 对比维度 | Harness 团队 | 服务端工程团队 |
|---------|-------------|---------------|
| 聚焦 | Agent 运行时设计（Loop/Tool/Memory） | 基础设施与生产服务 |
| 产出 | Harness 原则、机制、原型 | 在线服务、数据管道、工程平台 |
| 用户 | 研究员、工程师（内部） | 亿万用户（外部） |

三个方向覆盖了**生产 AI 系统的完整三层架构**：

```
线上核心服务   ← 用户前线（API 网关、应用层、数千万日活）
    ↓
Agent 后端    ← Agent 能力的工程化（执行环境、评测、数据）
    ↓
数据仓库      ← 数据底座（离线/实时计算、存储）
```

**Agent 后端方向**是三个方向中与 Harness Engineering 关系最密切的，包含三个独特工程课题：

| 课题 | 说明 | 关联 Harness 元件 |
|------|------|------------------|
| **Agent 执行环境快照** | 将 Agent 运行时完整状态序列化存储（上下文、工具调用轨迹、中间结果）| [[Agent_Loop]]（循环状态持久化）|
| **Agent 框架集成与评测** | 接入各类 Agent 框架构建高效评测基础设施 | [[Eval_Harness]]（自动化评估）|
| **Agent 数据生成** | 用 Agent 执行轨迹作为训练数据反哺模型 | **Harness→Model 反馈回路** |

详见 [[摘要-deepseek-service-engineer-jd]] — 完整职位描述与三层架构分析。

## Harness 工程师（新兴职业）

- **工作内容转变**：从"写代码"转变为"设计让 AI 可靠工作的控制系统"
- **核心能力**：定义架构约束、设计反馈回路、编码业务规则、构建自动化验证机制
- **工作方式**：深度优先，将更大目标拆解为更小的构建模块供智能体执行

### 角色光谱（DeepSeek 四方向模型）

DeepSeek 2026 年的 Harness 团队建制首次公开定义了 Agent Harness 领域**从研究到执行**的四个角色层次：

```
研究 (Research) ── 工程 (Engineering) ── 产品 (Product) ── 项目管理 (PM)
  科研深度 ────────────────────────────────────────────→ 执行宽度
  不确定性问题 ────────────────────────────────────────→ 确定性交付
```

### Agent Harness 知识图谱

来自 DeepSeek JD 和 wiki 三层工程模型的知识体系。所有角色共享**基础机制层**，各角色在**应用层**有不同侧重：

#### 基础机制层（全角色共享）

| 知识领域 | 核心问题 | wiki 映射 |
|---------|---------|----------|
| **LLM API / KV Cache** | 模型怎么调、上下文窗口怎么管理 | [[OpenAI_Compatible_API]] |
| **Agent Loop** | 思考→行动→观察的循环如何运转 | [[Agent_Loop]] |
| **Tool Use** | 工具怎么定义、调用、容错 | [[Tool_Calling]] |
| **Reasoning / Planning** | Agent 如何推理、如何拆解任务 | [[Chain_of_Thought]] |
| **Skills** | 可复用能力模块如何定义与加载 | [[Claude_Code_Skills]]、[[Skill_Factory]] |
| **MCP** | 工具-模型-数据的标准化协议 | [[MCP]] |
| **Memory** | 短期/长期记忆如何存储与检索 | [[Memory_Agent]] |
| **Subagent / Multi-Agent** | 子代理如何委派、多代理如何协作 | [[Claude_Code_Subagent]]、[[Multi_Agent_System]] |

#### 三层工程模型（全角色共享）

| 层级 | 核心问题 | 代表工作 |
|------|---------|---------|
| **Prompt Engineering** | "这次要怎么问？" | 指令优化、Few-shot、格式控制 |
| **Context Engineering** | "这次该给模型哪些信息？" | RAG、窗口管理、渐进式披露 |
| **Harness Engineering** | "整个流程怎么跑起来？" | Loop/Retry/Sandbox/Observability |

#### 应用层（角色差异化）

| 能力 | 研究 | 工程 | 产品 | PM |
|------|:---:|:---:|:---:|:--:|
| 科研实验设计 | ★★★ | ★☆☆ | ★☆☆ | — |
| Benchmark 构建 | ★★★ | ★★☆ | ★★☆ | — |
| 原型快速迭代 | ★★★ | ★★★ | ★☆☆ | — |
| 系统架构设计 | ★☆☆ | ★★★ | ★☆☆ | — |
| AI 辅助开发 | ★★★ | ★★★ | ★★☆ | — |
| UI/UX 设计 | — | ★☆☆ | ★★★ | — |
| 用户研究/数据分析 | ★★☆ | ★☆☆ | ★★★ | — |
| 社区运营 | — | ★☆☆ | ★★★ | — |
| 进度跟踪/风险管理 | — | ★☆☆ | ★★☆ | ★★★ |
| 沟通协调 | ★★☆ | ★★☆ | ★★★ | ★★★ |

### AI 辅助开发能力（跨角色基础要求）

> **"能够在 AI 辅助下，在没有直接经验的领域进行有质量保证的编程工作。"**
>
> — DeepSeek Harness 团队 JD

AI 辅助开发已从"加分项"变为 Harness 领域所有角色的**基础能力**。具体包括：
- AI 编程工具的高阶使用（Claude Code、Cursor、Copilot、Codex 等）
- Prompt AI 写出可维护的、生产级的代码
- AI 生成代码的审查、测试与调试
- 在新领域借助 AI 快速上手

### "高强度用户"门槛

DeepSeek JD 要求求职者**把 Agent 产品融入日常工作和生活**。这意味着：
- 深度使用代码类 Agent：Claude Code、Cowork、Codex、Cursor、Copilot 等
- 深度使用通用类 Agent：Manus、OpenClaw、Hermes 等
- **"对模型行为有品味有判断力"**——只有深度使用才能建立 Agent 行为的直觉

> 详见 [[Developer_Agentic_Workflow]] 中 Agent 工具链的分级使用模式。

## 关键原则

1. **代码仓库即记录系统** — 仓库之外的知识对智能体而言"不存在"
2. **AGENTS.md 是地图而非百科全书** — 渐进式披露，避免上下文挤占
3. **枯燥技术更优** — 可组合、API 稳定、训练集中表现好的技术栈更适合智能体
4. **吞吐量改变合并哲学** — 纠错成本低时，等待成本 > 错误成本
5. **品味编码化** — 人类的判断力持续转化为文档和工具规则

## 跨来源原则框架（4 大类别）

Anthropic、OpenAI、Cognition、Hamel Husain 等各自用不同词汇表达同一组设计约束。以下是跨来源整理的 4 大类别：

| 类别 | 核心问题 | 该类别下的原则 |
|------|---------|---------------|
| **① Context 管理** | 上下文不爆炸，Agent 永远拿到对的信息 | System of Record / Memory Persistence / Progressive Disclosure |
| **② Interface/沟通** | Agent 看得懂 Codebase，也能说清楚自己在做什么 | Legibility / ACI / Transparency（show planning）|
| **③ Quality/验证** | 写得对、不能 Hallucinate | Taste Invariants / Evaluator-Optimizer / LLM-as-Judge / "Evals are everything" |
| **④ Process 纪律** | Scale + Iterate 不爆 | Simplicity / Throughput Changes Merge Philosophy / Don't Build Multi-Agents |

### 5 个 OpenAI 原则展开 + Anthropic 对照

| #   | OpenAI 原则                               | 一句话                                   | Anthropic 对应词                                     |
| --- | --------------------------------------- | ------------------------------------- | ------------------------------------------------- |
| 1   | **Legibility**                          | 为 Agent 优化 Navigability（不是让人读懂 Agent） | ACI + Tool Documentation                          |
| 2   | **System of Record**                    | 知识住 docs、不住 prompt                    | CLAUDE.md hierarchy + Memory persistence          |
| 3   | **Progressive Disclosure**              | 小 Entry Point + 教 Agent 之后去哪查         | 同词（Anthropic Skills 自用的 core design principle）    |
| 4   | **Taste Invariants**                    | 定义边界、不细管实作；Lint 强制规范                  | Evaluator-optimizer loops + Poka-yoke tool design |
| 5   | **Throughput Changes Merge Philosophy** | Agent PR 速度 > 人类 QA 速度 → QA 必须自动化     | LLM-as-judge 并用 + Human Evaluation                |

### 原则之间的 Enabling 关系

| 关系                               | 描述                                                                    | 为什么重要                    |
| -------------------------------- | --------------------------------------------------------------------- | ------------------------ |
| **SoR + Memory + PD 三者配对**       | SoR 提供目的地、Memory 跨 Session 保存、PD 是导航                                  | 三者单独用不够，必须一起设计           |
| **Legibility ↔ Transparency 双向** | Agent 能读 Codebase 才能 Self-report；Agent 会 Self-report 你才能验证 Legibility | 互为前提                     |
| **Quality 是 Process 自动化前置**      | 没写死 Invariants + Eval Loop，人类无法把 Review 交给 Automation                 | Process 纪律的必要条件          |
| **Simplicity 是隐性 Root**          | 一上来就堆 Multi-Agent，其他所有原则的复杂度都会暴涨                                      | Cognition 与 Anthropic 一致 |

### Harness 5 原则 × Harness 8 元件对照

| 原则 ＼ Harness 元件            | Agent Loop | Tool Reg | Ctx Mgr | Retry | Sandbox | Obs | Eval | Cost/Lat |
| -------------------------- | :--------: | :------: | :-----: | :---: | :-----: | :-: | :--: | :------: |
| **Legibility**             |            |    ✓     |    ✓    |       |         |  ✓  |      |          |
| **SoR**                    |            |          |   ✓★    |       |         |  ✓  |      |          |
| **Progressive Disclosure** |     ✓      |          |   ✓★    |       |         |     |      |    ✓     |
| **Taste Invariants**       |            |    ✓     |         |   ✓   |    ✓    |     |  ✓★  |          |
| **Merge Philosophy**       |            |          |         |       |         |     |  ✓★  |    ✓     |

→ **Context Manager（#3）+ Eval（#7）** 是被 4-5 个原则同时作用的核心热点。

### Eval Rigor — Harness 设计对 Benchmark 的 Bias

> **关键事实**：同一 Model、不同 Scaffold（= Harness），分数可以差一倍。Scaffold 跟 Model 一样是 Benchmark 的变因。

| 你在做什么 | Harness 该怎么设计 |
|-----------|-------------------|
| 比较两个 Model | **固定 Scaffold**——否则你比的是 Scaffold 不是 Model |
| 报告 Agent 分数 | 报 pass^k（k≥3）或多 Run 平均 + 变异 |
| 自己写 Eval | 先假设"Agent 会 Reward Hack"——三管齐下：Held-out test + LLM judge + 改文件侦测 |
| 信 Benchmark 排名 | 先查 Reward Design 有没有被审计过 |

> 来源：[Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825) · [SWE-bench benchmark hygiene](https://www.whocodesbest.com/news/2026/swe-bench-april-2026-benchmark-hygiene-matters)

### Model-Harness-Fit 与 Bitter Lesson

> **你今天搭的 Harness，是为"今天这个 Model"量身搭的；Model 一变强，有些 Harness 就过期了。**

- **Model-Harness-Fit**：一套 Harness 跟当下 Model 的能力"配对"。补 Model 弱点的 Scaffold，下一代 Model 自己就会做，Scaffold 变成多余包袱
- **Bitter Lesson（苦涩的教训）**：AI 历史一再证明，靠"人工塞进去的巧思"长期几乎都输给"让模型用更多运算自己学"。过度搭建（Over-scaffolding）是在跟这个趋势对赌

> 概念根源：Rich Sutton, [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)（2019）

**白话的取舍**：能用"最薄、刚好能出货"的 Harness，就不要搭一座城堡。每加一层 Scaffold，先问一句："这是在补 Model 真正的弱点，还是只是我不放心？"

## 知识冲突

- **与 [[Agentic_Coding]] 的关系**：Agentic Coding 更聚焦于 Agent 如何自主编码的实践，Harness Engineering 则更强调为 Agent 设计运行环境的系统工程体系。二者互补而非冲突。
- **人类角色争议**：部分观点认为 Harness Engineering 最终目标是完全自动化；OpenAI 实验表明人类注意力仍是稀缺资源，判断力在未来很长时间内仍由人类主导。

## 关联连接
- [[Frontier研究]] — 范式探索层：超越当前 AI 范式，探索持续学习、自进化、下一代架构与学习算法的前沿研究实践
- [[情感智能数据工程]] — 情感温度评测数据层：以人类情感认知为基准，通过 Badcase 挖掘与归因分析，提升 AI 在情感陪伴与角色扮演场景中的互动真实感与沉浸度
- [[AI创作数据工程]] — 创作审美评测数据层：将人类审美标准转化为可操作的评测体系与数据管线，驱动模型在文学创作与实用写作领域的能力提升
- [[专业领域数据工程]] — 专业领域评测数据层：通过领域专家判断力构建评测体系与高质量数据，将人类专业知识注入模型；覆盖小语种/医学/法律等学科
- [[Agent数据产品工程]] — 评测数据桥梁层：通过评测体系设计与数据生产管线构建，连接产品体验与模型能力；聚焦办公/生活/搜索等通用场景
- [[Agent能力工程]] — 能力构建层：通过 RL 环境构建、评测任务设计和能力短板补齐，系统性地提升模型 Agent 能力
- [[AI产品工程]] — 最上层产品化层：站在模型与世界之间，将 AI 技术能力转化为用户体验的产品化工程层
- [[Agentic_Coding]] — AI Agent 自主驱动编程
- [[Agent_First_Engineering]] — Harness Engineering 的具体 7 步落地方法论
- [[AGENT_MD]] — AI Agent 行为规范入口文件
- [[摘要-openai-harness-engineering]] — OpenAI 官方实验报告摘要
- [[Claude_Code_Workflow]] — Claude Code 开发工作流方法论
- [[Monorepo]] — 单仓库策略
- [[AI_Mastery_Compass]] — AI 大模型驾驭进阶罗盘，与 Harness 工程的"角色设定"和"迭代优化"互为补充
- [[Legibility]] — OpenAI 五原则之一：为 Agent 优化 Codebase 可读性
- [[System_of_Record]] — OpenAI 五原则之二：知识权威来源
- [[Progressive_Disclosure]] — OpenAI 五原则之三（已在 Google ADK 中阐述）：渐进式披露架构
- [[Taste_Invariants]] — OpenAI 五原则之四：品味不变量 / 工程美学编码化
- [[Work_Boundary]] — Agent 自主权范围纪律，跨所有层的根概念
- [[Autonomy_Gradient]] — 基于风险的授权机制：Suggest / Propose / Execute
- [[Cost_Aware_Budget_Gates]] — 成本感知的预算门控
- [[Graceful_Degradation]] — Frontier Model 挂掉时的回退策略
- [[Agent_As_Judge]] — 用 Agent 评审 Agent 输出
- [[Contract_Driven_Handoffs]] — 契约驱动的 Agent 交接
- [[ADK]] — Google Agent Development Kit，Harness Engineering 方法论的具体实现框架之一
- [[Skill_Factory]] — 元 Skill / Skill Factory，Agent 自我扩展的高级编排模式
- [[Eval_Harness]] — Harness 第 7 个核心元件：自动化评估流水线
- [[Agent_Observability]] — Harness 第 6 个核心元件：Agent 可观测性
- [[Cost_Optimization]] — Harness 第 8 个核心元件：成本与延迟优化
- [[Claude_Code_Harness]] — Claude Code 作为 Reference Harness 实现的完整解剖
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — Harness Engineering 八元件 + 反馈循环的核心来源（Stage 7）
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 跨来源 Harness 原则框架 + Eval Rigor + Bitter Lesson 来源
- [[摘要-awesome-agentic-ai-zh-for-developer]] — 开发者工作流中的 Harness 实践（CI review / anti-patterns）
- [[Developer_Agentic_Workflow]] — 开发者场景分类中的 Harness 应用
- [[Continue_Dev]] — CI source-controlled AI checks（Harness CI 自动化实现）
- [[Repomix]] — codebase 打包（Harness 输入预处理工具）
- [[From_NoCode_To_Agent_Paradigm]] — Harness Engineering 是 Agent 范式的"部署运维层"，替代传统无代码的搭建运维
- [[Agent_Loop]] — 第 1 个核心元件的深度展开
- [[摘要-deepseek-service-engineer-jd]] — DeepSeek 服务端工程团队 JD：Agent 后端课题的工程实现层
- [[预训练数据工程]] — 预训练数据全生命周期工程体系，数据采集环路与分布式框架是 Harness Engineering 在 LLM 基础设施层的具体应用
- [[摘要-预训练数据工程师-jd]] — 预训练数据工程师 JD，数据基建方向与 Harness Engineering 的分布式系统能力要求高度重叠
- [[Agent沙箱工程]] — Agent 沙箱工程是 Harness Engineering Safety Layer 和 Sandboxed Execution 的物理基础设施实现

- [[后训练研究]] — 训练阶段映射：RL 训练循环是 Harness Engineering 八核心元件在训练阶段的重要应用

- [[多模态理解研究]] — Agent 执行映射：多模态 Agent 的执行逻辑和安全控制是 Harness Engineering 在多模态维度的应用
- [[摘要-deepseek-agent-infra-jd]] — Agent Infra JD，DSec 沙箱平台是 Harness 层依赖的物理执行环境
