---
title: "Failure Injection / Chaos Eval（故障注入与混沌评估）"
type: concept
tags: [agentic AI, 测试, 容错, 混沌工程, eval]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Failure Injection / Chaos Eval（故障注入与混沌评估）

## 定义

Failure Injection / Chaos Eval 是一种测试 Agent 容错能力的方法论：**故意给 Agent 注入 Broken Input / Stale Data / API Timeout 等故障**，观察 Agent 如何恢复、降级或报告错误。借鉴自混沌工程（Chaos Engineering）的理念——在受控环境中主动破坏来验证系统韧性。

## 测试模式

| 注入类型 | 说明 | Agent 期望行为 |
|----------|------|---------------|
| **Broken Input** | 传入格式错误的数据 | 检测异常并优雅报告 |
| **Stale Data** | 返回过期信息 | 识别数据新鲜度问题 |
| **API Timeout** | Tool 调用超时 | 触发 Retry 或 Fallback |
| **Partial Failure** | 部分子任务失败 | 不影响其他子任务 |
| **Conflicting Info** | 多源数据冲突 | 按优先级解决或上报 |

## 动到哪一层

- **Service（测试 Agent 容错）** — 属于 Service 层的测试策略

## 核心来源

- **Hamel Husain** — "Evals are everything" blog series
- [[Eval_Harness]] — 自动化评估流水线的补充实践

## 关联连接

- [[Eval_Harness]] — Chaos Eval 是 Eval 策略的一类
- [[Graceful_Degradation]] — 故障注入测试的就是降级路径
- [[Agent_As_Judge]] — 故障后的评审机制
- [[Harness_Engineering]] — 属于 Quality 验证类别
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
