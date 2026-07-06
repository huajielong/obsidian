---
title: "摘要-Let's build GPT: from scratch, in code, spelled out."
type: source
tags: [GPT, Transformer, Self-Attention, PyTorch, 深度学习, 视频课程]
sources: 
  - "https://www.youtube.com/watch?v=kCc8FmEb1nY"
last_updated: 2026-07-06
---

# Let's build GPT: from scratch, in code, spelled out.

**基本信息**

| 字段 | 内容 |
|------|------|
| **标题** | Let's build GPT: from scratch, in code, spelled out. |
| **讲师** | [[Andrej_Karpathy]] |
| **系列** | Zero to Hero |
| **上传日期** | 2023-01-17 |
| **时长** | 1小时56分20秒 |
| **播放链接** | https://www.youtube.com/watch?v=kCc8FmEb1nY |
| **观看次数** | 746万+ |
| **点赞数** | 16.2万+ |

## 核心主旨

本视频从零开始用 PyTorch 构建了一个生成式预训练 Transformer（GPT），遵循论文《Attention is All You Need》以及 OpenAI 的 GPT-2 / GPT-3。视频逐步讲解了 Tokenization、Bigram 语言模型、Self-Attention 机制、多头注意力、残差连接、LayerNorm 等 Transformer 核心组件，并讨论了与 [[GPT|ChatGPT]]、[[Transformer_Architecture|GPT-3]] 的联系。

**推荐先修**：观看 Andrej Karpathy 的 makemore 系列视频，熟悉自回归语言建模框架以及 Tensor 和 PyTorch 神经网络基础。

## 章节详解

### 开场与基础 (00:00:00 - 00:38:00)
- **00:00:00** — 开场：ChatGPT, Transformers, nanoGPT, Shakespeare
- **00:07:52** — 读取和探索数据（莎士比亚文本数据集）
- **00:09:28** — Tokenization：字符级分词，训练/验证集划分
- **00:14:27** — 数据加载器：批量生成上下文块
- **00:22:11** — 最简单的基线：Bigram 语言模型（仅基于前一个 token 预测下一个）
- **00:34:53** — 训练 Bigram 模型
- **00:38:00** — 将代码整理成脚本

### 构建 Self-Attention (00:42:13 - 01:16:56)
- **00:42:13** — 版本 1：用 for 循环平均过去上下文（最弱的聚合方式）
- **00:47:11** — Self-Attention 的核心技巧：矩阵乘法作为加权聚合
- **00:51:54** — 版本 2：使用矩阵乘法实现
- **00:54:42** — 版本 3：加入 Softmax 归一化
- **00:58:26** — 代码清理
- **01:00:18** — 位置编码 (Positional Encoding)
- **01:02:00 — 🎯 视频核心：版本 4：Self-Attention**
- **01:11:38** — 笔记 1：注意力机制本质是通信
- **01:12:46** — 笔记 2：注意力没有空间概念，作用于集合
- **01:13:40** — 笔记 3：batch 维度之间没有通信
- **01:14:14** — 笔记 4：Encoder Block vs Decoder Block
- **01:15:39** — 笔记 5：Attention vs Self-Attention vs Cross-Attention
- **01:16:56** — 笔记 6：为什么要除以 sqrt(head_size)——缩放点积注意力

### 构建完整 Transformer (01:19:11 - 01:41:24)
- **01:19:11** — 插入单个 Self-Attention 块到网络
- **01:21:59** — 多头自注意力（Multi-Head Attention）
- **01:24:25** — Transformer 块的前馈网络层（Feed-Forward Network）
- **01:26:48** — 残差连接（Residual Connections）
- **01:32:51** — LayerNorm（与之前 BatchNorm 的关系）
- **01:37:49** — 模型规模放大：添加变量、Dropout

### Transformer 纵览与总结 (01:42:39 - 01:56:20)
- **01:42:39** — Encoder vs Decoder vs 两者兼用
- **01:46:22** — nanoGPT 快速浏览：批量多头自注意力的高效实现
- **01:48:53** — 回到 ChatGPT、GPT-3：预训练 vs 微调、RLHF
- **01:54:32** — 结论

## 关键资源

- **Google Colab 笔记本**: https://colab.research.google.com/drive/1JMLa53HDuA-i7ZBmqV7ZnA3c_fvtXnx-
- **GitHub 仓库**: https://github.com/karpathy/ng-video-lecture
- **nanoGPT**: https://github.com/karpathy/nanoGPT
- **Zero to Hero 播放列表**: https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ
- **论文: Attention is All You Need**: https://arxiv.org/abs/1706.03762
- **GPT-3 论文**: https://arxiv.org/abs/2005.14165

## 建议练习

1. **EX1** — 将 `Head` 和 `MultiHeadAttention` 合并为一个类，把所有 head 当作 batch 维度并行处理（答案在 nanoGPT 中）
2. **EX2** — 在自己的数据集上训练 GPT！尝试训练 GPT 做加法（a+b=c），可能需要从右到左预测
3. **EX3** — 在大数据集上预训练 Transformer，然后在莎士比亚小数据集上微调，观察预训练能否降低验证损失
4. **EX4** — 阅读其他 Transformer 论文，实现一个额外特性，观察能否提升 GPT 性能

## 关键概念提炼

| 概念 | 说明 |
|------|------|
| [[Self_Attention\|Self-Attention]] | Token 之间通过 Q/K/V 进行加权通信的核心机制 |
| [[Transformer_Architecture\|Transformer]] | 由 Self-Attention + FFN + 残差连接 + LayerNorm 组成的深度架构 |
| [[GPT\|GPT]] | Generative Pretrained Transformer — 自回归解码器-only 架构 |
| [[Andrej_Karpathy]] | 本视频讲师，前 Tesla AI 总监、OpenAI 研究科学家 |

## 关联连接
- [[Andrej_Karpathy]] — 讲师与作者
- [[GPT]] — 本视频从头构建的核心模型
- [[Transformer_Architecture]] — GPT 所基于的架构
- [[Self_Attention]] — Transformer 中最关键的机制
- [[Harness_Engineering]] — AI 模型工程化实践
- [[Agentic_Coding]] — AI 编码智能体（视频中用 GitHub Copilot 写 GPT 是 Meta 示例）
