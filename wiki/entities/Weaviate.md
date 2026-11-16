---
title: "Weaviate"
type: entity
tags: [向量数据库, Vector DB, RAG, 混合检索, 工具]
sources: [raw/01-articles/向量数据库与向量索引库-课程笔记.md]
last_updated: 2026-11-04
---

# Weaviate

## 定义

Weaviate 是一个开源的**向量数据库**：它把向量、原始文本、标题和业务元数据存放在同一条对象中，并同时提供 Dense 向量检索、BM25 关键词检索、Hybrid 混合检索、条件过滤、分页与持久化能力。

> 一句话定位：Weaviate = 数据库（向量 + 原文 + 检索 + 过滤），而不是单纯的向量索引库。

## 关键信息

| 能力 | 说明 |
|------|------|
| **向量存储** | 保存 embedding 并构建 ANN 索引 |
| **原文与元数据** | 同一条数据可放 `text, title, url, lang, views` 等字段 |
| **Dense 检索** | 基于向量相似度的语义检索 |
| **BM25** | 内置关键词/字面检索 |
| **Hybrid** | Dense + BM25 混合检索 |
| **过滤 / 分页** | 支持 `where lang = "en"` 一类条件与分页 |
| **持久化** | 服务重启后数据仍在 |
| **Embedding 集成** | 可内置对接 [[Cohere]] 等 embedding 模型，提供 RAG 能力 |
| **多集合 / 权限 / 集群** | 支持多 collection、RBAC、副本与集群部署 |
| **部署形态** | 独立服务进程；Colab 中的 embedded Weaviate 也是在后台启动一个服务 |

## 典型使用方式

```python
# 伪代码：一条对象同时携带原文、元数据与向量
client.collections.create("Article")
articles.data.insert({
    "text": "文章正文...",
    "title": "标题",
    "url": "https://...",
    "lang": "en",
})

# 检索时直接带过滤条件
client.collections.get("Article").query.near_vector(
    near_vector=query_vector,
    filters=Filter.by_property("lang").equal("en"),
    limit=10,
)
```

## 优点与限制

**优点**

- 一个系统同时解决「存原文 + 存元数据 + 向量检索 + 关键词检索 + 过滤」
- 适合长期保存的 RAG 知识库，重启不丢数据
- 内置 embedding 对接与 Hybrid 检索，减少自建元数据层的工作量
- 支持多集合、权限与集群，可走向生产

**限制**

- **重**：是一个独立服务进程，部署与运维成本高于纯 Python 库
- 需要理解 collection/schema/filter 等数据库概念
- 小数据集、只做相似度实验时属于过度设计

## 适用场景

- 生产级 RAG 项目
- 需要同时做关键词 + 向量检索（Hybrid Search）
- 需要按 `lang`、`url`、时间等字段过滤
- 需要长期保存数据、重启不丢
- 不想自己维护「向量下标 ↔ 原文/元数据」映射

## 使用注意

来源笔记称 Weaviate 支持「事务」。严格说，Weaviate 并不是传统关系数据库那种跨对象 ACID 事务系统；它的数据一致性主要体现在单对象/批量写入、副本与多租户隔离层面。选型时若事务是关键需求，应按具体版本与部署模式核实，不要直接按「完整 ACID 数据库」预期使用。

## 关联连接

- [[Vector_Database]] — Weaviate 所属的产品类别
- [[Vector_Index]] — Weaviate 与 FAISS/Annoy 的本质分界
- [[FAISS]] — 只做向量检索的索引库对照
- [[Annoy]] — 轻量级索引库对照
- [[Cohere]] — 可对接的 embedding 提供方
- [[RAG]] — Weaviate 最主要的应用场景
- [[Dify]] — 支持将 Weaviate 作为 Vector DB 后端
- [[LlamaIndex]] — 提供 Weaviate 向量存储集成
- [[摘要-向量数据库与向量索引库]] — 本实体的来源
