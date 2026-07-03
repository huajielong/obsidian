---
title: "Agent Loop"
type: concept
tags: [智能体, 循环设计, ReAct, 控制系统, Agent]
sources: [raw/01-articles/技术资源库/Agent Loop 设计完整指南.md]
last_updated: 2026-07-03
---

# Agent Loop（智能体循环）

## 定义

Agent Loop 是让 AI 智能体自主完成任务的核心运行机制。它将大模型从"文本生成器"升级为"能完成任务的执行系统"，通过**"执行→验证→下一任务"**的循环实现可靠交付。

> Agent Loop = 调用模型 → 判断是否要用工具 → 执行工具 → 把结果回喂给模型 → **重复**

## 演进历程

| 年份 | 演进 | 来源 |
|------|------|------|
| 2022 | **ReAct 循环**（Reasoning + Acting 交错执行） | Yao et al. |
| 2023 | **Plan-and-Execute**（规划-执行分离） | LangChain |
| 2023 | **Reflexion**（自我反思 + 语言强化学习） | Shinn et al. |
| 2024-2026 | **生产级闭环系统**（八步完整循环） | 行业实践 |

## 生产级八步循环

```plaintext
Plan → Decompose → Retrieve → Act → Verify → Critique → Repair → Commit
```

### 各阶段详细说明

| 阶段 | 职责 | 核心决策 |
|------|------|----------|
| **Plan** | 制定整体计划 | 任务理解与策略选择 |
| **Decompose** | 任务拆解 | 原子化粒度控制 |
| **Retrieve** | 检索相关信息 | 上下文检索策略 |
| **Act** | 执行具体操作 | 工具选择与参数 |
| **Verify** | 验证结果质量 | **quality_gate 判断** |
| **Critique** | 分析失败原因 | 诊断路径选择 |
| **Repair** | 修复问题 | 修复幅度控制 |
| **Commit** | 提交最终结果 | 结果汇总与输出 |

### 状态机定义

```
L = (S, s₀, Σ, δ, F)
S = {PLAN, DECOMPOSE, RETRIEVE, ACT, VERIFY, CRITIQUE, REPAIR, COMMIT, FAIL, HALT}
s₀ = PLAN
F = {COMMIT, FAIL, HALT}
```

关键转换：`δ(VERIFY, quality_gate_fail) = CRITIQUE` → REPAIR → VERIFY（闭环）

## 工程化关键技术

### 上下文管理（三层记忆）
```
Layer 1: Working Memory  — 最近 N 轮完整保留
Layer 2: Episodic Memory — 关键事件压缩存储
Layer 3: Semantic Memory — 结构化存储，按需检索
```

### 失败处理策略
- **Transient**（瞬态）：网络抖动、限流 → 指数退避重试
- **Recoverable**（可恢复）：接口不可用 → 切换备用方案
- **Fatal**（致命）：权限拒绝 → 早停并上报人工

### PID 控制理论应用
Agent Loop 可建模为控制系统：`u(k) = Kp·e(k) + Ki·Σe(j) + Kd·(e(k)-e(k-1))`
- `e(k)` = 质量误差（目标质量 - 当前质量）
- 质量演化：`y(k+1) = y(k) + G·u(k) + w(k)`

### 状态持久化
每完成一个 Action，持久化 `(step_id, state_snapshot, decision_log)`，支持中断恢复。

## Loop 范式选择指南

| 任务特征 | 推荐范式 |
|----------|----------|
| 短链路、确定性高 | ReAct |
| 多步骤、可拆分 | Plan-and-Execute + Replan |
| 有明确成败判断 | Reflexion 自校验 |
| 复杂协同任务 | Hierarchical / Multi-Agent |

## 关联连接
- [[Harness_Engineering]] — 驾驭工程体系
- [[摘要-agent-loop-guide]] — Agent Loop 完整指南源摘要
- [[OpenClaw]] — OpenClaw 实体（Agent Loop 实践案例）
- [[Agentic_Coding]] — AI Agent 编程范式
