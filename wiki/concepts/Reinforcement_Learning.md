---
title: "强化学习 Reinforcement Learning"
type: concept
tags: [机器学习, 强化学习, RL, 奖励信号]
sources:
  - "raw/09-archive/AI-for-Everyone-吴恩达-p7-35/AI for everyone 系列教程原声中文版【吴恩达】 21.md"
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

# 强化学习 Reinforcement Learning

## 定义

强化学习（Reinforcement Learning，RL）是机器学习的一种范式：AI 通过**试错 + 奖励信号**学习行为。每当行为好时给一个正数（正奖励），行为差时给负数（负奖励），AI 自动学习最大化累计奖励的行为策略。

## 关键信息

### 直觉类比：训练宠物狗

- 狗做对就表扬"好狗狗"（正奖励）、做错就"坏狗狗"（负奖励），随时间学会多做好事少做坏事
- 强化学习把同一原理应用到直升机、游戏、机器人等对象上

### 课程案例

- **斯坦福自主直升机**：在模拟器中飞行（可安全坠毁），按飞行好坏给奖励信号，最终造出世界最强自主直升机之一（可倒飞）
- **AlphaGo**：用强化学习在围棋中表现出色
- **电子游戏**：可与自己对弈无限获取数据，训练极高效

### 特点与现状

- **优势**：无需标注"最佳行为"（监督学习难以定义复杂场景的最优输出，如直升机在特定位置的最佳飞法）
- **弱点**：通常需要海量数据（模拟器可加速，无精确模拟器时更困难）
- **现状**：获得大量媒体关注，但**今天创造的经济价值仍远低于监督学习**；未来突破可能改变

### 与 LLM 后训练的联系

现代 LLM 的后训练阶段（RLHF/RLVR/PPO/GRPO）正是强化学习思想的工业级应用——用人类/AI 偏好作为奖励信号微调模型行为（见[[后训练研究]]）。

### 以结果为导向的推理 RL（Reasoning RL）

打造推理模型的方法四：**只以最终答案对错给 reward，完全不管推理过程内容**（DeepSeek-R1 系列主打）。这是 RLVR（可验证奖励学习）在数学/代码等可验证场景的直接应用：

- 设定：把问题给模型要求先 reasoning 再给答案；答案对→正 reward，错→负 reward。推理过程说什么不重要。
- **R1-Zero**：DeepSeek-V3-Base 只做 RL（正确率 reward + Format reward 要求输出 `think` token），AIME 数学竞赛逼近 o1；再做 majority vote 可与 o1 的 majority vote 相当。
- **Aha moment（顿悟时刻）**：RL 中模型自发学会"发现问题、推翻重来"（"等等，这里可能有错"）。但有论文检验发现 **DeepSeek-V3-Base 在 RL 之前本来就会"啊哈"**（会自我质疑、会检查错误）——RL 只是强化了模型已有能力。
- **RL 只强化已有能力**：RL 的前提是模型能自己产生正确答案。直接对 Qwen2.5-32B 做 R1-Zero 式 RL 提升有限（≈ QWQ-32B），而 RL 能大幅强化 DeepSeek-V3（500B+ 巨模型）；对中小模型**蒸馏（[[Knowledge_Distillation]]）比 RL 更有效**。
- 纯 RL 的推理过程可能**难读、多语言混杂**（R1-Zero 因此未上线），需要配合模仿学习/人工改写修正（见 [[DeepSeek_R1]]）。

## 关联连接
- [[Supervised_Learning]] — 监督学习对比（标注 vs 奖励信号）
- [[Unsupervised_Learning]] — 另一非监督范式对比
- [[Machine_Learning]] — 强化学习是机器学习三大范式之一
- [[后训练研究]] — RLHF/RLVR/PPO 的 LLM 后训练应用
- [[Reasoning]] — 方法四：以结果为导向的推理 RL
- [[DeepSeek_R1]] — RL 训练推理模型的代表案例（R1-Zero）
- [[Imitation_Learning]] — 对比：模仿学习在意推理过程，RL 只在意结果
- [[Knowledge_Distillation]] — 对中小模型比 RL 更有效的替代方案
- [[Self_Consistency]] — 推理时增强可与 RL 叠加（R1-Zero + majority vote）
- [[Andrew_Ng]] — 斯坦福自主直升机项目负责人
- [[摘要-ai-for-everyone-andrew-ng]] — 来源
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — 推理 RL 来源
