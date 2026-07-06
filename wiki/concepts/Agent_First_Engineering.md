---
title: "Agent-First Engineering"
type: concept
tags: [AI编码, Agent-First, Harness, 工作流]
sources: [raw/01-articles/harness-engineering/智能体优先的工程（Agent-First Engineering）.md]
last_updated: 2026-07-03
---

# Agent-First Engineering（智能体优先工程）

## 定义

Agent-First Engineering 是 [[Harness_Engineering]] 的具体实现方法论，将传统软件开发流程完全反转：

> **人定目标、做审核；AI 做规划、设计、编码、测试、部署、迭代。**

- **传统开发**：人写代码 → AI 辅助补全
- **Agent-First**：AI 主导全流程工程 → 人只做需求、决策、验收

## 7 步实操流程

```
① 人定需求 → ② AI 架构设计 → ③ AI 写代码 → ④ AI 自测 → ⑤ AI 自修 → ⑥ 人审核 → ⑦ AI 部署运维
```

| 步骤             | 主导者   | 产出               |
| -------------- | ----- | ---------------- |
| 1. 定义高层目标与约束   | **人** | 需求 + 边界条件        |
| 2. 系统拆解与架构设计   | Agent | 架构图、接口文档、技术选型    |
| 3. 生成完整代码骨架    | Agent | 完整可编译代码          |
| 4. 自动写测试       | Agent | 单元/集成/边界测试       |
| 5. 自验证、自调试、自重构 | Agent | **Harness 闭环核心** |
| 6. 关键评审 + 安全审核 | **人** | 架构安全、关键逻辑        |
| 7. 自动部署与持续迭代   | Agent | 容器化、监控、告警        |

## 与 Harness Engineering 的关系

Agent-First Engineering 是 Harness Engineering 思想的具体落地步骤。Harness 提供控制系统和约束框架，Agent-First 提供端到端的工作流编排。

## 关联连接
- [[Harness_Engineering]] — 驾驭工程核心概念
- [[摘要-agent-first-engineering]] — 实操指南源摘要
- [[Agentic_Coding]] — AI Agent 编程范式
- [[Agent_Loop]] — Agent 循环机制
