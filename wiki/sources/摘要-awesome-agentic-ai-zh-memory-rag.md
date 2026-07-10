---
title: "摘要-awesome-agentic-ai-zh-memory-rag"
type: source
tags: [RAG, memory, 上下文工程, context engineering, chunking, embedding, vector DB, 学习路线]
sources: [raw/01-articles/06-memory-rag.zh-Hans.md]
last_updated: 2026-07-10
---

## 核心摘要

该资料是 "awesome-agentic-ai-zh" Agentic AI 系统学习路线图的 **Stage 6——上下文管理（Context Engineering）：RAG 与 Memory**，专注于 Agent 系统如何管理上下文的两个核心能力：**Retrieval（从外部知识库查找相关资料）** 和 **Memory（跨对话/跨 session/跨任务保持状态与经验）**。系统性地拆解了 RAG 基础流水线（Ingest → Chunk → Embed → Store → Retrieve → Generate）、八大进阶 RAG 技巧（GraphRAG / Contextual Retrieval / Hybrid Search / Query Transformations / Adaptive RAG / RAPTOR / DSPy）、Memory 的四层分类架构（CoALA 框架）、三种设计模式（Buffer / Summary + Recent / Vector Store），以及 Chunking 策略、Reflexion 持久记忆、RAG Eval 等配套技术。同时覆盖了 2025-2026 年的三大主线演进（KG+Memory 融合、Multimodal RAG、Agentic RAG）和前沿模型 Path 1 vs Path 2 Reasoning 的对比。

## 关键提炼

- **Context Engineering 的定义**：决定每次 LLM 调用时，把哪些信息塞进 context window 的精细艺术（Karpathy 2025-06），对应 Prompt → Context → Harness 三层工程堆栈的中间层
- **四个 Sub-problem**：Select（捞哪些外部信息）、Write（写哪些记忆）、Compress（如何压缩长对话）、Isolate（多 Agent 窗口隔离）
- **RAG vs Long Context vs Fine-tuning 选型**：先试 RAG（成本最低）→ RAG 不够再考虑 Long Context → 两者都不行再考虑 Fine-tuning
- **RAG 三条进阶主线 (2025-2026)**：KG+Memory 融合（HippoRAG 2 / A-MEM）、Multimodal RAG（ColPali）、Agentic RAG（Self-RAG / CRAG）
- **Memory 四层（CoALA 框架）**：Working Memory（当前任务上下文）、Episodic Memory（过去经验）、Semantic Memory（抽象事实）、Procedural Memory（技能与执行规则）
- **Memory 三种设计模式**：Pattern 1 Naive Buffer（全塞 Context）、Pattern 2 Summary + Recent（摘要远的+保留近的）、Pattern 3 Vector Store + Retrieval（外部 Store + 语义搜索）
- **RAG 最常踩的 3 个坑**：Chunk 太大/太小、Embedding model 选错（中文文档用英文模型）、top-k 设太大/太小
- **Reflexion 完整版需要持久 Memory**：跨 trial 累积教训（Episodic Memory），与 Self-Refine 的单 session 循环本质不同
- **Path 1 vs Path 2 Reasoning**：Prompt-based reflection（ToT / CoVe / Self-Consistency）vs Trained-in reasoning（o1 / R1 / Opus 4.8 / GPT-5.5），两条路径将长期共存
- **RAG Eval 三核心指标**：Retrieval Recall@K（是否检索到 Ground Truth）、Answer Faithfulness（是否基于检索结果生成）、Answer Relevance（是否答非所问）

## 关联连接

- [[Context_Engineering]] — 三层工程堆栈的中间层，本资料是其核心内容展开
- [[RAG]] — 本资料的核心话题之一，RAG 基础流水线与进阶技巧全览
- [[Memory_Agent]] — 本资料的核心话题之二，Agent Memory 系统设计与架构模式
- [[Chunking]] — RAG 与 Memory 都会用到的关键技术——文档分块策略
- [[Reflexion]] — 持久 Episodic Memory 的 Reflexion 完整版，本资料的进阶章节
- [[DSPy]] — Programming-not-Prompting 范式，Path 3 自动优化框架
- [[Agent_Loop]] — Stage 3 的 ReAct 循环是 Agent 底层机制，Memory 在其中持久化状态
- [[Prompt_Engineering]] — 三层堆栈的底层基础
- [[Harness_Engineering]] — 三层堆栈的最外层，Stage 7 将在本资料基础上扩展
- [[Multi_Agent_System]] — Stage 7 Multi-agent 中每个 Agent 都有"自己的 Memory"+"Shared Memory"
- [[Claude_Code_Memory_System]] — Claude Code 的三层持久记忆机制，与本资料的 Memory 模式对应
- [[摘要-awesome-agentic-ai-zh-foundations]] — 本路线图 Stage 0
- [[摘要-awesome-agentic-ai-zh-llm-basics]] — 本路线图 Stage 1
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 本路线图 Stage 2
- [[摘要-awesome-agentic-ai-zh-tool-use]] — 本路线图 Stage 3
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本路线图 Stage 4
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 本路线图 Stage 5
