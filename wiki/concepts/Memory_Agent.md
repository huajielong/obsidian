---
title: "Memory_Agent"
type: concept
tags: [memory, agent, CoALA, working memory, long-term memory, episodic memory]
sources: [raw/01-articles/06-memory-rag.zh-Hans.md]
last_updated: 2026-07-10
---

# Memory（Agent 记忆系统）

Agent Memory 是让 Agent 能够跨对话、跨 session、跨任务保持状态、偏好与经验的能力。它解决的是 **RAG 无法覆盖的三个场景**：跨 session 记住用户偏好、累积 agent 过往的成败教训（[[Reflexion]]）、Long-horizon task 中的中间状态保持。

> RAG 解决"从外部知识库检索相关片段"，Memory 解决"Agent 自己跨对话/跨 session 记住事情"——两者互补而非替代。

## Working Memory vs Long-term Memory（时间轴）

| 维度               | Working Memory（工作记忆）    | Long-term Memory（长期记忆）        |
| ---------------- | ----------------------- | ----------------------------- |
| 核心意思             | 当前 task / 对话中模型看得到的信息   | 存在外部、可跨 session 取回的信息         |
| 持续时间             | 短，限于当前 session          | 长，可跨 session                  |
| 技术基础             | Context Window / Prompt | Memory Store / Vector DB / 文件 |
| 是否受 Context 长度限制 | 会                       | 较不受限（只取一小段放回 Context）         |
| 生活例子             | 刚收到的验证码、上一句话            | 你深学过的知识、图书馆、读过的书              |

## Episodic / Semantic / Procedural Memory（内容轴）

**注意**：Working/Long-term 是 **时间轴**，下面三种是 **内容轴**，两组分类正交不互斥。Long-term Memory 里可以同时有三种内容。

| 类型 | 核心意思 | 示例 |
|------|---------|------|
| **Episodic Memory**（情节记忆） | 某次任务、某次互动、某次失败的具体经验 | Reflexion 记录、过往 Trajectories |
| **Semantic Memory**（语义记忆） | 稳定知识、用户偏好、背景事实 | RAG 知识库、用户画像、偏好 |
| **Procedural Memory**（程序记忆） | Agent 知道"怎么做事"的规则、工具、Workflow | Tool Definitions、Claude Code Skills |

## CoALA 框架 — Agent Memory 的 4 层分类法

[Sumers et al. 2023](https://arxiv.org/abs/2309.02427) 提出的 Cognitive Architectures for Language Agents 框架：

| 类型 | 存储什么 | 对应示例 |
|------|---------|---------|
| **Working Memory** | 当前任务上下文 | LLM Context Window 本身 |
| **Episodic Memory** | 过去任务的具体经验 | Reflexion 记录、过往 Trajectories |
| **Semantic Memory** | 抽象事实 / 知识 | RAG 知识库、用户画像 |
| **Procedural Memory** | 如何执行动作 / 技能 | Tool Definitions、[[Claude_Code_Skills]] |

> 可当作检查表，帮你看出 Agent 缺了哪一层。Production Agent 通常需要兼顾全部 4 层。

## 3 种设计模式（何时用什么）

| Pattern | 适合场景 | 怎么跑 | 成本 |
|---------|---------|--------|------|
| **1. Naive Buffer**（全塞 Context） | 短对话 ≤10 turn，不需要跨 session | 每次把整段 history 送进 prompt | 线性增长，token 烧得快 |
| **2. Summary + Recent** | 中长对话 ~50 turn，想压缩历史 | 每 N 轮 LLM 摘要旧历史；prompt = summary + last N turns | 中等，有 LLM 摘要成本 |
| **3. Vector Store + Retrieval** | 跨 session、知识库场景 | Embed 过去消息 → Vector DB → 每轮 query 相关片段 | 高，但 token 用量稳定 |

**选型指南**：
- 无跨 session 需求 → **Pattern 1**
- 长对话需记住今天聊过什么 → **Pattern 2**
- 跨 session + 知识库 → **Pattern 3**
- Production 大型 Agent → 通常 **混用**（近期用 Pattern 1/2，长期用 Pattern 3）

## 5 个可上生产的 Memory Layer

| Framework | 主场 Use Case | 特色 |
|-----------|-------------|------|
| **agentmemory**（★7.7k, Apache-2.0） | Coding Agent 跨 session 记忆 | MCP-universal（Claude Code / Cursor / Gemini CLI 都能接），95.2% R@5 |
| **mem0**（★55.6k, Apache-2.0） | Chatbot / 个人助手 user-level memory | 自动事实提取 + 遗忘 + namespace，社区最大 |
| **Letta**（原 MemGPT, ★22.7k, Apache-2.0） | 长 session Agent（按月计） | OS-style paging memory（working + archival 双层） |
| **Zep**（★4.6k, Apache-2.0） | Temporal KG-based memory | 对话历史建成 Temporal KG，适合 time-aware reasoning |
| **graphiti**（★27.5k, Apache-2.0） | 实时知识图谱 Agent 记忆 | 带时间轴的 Knowledge Graph；Zep 背后的引擎 |
| **LangMem**（★1.4k, MIT） | LangChain-native memory | 直接接 LangGraph，适合已 commit LangChain stack 的项目 |

**选型指南**：
- Coding Agent → **agentmemory**（MCP-native）
- Chatbot / 个人助手 → **mem0**
- 长运行 Agent（周/月） → **Letta**
- 时间感知推理 + Audit Trail → **Zep**
- 已用 LangChain 栈 → **LangMem**

## Generative Agents — 三重评分加权（经典案例）

[Park et al. 2023 — Generative Agents: Smallville](https://arxiv.org/abs/2304.03442) 的 25 个 NPC Agent 使用三重评分检索记忆：

- **Importance**：LLM 为每个 memory 打 1-10 分（吃饭=2，分手=9）
- **Recency**：基于时间的指数衰减
- **Relevance**：与当前查询的 embedding 相似度

**最终得分** = α·importance + β·recency + γ·relevance，按得分排序检索 top-k。这是 mem0 / Letta 等 production memory layer 的概念骨架。

## 2024-2026 Memory 三大主线

1. **🧠 结构化、可演化、可联想** — A-MEM（Zettelkasten 风格，memory 之间自动链接）、HippoRAG 2（KG + PageRank）
2. **📚 调查爆发** — "Memory in the Age of AI Agents"（3D 分类法 + benchmark）、"Memory for Autonomous LLM Agents"（形式化 write-manage-read 循环）
3. **🛡 Memory 安全** — Cross-session poisoning / 未授权访问攻击（Memory Security survey）

## 关联连接

- [[Context_Engineering]] — Memory 是 Context Engineering 的核心 Sub-problem（Write + Compress）
- [[RAG]] — RAG 解决外部知识检索，与 Memory 互补而非替代
- [[Reflexion]] — 典型的 Episodic Memory 应用，跨 trial 累积教训
- [[Claude_Code_Memory_System]] — Claude Code 的三层持久记忆机制（Claude Code Memory / File-based Memory / Project Context）
- [[Agent_Loop]] — Agent 主循环中 Memory 模块的读写位置
- [[Chunking]] — Pattern 3 Vector Store 依赖 Chunking 策略
- [[Multi_Agent_System]] — Stage 7 Multi-agent 中每个 Agent 有自己的 Memory + Shared Memory
- [[Claude_Code_Skills]] — Procedural Memory 的 Claude Code 实现
- [[摘要-awesome-agentic-ai-zh-memory-rag]] — 本概念的来源资料
