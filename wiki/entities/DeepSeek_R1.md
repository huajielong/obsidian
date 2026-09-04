---
title: "DeepSeek-R1"
type: entity
tags: [模型, DeepSeek, 推理, reasoning, RL, 强化学习, 蒸馏]
sources:
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

## 定义

DeepSeek-R1 是深度求索（[[DeepSeek]]）推出的**推理增强（reasoning）模型系列**，主打"深度思考"能力：回答前先产生一段很长的思考过程再给出答案。它是 **DeepSeek-R1-Zero 纯强化学习路线 + 人类可读性修正**的最终产物，也是 2025 年初引爆"推理模型"话题的代表模型（其训练流程常被简化误传为"只用 RL"，实际上四大打造推理模型的方法全部用上）。

## 模型家族

| 模型 | 训练方式 | 特点 |
|------|---------|------|
| **DeepSeek-R1-Zero** | 纯 RL（DeepSeek-V3-Base + 正确率 reward + Format reward） | 能力逼近 o1、自发涌现 Aha moment，但**推理过程难读、多语言混杂**，几乎不可用，从未上线 |
| **DeepSeek-R1** | 复杂流水线（见下） | 正式上线模型（`deepseek-reasoner`），推理过程人类可读 |

## 关键信息

### R1-Zero 的实验发现

- **Reward 设计**：正确率 reward（答对/错）+ **Format reward**（要求输出 `think` token）——这正是 RL 之后模型会产出 think token 的原因。
- **AIME（数学竞赛难题）表现**：单次作答逼近 o1；对每题采样 16 个答案做 majority vote 后，与 o1 做 majority vote 一样好，且优于不做 majority vote 的 o1。
- **Aha moment（顿悟时刻）**：RL 过程中模型自发学会"发现问题、推翻重来"（如自己说出"等等，这里可能有错，我要重新想"），作者强调非人为教导。但有论文检验发现：**DeepSeek-V3-Base 在做 RL 之前本来就会"啊哈"**（会自我质疑、会检查错误），RL 只是强化了已有能力。

### R1 的真实训练流水线（技术报告还原）

```
DeepSeek-V3-Base
 ① RL（正确率 + Format reward）            → R1-Zero
 ② R1-Zero 生成推理数据 + 少量人工筛选/改写
   （另用 Few-shot CoT / Supervised CoT 生成带 reflection/verification 的数据）
   + Imitation Learning 重训 V3            → 模型 A（未命名）
 ③ RL（正确率 reward + 语言一致性 reward）  → 模型 B
 ④ 模型 B 自动生成 60 万条推理数据 + V3 生成 20 万条 SFT 数据（防遗忘）
   （用 V3 当 verifier 判断无标准答案问题的好坏；规则过滤多语言/过长/含代码）
   + Imitation Learning 重训 V3            → 模型 C
 ⑤ RL 强化 safety 与 helpfulness            → DeepSeek-R1
```

- 技术报告对"人工介入量"写得非常隐晦，只提"耗费大量人力修改 R1-Zero 输出"。
- 前三个阶段（CoT / 工作流 / 模仿学习）在 R1 打造过程中**全部用上**，"R1 就是 RL 做的"是農場文的过度简化。
- DeepSeek 曾尝试 **Process Verifier 与 MCTS**，但最终没有做起来、未取得好结果。
- 由于主要靠 RL、人工介入少，R1 的推理过程有时会出现奇怪内容（如拼错 strawberry 让它有 4 个 R、只有左括号没有右括号），因为训练时并不在意推理过程的文字质量。

### RL 只强化已有能力（对中小模型的启示）

- 直接对 Qwen2.5-32B-Base 做 R1-Zero 式 RL，提升有限（≈ QWQ-32B）；RL 能大幅强化 DeepSeek-V3（500B+ 巨模型）。
- 原因：**RL 的前提是模型能自己产生正确答案**——RL 强化已有能力，无法无中生有。
- 结论：对中小模型，**Knowledge Distillation（蒸馏）比 RL 更有效**——Qwen-32B 直接向 R1 学习可大幅增强数学/编程能力（R1 论文展示蒸馏 Qwen、Llama 8B/70B 后能力可媲美强模型）。

## 关联连接

- [[DeepSeek]] — 所属公司实体（公司/API/团队）
- [[Reasoning]] — 深度思考概念
- [[Reinforcement_Learning]] — R1 主打的方法（结果导向 RL）
- [[Imitation_Learning]] — R1 流水线中的重要环节
- [[Knowledge_Distillation]] — 蒸馏 R1 给中小模型
- [[Self_Consistency]] — R1-Zero 的推理时增强（majority vote）
- [[Process_Verifier]] — DeepSeek 尝试过但未做起来的方法
- [[Test_Time_Compute]] — R1 深度思考的理论框架
- [[Chain_of_Thought]] — 方法一：CoT（R1 也使用）
- [[Qwen]] — RL 效果有限、蒸馏更有效的对照模型
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — 本实体主要来源
