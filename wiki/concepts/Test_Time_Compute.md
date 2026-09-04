---
title: "Test_Time_Compute 测试时计算"
type: concept
tags: [测试时计算, test-time, reasoning, 推理, 算力, scaling]
sources:
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

# Test-Time Compute（测试时计算 / 测试时缩放）

## 定义

Test-Time Compute（测试时计算）指**在测试（推理）阶段投入更大的算力来换取更好的结果**。对应的 **Test-Time Scaling** 指"思考越多往往结果越好"：只要能在推理时投入更多算力，通常就能得到更好结果。

- 深度思考（[[Reasoning]]）模型就是 Test-Time Compute 在语言模型上的典型应用——通过产生超长思考过程解更难的问题，即"**深度不够、长度来凑**"。
- 与**训练时算力（Training-Time Compute）**相对：可以把算力投在训练（训练更强的模型）或测试（推理时更深度搜索），两者可以互相成就。

## 起源与经典案例：AlphaGo

Test-Time Compute 并非新概念，**AlphaGo** 就是早期经典：

- **训练时**：训练 Policy Network（决定下一步落子位置）+ Value Network（评估盘面优势）。
- **测试时**：Policy Network 的抉择只作为参考，实际用 **Monte Carlo Tree Search（MCTS）** 做巨额运算——在脑内模拟"落子后接下来会发生什么"，预测各位置胜率，选胜率最高者。
- 上古棋类游戏论文已给出证据：横轴 training compute、纵轴 test compute，等高线代表相同得分——**同样分数既可由大训练算力 + 小测试算力达成，也可由小训练算力 + 大测试算力达成**；且当时作者惊叹"测试时只要用少量算力就能减少大量训练算力"。

## 在语言模型中的应用

- 让模型**产生非常长的思考过程**来解更难的题目（reasoning / 深度思考）。
- 把推理工作流程显式交给模型：大规模采样 + 选出正确答案的方法（[[Self_Consistency]]、Best-of-N、[[Process_Verifier]] + Beam Search、MCTS）都属于在测试阶段投入更多算力的实践。

## 关键要点

- **预算可调**：Test-Time Scaling 意味着可以按问题难度调节推理时投入的算力（think budget）。
- **边界问题**：思考越多结果越好，但**无谓推理浪费算力**——模型常做不必要的冗长思考（如算 123×456 反复验算多遍）。"该 reasoning 时才 reasoning"是当前的核心挑战（见 [[Over_Thinking]]）。

## 关联连接

- [[Reasoning]] — 深度思考是 Test-Time Compute 的 LLM 应用
- [[AlphaGo]] — 测试时计算的早期经典案例（MCTS）
- [[Chain_of_Thought]] — 通过思考链在推理时投入更多计算
- [[Self_Consistency]] — 推理时大规模采样 + 投票
- [[Process_Verifier]] — 推理时逐步验证的搜索方法
- [[Over_Thinking]] — 测试时计算过度投入的失效模式
- [[Cost_Optimization]] — 思考预算与推理成本的权衡
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — 来源
