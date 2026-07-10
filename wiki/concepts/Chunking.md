---
title: "Chunking"
type: concept
tags: [chunking, RAG, retrieval, text splitting, embedding]
sources: [raw/01-articles/06-memory-rag.zh-Hans.md]
last_updated: 2026-07-10
---

# Chunking（文档分块）

Chunking 是将文档切分成适合被搜索和处理的语义片段的策略性操作。它不是简单地将文本平均分割——分割方式取决于应用场景和文档内容，决定了 Retriever 所能看到的最细粒度的语义单元。

> 一个好的 Chunk 应同时做到两件事：**足够完整**让模型理解上下文，**足够聚焦**让检索不带过多杂讯。

## 常见分块策略

| 策略 | 做法 | 优点 | 缺点 |
|------|------|------|------|
| **固定长度（Fixed-Length）** | 按字符数或 token 数分割 | 简单稳定 | 死板，容易切断段落/句子/表格 |
| **滑动窗口（Sliding Window）** | 每个 Chunk 之间保留重叠区域（Overlap） | 不易丢失边界信息 | 索引量增大 |
| **递归切割（Recursive）** | 先尝试保留段落，若长度不合适则退而求句子/词语 | 入门 RAG 的良好基准 | — |
| **语义切割（Semantic Chunking）** | 基于 embedding 或语义变化进行分割 | 适合长文档 | 成本和复杂度较高 |
| **混合策略（Hybrid）** | 根据文档结构混合使用多种分割方法 | 灵活适应不同场景 | 配置复杂 |

## 直观判断分块效果

- **回答信息缺失，或有头无尾** → Chunk 太小，或 Overlap 不够
- **回答包含正确信息，但混入无关内容** → Chunk 太大，或 top-k 检索过多

## 首次实现建议

LangChain 文档建议大多数场景从 `RecursiveCharacterTextSplitter` 开始：

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "这是一个很长的文档内容..."
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)
chunks = splitter.split_text(text)
```

先跑出基准版本，再根据后续的 retrieval 结果决定是否更换策略。

## 进阶变体

- **Sentence-Window Retrieval**：Embedding 句子，检索后返回 +/- N 句的窗口
- **Parent-Child / Small-to-Big**：Embedding 小 Chunk，检索时返回父 Chunk
- **Multi-Vector Retrieval**：一个 Chunk，多个 Embedding（摘要 / 原文 / 假设问题）

> Chunk size、overlap、top-k、reranker 之间会相互影响，不要只单独看其中一个参数。

## 关联连接

- [[RAG]] — Chunking 是 RAG 流水线数据预处理阶段的关键步骤
- [[Memory_Agent]] — Pattern 3 Vector Store 依赖 Chunking 策略
- [[Context_Engineering]] — Chunking 影响 Context Window 的信息组装质量
- [[摘要-awesome-agentic-ai-zh-memory-rag]] — 本概念的来源资料
