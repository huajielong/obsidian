---
title: "Agent Loop"
type: concept
tags: [智能体, 循环设计, ReAct, 控制系统, Agent]
sources: [raw/01-articles/技术资源库/Agent Loop 设计完整指南.md, raw/01-articles/从零实现 ReAct 循环.md, raw/01-articles/多步骤推理任务 — 连续 Tool 调用.md]
last_updated: 2026-07-15
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

| 阶段            | 职责     | 核心决策                |
| ------------- | ------ | ------------------- |
| **Plan**      | 制定整体计划 | 任务理解与策略选择           |
| **Decompose** | 任务拆解   | 原子化粒度控制             |
| **Retrieve**  | 检索相关信息 | 上下文检索策略             |
| **Act**       | 执行具体操作 | 工具选择与参数             |
| **Verify**    | 验证结果质量 | **quality_gate 判断** |
| **Critique**  | 分析失败原因 | 诊断路径选择              |
| **Repair**    | 修复问题   | 修复幅度控制              |
| **Commit**    | 提交最终结果 | 结果汇总与输出             |

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
- **Transient**（瞬态）：网络抖动、限流 → [[Exponential_Backoff|指数退避重试]]
- **Recoverable**（可恢复）：接口不可用 → 切换备用方案
- **Fatal**（致命）：权限拒绝 → 早停并上报人工

### PID 控制理论应用
Agent Loop 可建模为控制系统：`u(k) = Kp·e(k) + Ki·Σe(j) + Kd·(e(k)-e(k-1))`
- `e(k)` = 质量误差（目标质量 - 当前质量）
- 质量演化：`y(k+1) = y(k) + G·u(k) + w(k)`

### 状态持久化与执行环境快照

每完成一个 Action，持久化 `(step_id, state_snapshot, decision_log)`，支持中断恢复。

**执行环境快照（Execution Environment Snapshot）**进一步将 Agent 运行时的完整状态序列化存储，包括：
- 上下文历史（message history）
- 工具调用轨迹（tool call traces）
- 中间结果（intermediate outputs）
- 环境变量与配置（runtime environment）

这为超长程任务提供断点续传、回放调试、状态迁移和审计合规能力。DeepSeek 的 Agent 后端方向将执行环境快照作为核心工程课题之一。

> 详见 [[摘要-deepseek-service-engineer-jd]] — Agent 后端工程实践

## Loop 范式选择指南

| 任务特征 | 推荐范式 |
|----------|----------|
| 短链路、确定性高 | ReAct |
| 多步骤、可拆分 | Plan-and-Execute + Replan |
| 有明确成败判断 | Reflexion 自校验 |
| 复杂协同任务 | Hierarchical / Multi-Agent |

## 手写 ReAct 实现参考

理解 ReAct 循环的最佳方式是手写一遍。核心是一个 `for` 循环 + 原生 `tools` 参数：

```python
for step in range(5):
    response = client.chat.completions.create(
        model="qwen2.5:3b",
        tools=TOOLS,
        messages=messages,
    )
    msg = response.choices[0].message
    messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})

    if not msg.tool_calls:     # 没有 tool_calls = 终止
        break

    for tc in msg.tool_calls:
        observation = TOOL_IMPL[tc.function.name](json.loads(tc.function.arguments))
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(observation)})
```

**三条核心规则：**
1. LLM 输出必须追回 messages — `role: "assistant"` 保留 `content` + `tool_calls`
2. 工具结果必须追回 messages — `role: "tool"` + 匹配的 `tool_call_id`
3. 没有 tool_calls 就是终止 — `msg.content` 即最终答案

**多步依赖陷阱**：当多个工具有数据依赖链时（如 `calculator` 依赖 `get_population` 的结果），小模型可能**并行预测所有工具调用**，导致下游工具在上游未完成时就被调用。详见 [[Tool_Calling#多步调用的依赖链]]。

详见 [[摘要-llm-tool-calling-practice]] 中的完整实现（含多步骤推理链和多工具并行调用示例）。

## 关联连接
- [[Agent数据产品工程]] — 评测数据桥梁层：通过评测体系设计与数据生产管线构建，连接产品体验与模型能力；聚焦办公/生活/搜索等通用场景
- [[Agent能力工程]] — 能力构建层：通过 RL 环境构建、评测任务设计和能力短板补齐，系统性地提升模型 Agent 能力
- [[Multi_Agent_System]] — 从 Single-agent Loop 扩展到多 Agent 协作
- [[Agent_Orchestration_Patterns]] — Multi-agent 编排模式，与单 Agent Loop 互补
- [[Harness_Engineering]] — 驾驭工程体系
- [[Loop_Engineering]] — 第四层工程范式，设计 Agent 循环的元层方法论
- [[摘要-agent-loop-guide]] — Agent Loop 完整指南源摘要
- [[OpenClaw]] — OpenClaw 实体（Agent Loop 实践案例）
- [[Agentic_Coding]] — AI Agent 编程范式
- [[AI_Mastery_Compass]] — AI 大模型驾驭进阶罗盘，Agent Loop 的 ReAct 循环与其理念相通
- [[摘要-awesome-agentic-ai-zh-tool-use]] — Agentic AI 学习路线 Stage 3，包含从零实现 ReAct 循环的 6 个动手练习
- [[摘要-llm-tool-calling-practice]] — 手写 ReAct 循环的完整代码实现（含多步骤推理链）
- [[Tool_Calling]] — Tool Calling 协议格式与 Schema 设计，ReAct 中 Action 阶段的技术基础
- [[Agent实例生命周期管理]] — Agent 从创建到销毁的全生命周期管控，Agent Loop 在平台工程维度的扩展
