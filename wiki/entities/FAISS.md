---
title: "FAISS"
type: entity
tags: [向量索引, 向量检索, Meta, 近似最近邻, 工具]
sources: [raw/01-articles/向量数据库与向量索引库-课程笔记.md]
last_updated: 2026-11-04
---

# FAISS

## 定义

FAISS（Facebook AI Similarity Search）是 Meta 开源的**高性能向量相似度搜索库**。它的核心职责只有一个：在海量向量中快速找到与查询向量最相近的 top-k 结果。

> 定位：[[Vector_Index|向量索引库]]，不是[[Vector_Database|向量数据库]]。索引里只有向量，没有原文和元数据。

## 关键信息

| 维度 | 说明 |
|------|------|
| **开发者** | Meta（Facebook AI Research） |
| **核心优势** | 向量搜索性能强、速度快，可承载海量向量 |
| **索引持久化** | 可将索引写入本地文件，之后加载回来 |
| **存储内容** | **只有向量**；原文、标题、元数据不在索引内 |
| **关键词检索** | ❌ 没有 BM25 |
| **条件过滤** | ❌ 没有 `where` 过滤 |
| **查询语法** | ❌ 没有数据库查询语言 |
| **内置向量化** | ❌ 需自己调用 [[Cohere]]/OpenAI 等生成向量 |
| **常见索引类型** | Flat / IVF / PQ / HNSW 等（按精度、内存、速度取舍） |
| **适用规模** | 百万级到海量向量 |

## 使用方式与元数据映射

```python
# 1. 自己生成向量（FAISS 不负责 embedding）
vectors = embed(texts)          # 调用 Cohere/OpenAI

# 2. 建立索引
index = faiss.IndexFlatL2(dim)
index.add(vectors)

# 3. 自己维护与下标对齐的元数据
meta = [{"text": t, "lang": lang} for t, lang in zip(texts, langs)]

# 4. 检索后手动回查
distances, ids = index.search(query_vector, k)
results = [meta[i] for i in ids[0]]
```

**核心成本**：索引与原文的对齐、过滤、持久化后的元数据恢复，全部由应用层自己负责。

## 持久化

来源笔记写作 `index.save()`；FAISS 官方 API 实际为：

```python
faiss.write_index(index, "index.faiss")
index = faiss.read_index("index.faiss")
```

原文、元数据仍需另行用 JSON/DataFrame/数据库保存，并保证与索引下标一致。

## 适用场景

- 百万级向量、追求检索速度
- 已有自己的原文存储与业务过滤逻辑
- 只需要「向量相似度」这一种检索能力
- 接受自行维护元数据映射

## 不适用场景

- 需要 BM25 + 向量混合检索
- 需要按语言/时间/标签过滤
- 需要长期保存完整数据（原文 + 元数据）
- 不想自己维护下标对齐

以上场景应使用[[Vector_Database|向量数据库]]。

## 关联连接

- [[Vector_Index]] — FAISS 所属的产品类别
- [[Vector_Database]] — 完整数据库对照
- [[Annoy]] — 另一款轻量级向量索引库
- [[近似最近邻检索]] — FAISS 各类索引所属的 ANN 范式
- [[Weaviate]] — 完整向量数据库代表
- [[Cohere]] — 提供向量化的上游服务
- [[RAG]] — FAISS 常作为 RAG 的检索内核
- [[摘要-向量数据库与向量索引库]] — 本实体的来源
