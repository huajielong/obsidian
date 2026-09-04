---
title: "Reasoning 推理"
type: concept
tags: [推理, reasoning, 深度思考, 测试时计算, test-time, 思维链]
sources:
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

# Reasoning（推理 / 深度思考）

## 定义

Reasoning（推理，中文语境中也称**深度思考**）指大型语言模型在给出最终答案前，**先产生一段很长的思考过程**的行为。这段思考通常包裹在 `think`/`/think` 标记中（加标记主要为了界面呈现方便——界面可选择是否展示内部思考）。拥有该行为的模型称为 **推理模型（reasoning model）**，代表：ChatGPT o 系列、DeepSeek R 系列、Gemini Flash Thinking、Claude 3.7 Sonnet Extended Thinking。

## 与 Inference 的辨析

| 词 | 中文 | 含义 |
|----|------|------|
| **Inference** | 推论 | 使用模型（让模型产生答案）的动作本身 |
| **Reasoning** | 推理 | 模型在产生答案时输出特别长的思考过程这一行为 |

- 称其为"推理"**不代表模型的行为与人类推理相同**——只是借用这个词描述可观察的行为。

## 深度思考过程中的典型行为

- **验证**：检查刚才得出的答案是否正确（"Let me check the answer"）。
- **探索**：尝试思考其他可能性。
- **规划**：规划解这道题需要哪些步骤。
- 深度思考的模型往往**解到一半就开始验证中间步骤**，避免"一步错、步步错"（如 DeepSeek 算 123×456 时先验算 123×4=492 再继续）。

## 理论框架：Test-Time Compute

Reasoning 是 **[[Test_Time_Compute|测试时计算]]** 的一种——在测试阶段投入更大算力换取更好结果，即"深度不够、长度来凑"；对应的 **Test-Time Scaling** 指"思考越多往往结果越好"。此概念最早可见于 AlphaGo（测试时用 MCTS 做巨额运算）。

## 如何打造推理模型：四大方法

| # | 方法 | 是否需要微调 | 适用模型 | 关键概念 |
|---|------|:---:|---------|---------|
| 1 | 更强的思维链（Better CoT） | 否 | 强模型 | [[Chain_of_Thought]]（Few-shot / Zero-shot / Supervised CoT） |
| 2 | 提供推理工作流程 | 否 | 弱模型也能用 | 大规模采样 + [[Self_Consistency]] / [[Process_Verifier]] + Beam Search / MCTS |
| 3 | 教导推理过程（Imitation Learning） | 是 | 后训练 | [[Imitation_Learning]]、[[Knowledge_Distillation]]、Journey Learning |
| 4 | 以结果为导向学习推理（RL） | 是 | 强基座 | [[Reinforcement_Learning]]、R1-Zero、Aha moment |

- **四大方法不互斥**，可自由组合（如 DeepSeek-R1 全部用上；RL 训练后可再叠加推理时 majority vote）。

## 已知问题与挑战

- **无谓推理**：模型常做不必要的冗长思考，浪费算力（如算 123×456 反复验算多遍）。如何让模型"该想时才想"是核心挑战。
- **[[Over_Thinking|过度思考]]**：作为 Agent 时的失效模式——想得太多、做得太少。
- 纯 RL 训练的推理模型（R1-Zero）推理过程**难读、多语言混杂**，需要模仿学习/人工改写修正。

## 关联连接

- [[Test_Time_Compute]] — 深度思考的理论框架
- [[Chain_of_Thought]] — 方法一：更强的思维链
- [[Self_Consistency]] — 方法二：多数投票选出正确答案
- [[Process_Verifier]] — 方法二：逐步验证的中间步骤验证器
- [[Imitation_Learning]] — 方法三：教导模型推理过程
- [[Knowledge_Distillation]] — 方法三的捷径：向强推理模型学习
- [[Reinforcement_Learning]] — 方法四：以结果为导向的 RL
- [[DeepSeek_R1]] — 推理模型代表实体
- [[Over_Thinking]] — 推理模型的过度思考失效模式
- [[Model_Based_Planning]] — 推理模型作为 Agent 的"脑内小剧场"规划
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — 来源
