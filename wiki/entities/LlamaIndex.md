---
title: "LlamaIndex"
type: entity
tags: [LLM框架, RAG, Agent框架, 数据框架, 检索增强生成, 索引]
sources: [raw/01-articles/04-agent-frameworks.md, raw/01-articles/06-memory-rag.zh-Hans.md]
last_updated: 2026-07-16
---

# LlamaIndex — LLM 数据框架

LlamaIndex（原名 GPT Index）是由 **Jerry Liu** 于 2022 年 11 月创建的 **LLM 数据框架**，专注于解决「LLM 如何连接私有数据」这一核心问题。不同于 LangChain 的全栈编排定位，LlamaIndex 深耕**数据接入层（Data Ingestion）→ 索引构建（Indexing）→ 检索（Retrieval）→ 合成（Synthesis）**这一知识路径，是 **RAG 架构的事实标准框架**之一。

截至 2026 年中，LlamaIndex 已从单纯的 RAG 索引库演变为包含 **Workflows（事件驱动编排）**、**llama-deploy（生产运行时）**、**LlamaParse（文档解析）** 等子项目的完整生态系，GitHub 49k+ ★，服务 30 万+ 开发者。

## 发展历程

| 年份 | 里程碑 | 意义 |
|------|--------|------|
| 2022.11 | Jerry Liu 创建 GPT Index（后更名 LlamaIndex） | 首个以「数据索引」为中心的 LLM 框架诞生 |
| 2023 | 引入 Agent 概念与 ReAct Agent | 从纯 RAG 走向 Agent 能力，支持工具调用 |
| 2024 | v0.10 大重构 — 包结构拆分 + PropertyGraphIndex | 模块化架构，废弃 `KnowledgeGraphIndex`；引入 Workflows 预览 |
| 2025 | Workflows 成为推荐编排原语 + llama-deploy 发布 | 事件驱动替代 Query Pipeline 成为生产级首选；分布式运行时正式推出 |
| 2026 | v0.14.x — Workflows 成熟 + OTel 可观测性 + 内置 Eval | Workflows 全面稳定，OpenTelemetry 原生支持，Span 级评估集成 |

## 核心架构

### 1. 数据接入层（Readers / Loaders）

LlamaIndex 拥有框架中最丰富的文档加载器生态（LlamaHub 提供 300+ 连接器）：

```python
from llama_index.readers.file import PDFReader
from llama_index.readers.web import SimpleWebPageReader

# PDF
documents = PDFReader().load_data("report.pdf")

# 网页
documents = SimpleWebPageReader().load_data(["https://example.com"])
```

覆盖格式：PDF、Notion、Confluence、Slack、GitHub、S3、JIRA、SAP、Salesforce、Google Drive 等。

### 2. 文档与节点（Document & Node）

- **Document**：原始内容 + 元数据（文件路径、来源 URL 等）
- **Node**：Document 切分后的最小可检索单元

支持多种分块策略：

| 分块器 | 策略 | 适用场景 |
|--------|------|---------|
| `SimpleNodeParser` | 固定大小 + 重叠 | 通用场景，默认推荐 |
| `SemanticSplitter` | 嵌入相似度断点切割 | 段落边界清晰的内容 |
| `HierarchicalNodeParser` | 递归分块构建层级树 | RAPTOR 阶层式检索 |

### 3. 索引（Indexes）

| 索引类型 | 原理 | 最佳场景 |
|---------|------|---------|
| **VectorStoreIndex** | Embedding → 向量检索 | 语义搜索（最常用） |
| **SummaryIndex** | 顺序遍历所有 Node 汇总 | 小文档全文理解 |
| **PropertyGraphIndex** | 实体关系图谱（v0.10+ 推荐） | 跨文档 Multi-hop 推理 |
| **KeywordTableIndex** | 关键词 → Node 映射 | 字面匹配精确检索 |
| **TreeIndex** | 递归摘要构建层级树 | 长文档层级问答 |

### 4. 检索器（Retrievers）

多路检索一体：

```python
from llama_index.core.retrievers import (
    VectorIndexRetriever,
    BM25Retriever,
)

# 向量检索
vector_retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

# 混合检索（向量 + BM25）
from llama_index.core.retrievers import RouterRetriever
hybrid_retriever = RouterRetriever(
    retriever_list=[vector_retriever, BM25Retriever(...)]
)
```

### 5. 查询引擎（Query Engines）

```python
query_engine = index.as_query_engine(
    response_mode="tree_summarize",  # compact / refine / tree_summarize / accumulate
    streaming=True,
)
response = query_engine.query("你的问题")
```

### 6. Agents（FunctionAgent / ReActAgent）

```python
from llama_index.core.agent import FunctionAgent
from llama_index.core.tools import QueryEngineTool

tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="doc_search",
    description="搜索文档库"
)
agent = FunctionAgent.from_tools([tool], llm=llm, verbose=True)
agent.chat("帮我分析...")
```

### 7. Workflows — 事件驱动编排（2026 主流方式）

Workflows 是 LlamaIndex 在 2025–2026 的主推编排原语，替代了旧的 Query Pipeline：

```python
from llama_index.core.workflow import (
    Workflow, StartEvent, StopEvent, step
)

class MyRAGWorkflow(Workflow):
    @step
    async def retrieve(self, ev: StartEvent) -> RetrievedEvent:
        nodes = self.retriever.retrieve(ev.query)
        return RetrievedEvent(nodes=nodes)

    @step
    async def synthesize(self, ev: RetrievedEvent) -> StopEvent:
        response = self.llm.complete(f"基于：{ev.nodes}\n回答：{ev.query}")
        return StopEvent(result=str(response))

wf = MyRAGWorkflow(retriever=retriever, llm=llm, timeout=120, verbose=True)
result = await wf.run(query="什么是 RAG")
```

关键特性：异步原生、类型化事件传递、并行步骤自动调度、与 llama-deploy 无缝对接。

## LlamaIndex 生态全景

```
LlamaIndex 生态系（2026）：
├── llama-index-core          ← 核心抽象（Document / Node / Index / Retriever / Workflow）
├── llama-index-readers-*     ← 300+ 数据连接器（LlamaHub 注册表）
├── llama-index-vector-stores-* ← 向量数据库集成（Chroma / Qdrant / Pinecone / Weaviate / Milvus）
├── llama-index-embeddings-*  ← 嵌入模型封装（OpenAI / HuggingFace / BGE / Ollama）
├── llama-index-llms-*        ← LLM 模型封装（OpenAI / Anthropic / Ollama / DeepSeek）
├── llama-deploy              ← Workflows 分布式生产运行时
├── LlamaParse                ← 托管文档解析器（复杂布局 / 表格 / 图表）
├── LlamaCloud                ← 托管检索与解析基础设施（企业级）
├── LlamaHub                  ← 社区集成注册表（Loader / Tool / 集成包）
└── traceAI / OpenInference   ← OpenTelemetry 可观测性仪表化
```

## 关键创新与贡献

### 数据接入生态的行业标准
LlamaIndex 的 LlamaHub 提供了 300+ 开箱即用的数据连接器，从 PDF/网页到 Notion/Confluence/Slack/SAP/ Salesforce，覆盖了几乎所有企业数据源。这使得它成为「文档密集型 RAG」场景的默认选择。

### PropertyGraphIndex — 知识图谱 RAG 的简化路径
不同于需要外部图数据库的传统 GraphRAG，LlamaIndex 的 `PropertyGraphIndex` 直接在框架内构建实体关系图，降低了 GraphRAG 的落地门槛，与 [[LightRAG]] 形成互补（LightRAG 更轻量，PropertyGraphIndex 更框架原生）。

### Workflows — RAG 框架中的编排统一
LlamaIndex Workflows 的**事件驱动 + 类型化步骤**模式，让 RAG 流水线从「硬编码链」进化为「可观察、可部署、可并行」的生产级系统。与 [[LangGraph]] 的有状态图编排形成差异化竞争——Workflows 更轻量、与数据层一体化，LangGraph 更通用、适用于跨框架编排。

### llama-deploy — RAG 框架的首个专用生产运行时
LlamaIndex 是第一个为自身编排原语提供**分布式生产运行时**（Control Plane + Message Queue + API Gateway）的 RAG 框架。开发阶段用 Workflows 本地运行，生产环境无需改写代码即可部署到多节点。

## LlamaIndex 与 LangChain 对比

| 维度 | LlamaIndex | LangChain / LangGraph |
|------|-----------|----------------------|
| **核心定位** | 数据知识路径（Ingest → Index → Retrieve → Synthesize） | 全栈 LLM 编排（Model → Tools → Memory → Agent） |
| **最强项** | 300+ 数据连接器、多索引策略、检索优化 | 工具系统、图编排、生态广度 |
| **编排原语** | Workflows（事件驱动） | LangGraph（有状态图） |
| **Agent** | FunctionAgent / ReActAgent（数据查询为主） | create_agent（通用 Agent） |
| **生产运行时** | llama-deploy（原生 RAG 运行时） | LangServe（通用服务化）；LangGraph Platform |
| **可观测性** | traceAI / OpenInference（OTel 原生） | LangSmith（Saas 平台） |
| **GitHub Stars** | ~49k | ~105k |
| **最佳场景** | 文档密集型 RAG、多源数据检索 | 多 Agent 状态机、跨框架编排 |

**互补关系**：两者在实际生产中可以共存——LlamaIndex 负责数据接入与检索，LangGraph 负责 Agent 编排与状态管理。

## 2026 典型应用场景

| 场景 | 实现方式 |
|------|----------|
| **企业知识库问答** | LlamaIndex Reader 接入文档 → Index → Agent + Workflows 编排 |
| **多 PDF 对比分析** | LlamaParse 解析 + PropertyGraphIndex 跨文档实体关联 |
| **RAG 结合搜索** | Hybrid Retriever（向量 + BM25）+ Reranker → Query Engine |
| **自动化报告生成** | Workflows：Retrieve → Synthesize → Format → Review |
| **多模态文档检索** | LlamaParse 提取图表数据 → Multimodal LLM 问答 |
| **生产级 RAG 微服务** | Workflows + llama-deploy 分布式部署 |

## 基本信息

- **创建者**: Jerry Liu
- **维护方**: LlamaIndex Inc.
- **License**: MIT
- **语言**: Python（主） + TypeScript
- **GitHub**: https://github.com/run-llama/llama_index
- **官方网站**: https://llamaindex.ai
- **当前版本**: v0.14.x（2026）
- **LlamaParse**: https://cloud.llamaindex.ai

## 关联连接

- [[LangChain]] — LlamaIndex 在 LLM 应用框架中的主要对比对象，定位互补（数据路径 vs 全栈编排）
- [[LangGraph]] — LlamaIndex Workflows 对标的有状态图编排框架
- [[RAG]] — LlamaIndex 的核心应用领域，RAG 页面大量引用 LlamaIndex 作为推荐工具
- [[LightRAG]] — 轻量级 Graph RAG 框架，与 PropertyGraphIndex 互补
- [[ragas]] — RAG 评估框架，与 LlamaIndex 内置 Eval 互补
- [[Chunking]] — LlamaIndex 的 `SimpleNodeParser` / `SemanticSplitter` 是 Chunking 的重要实现
- [[Agent_Orchestration_Patterns]] — LlamaIndex tool router 作为 Dynamic tool selection 的代表实现
- [[Agent_Loop]] — LlamaIndex 的 ReActAgent 与 FunctionAgent 是 Agent Loop 的实现
- [[Memory_Agent]] — LlamaIndex 提供 4 种内置对话记忆类型
- [[Harness_Engineering]] — LlamaIndex 是 Harness Engineering 在数据接入与检索层的关键工具实例
- [[Context_Engineering]] — LlamaIndex 定位在 Context Engineering 的 Select/Retrieve 阶段
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — Agent 框架全览来源（提及 LlamaIndex）
- [[摘要-awesome-agentic-ai-zh-memory-rag]] — RAG 与 Memory 深度来源（提及 LlamaIndex as RAG 工具）
- [[摘要-算法应用开发工程师-jd]] — JD 中将 LlamaIndex 列为 Agent 框架技术要求之一
