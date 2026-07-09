---
title: "摘要-ollama-experiment-index"
type: source
tags: [来源, ollama, llm, 实验, 系列索引]
sources: [raw/01-articles/Ollama LLM 实验系列索引.md]
last_updated: 2026-07-09
---

## 核心摘要

Ollama LLM 实验系列的总索引文档，汇总了 7 个本地 + 云端 LLM 实验的完整结论。涵盖中英文 Token 差异、温度参数扫描与选择指南、确定性验证、Token 波动分析、跨平台成本对比、Tokenizer 效率差异以及多模型回答风格对比。实验基于 llama3.2:3b、qwen3.5:0.8b、DeepSeek V4 Pro/Flash 和豆包 Seed Character 四个模型。关键发现：云端 API 比本地快 2~14 倍且成本极低；Fine-tuning 决定模型"性格"（0.8B 回复可达 3B 的 6.5 倍长）。

## 关联连接
- [[Ollama]] — 本地模型运行工具
- [[Llama]] — 实验用模型（llama3.2:3b）
- [[Qwen]] — 实验用模型（qwen3.5:0.8b）
- [[DeepSeek]] — 云端 API 模型提供商
- [[Doubao]] — 字节跳动云端 LLM 产品
- [[BPE_Tokenizer]] — Token 差异的底层编码机制
- [[Temperature_Parameter]] — 温度参数的核心实验数据来源
- [[Model_Fine_Tuning]] — 模型性格差异的根因
