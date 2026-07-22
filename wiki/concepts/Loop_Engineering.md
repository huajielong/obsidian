---
title: "Loop Engineering"
type: concept
tags: [循环工程, Agent Loop, 智能体循环, 控制系统, 工程范式, 第四层]
sources: 
  - wiki/concepts/Harness_Engineering.md
  - wiki/concepts/Agent_Loop.md
  - wiki/sources/摘要-agent-loop-guide.md
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-23
---

# Loop Engineering（循环工程）

## 定义

**Loop Engineering（循环工程）** 是 2026 年浮现的**第四层工程范式**，位于 Prompt → Context → Harness 三层模型之上。它的核心命题是：

> **设计 Agent 的迭代循环本身**——包括目标设定、工具选择、上下文管理、终止条件与错误处理，让 Agent 能稳定跑数百步、跨 Session 仍可靠运行。

如果说 [[Harness_Engineering]] 回答的是"整个流程怎么跑起来？"，那么 Loop Engineering 回答的是：

> **"这个循环本身应该怎么设计，才能让 Agent 在复杂长任务中不跑偏、不卡死、不浪费？"**

### 四层工程模型定位

| 层级 | 工程对象 | 核心问题 |
|------|---------|---------|
| **1. Prompt Engineering** | 送进 LLM 的**字符串** | "这一次要怎么问？" |
| **2. Context Engineering** | 窗口里装的**信息** | "该给模型哪些信息？" |
| **3. Harness Engineering** | 模型**外围的执行与控制层** | "整个流程怎么跑起来？" |
| **4. 🔁 Loop Engineering** | Agent **迭代循环的设计本身** | **"循环怎么设计才能稳定可靠？"** |

## 与相关概念的关系

| 概念 | 关系 | 区别 |
|------|------|------|
| **[[Agent_Loop]]** | **运行时 vs 元层** | Agent Loop 是循环的**运行机制**（Plan→Act→Verify 怎么做）；Loop Engineering 是循环的**设计方法论**（该怎么设计这些步骤、何时终止、如何容错） |
| **[[Harness_Engineering]]** | **下层 vs 上层** | Harness Engineering 提供 Agent 运行所需的**基础设施**（Tool Registry、Safety Layer、Observability）；Loop Engineering 在这些之上设计**循环的控制逻辑** |
| **[[Agentic_Coding]]** | **应用 vs 元层** | Agentic Coding 是 AI 自主编程的**实践范式**；Loop Engineering 为其提供**循环控制的理论基础** |

## 核心组成

### 1. 目标与任务设计（Goal & Task Design）

循环的起点是明确的目标定义。目标设计决定了 Agent 知道"什么算完成"：

- **目标原子化**：将大目标拆解为可验证的子目标
- **质量门控标准**：定义 `quality_gate` 的判定条件（通过/失败/部分通过）
- **目标层级化**：战略性长期目标 vs 战术性短期目标，嵌套管理

### 2. 工具选择与调度（Tool Selection & Dispatch）

Agent 在每次循环中需要决定"用什么工具"——Loop Engineering 关注工具层的设计：

- **Tool Registry 设计**：可用工具的动态注册与发现
- **依赖链管理**：处理多步工具调用之间的数据依赖（避免小模型"跳跃"问题）
- **Permission Gate**：敏感操作的权限校验时机与策略
- **Fallback 策略**：工具不可用时的备选路径

> 详见 [[Tool_Calling#多步调用的依赖链]]

### 3. 上下文管理（Context Management）

循环越深，上下文越容易爆炸。Loop Engineering 设计上下文如何在循环中流动：

```
Layer 1: Working Memory  — 最近 N 轮完整保留（实时决策用）
Layer 2: Episodic Memory — 关键事件压缩存储（反思与校验用）
Layer 3: Semantic Memory — 结构化长期存储，按需检索（跨 session 用）
```

核心控制点：
- **窗口溢出检测**：在 Context Window 即将满时触发压缩或滑动
- **关键信息保留策略**：决定哪些信息必须保留、哪些可以丢弃
- **跨 Session 持久化**：将循环状态保存到磁盘，支持中断恢复

### 4. 终止条件系统（Termination Conditions）

循环工程最关键的课题之一：**什么时候停？**

| 条件 | 说明 | 优先级 |
|------|------|--------|
| **任务完成** | 质量门控达标，所有子目标验证通过 | 最高——正常结束 |
| **步数上限** | 超出最大迭代步数（如 100 步） | 保护性停止 |
| **时间上限** | 超时保护（如 30 分钟） | 保护性停止 |
| **Token 预算** | 成本控制（消耗超过 N 个 Token） | 保护性停止 |
| **死循环检测** | 检测到"原地打转"（重复相同动作 N 次） | 异常停止 |
| **不可恢复错误** | Fatal 级错误触发早停 | 异常停止 |
| **人工打断** | 用户中途注入干预信号 | 外部停止 |

### 5. 错误处理与恢复（Error Handling & Recovery）

```
Transient（瞬态）    → 指数退避重试（网络抖动、限流）
Recoverable（可恢复） → 切换备用方案（接口不可用、工具切换）
Fatal（致命）       → 早停并上报人工（权限拒绝、数据损坏）
```

Loop Engineering 进一步引入**错误分类反馈机制**：
- 将错误类型编码反馈给下一轮循环，让 Agent 学会避免同类错误
- 错误频率统计：当同一类错误反复出现时升级处理策略

> 详见 [[Exponential_Backoff]]

### 6. 状态持久化（State Persistence）

每完成一个 Action，持久化 `(step_id, state_snapshot, decision_log)`，核心能力：

| 能力 | 说明 |
|------|------|
| **断点续传** | Agent 运行中断后可从上一步恢复，不必从头重跑 |
| **回放调试** | 开发者可以回溯 Agent 每一步的决策轨迹 |
| **审计合规** | 完整的行为轨迹记录，满足合规要求 |
| **跨 Session 延续** | 今天没跑完的任务，明天接着跑 |

> 这是 [[Agent沙箱工程]] 和 [[Agent实例生命周期管理]] 在循环维度上的延伸。

### 7. 循环控制理论（Control Theory）

Agent Loop 可建模为控制系统，运用 PID（比例-积分-微分）控制理论来稳定循环：

```
u(k) = Kp·e(k) + Ki·Σe(j) + Kd·(e(k)-e(k-1))
```

- `e(k)` = 质量误差（目标质量 - 当前质量）
- `Kp·e(k)` = **比例项**：对当前偏差立即响应
- `Ki·Σe(j)` = **积分项**：对长期偏差累积修正
- `Kd·(e(k)-e(k-1))` = **微分项**：预测偏差变化趋势，提前抑制震荡

**PID 在 Agent Loop 中的应用：**

| 控制项 | Agent 对应 | 效果 |
|--------|-----------|------|
| 比例控制 | 根据当前质量差距调整修复力度 | 快速响应，但可能过冲 |
| 积分控制 | 记录历史错误模式，逐步调整策略 | 消除累积偏差 |
| 微分控制 | 预测质量变化趋势，提前干预 | 防止震荡，提高稳定性 |

### 8. 收敛检测（Convergence Detection）

循环是否在"真正进步"？Loop Engineering 引入收敛检测机制：

- **进步率监控**：每轮验证分数是否单调递增？若连续 N 轮无明显进步则触发策略调整
- **状态重复检测**：比较当前状态与历史状态，检测是否回到同一点
- **策略切换触发**：当当前策略收敛缓慢时，主动切换解决路径

## 设计原则

### 1. 渐进式复杂度

不要在一开始就设计八步完整循环。从最简单的 ReAct（Think → Act → Observe）开始，按需逐步增加 Verify、Critique、Repair 等阶段。

```
ReAct → 加 Verify → 加 Critique/Repair → 加 Plan/Decompose → 加跨 Session 持久化
```

### 2. 终止条件是第一公民

循环设计的第一步不是"怎么开始"，而是**"什么时候停"**。明确的终止条件比复杂的循环逻辑更重要。

### 3. 错误要结构化返回

工具错误不是 Exception——它是**Data**。将错误信息以结构化格式返回给 LLM，让模型能自主反思和调整，而不是让 Harness 层静默重试。

> 详见 [[摘要-tool-error-is-data]]

### 4. 独立验收优于自我评估

让"做事的 Agent"和"验收的 Agent"分开，而不是让同一个 Agent 对自己更严格。这避免了自我称赞的偏差。

> 详见 [[Harness_Engineering#反馈循环：Agent 进步的真正机制]]

### 5. 状态持久化是长程任务的前提

没有状态持久化，Agent 跑超过上下文窗口长度的任务时必然失败。每步持久化 `(step_id, state, decision_log)` 是长程可靠运行的最低要求。

### 6. 资源预算贯穿全循环

成本（Token、Time、Money）不是事后优化，而是循环控制的内生变量——每一步都应该知道还剩多少"预算"。

> 详见 [[Cost_Aware_Budget_Gates]]

## 与 Agent Loop 的对照

| 维度 | Agent Loop | Loop Engineering |
|------|-----------|-----------------|
| **抽象层级** | 实现层——循环的运行时 | 元层（Meta-layer）——设计循环的方法论 |
| **关注点** | 每一轮循环怎么转 | 整个循环系统怎么设计 |
| **核心问题** | 当前步该做什么？ | 这个循环应该长什么样？ |
| **产出物** | 运行的循环实例 | Loop 设计规范、终止条件集、容错策略 |
| **失败模式** | 单次工具调用失败 | 循环发散、资源耗尽、死循环 |

## 知识冲突

- **与 [[Agent_Loop]] 的边界**：目前知识库中 [[Agent_Loop]] 已包含部分 Loop Engineering 的内容（如 PID 控制、状态持久化、终止条件）。Loop Engineering 作为第四层工程范式的独立概念，将这部分内容提升为**元层设计方法论**，而非 Agent Loop 的实现细节。二者是互补的上下层关系。
- **与 [[RLHF]]/[[RL]] 的关系**：Loop Engineering 的"反馈循环"设计与强化学习的 Reward Signal 设计有概念交集。区别在于：RL 的反馈是**训练时**的梯度信号，Loop Engineering 的反馈是**推理时**的决策修正。二者可互补但不等同。

## 关联连接
- [[Agent_Loop]] — Agent 循环的运行时机制，Loop Engineering 的实现对象
- [[Harness_Engineering]] — 第三层工程范式，Loop Engineering 的基础设施层
- [[Context_Engineering]] — 第二层工程范式，Loop Engineering 依赖的信息组织方式
- [[Prompt_Engineering]] — 第一层工程范式，Loop 中每一轮调用的输入设计
- [[摘要-agent-loop-guide]] — Agent Loop 设计完整指南源摘要
- [[Tool_Calling]] — 工具调用机制，循环中的 Action 阶段基础
- [[摘要-tool-error-is-data]] — 错误结构化的设计哲学
- [[Exponential_Backoff]] — 瞬态错误的指数退避重试策略
- [[Cost_Aware_Budget_Gates]] — 成本感知的预算门控，贯穿全循环的资源控制
- [[Agent沙箱工程]] — Agent 执行环境，循环的物理运行层
- [[Agent实例生命周期管理]] — Agent 全生命周期管控，循环的平台工程维度
- [[Agent_Observability]] — 循环的可观测性，Harness 第 6 核心元件
- [[Eval_Harness]] — 循环的外部验证层，Harness 第 7 核心元件
- [[Agent_As_Judge]] — 独立验收机制，循环中 Critique 阶段的核心模式
- [[Multi_Agent_System]] — 从单 Agent 循环扩展到多 Agent 协作循环
- [[Agent_Orchestration_Patterns]] — 多 Agent 编排模式，循环在协作场景的展开
- [[Hierarchical_Task_Decomposition]] — 层级任务分解，循环中 Decompose 阶段的深度展开
- [[Failure_Injection_Chaos_Eval]] — 混沌评估，检验循环容错能力的测试方法
- [[Claude_Code_Dynamic_Workflows]] — Opus 4.8+ 自生成 Workflow，Loop Engineering 在 Claude Code 中的高级实现
