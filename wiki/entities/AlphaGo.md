---
title: "AlphaGo"
type: entity
tags: [agent, 强化学习, 围棋, DeepMind, RL]
sources:
  - wiki/sources/摘要-hung-yi-lee-ai-agent-原理.md
last_updated: 2026-08-04
---

## 定义

AlphaGo 是 DeepMind 开发的围棋 AI，2016 年击败李世石而举世闻名。在 AI Agent 语境中，它是**RL（强化学习）驱动 Agent 的经典范例**：目标=赢棋，observation=棋盘盘面，action=19×19 路中选择落子位置。

## 关键信息

- **作为 Agent 的要素**：目标（赢棋）→ 观察（黑白子位置/盘面）→ 行动（落子）→ 环境反馈（对手落子改变盘面）→ 循环。
- **RL 范式**：把目标转成 reward（赢=+1，输=-1），训练模型最大化 reward。
- **局限性**：每个任务都需单独 RL 训练——AlphaGo 只能下围棋，不能直接下西洋棋/将棋。
- **AlphaZero**：后续版本（口误纠正：AlphaGo Zero 应为 AlphaZero）经单独训练后扩展到将棋与西洋棋，仍是**不同参数的不同模型**。
- **与 LLM Agent 的对比**：LLM 输出近乎无穷、无需重新训练，而 AlphaGo 只能做"19×19 选择题"，且不能理解文字指令。

## 关联连接

- [[Reinforcement_Learning]] — AlphaGo 是 RL 训练 Agent 的代表
- [[Agent_Loop]] — observation→action 循环的经典案例
- [[Model_Based_Planning]] — AlphaGo 自弈的世界模型对照
- [[摘要-hung-yi-lee-ai-agent-原理]] — 本实体的来源
