---
title: "AlphaGo"
type: entity
tags: [agent, 强化学习, 围棋, DeepMind, RL]
sources:
  - wiki/sources/摘要-hung-yi-lee-ai-agent-原理.md
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

## 定义

AlphaGo 是 DeepMind 开发的围棋 AI，2016 年击败李世石而举世闻名。在 AI Agent 语境中，它是**RL（强化学习）驱动 Agent 的经典范例**：目标=赢棋，observation=棋盘盘面，action=19×19 路中选择落子位置。

## 关键信息

- **作为 Agent 的要素**：目标（赢棋）→ 观察（黑白子位置/盘面）→ 行动（落子）→ 环境反馈（对手落子改变盘面）→ 循环。
- **RL 范式**：把目标转成 reward（赢=+1，输=-1），训练模型最大化 reward。
- **局限性**：每个任务都需单独 RL 训练——AlphaGo 只能下围棋，不能直接下西洋棋/将棋。
- **AlphaZero**：后续版本（口误纠正：AlphaGo Zero 应为 AlphaZero）经单独训练后扩展到将棋与西洋棋，仍是**不同参数的不同模型**。
- **与 LLM Agent 的对比**：LLM 输出近乎无穷、无需重新训练，而 AlphaGo 只能做"19×19 选择题"，且不能理解文字指令。

### 作为 Test-Time Compute 的早期经典案例

- AlphaGo 在**测试阶段**投入巨大算力：训练时训 Policy Network（决定落子位置）+ Value Network（评估盘面优势），但测试时 Policy Network 的抉择只作为参考，实际用 **Monte Carlo Tree Search（MCTS）** 做脑内模拟——假设落子后预测后续局面与胜率，最终选择胜率最高的位置。
- 上古棋类游戏论文已提出"把算力投在训练 vs 投在测试"的权衡，二者可互相成就；这成为今天 **[[Test_Time_Compute|测试时计算 / Test-Time Scaling]]** 概念的先声——推理模型"深度不够、长度来凑"的远祖。

## 关联连接

- [[Reinforcement_Learning]] — AlphaGo 是 RL 训练 Agent 的代表
- [[Agent_Loop]] — observation→action 循环的经典案例
- [[Model_Based_Planning]] — AlphaGo 自弈的世界模型对照
- [[Test_Time_Compute]] — AlphaGo 的 MCTS 是测试时计算的早期案例
- [[Reasoning]] — 深度思考模型与 AlphaGo 共享测试时算力思路
- [[摘要-hung-yi-lee-ai-agent-原理]] — 本实体的来源
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — Test-Time Compute / MCTS 案例来源
