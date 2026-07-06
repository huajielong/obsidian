---
title: "Self-Attention (自注意力机制)"
type: concept
tags: [深度学习, 注意力机制, Transformer, 神经网络]
sources: 
  - "https://arxiv.org/abs/1706.03762"
  - "https://www.youtube.com/watch?v=kCc8FmEb1nY"
last_updated: 2026-07-06
---

# Self-Attention (自注意力机制)

## 定义

Self-Attention（自注意力机制）是 [[Transformer_Architecture|Transformer]] 架构的核心操作，允许序列中的每个 token 通过加权聚合所有其他 token 的信息来更新自身的表示。它的本质是 **Token 之间的通信机制**——每个 token 通过 Query 向其他 token 问问题，通过 Key 宣告自己有什么信息，通过 Value 提供实际要分享的内容。

## 核心公式

```
Attention(Q, K, V) = softmax(Q × K^T / √d_k) × V
```

其中：
- **Q (Query)**：当前 token 想要查询什么
- **K (Key)**：其他 token 有什么信息可被查询
- **V (Value)**：其他 token 实际提供的值
- **√d_k**：缩放因子，防止内积过大导致 softmax 梯度消失

## 关键特性

### 1. 注意力即通信
Self-Attention 的本质是让序列中的每个 token **看（关注）其他 token**，并根据相关性聚合信息。它允许数据在不同 token 之间流动和交换。

### 2. 注意力没有空间概念
Self-Attention 作用于集合（Set），而不是序列。如果不加位置编码，置换输入顺序会得到完全相同的结果。位置信息需要通过 **Positional Encoding** 额外注入。

### 3. 不同批次之间没有通信
Attention 仅在每个样本内部（每个 batch 维度内）计算，batch 之间彼此独立。

### 4. 三种注意力变体
- **Self-Attention**：Q、K、V 来自同一个序列
- **Cross-Attention**：Q 来自一个序列，K、V 来自另一个序列（如 Encoder-Decoder）
- **Masked Self-Attention**：在自回归模型中，通过掩码防止当前 token 看到未来 token

### 5. 为什么要除以 √d_k
当维度 d_k 很大时，Q × K^T 的内积值也会很大，导致 softmax 进入梯度极小的饱和区。除以 √d_k 可以将方差缩放到 1，维持 softmax 的梯度流动性。

## 实现演化

| 版本 | 方式 | 说明 |
|------|------|------|
| v1 | For 循环平均 | 最简单的上下文聚合，各 token 权重相等 |
| v2 | 矩阵乘法 | 利用矩阵乘并行计算所有加权和 |
| v3 | 加入 Softmax | 根据不同 token 的相关性分配不同的权重 |
| v4 | **完整 Self-Attention** | Query × Key 计算注意力分数 → Softmax → Value 加权求和 |

## 学习资源

- [[摘要-gpt-from-scratch]] — Andrej Karpathy 从直觉到数学完整讲解 Self-Attention（视频 01:02:00 处为核心讲解）

## 关联连接
- [[Transformer_Architecture]] — Self-Attention 是其核心组件
- [[GPT]] — 基于 Masked Self-Attention 的自回归模型
- [[Andrej_Karpathy]] — 其教程对 Self-Attention 有深入浅出的讲解
- [[摘要-gpt-from-scratch]] — 视频中从 v1 到 v4 逐步构建 Self-Attention
