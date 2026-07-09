---
title: "Qwen"
type: entity
tags: [模型, 阿里云, 开源, LLM]
sources: [raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md]
last_updated: 2026-07-08
---

## 定义

Qwen（通义千问）是阿里云推出的开源大语言模型系列，包含从 0.5B 到 72B 不等参数规模的模型。Qwen 系列在 Ollama 生态中广泛使用，但部分版本存在 API 兼容性问题。

## 关键信息

- **开发者**：阿里云（Alibaba Cloud）
- **模型范围**：0.5B ~ 72B 参数
- **Ollama 兼容性**：原生 API 正常，但 qwen3.5:0.8b 在 OpenAI 兼容端口下存在 `content` 字段返回空字符串的 Bug
- **模型大小示例**：qwen3.5:0.8b 约 1.0 GB
- **CPU 推理速度**：qwen3.5:0.8b 在 CPU 上约 18.6 token/s

### 已知兼容问题

qwen3.5:0.8b 在 Ollama 的 OpenAI 兼容 API 下：调用成功、Token 正常消耗、`finish_reason="length"`，但 `content` 字段为空。这是模型与 Ollama 版本间的兼容问题，非代码错误。建议换用 `qwen2.5:3b` 或 `llama3.2:3b`。

## 关联连接
- [[Ollama]] — 运行 Qwen 模型的本地推理工具
- [[Llama]] — 同为 Ollama 生态的另一模型系列
- [[OpenAI_Compatible_API]] — Qwen 在 OpenAI 兼容端口下存在已知 Bug
