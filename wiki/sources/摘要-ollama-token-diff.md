---
title: "摘要-ollama-token-diff"
type: source
tags: [来源, ollama, token, 中英文差异, BPE]
sources: [raw/01-articles/01-中英文Token差异分析.md]
last_updated: 2026-07-09
---

## 核心摘要

实验一：对比 llama3.2:3b 对中英文相同语义的分词差异。实验表明中文每个字约消耗 3~4 Token（因需以 UTF-8 字节序列编码），而英文每个词约 1 Token（天然在 BPE 词表中）。这意味着模型宣称的上下文窗口对中文的实际承载能力仅为英文的 1/3~1/4。

## 关联连接
- [[Ollama]] — 实验平台
- [[Llama]] — 实验模型
- [[BPE_Tokenizer]] — Token 差异的底层算法机制
