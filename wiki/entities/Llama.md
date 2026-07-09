---
title: "Llama"
type: entity
tags: [模型, Meta, 开源, LLM]
sources: [raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md]
last_updated: 2026-07-08
---

## 定义

Llama（Large Language Model Meta AI）是 Meta 推出的开源大语言模型系列。Llama 3.2 是其中的一个重要版本，在 Ollama 生态中被广泛使用，以其良好的 API 兼容性和稳定的性能著称。

## 关键信息

- **开发者**：Meta
- **Ollama 兼容性**：llama3.2:3b 在原生 API 和 OpenAI 兼容 API 下均可正常工作，无已知兼容问题
- **模型大小**：llama3.2:3b 约 2.0 GB
- **CPU 推理速度**：约 8.8 token/s（参数越多，速度越慢）
- **集成显卡**：被 Ollama 自动跳过，CPU 推理

## 关联连接
- [[Ollama]] — 运行 Llama 模型的主要本地推理工具
- [[Qwen]] — 同为 Ollama 生态的另一模型系列（部分版本存在兼容性问题）
- [[OpenAI_Compatible_API]] — Llama 在此接口下表现稳定
