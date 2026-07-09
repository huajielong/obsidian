---
title: "摘要-ollama-tokenizer-personality"
type: source
tags: [来源, ollama, tokenizer, fine-tuning, qwen, llama]
sources: [raw/01-articles/06-Tokenizer差异与模型性格分析.md]
last_updated: 2026-07-09
---

## 核心摘要

实验六：同机对比 llama3.2:3b 与 qwen3.5:0.8b 的分词效率和回复风格。qwen3.5 分词效率高 2.5×（"你好"仅 11 vs 27 Tokens），但回复长度是 llama 的 15×（278 vs 18 tokens），总耗时反而慢 6 倍。核心发现：模型的"性格"由 fine-tuning 决定而非参数规模——0.8B 模型可以比 3B 模型回复长 15 倍。

## 关联连接
- [[Ollama]] — 实验平台
- [[Llama]] — 惜字如金的实验模型
- [[Qwen]] — 话痨风格的实验模型
- [[BPE_Tokenizer]] — Tokenizer 效率差异的底层机制
- [[Model_Fine_Tuning]] — 决定模型"性格"的根因
