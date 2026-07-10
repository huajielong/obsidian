---
title: "ragas"
type: concept
tags: [RAG, 评估, Evals, 框架]
sources: []
last_updated: 2026-07-10
---

## 定义

ragas（RAG Assessment）是一个**开源的 RAG 评估框架**，提供 8+ 标准化指标来评估检索增强生成系统的各环节质量，包括检索召回率、答案忠实度和答案相关性等核心维度。★ 13.9k。

## 关键信息

### 核心评估指标

| 指标 | 衡量什么 |
|:----|:--------|
| **Retrieval Recall@K** | Top-K 检索结果是否包含 Ground Truth |
| **Answer Faithfulness** | 答案是否基于检索结果（vs 幻觉） |
| **Answer Relevance** | 答案与查询的相关度 |

### 同类工具

- ragas（★ 13.9k，8+ 指标）
- TruLens
- LangSmith

## 关联连接

- [[RAG]] — RAG 系统的评估体系
- [[Eval_Harness]] — RAG 评估是 Eval Harness 的子集
- [[DSPy]] — 同为 RAG 生态的进阶工具
