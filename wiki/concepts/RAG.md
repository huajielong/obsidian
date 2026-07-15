---
title: "RAG"
type: concept
tags: [RAG, retrieval, embedding, vector DB, LLM, 上下文工程]
sources: [raw/01-articles/06-memory-rag.zh-Hans.md]
last_updated: 2026-07-10
---

# RAG（Retrieval-Augmented Generation）

RAG（检索增强生成）是一种将 **外部知识检索** 与 **LLM 生成能力** 相结合的架构模式：在 LLM 生成回答之前，先从外部知识库中检索出与当前查询最相关的文档片段，然后将这些片段拼接进 prompt，让 LLM 基于检索到的信息生成回答。

> 心智模型：RAG = retrieve 相关片段 → 塞进 prompt → 生成

## RAG 基础流水线

最基础的 RAG 分为两条流水线：

### 1. 数据预处理（Ingest — 一次性）
```
Ingest（加载数据）→ Chunk（分块）→ Embed（向量化）→ Store（存入 Vector DB）
```

| 步骤 | 做什么 | 典型工具 |
|------|--------|---------|
| **Ingest** | 加载数据（PDF / Web / DB） | LlamaIndex Loader / docling / MarkItDown |
| **Chunk** | 将文档切分成小块（500-2000 token） | `RecursiveCharacterTextSplitter` |
| **Embed** | 将每个 Chunk 转换为 N 维向量 | `sentence-transformers` / OpenAI ada-002 / BGE-M3 |
| **Store** | 将向量 + 元数据存储进 Vector DB | Chroma / Qdrant / pgvector / Weaviate |

### 2. 检索生成（每次 Query）
```
Query → Embed → Vector Search（top-k）→ 拼接 Prompt → LLM 生成回答
```

## 最常踩的 3 个坑

1. **Chunk 太大/太小**：太大时检索到的 chunk 可能只有一句相关；太小时会失去上下文
2. **Embedding model 选错**：中文文档用英文模型，检索精度直接掉一半 → 看 [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)，中文推荐 BGE-M3
3. **top-k 设太大/太小**：太小漏掉相关 chunk，太大杂讯多 / token 消耗大

## RAG vs Long Context vs Fine-tuning

| 选择 | 适合 | 不适合 | 成本 |
|------|------|--------|------|
| **RAG** | 大型/变化快/私有知识库，需要 citation | 需要跨文档 multi-hop reasoning | 每次 query 多一次 vector search latency |
| **Long Context** | 200k token 以内的中型文档，需要 cross-doc reasoning | 知识库很大 / 经常变化 | 每次 query 烧大量 input token |
| **Fine-tuning** | 风格/格式统一，特定领域语言 | 知识会变化、需要 citation | 训练成本 + 维护成本 + 模型 lock-in |

**选型策略**：先试 RAG（成本最低）→ RAG 不够再考虑 Long Context → 两者都不行再考虑 Fine-tuning。

## 进阶 RAG 技巧

### GraphRAG — 知识图谱 + RAG
Vanilla RAG 不知道 entity 之间的关系。GraphRAG 在 ingest 阶段先用 LLM 将文档抽取成 (entity, relation, entity) 三元组构建知识图谱，检索时除了向量比对，还会进行 graph traversal。

- **适用**：Multi-hop reasoning、跨文档实体引用（财报、论文、法律案例）
- **不适用**：文档之间无实体关系（FAQ、独立产品手册）、小规模知识库
- **代表框架**：[[LightRAG]]（轻量级 ★35.1k）、Microsoft GraphRAG、nano-graphrag

### Contextual Retrieval — Anthropic 的 Prompt Caching 方案
Vanilla chunk 会丢失原始文档上下文。Anthropic 提出用 LLM 为每个 chunk 编写 50-100 token 的**上下文头部**（contextual header），拼接到 chunk 前再进行 embedding。搭配 prompt caching 可将 ingest 成本降低约 90%。

- **适用**：财务报告、研究论文、长篇叙事文档
- **不适用**：Chunk 本身自包含（FAQ、产品介绍页）、知识库频繁变动
- **实现**：[[Anthropic]] Contextual Retrieval Cookbook

### Hybrid Search & Reranking — 性价比最高的 Production 优化
- **Hybrid Search** = Vector 相似度（语义匹配）+ BM25 / keyword 搜索（字面匹配），使用 RRF（Reciprocal Rank Fusion）融合分数
- **Reranking** = 第一阶段检索 top-50（高召回）→ Cross-encoder reranker 重排为 top-5（高精确率）

**效果**：Production RAG 评估几乎一致表明，添加 Hybrid Search + Reranker 后 recall@5 从 ~70% 提升到 85-90%。

### Query Transformations — 检索前改写查询
| 技巧 | 做法 | 适用场景 |
|------|------|---------|
| **HyDE** | LLM 生成"假设答案"，用答案的 embedding 检索 | 查询与文档用词/风格差异大 |
| **Multi-Query** | 将查询改写为 N 个变体，分别检索后合并去重 | 查询过短 / 模糊 / 多义 |
| **RAG Fusion** | Multi-Query + RRF 融合排名 | 同上，需要更稳定的排名 |

### Adaptive / Agentic RAG — 2024 年 RAG 研究主轴
将固定 Pipeline 变成具有判断能力的 Agent Loop——LLM 自己决定是否检索、评估检索质量、调整查询方式。

- **Self-RAG**：输出 `[Retrieve]` token 决定是否检索，`[IsRel]/[IsSup]/[IsUse]` 评分每个片段
- **CRAG（Corrective RAG）**：检索评估器评分，高置信度直接使用，低回退到 web search，中触发查询重写
- **Adaptive RAG**：分类器判断查询复杂性 → 路由到"不检索 / 单步 / 多步"策略

### RAPTOR — 阶层式递归检索
递归聚类和摘要 chunk，构建多层树：底层 = 原始 chunk，中层 = 相关 chunk 的摘要，顶层 = 全文摘要。可检索不同抽象层级。

## 2025-2026 进阶 RAG 三大主线

1. **🧠 KG + Memory 融合** — HippoRAG 2（KG + PageRank，海马体启发）、A-MEM、KAG
2. **🎬 Multimodal RAG** — ColPali（直接对 PDF 图像 embedding 绕过 OCR）、TV-RAG、MegaRAG
3. **🤖 Agentic RAG** — Retrieval 作为 Tool，Agent 自主决定检索次数与方式（Self-RAG / A-RAG）

## RAG / Memory Eval

**没有 Eval 的 Production Agent 基本上就是未经验证。**

| Metric | 衡量什么 | 工具 |
|--------|---------|------|
| **Retrieval Recall@K** | Top-K 是否包含 Ground Truth | ragas / TruLens / LangSmith |
| **Answer Faithfulness** | 答案是否基于检索结果（vs 幻觉） | ragas / TruLens |
| **Answer Relevance** | 答案与查询的相关度 | ragas / LLM-as-judge |

**代表性框架**：[[ragas]]（★13.9k，8+ 指标）、TruLens、LangSmith

## 常用工具推荐

| 场景 | 推荐工具 |
|------|---------|
| 首次运行 RAG（上手最快） | Chroma + LlamaIndex |
| 企业级 RAG 框架 | Haystack |
| Production Scale（百万级文档） | Qdrant + LlamaIndex |
| 已有 Postgres 环境 | pgvector |
| 企业级 RAG + Web UI | RAGFlow |
| 中文 RAG 范例 | Langchain-Chatchat |

## 关联连接

- [[Context_Engineering]] — RAG 是 Context Engineering 的核心 Sub-problem（Select）
- [[Memory_Agent]] — RAG 解决外部知识检索，Memory 解决跨 session 状态保持，两者互补
- [[Chunking]] — RAG 流水线的关键步骤，影响检索质量
- [[Reflexion]] — 持久 Memory 的反思机制，可与 RAG 结合使用
- [[DSPy]] — 自动优化 RAG Prompt + Retriever 设置的 Path 3 范式
- [[Agent_Loop]] — ReAct 循环中 RAG 作为 Tool 被调用
- [[摘要-awesome-agentic-ai-zh-memory-rag]] — 本概念的来源资料
- [[AI搜索工程]] — AI 原生搜索工程，RAG 在搜索引擎尺度的独立展开（多路召回、级联排序、Hybrid Search）
- [[摘要-deepseek-ai-search-jd]] — DeepSeek AI 搜索 JD，RAG 技术在大规模搜索系统中的应用实践
