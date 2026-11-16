---
title: "Cohere"
type: entity
tags: [Embedding, 向量化, RAG, 企业级AI, 工具]
sources: [raw/01-articles/向量数据库与向量索引库-课程笔记.md]
last_updated: 2026-11-04
---

# Cohere

## 定义

Cohere 是一家提供企业级 NLP/生成式 AI 模型的公司，其 Embed 系列模型负责把文本转换为向量（embedding）。在本知识库的语境中，Cohere 的核心角色是 **文本 → 向量** 的 embedding 提供方，而不是向量数据库或检索系统。

> 关键边界：Cohere 只负责生成向量；向量生成之后，存到哪里、怎么检索，由 [[Vector_Database|向量数据库]] 或 [[Vector_Index|向量索引库]] 决定。

## 关键信息

| 维度 | 说明 |
|------|------|
| **核心职责** | 文本 → 向量（embedding） |
| **代表模型** | Cohere Embed v3（1024 维，最大 512 token，多语言，支持压缩模式） |
| **是否存原文** | ❌ 不存 |
| **是否做检索** | ❌ 不做 |
| **是否做过滤** | ❌ 不做 |
| **与其他组件的关系** | 生成的向量可存入 [[Weaviate]]、[[FAISS]]、[[Annoy]] 等任意后端 |
| **附加能力** | 除 Embedding 外还提供 Rerank / Generate 等模型（本笔记只讨论 Embedding 角色） |

## 典型链路

```
原始文本
   │
   ▼
Cohere Embedding  →  向量
   │
   ├──→ [[Weaviate]]   （向量 + 原文 + 元数据 + 混合检索）
   ├──→ [[FAISS]]      （仅向量，元数据自己维护）
   └──→ [[Annoy]]      （仅向量，元数据自己维护）
```

## 选型提示

- 需要**多语言 embedding**、企业级 API 与压缩向量 → Cohere Embed v3 是可选项
- 需要**中文/多语言综合最强** → 参见 [[RAG]] 中的 BGE-M3 等开源模型对比
- Cohere 不解决存储与检索问题；选完 embedding 模型后仍需单独选向量数据库/索引库

## 关联连接

- [[RAG]] — Cohere Embedding 的主要应用场景
- [[Vector_Database]] — 向量生成后的存储与检索后端
- [[Vector_Index]] — 轻量级向量检索后端
- [[Weaviate]] — 可对接 Cohere embedding 的向量数据库
- [[FAISS]] — 可接收 Cohere 向量的索引库
- [[Annoy]] — 可接收 Cohere 向量的索引库
- [[摘要-向量数据库与向量索引库]] — 本实体的来源
