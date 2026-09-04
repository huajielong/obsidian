---
title: "Context_Engineering"
type: concept
tags: [上下文工程, RAG, memory, agent loop, context window, chunking]
sources: [raw/01-articles/awesome-agentic-ai-zh-stage-02-prompt-engineering.md, raw/01-articles/06-memory-rag.zh-Hans.md, raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md, raw/09-archive/【生成式人工智慧與機器學習導論2025】第 2 講：上下文工程 (Context Engineering) — AI Agent 背後的關鍵技術.md]
last_updated: 2026-08-05
---

# Context Engineering（上下文工程）

Context Engineering（上下文工程）是 **LLM-powered system 三层工程堆栈的第二层**，工程对象是 **每次 LLM 调用时上下文窗口中填充的信息**——包括 RAG 检索结果、对话历史、工具定义（Tool Definitions）、长期记忆等。

> Karpathy 2025-06 原推文：Context Engineering 是"把 **刚好对下一步有用的信息** 填进 context window 的精细艺术。"

[[Hung_yi_Lee]] 在《生成式人工智慧與機器學習導論(2025)》第一讲给出更直觉的教学定义：语言模型像"关在暗无天日小房间里只会接龙的人"，看不到外部世界，**人类的责任是确保输入 Prompt 的信息足够**，让模型有机会接出正确结果——这就是 Context Engineering。课程实例：平台把"今天是几月几号、模型叫什么名字"等信息通过 System Prompt 预先塞进对话最前面，模型才能正确回答日期类问题。

李宏毅同一门课**第二讲**又给出另一层视角：把语言模型看作函数 `f`，训练是改 `f`（线上模型多为闭源、改不了），**Context Engineering 就是改输入 x**——自动化管理模型输入，让 `f(x)` 符合预期。其核心目标一句话：**「避免塞爆 context」**——把需要的东西放进去、把不需要的请出来。课程进一步拆解了一个完整 Context 的组成（User Prompt / System Prompt / 对话历史 / 长期记忆 / RAG 结果 / 工具结果 / 推理过程）与三大招数（选择 / 压缩 / Multi-Agent），见下两节。

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

## 上下文（Context）应包含的组件（李宏毅第 2 讲）

| 组件 | 说明 | 关键点 |
|------|------|--------|
| **User Prompt** | 任务 + 详细指引 + 前提 + 范例 | 模型不会读心术，前提讲清楚能大幅改变答案（曼谷水巨蜥例）；范例直接影响能力（火星文例） |
| **System Prompt** | 开发者预设的固定输入（身份/日期/限制/风格） | Claude 3 Opus 的 System Prompt 公开且超 2500 字 |
| **对话历史** | 短期记忆 | 多轮对话只是按历史继续接龙；单靠对话无法改变模型参数 |
| **长期记忆** | 跨对话记忆（2024-09 后 ChatGPT 推出） | 植入在用户看不到的输入最前方 |
| **搜索 / [[RAG]] 结果** | 外部资讯 | RAG 不保证正确（Google AI Overview 起司胶水例） |
| **工具调用结果** | 工具输出回填 context | 需要开发者执行层（eval 循环）真正驱动工具，见 [[Tool_Calling]] |
| **Reasoning 思考过程** | 模型自己产生的 context（脑内小剧场） | O 系列 / R 系列深度思考；可对用户隐藏，见 [[Model_Based_Planning]] |

## 李宏毅三大招数与四个 Sub-problem 的对应

课程给出的三大常用招数，可与上方 Lance Martin 四子问题互相印证（互补视角，非冲突）：

| 李宏毅招数 | 对应 Sub-problem | 要点 |
|-----------|-----------------|------|
| **① 选择（Selection）** | Select | [[RAG]]、Reranking、Provence 句子级筛选（<300M 参数小模型）、工具版 RAG（工具多时只挑相关的）、记忆挑选（史丹佛小镇 recency/importance/relevance 三指标） |
| **② 压缩（Compression）** | Compress | 递归式摘要（每 N 回合 / 90% 满 / 定时触发）；细节存硬盘 + RAG 取回；摘要里留"指针"避免检索错误 |
| **③ Multi-Agent** | Isolate | 总召 agent 只记"餐厅订好了"一句话，隔离各 agent 的 context，见 [[Multi_Agent_System]] |
| （隐含在"选择"中） | Write | 记忆挑选即 Write 的检索侧，见 [[Memory_Agent]] |

> 课程的实证警示：**"能输入百万 token" ≠ "能读懂百万 token"**——在远未到达窗口上限时模型就已困惑（复制任务 10^4 token 即崩、RAG 资料越多正确率先升后降、Lost in the Middle、挤牙膏式提问拉低能力）。详见 [[上下文腐败]] 与 [[Context_Window]]。

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
- [[上下文腐败]] — 上下文窗口效率衰减现象，Context Engineering 需要应对的核心约束
- [[Agent_Loop]] — Context Engineering 的执行载体
- [[Multi_Agent_System]] — Stage 7 涉及 Isolate Sub-problem
- [[Andrej_Karpathy]] — Context Engineering 概念的共同推动者
- [[Claude_Code_Memory_System]] — Claude Code 中的 Memory 实现
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 来源资料（Stage 2）
- [[摘要-awesome-agentic-ai-zh-memory-rag]] — 来源资料（Stage 6）
- [[预训练数据工程]] — 预训练数据工程的核心工作（语料清洗、去重、质量筛选、数据组织）属于 Context Engineering 的"Select"子问题前置步骤
- [[摘要-预训练数据工程师-jd]] — 预训练数据工程师 JD 中语言数据处理方向和多模态数据方向的内容与 Context Engineering 直接相关
- [[预训练数据四方向对比]] — 综合报告中详细分析了各方向与三层工程模型的对应关系
- [[AI搜索工程]] — AI 搜索工程是 Context Engineering "Select"子问题在搜索引擎尺度的独立展开
- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — 李宏毅课程"确保 Prompt 信息足够"定义的来源
- [[摘要-hung-yi-lee-上下文工程-第2讲]] — 李宏毅第 2 讲：上下文组件、三大招数、"避免塞爆 context"的来源
- [[In_Context_Learning]] — 给范例（few-shot）改 context、不改参数的机制
- [[System_Prompt]] — 注入基础信息（日期/身份）的具体实现手段
