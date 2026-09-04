---
title: "Process_Verifier 过程验证器"
type: concept
tags: [验证器, verifier, 推理, reasoning, 搜索, process-reward]
sources:
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

# Process Verifier（过程验证器）

## 定义

Process Verifier（过程验证器，process reward model）是一种**对推理中间步骤进行打分验证的模型**：不需要看到完整计算过程与最终答案，只根据**已产生的部分推理过程**判断"从这里继续解下去，得到正确答案的机率有多大"。它回答的核心问题是"**这一步对吗？该不该继续？**"，让模型避免"第一步就错、白算很久"。

## 与结果验证器（Outcome Verifier）的对比

| 维度 | Outcome Verifier | Process Verifier |
|------|-----------------|------------------|
| **输入** | 完整的答案 | 部分推理过程（如 step1、step1+step2） |
| **判断** | 这个答案对不对（给 0/1 或分数） | 从这一步继续解下去答对的概率 |
| **用途** | Best-of-N 选最优答案 | 搜索过程中逐步剪枝/择优 |
| **时机** | 模型解完最终答案后 | 解题中途即可验证 |

## 如何训练 Process Verifier

只有"问题 + 正确答案"的数据时，无法直接判断中间步骤对错。做法：

1. 从某一步（如 step1）出发，**让原模型多次采样**继续解完（每次后续步骤与答案可能不同）。
2. 统计"从这一步出发最终答对的比例"——作为该步骤的"质量标签"（例：从 step1 出发答对率 2/3 ⇒ 给 step1 打 2/3 分；从 step1+step2 出发答对率 1/3 ⇒ 打 1/3 分）。
3. 用"步骤 → 答对率"数据训练过程验证器，学会给更有希望的解步骤打更高分。

## 如何配合搜索使用：Beam Search

- 让模型只生成一步就停（用 `step`/`/step` 标记，遇到 `/step` 就停止生成），生成多个候选 step1。
- 用 Process Verifier 给每个候选打分，**只保留最好的 n 条路径**（或前 25%），丢弃其余。
- 在保留下来的路径上继续生成 step2，再打分、再保留……循环（这就是 Beam Search；变体：DVTS 保留更多样化的路径）。
- 同一框架可替换为 **MCTS / A* 等启发式搜索算法**。
- 实验（Hugging Face）：**Beam Search 能让 1B 模型超越 8B 模型**——这是 Majority Vote 做不到的。

## 与推理模型的关系

- 现在的深度思考模型"解到一半就验证中间步骤"的行为，正对应 Process Verifier 的思路。
- DeepSeek 曾在 R1 开发中尝试 Process Verifier 与 MCTS，但最终未取得好结果，未用于最终模型。
- 在模仿学习（方法三）中，Process Verifier 用于**生成高质量的推理过程训练数据**：树状搜索逐步验证，只保留验证通过的步骤拼成训练数据。

## 关联连接

- [[Reasoning]] — 打造推理模型的方法二/三的核心组件
- [[Self_Consistency]] — 相对更简单的结果选择方法（多数投票）
- [[Test_Time_Compute]] — 过程验证 + 搜索是在测试阶段投入更多算力
- [[Imitation_Learning]] — 用过程验证器生成推理训练数据
- [[Model_Based_Planning]] — 搜索/树状结构在规划中的应用
- [[Chain_of_Thought]] — 分步推理的形式（step 标记）
- [[Hugging_Face]] — Beam Search 实验来源
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — 来源
