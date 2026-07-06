---
title: "Transformer 架构"
type: concept
tags: [深度学习, 神经网络, 注意力机制, NLP, 基础架构]
sources: 
  - "https://arxiv.org/abs/1706.03762"
  - "https://www.youtube.com/watch?v=kCc8FmEb1nY"
last_updated: 2026-07-06
---

# Transformer 架构

## 定义

Transformer 是一种基于 **自注意力机制 (Self-Attention)** 的深度神经网络架构，由 Google 在 2017 年的论文《Attention is All You Need》中提出。它完全摒弃了传统的循环 (RNN) 和卷积 (CNN) 结构，仅依靠注意力机制来处理序列数据，具有并行计算能力强、长程依赖建模好的优势。

## 核心创新

1. **Scaled Dot-Product Attention (缩放点积注意力)**
   - Query、Key、Value 三个矩阵
   - 注意力分数 = softmax(Q × K^T / √d_k)
   - 除以 √d_k 防止 softmax 进入梯度饱和区

2. **Multi-Head Attention (多头注意力)**
   - 将 Q、K、V 投影到多个子空间分别计算注意力
   - 拼接后线性变换得到最终输出
   - 每个 head 可以关注序列中不同的关系模式

3. **Positional Encoding (位置编码)**
   - 由于注意力机制本身没有位置概念（对集合操作）
   - 使用正弦/余弦函数或可学习嵌入注入位置信息

4. **架构变体**
   - **Encoder-only** (如 BERT)：双向注意力，适合理解任务
   - **Decoder-only** (如 [[GPT]])：因果掩码自注意力，适合生成任务
   - **Encoder-Decoder** (如 T5)：编码器处理输入、解码器生成输出

## Transformer Block 组成

每个标准的 Transformer Block 包含：

```
输入 → LayerNorm → Self-Attention → 残差连接 → LayerNorm → FFN → 残差连接 → 输出
```

- **Self-Attention 子层**：token 之间的通信（交换信息）
- **Feed-Forward Network (FFN)**：每个 token 位置独立计算（加工信息）
- **残差连接 (Residual Connection)**：梯度直通路径，使深层网络可训练
- **Layer Normalization**：稳定训练过程

## 影响与意义

Transformer 已成为现代 AI 的基石架构，几乎所有主流大语言模型（[[GPT]]、Claude、LLaMA、Gemini 等）以及多模态模型都基于此架构或其变体。它彻底改变了 NLP、计算机视觉、语音处理等多个领域。

## 学习资源

- [[摘要-gpt-from-scratch]] — Andrej Karpathy 从零实现 Transformer 的视频教程
- **原始论文**: https://arxiv.org/abs/1706.03762

## 关联连接
- [[Self_Attention]] — Transformer 最核心的机制
- [[GPT]] — Decoder-only 的 Transformer 变体
- [[Andrej_Karpathy]] — Transformer 教育的核心推广者
- [[摘要-gpt-from-scratch]] — 视频教程摘要
