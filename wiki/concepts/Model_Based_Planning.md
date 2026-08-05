---
title: "Model_Based_Planning"
type: concept
tags: [agent, planning, 规划, tree search, world model, 脑内小剧场, 梦境模拟]
sources:
  - wiki/sources/摘要-hung-yi-lee-ai-agent-原理.md
last_updated: 2026-08-04
---

# Model-Based Planning（基于模型的规划 / 脑内小剧场）

## 定义

Model-Based Planning 是一种强化 LLM Agent **规划能力**的范式：让模型在"脑内小剧场"（梦境模拟）中，用自己扮演的环境模型（**World Model**）推演各条行动路径的后果，通过 **Tree Search** 探索并剪枝，评估成功率后再在实际世界中执行最优一步。它区别于"直接反射式输出"和"在真实环境里穷举试错"。

## 为什么需要

| 朴素方案 | 问题 |
|---------|------|
| 直接按初始 Plan 执行 | 环境不可预测（对手的招数、弹出的广告窗口），计划会被打破 → 需要 Replan |
| 每次看到新 observation 都重新规划 | 可行，但仍有局限（见下） |
| 在真实环境中穷举所有路径 | **算力爆炸**：复杂任务的所有可能性路径不可行 |
| 在真实环境先试一步再试另一步 | **覆水难收**：有些动作做了就回不了头（先订了 pizza 就不能改订便当） |

→ 所以让一切尝试都发生在**梦境中（模型脑内的模拟）**，不产生真实后果。

## 核心技术组件

### 1. Tree Search（树搜索）

- 从初始 observation 出发，逐层展开可执行的 action，形成搜索树；自问自答评估每条路径"还有希望吗"，低于阈值（threshold）的路径直接剪枝放弃，换下一条。
- 代表工作：**Tree Search for Language Model Agents**（2024 夏）——给模型指令+截图让它上网完成任务，配合剪枝后效果显著优于普通反射式回答。
- 缺点：在现实世界执行时覆水难收——这正是转去"梦境模拟"的动因。

### 2. World Model（世界模型）

- **定义**：模拟"行动 → 环境变化"的模型。在 Agent 场景，模型执行某动作后看到什么新 observation，**不是由模型而是由环境决定的**，模型需要猜环境会怎么变。
- **实现**：让模型**自问自答扮演 World Model**，用文字描述行动后果（而不是生成新的网页画面——后者难度太高）。
- 代表工作：**"is your LLM secretly a world model of the internet?"**——用 model-based planning 打造 web agent：在脑内想象点按钮 1/2/3 后各自会发生什么，自己评估每步成功率（40%/80%/10%），挑出最优项（80%）在实际世界执行。
- **对比**：AlphaGo 中由另一个"对手模型"扮演环境自弈。

### 3. 梦境模拟流程（脑内小剧场）

```
现实观察 ──► 脑内展开（想象 action 及后续）
          │    每个想象状态继续展开
          │    自己扮演 World Model 描述环境变化
          │    自评每条路径成功率，剪枝低分路径
          ▼
     找到成功路径 ──► 只在实际世界执行该路径的第一步
```

- **Reasoning 模型的连接**：有 reasoning 能力的模型（能演脑内小剧场）正好可能在做这种规划——DeepSeek-R1 面对叠积木问题时在"内心"做了 1500 字搜索，梦到最优解（先拿开蓝色、放回桌面、再放橙色）后才执行第一步。见 [[Chain_of_Thought]]。

## 规划能力评测现状

| Benchmark | 内容 | 结果 |
|-----------|------|------|
| **PlanBench（Blocksworld）** | 叠积木规划 | 普通问题模型能解 |
| **PlanBench（神秘方块世界）** | 奇怪规则防"照本宣科" | 2023 年 GPT-4 仅 ~9%；2024 年 o1 等 reasoning 模型有希望 |
| **旅行规划（TravelPlanner 类）** | 带预算/约束的行程规划 | 2024 年初纯 LLM 成功率 ~0%；把约束交给 solver 工具后 90%+ |

> 结论：纯 LLM 规划能力"介乎有与没有之间"，**工具辅助 + 模型内模拟**是两条主要增强路径。

## 关联连接

- [[Agent_Loop]] — 规划是 Agent 循环中"行动前"的显式步骤
- [[Hierarchical_Task_Decomposition]] — Plan-Execute 模式：本范式的工程化对照
- [[Chain_of_Thought]] — Reasoning 模型的思考链 = 脑内小剧场
- [[Over_Thinking]] — 脑内小剧场的副作用：想太多而行动太少
- [[Reinforcement_Learning]] — AlphaGo 的世界模型/自弈对照
- [[Agent_Memory_Architecture]] — 记忆检索支撑规划所需的情境经验
- [[Tool_Calling]] — 规划可调用 solver 等工具增强
- [[摘要-hung-yi-lee-ai-agent-原理]] — 本概念的核心来源
