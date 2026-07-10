---
title: "Agent-as-Judge / Constitutional AI"
type: concept
tags: [agentic AI, 评审, 质量控制, 宪法AI, 评估]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Agent-as-Judge / Constitutional AI

## 定义

Agent-as-Judge 是一种质量保障模式：**用一个 Agent 评审另一个 Agent 的输出**，按明确原则（Constitution）反复修正直到达标。这是 [[Harness_Engineering]] 中 Quality 验证类别的核心模式。

## 核心架构

```
Agent A（执行者）→ 产出 → Agent B（评委）→ 按 Constitution 评分
→ 不符合 → 反馈给 Agent A 修正 → 重新提交
→ 符合 → 通过
```

## Constitutional AI（Bai 2022）

Constitutional AI 为 Agent-as-Judge 提供了"评审标准"的理论基础：

- **Constitution** = 一组明确的行为准则（如"不要做未经验证的推测"）
- Agent B 按照 Constitution 给定的原则评审，而非自由评判
- 避免"让 Agent 自己评自己"的自我称赞问题

## 跨 Vendor 对照

| 来源 | 实现 |
|------|------|
| [[Anthropic]] | Evaluator-Optimizer Loop + Multi-Agent Research 中的 Review Agent |
| [[OpenAI]] | LLM-as-Judge + Taste Invariants 中的 Quality Gate |
| [[Hamel_Husain]] | "Evals are everything" — EVals 驱动的评审流程 |

## 实作建议

1. **执⾏者与评审者分离** — 不让同一个 Agent 既做又评
2. **Constitution 明确化** — 评审标准先写死，不让评审 Agent 自由发挥
3. **Pass^k 机制** — k 次都通过才算过关，防止单次侥幸

## 关联连接

- [[Harness_Engineering]] — Quality 验证类别的核心实践
- [[Eval_Harness]] — 自动评估流水线
- [[Taste_Invariants]] — 评审标准可编码为 Invariants
- [[Reflexion]] — Agent 自反思机制，与外部评审互补
- [[Work_Boundary]] — 评审确保 Agent 输出不越界
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
