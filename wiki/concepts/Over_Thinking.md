---
title: "Over_Thinking"
type: concept
tags: [agent, reasoning, 过度思考, thinking模型, 效率, 规划]
sources:
  - wiki/sources/摘要-hung-yi-lee-ai-agent-原理.md
last_updated: 2026-08-04
---

# Over-Thinking（过度思考）

## 定义

Over-Thinking 指具备 **reasoning（思考）能力**的模型在作为 AI Agent 时的失效模式：**想得太多、做得太少**——"思考的巨人、行动的矮子"。论文来源《The Danger of Overthinking》（2025）。

## 表现

| 失效模式 | 例子 |
|---------|------|
| **反复推演而不行动** | "按钮点下去会怎样？"一直想不停——但很多情况下直接点一下（不是信用卡付款）就知道结果，按返回键即可撤销 |
| **尝试前先自我否定** | 还没尝试就反复想"这我做不到"，直接放弃 |
| **把内部模拟当真实反馈** | 用脑内想象替代真实环境反馈，但想象永远无法替代"点击后的实际页面" |

## 与思考能力的关系

- **整体仍然更好**：能演脑内小剧场的模型（reasoning 模型）在 AI Agent 任务上总体表现仍优于不能思考的模型。
- **副作用**：思考能力被滥用——在"无法通过思考得知结果"的情境（环境反馈型任务）上，思考成本高且无收益。
- **关键区分**：有些问题适合思考（推理型），有些问题适合行动（环境交互型）——过度思考把两者混为一谈。

## 与 Model-Based Planning 的关系

[[Model_Based_Planning]]（脑内小剧场/Tree Search/World Model）本质也是"想"，但它有**明确的收敛机制**（剪枝、成功率评估、只选最优路径执行）。Over-Thinking 则是**失去了收敛机制的想**——没有评估就永远想下去。

## 未来方向

> 如何**避免模型想太多**是当前 research 的关键课题——即在保留 reasoning 能力的同时，教会模型判断"何时该想、何时该做"。

## 关联连接

- [[Model_Based_Planning]] — 脑内小剧场的收敛版，Over-Thinking 是其失控形态
- [[Chain_of_Thought]] — Reasoning 模型的思考链
- [[Agent_Loop]] — Agent 循环中"思考 vs 行动"的权衡位置
- [[摘要-hung-yi-lee-ai-agent-原理]] — 本概念的核心来源
