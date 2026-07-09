---
title: "BPE_Tokenizer"
type: concept
tags: [分词, BPE, tokenizer, 算法, LLM基础]
sources: [raw/01-articles/01-中英文Token差异分析.md, raw/01-articles/06-Tokenizer差异与模型性格分析.md, raw/01-articles/Ollama LLM 实验系列索引.md]
last_updated: 2026-07-09
---

## 定义

BPE（Byte Pair Encoding，字节对编码）是一种子词分词算法，广泛应用于现代 LLM（如 GPT、Llama、Qwen 系列）。它通过统计频率逐步合并最常见的字符/字节对来构建词表。BPE 的核心特点是：**英文单词天然在词表中（约 1 Token/词），而中文需要拆分为 UTF-8 字节序列（约 3~4 Token/字）**。

## 关键信息

### 语言 Token 效率差异

| 语言 | Token/单位 | 原因 |
|:---|:---------:|:-----|
| 英文 | ~1 Token/词 | 常见单词直接存在于 BPE 词表中 |
| 中文 | ~3~4 Token/字 | 需以 UTF-8 字节序列编码，不在基础词表中 |

### 不同模型的 Tokenizer 效率差异

以"你好"为例：

| 模型 | Token 数 | 效率比 |
|:---|:-------:|:-----:|
| qwen3.5:0.8b | **11** | 基准（最高效） |
| llama3.2:3b | **27** | 2.5× 差 |

> Qwen 系列因其中文优化，BPE 词表中包含更多中文词汇，不需要回退到逐字节编码。

### 实际影响

1. **上下文窗口虚标**：模型宣称的 128K 上下文，用中文时实际容纳的内容量仅为英文的 **1/3~1/4**
2. **中英文混合 Prompt 成本更高**：同样的语义内容，中文部分消耗更多 Token
3. **不同模型成本差异**：Tokenizer 效率差异可达 2.5×，同样输入不同模型 Token 消耗不同

## 关联连接
- [[GPT]] — BPE 是 GPT 系列的基础分词算法
- [[Transformer_Architecture]] — Tokenizer 的输出是 Transformer 的输入
- [[本地_LLM_推理]] — Tokenizer 效率直接影响本地推理的 Token 消耗
- [[Temperature_Parameter]] — 温度参数影响输出 Token 数（高温度下波动可达 28×）
