---
title: "Multi_Agent_System"
type: concept
tags: [multi-agent, agent框架, orchestration, LLMT系统设计]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-10
---

# Multi-Agent System

Multi-Agent System 是多个 LLM Agent 协同工作的架构模式。与 Single-agent（一个 LLM + ReAct loop + 若干 tools）不同，Multi-agent 将任务拆分为多个角色，让不同 LLM instance 从不同视角协作。

## 核心分类矩阵

Multi-agent 的理解需要先理清两个正交维度：

| | **Workflow**（固定 code path） | **Agent**（LLM 动态决策） |
|---|---|---|
| **Single LLM** | 线性 pipeline、无分支判断 | 一个 LLM + ReAct loop、自己 plan + adapt |
| **Multi LLM** | 预设 routing（如销售→A、技术→B） | **2+ agent 互相 handoff、orchestrator 动态分配** |

**真正需要 Multi-agent Framework 的是右下角象限**——LLM 自主性高 + 多角色协作。

## Single-agent vs Multi-agent 对比

| 维度 | Single-agent | Multi-agent system |
|---|---|---|
| 架构 | 一个 LLM + ReAct loop + tools | 2+ LLM、各有角色、orchestrator 协调 |
| 决策方式 | 同一 LLM 从头想到尾 | 角色拆分 + handoff、不同视角 |
| State 管理 | 线性 message history | shared state / message passing / checkpoint |
| 适合场景 | 逻辑线性、tool < 20-30、单一目标 | 任务可分解、需要 diversity、长 workflow |
| Debug 成本 | 低 | 高（cross-agent 互动难定位）|
| Token 成本 | 1x | 通常 **3-10x** |
| Latency | 低 | 高（除非并行） |

## 何时真的需要 Multi-agent

**Multi-agent 不是 default、是 last resort。** Anthropic 和 Cognition 两家前沿实验室明确表示：**90% 用例不该用 Multi-agent。** 硬上的代价：3-10× Token、Debug 痛苦、Context Fragmentation。

### 四个信号

1. **任务天然分解** — 大任务有清楚的子步骤 → Sequential / Planner-Executor
2. **Token explosion** — Single agent prompt 装不下所有 tool description → Supervisor-Worker
3. **角色冲突** — 同一 LLM 既当 writer 又当 critic 会 self-justify → Debate / Peer review
4. **并行加速** — 多个子任务同时跑、省 wall-clock → Parallel / Map-Reduce

### 权威立场

| 来源 | 核心论点 |
|---|---|
| **Anthropic** — Building Effective Agents (2024) | 多数场景 simple workflow + single agent 就够；multi-agent 只在研究型/并行探索任务有帮助 |
| **Cognition** — Don't Build Multi-Agents (2025) | Multi-agent 的 context fragmentation 严重；先穷尽 single-agent + long-context 才考虑 |

## 两条实现路线

| 维度 | Framework 路线 | Claude Code Subagent 路线 |
|---|---|---|
| 启动方式 | Python orchestration code | 写 `.claude/agents/<name>.md` |
| Runtime | 跨 LLM provider | 只在 Claude Code runtime 内 |
| Context 隔离 | 需手动实现 | 天生隔离 |
| Provider lock-in | 无 | Anthropic Claude 限定 |
| 学习曲线 | 中高（需学 framework API）| 低（写 markdown 即可）|
| Checkpoint / Audit | 完善（LangGraph checkpointing）| 依赖 Claude Code 内置 |

## Claude Code 的三种 Multi-Agent 机制

| 机制 | 状态 | 用途 |
|------|------|------|
| **Subagent**（稳定版） | 正式可用 | Delegate 大 Context 任务，独立 Context Window，结果回主 Session |
| **Agent Team**（Opt-in） | 正式文档 | 多 Worker 互相沟通/辩论/多角度探索 |
| **Background Agent**（Preview） | Research Preview | 多个独立任务各自后台跑，统一监控 |

> 截至 2026 年中，Claude Code 是**唯一拥有完整 Native Multi-Agent Stack 的 CLI Agent**。Codex CLI / Gemini CLI / Cursor 均为 Single-agent。

## Dynamic Workflows（上层编排）

Opus 4.8+ 引入的 **Dynamic Workflows** 机制建立在 Subagent 之上——让 Claude 自己生成 Workflow 脚本，再 Orchestrate 一群 Subagent 实现确定性的 Loop / 并行 Fan-out / 验证阶段。详见 [[Claude_Code_Dynamic_Workflows]]。

## Production 化注意事项（Stage 7 补充）

将 Multi-agent 推向 Production 时，[[Harness_Engineering]] 的 8 个核心元件变得尤为关键：

| 挑战 | 说明 | 应对元件 |
|------|------|---------|
| **3-10× Token 成本** | Multi-agent 的 LLM call 次数是 single-agent 的数倍 | [[Cost_Optimization]]（第 8 元件）|
| **Context Fragmentation** | Context 被切散在多个 Agent、彼此看不到全貌 | Context Manager（第 3 元件）|
| **Cross-agent Debug** | 问题根源跨多个 Agent，难以定位 | [[Agent_Observability]]（第 6 元件）+ Trace |
| **质量不一致** | 下游 Agent 输出受上游 Agent 误差累积影响 | [[Eval_Harness]]（第 7 元件）|
| **协调失败** | Agent 之间 handoff 失败、死锁、重复工作 | Agent Loop（第 1 元件）+ Safety Layer（第 4 元件）|

### 失败模式分类（MAST）

多 Agent 系统的失败可用 **MAST** 框架（arXiv 2503.13657）分类——14 种失败模式分 3 类，用于结构化地报告和修复 Multi-agent 问题。

## 关联连接

- [[Claude_Code_Subagent]] — Claude Code 原生 Subagent 机制详解
- [[Claude_Code_Dynamic_Workflows]] — Opus 4.8+ 动态 Workflow 编排
- [[Agent_Orchestration_Patterns]] — Multi-agent 的 5 种经典编排模式详解
- [[Agent_Loop]] — Single-agent ReAct 循环（Multi-agent 的前置基础）
- [[Eval_Harness]] — Production 化必备：自动化评估流水线
- [[Agent_Observability]] — Production 化必备：Agent 可观测性
- [[Cost_Optimization]] — Production 化必备：成本与延迟优化
- [[Harness_Engineering]] — 8 核心元件框架，Multi-agent Production 化的工程基础
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本概念的核心来源（Stage 4）
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — Subagent 路线的深度来源（Stage 5）
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — Production 化注意事项的补充来源（Stage 7）
- [[Anthropic]] — Building Effective Agents 的发布者
- [[Claude_Code]] — Subagent 路线的宿主环境
- [[Agentic_Coding]] — Multi-agent 在软件开发中的应用范式
