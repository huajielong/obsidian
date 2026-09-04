---
title: "Auto_Regressive_Generation"
type: concept
tags: [自回归, 生成策略, LLM基础, 文字接龙, 生成式AI]
sources: [raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md]
last_updated: 2026-08-05
---

## 定义

**自回归生成（Auto-Regressive Generation）** 是生成式 AI 最基本的生成策略：给定一串已有的 Token（Z₁…Zₜ₋₁），模型预测（采样）下一个 Token Zₜ，再把 Zₜ 拼回输入，如此循环，直到输出结束符（EOS）。李宏毅在课程中形象地称之为"**文字接龙**"。

## 关键信息

### 运作循环

```
输入 Z₁…Zₜ₋₁ → 模型给出每个候选 Token 的概率分布 → 采样选出 Zₜ
→ 新输入 Z₁…Zₜ₋₁Zₜ → 预测 Zₜ₊₁ → … → 输出 EOS 结束
```

- 每一步的输出都拼回输入，输入不断变长。
- 生成单位**不限于文字**：可以是声音 Token、影像 Token（像素/压缩符号），"万事万物都是 Token"。
- 结束符（EOS / `<|end_of_text|>`）是 Vocabulary 中的一个特殊 Token，模型可在任一步输出它表示接龙结束。

### 为什么"每次答案不同"

每一步都在**按概率分布采样（掷骰子）**而非取最大值，因此同一 Prompt 多次生成结果通常略有差异。若改成每次都取概率最高的 Token（贪婪解码 / Top-K=1），则输出确定。

### 与分类问题的关系

每次"给一串 Token 选择下一个 Token"本质上是一个**分类问题（选择题）**：从 Vocabulary（有限候选）中选一个答案。机器学习早已能解选择题，把生成问题化约为一连串选择题，是生成问题可解的关键。

### 工程上的采样控制

- 完全按概率采样容易中途掷到低概率 Token，导致后续全盘出错（"乱讲话"）。
- 工程做法：只允许**概率排名前 Top-K** 的 Token 参与采样（参见 [[Temperature_Parameter]]）。

### 与其他生成策略的关系

文字接龙（自回归）**不是唯一**的生成策略；**Diffusion Model** 是影像生成领域更常见的另一种策略，二者都属于"如何依序生成 Token/结构"的生成策略范畴。

## 关联连接

- [[Generative_AI]] — 生成式 AI 的定义（复杂有结构物件），自回归是最基本的生成策略
- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — 本概念的来源
- [[Temperature_Parameter]] — 采样与 Top-K 控制
- [[AI_Hallucination]] — 自回归采样的概率尾巴导致幻觉/荒谬输出
- [[Chat_Template]] — 让自回归接龙"回答"用户问题的输入包装
- [[GPT]] — 自回归 Decoder-only 语言模型（GPT 的 G 即 Generative、模型按自回归训练）
- [[Diffusion_Model]] — 另一种生成策略
- [[BPE_Tokenizer]] — Token 的定义与词汇表
- [[Machine_Learning]] — 自回归所需的分类/预测学习范式
