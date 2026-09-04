---
title: "Knowledge_Distillation 知识蒸馏"
type: concept
tags: [知识蒸馏, distillation, 推理, reasoning, 模型压缩, 后训练]
sources:
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

# Knowledge Distillation（知识蒸馏）

## 定义

Knowledge Distillation（知识蒸馏）指**用一个已训练好的强模型（老师）生成数据/输出，训练一个更小的模型（学生）**以继承其能力。在推理模型语境中：拿一个能深度思考的模型当老师，让它先产生推理过程再产生答案，学生模型直接学习这段"推理过程 + 答案"即可获得推理能力。

## 在推理模型中的应用

- 是打造推理模型**方法三（模仿学习）**的捷径：不需要费劲自造/人工改写推理数据，直接复用现成推理模型。
- **案例**：
  - **SkyT1、S1** 都用蒸馏方法教模型推理能力。
  - **DeepSeek-R1 论文展示**：用 R1 当老师蒸馏 Qwen、Llama（8B/70B 等），数学与编程能力"起飞"，可与这些强模型相提并论。

## 与 RL 的对比：为什么蒸馏对中小模型更有效

| 维度 | RL（方法四） | 蒸馏（模仿学习） |
|------|------------|----------------|
| **前提** | 模型必须能自己产生正确答案（RL 只强化已有能力） | 不需要学生模型本身会推理，直接抄老师 |
| **对强基座** | 有效（DeepSeek-V3 500B+ 大幅强化） | 有效 |
| **对中小模型** | **效果有限**（Qwen2.5-32B 直接 RL ≈ QWQ-32B） | **大幅增强**（Qwen-32B 向 R1 学习后能力起飞） |
| **推理过程可读性** | 纯 RL 可能产出难读、多语言混杂的过程 | 老师的过程可读，学生继承可读性 |

## 关联连接

- [[Imitation_Learning]] — 蒸馏是模仿学习的捷径
- [[Reasoning]] — 打造推理模型的方法三
- [[Reinforcement_Learning]] — 对比：RL 强化已有能力 vs 蒸馏直接继承
- [[DeepSeek_R1]] — R1 作为老师蒸馏 Qwen/Llama
- [[Qwen]] — 蒸馏受益的模型家族
- [[Llama]] — 蒸馏受益的模型家族
- [[Model_Fine_Tuning]] — 蒸馏属于模型微调/后训练范畴
- [[Transfer_Learning]] — 蒸馏是知识迁移的一种形式
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — 来源
