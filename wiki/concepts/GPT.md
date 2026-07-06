---
title: "GPT (Generative Pretrained Transformer)"
type: concept
tags: [语言模型, Transformer, Self-Attention, OpenAI]
sources: 
  - "https://www.youtube.com/watch?v=kCc8FmEb1nY"
last_updated: 2026-07-06
---

# GPT (Generative Pretrained Transformer)

## 定义

GPT（Generative Pretrained Transformer）是 OpenAI 提出的一系列自回归语言模型，采用 **Decoder-only** 的 [[Transformer_Architecture|Transformer]] 架构。核心思想是通过海量文本数据的预训练（Pretraining），让模型学习语言的统计规律，然后通过微调（Finetuning）适配特定任务。

## 核心架构

GPT 是 Decoder-only Transformer，其核心组件包括：

1. **Tokenization** — 将文本切分为子词单元（如 BPE 编码）
2. **Token Embedding + Positional Encoding** — 将离散 token 映射为连续向量并加入位置信息
3. **Masked Self-Attention** — 因果注意力掩码确保每个 token 只能关注其左侧的上下文
4. **Feed-Forward Network (FFN)** — 每个 token 独立的位置级前馈变换
5. **残差连接 (Residual Connections)** — 跨层梯度直通路径，防止梯度消失
6. **Layer Normalization** — 层归一化稳定训练

## 发展历程

| 版本 | 发布时间 | 参数量 | 关键特性 |
|------|----------|--------|----------|
| GPT-1 | 2018 | 1.17亿 | 首次证明 Transformer Decoder 可以用于语言建模 |
| GPT-2 | 2019 | 15亿 | 规模扩大，展示了零样本迁移能力 |
| GPT-3 | 2020 | 1750亿 | 规模进一步扩大，展示了强大的少样本学习能力 |
| GPT-3.5 / ChatGPT | 2022 | — | 引入 RLHF（基于人类反馈的强化学习）微调 |
| GPT-4 | 2023 | — | 多模态能力，更强推理 |

## 与 Encoder-Decoder Transformer 的区别

- **GPT (Decoder-only)**：每个 token 只关注左侧上下文（因果掩码），适用于文本生成
- **BERT (Encoder-only)**：每个 token 关注双向上下文，适用于理解任务
- **T5 (Encoder-Decoder)**：编码器处理输入，解码器自回归生成，适用于序列到序列任务

## 学习资源

- [[摘要-gpt-from-scratch]] — Andrej Karpathy 从零实现 GPT 的视频教程
- [[Andrej_Karpathy]] — GPT 教育的核心推广者
- **nanoGPT**: https://github.com/karpathy/nanoGPT — 最简化的 GPT 实现

## 关联连接
- [[Transformer_Architecture]] — GPT 所基于的架构
- [[Self_Attention]] — 核心机制之一
- [[Andrej_Karpathy]] — GPT 教育者
- [[摘要-gpt-from-scratch]] — 深入讲解 GPT 从零实现的视频摘要
- [[Harness_Engineering]] — AI 模型工程化实践
- [[Codex]] — OpenAI 基于 GPT 的编码智能体
