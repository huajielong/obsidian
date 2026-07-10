---
title: "LightRAG"
type: concept
tags: [RAG, 检索, Graph, 框架]
sources: []
last_updated: 2026-07-10
---

## 定义

LightRAG 是一个**轻量级 Graph RAG 检索框架**，通过构建文档实体之间的关系图来增强跨文档推理与检索质量。由 HkuMarshall 团队开发，★ 35.1k。

## 关键信息

- **定位**: 轻量级图增强检索（Graph RAG）
- **适用场景**: Multi-hop reasoning、跨文档实体引用（财报、论文、法律案例）
- **不适用场景**: 文档之间无实体关系（FAQ、独立产品手册）、小规模知识库
- **同类框架**: Microsoft GraphRAG、nano-graphrag
- **优势**: 相比 Microsoft GraphRAG 更轻量，部署成本更低

## 关联连接

- [[RAG]] — RAG 架构的进阶分支（GraphRAG）
- [[Chunking]] — 文档分块是 RAG 的基础步骤
- [[DSPy]] — 同为 RAG 进阶优化框架
