---
title: "Model_Fine_Tuning"
type: concept
tags: [微调, fine-tuning, 模型性格, 训练]
sources: [raw/01-articles/06-Tokenizer差异与模型性格分析.md, raw/01-articles/07-多模型回答风格对比.md, raw/01-articles/Ollama LLM 实验系列索引.md]
last_updated: 2026-07-09
---

## 定义

模型微调（Fine-tuning）是指在预训练模型基础上，使用特定任务或风格的数据对模型进行额外训练的过程。Fine-tuning 决定了模型的"性格"——包括回复风格、长度偏好、立场倾向和行为模式，其影响力甚至超过模型本身的参数规模。

## 关键信息

### Fine-tuning 的影响维度

| 维度 | 描述 |
|:---|:------|
| **回复长度** | 训练数据的风格决定模型是"惜字如金"还是"长篇大论" |
| **语言偏好** | 训练数据的中英文比例决定模型混用语言的程度 |
| **输出结构** | 要点列表 vs 段落论述 vs 分析框架 |
| **立场倾向** | 中立客观 vs 先批评再分析 |

### 核心发现：Fine-tuning > 参数规模

> **0.8B 的 qwen3.5 回复长度是 3B 的 llama3.2 的 15 倍**（278 vs 18 tokens）。

这一发现证明：**模型的"性格"由 fine-tuning 决定，而非参数规模**。参数规模影响的是知识广度和推理能力，而行为模式由 fine-tuning 塑造。

### 具体案例

| 维度 | llama3.2:3b（3B） | qwen3.5:0.8b（0.8B） |
|:----|:-----------------|:-------------------|
| **回复风格** | 简洁要点式（475字） | 长篇学术风（1,404字，3×） |
| **语言** | 中英混用（flexible/office） | 纯中文书面语 |
| **立场** | 中立，正反并列表述 | 先批评原观点片面性，再分析 |
| **话痨程度** | 低（18 tokens/简单问候） | 极高（278 tokens/简单问候） |

### llama3.2 中英混用的原因

llama3.2 在中文回复中混入英文词（flexible/office/remote work），而 qwen3.5 是纯中文。这是因为 llama3.2 的预训练数据英文占主导，中文是微调阶段加入的，模型在某些概念上"更习惯"用英文表达。

## 关联连接
- [[摘要-ollama-tokenizer-personality]] — Tokenizer 效率与模型性格实验来源
- [[摘要-ollama-style-comparison]] — 多模型回答风格对比实验来源
- [[Temperature_Parameter]] — 温度在 fine-tuning 确定的基线行为上调节多样性
- [[BPE_Tokenizer]] — Tokenizer 效率影响 Token 消耗，与实际输出风格共同决定总延迟
- [[Ollama]] — 运行经过 fine-tuning 的本地模型
- [[Qwen]] — 中文优化且话痨风格的 fine-tuning 代表
- [[Llama]] — 简洁风格的 fine-tuning 代表
