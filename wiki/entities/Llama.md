---
title: "Llama"
type: entity
tags: [模型, Meta, 开源, LLM]
sources: [raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md, raw/01-articles/awesome-agentic-ai-zh-stage-01-llm-basics.md]
last_updated: 2026-07-10
---

## 定义

Llama（Large Language Model Meta AI）是 Meta 推出的开源大语言模型系列，是自托管（self-host）和本地推理场景的生态最广、最主流的开源 LLM 系列。

## 关键信息

- **开发者**：Meta
- **最新活跃版本**：Llama 3.3 70B（截至 2026-05，Llama 4 尚未释出）
- **许可证**：Llama Community License — 开源但有条款限制（如 ≥ 7 亿 MAU 需单独授权）
- **生态地位**：Ollama 预设模型，self-host 入门首选，fine-tune base 的标准选择
- **模型大小示例**：llama3.2:3b 约 2.0 GB
- **CPU 推理速度**：llama3.2:3b 约 8.8 token/s
- **Ollama 兼容性**：原生 API 和 OpenAI 兼容 API 下均可正常工作，无已知兼容问题

## 关联连接
- [[Ollama]] — 运行 Llama 模型的主要本地推理工具
- [[Qwen]] — 同为 Ollama 生态的另一模型系列（部分版本存在兼容性问题）
- [[OpenAI_Compatible_API]] — Llama 在此接口下表现稳定
