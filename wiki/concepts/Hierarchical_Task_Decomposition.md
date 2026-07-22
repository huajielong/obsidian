---
title: "Hierarchical Task Decomposition（层级任务分解）"
type: concept
tags: [agentic AI, 编排, 任务分解, 多层监督, supervisor, plan-execute, 规划执行]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
  - wiki/sources/摘要-agent-loop-guide.md
last_updated: 2026-07-22
---

# Hierarchical Task Decomposition（层级任务分解）

## 定义

Hierarchical Task Decomposition 是一种 Multi-Agent 编排模式：通过 **Supervisor → Worker → Sub-worker** 的多层递归结构，将复杂任务逐层分解为可执行的子任务。这是 [[Agent_Orchestration_Patterns]] 中 Supervisor-Worker 模式的深层变体。

## 核心特征

| 特征                   | 说明                                             |
| -------------------- | ---------------------------------------------- |
| **至少 2 层 Recursion** | Supervisor → Worker 还不够，需要 Worker → Sub-worker |
| **逐层 Scope 缩减**      | 每下一层任务范围更窄、Context 更聚焦                         |
| **结果向上汇总**           | Sub-worker → Worker → Supervisor 逐层合并          |

## 解决的问题

- **Context 爆炸**：单 Agent 无法处理超长任务
- **责任模糊**：没有清晰的任务边界导致 Agent 越界
- **评审困难**：大型任务难以一次性验证正确性

---

## Plan-Execute 模式：工程实践展开

层级任务分解的核心理念在实践中演化为 **Plan-Execute 模式**——将 Agent 执行过程显式划分为规划阶段和执行阶段。这与 [[Agent_Loop]] 中的"规划→行动→观察"循环一脉相承，但在工程实现上更强调**规划的可见性、可校正性和可复用性**。

### Plan-Execute 架构总览

```
┌─────────────────────────────────────────────────┐
│                Orchestrator                      │
│  Plan: 任务分解 → 子任务DAG → 依赖排序              │
│  Dispatch: 分配子任务 → 监控进度 → 动态调整          │
│  Synthesize: 汇聚结果 → 全局一致性检查 → 最终输出     │
└────────────┬──────────────────────┬──────────────┘
             │  Plan 阶段            │  Execute 阶段
             ▼                      ▼
     ┌──────────────┐     ┌──────────────────┐
     │   Plan Agent  │     │  Worker Agent 1   │
     │   (战略层)    │     │  (执行单元)        │
     │               │     ├──────────────────┤
     │ • 需求分析     │     │  Worker Agent 2   │
     │ • 任务分解     │────▶│  (执行单元)        │
     │ • 资源估算     │     ├──────────────────┤
     │ • 风险评估     │     │  Worker Agent 3   │
     │ • 规划输出     │     │  (执行单元)        │
     └──────────────┘     └──────────────────┘
```

### 1. Plan 阶段：显式规划

#### 规划输出契约

Plan Agent 产出的规划文档应包含以下结构化信息：

```yaml
plan:
  task_id: "T-001"
  goal: "完成功能 X 的开发"
  subtasks:
    - id: "S1"
      type: "research"
      description: "调研现有方案"
      depends_on: []
      estimated_cost: "2k tokens"
      acceptance_criteria: "输出调研报告含 3 种方案对比"
    - id: "S2"
      type: "implementation"
      description: "实现核心逻辑"
      depends_on: ["S1"]
      estimated_cost: "10k tokens"
      acceptance_criteria: "代码通过单元测试"
    - id: "S3"
      type: "verification"
      description: "集成测试验证"
      depends_on: ["S2"]
      estimated_cost: "5k tokens"
      acceptance_criteria: "E2E 测试通过"
  risk_assessment:
    - "S2 依赖外部 API，需准备 Mock 方案"
    - "S1 可能返回 no-go，需准备备用方案 B"
```

#### 规划阶段的工程要点

| 要点 | 说明 | 反模式 |
|------|------|--------|
| **规划可校正** | Plan 不是一次性输出的，在执行过程中可被调整 | 规划输出后不再修改，导致执行僵化 |
| **依赖显式化** | 子任务的依赖关系必须显式声明 | 隐式依赖导致 Worker 等待阻塞 |
| **成本可估算** | 每个子任务预估 Token/API 成本 | 不做估算导致预算超标 |
| **接受标准** | 每个子任务有明确的完成定义（DoD） | 模糊的接受标准导致 Worker 产出不可验收 |
| **风险预判** | 标记高风险子任务，准备降级/备用方案 | 遇到障碍才处理，浪费执行轮次 |

### 2. Execute 阶段：分工执行

#### 执行模式对比

| 模式 | 调度策略 | 适用场景 | 优势 | 劣势 |
|------|---------|---------|------|------|
| **串行执行** | 按依赖顺序逐一执行 | 强依赖链任务 | 简单可控，容易调试 | 慢，资源利用率低 |
| **并行执行** | 无依赖的子任务同时启动 | 独立子任务 | 快，充分利用 Worker | 需要更多 Worker，协调复杂 |
| **动态调度** | 根据执行进度动态分配 | 子任务数量不固定 | 灵活，适应性强 | 实现复杂，调度开销大 |
| **迭代精化** | 先浅后深，逐步细化子任务 | 探索性任务 | 容忍不确定性 | 可能多次返工 |

#### Worker 执行契约

Worker 在执行子任务时应遵循统一的输入/输出契约：

```
输入:
  - subtask_id: "S2"
  - description: "实现核心逻辑"
  - context: "[来自 Plan 的全局上下文 + 依赖子任务的输出]"
  - constraints: "不超过 500 行代码，Python 3.12+"

输出:
  - subtask_id: "S2"
  - status: "completed" | "failed" | "partial" | "blocked"
  - artifacts: [...]
  - token_cost: 9523
  - summary: "实现了核心逻辑，通过了 8/10 单元测试"
  - issues: ["问题 1：边缘 Case 未覆盖", "问题 2：依赖上游接口变更"]
```

### 3. 反馈循环：Plan → Execute → Monitor → Replan

Plan-Execute 不是一次性的"规划→执行"线性流程，而是一个带反馈的闭环：

```
       初始需求
          ↓
   ┌─→ Plan（规划）──────── ─┐
   │      ↓                  │
   │  Execute（执行）         │  每次 Replan 可能调整：
   │      ↓                  │   - 新增子任务
   │  Monitor（监控）── 异常 ─┤   - 修改优先级
   │      │ 正常              │   - 重新分配 Worker
   │      ↓                  │   - 放弃不可行路径
   │  Verify（验证）── 不通过 ─┘
   │      │ 通过
   │      ↓
   └── Synthesize（汇总输出）
```

#### 四种 Replan 触发条件

| 触发条件 | 示例 | 响应策略 |
|---------|------|---------|
| **子任务失败** | Worker 返回 status: "failed" | 分析失败原因→重试/降级/重新规划 |
| **上下文变化** | 执行中发现新信息 | 更新全局 Context→相关子任务重新规划 |
| **估计偏差** | 实际 Token 消耗超出预估 2 倍 | 标记成本异常→调整后续子任务预算 |
| **外部中断** | 用户中途修改需求 | 暂停当前执行→重新 Plan |

### 4. 工程实现模式

#### 模式 A：单 Agent Plan-Execute（适合简单任务）

```
同一 Agent 先 Plan（输出规划到 artifact），
然后 self-execute（逐条执行规划中的子任务）。
```

- **适合**：任务复杂度较低，Context 窗口足够的场景
- **实现**：ReAct Loop 中嵌入 Plan 步骤
- **风险**：Agent 可能 Plan 完不 follow plan，直接"走捷径"

#### 模式 B：双 Agent Plan-Execute（适合中等复杂度）

```
Plan Agent（负责制定规划 + 监控进度）
    ↕ 契约通信
Worker Agent（负责执行具体子任务）
```

- **适合**：需要多人协作视角的任务
- **实现**：两个独立 Agent session，通过文件/消息传递状态
- **优势**：Plan Agent 保持全局视角，不受执行细节干扰

#### 模式 C：多 Agent 层级 Plan-Execute（适合复杂任务）

```
Supervisor Plan Agent
    ├── Worker Agent 1（子领域 1）
    │     └── Sub-worker Agent 1.1
    │     └── Sub-worker Agent 1.2
    ├── Worker Agent 2（子领域 2）
    └── Worker Agent 3（子领域 3）
```

- **适合**：跨领域复杂任务（如全栈开发 + DevOps + 文档）
- **实现**：[[Claude_Code_Dynamic_Workflows]] / [[LangGraph]] / [[AutoGen]]
- **关键成功要素**：层间通信契约、Context 隔离、结果汇聚策略

### 5. 实践的注意事项

| 陷阱 | 现象 | 解决方案 |
|------|------|---------|
| **Over-planning** | 90% Token 花在规划上，实际执行时间不足 | 设置规划 Token 预算（如总预算的 20%） |
| **Plan 漂移** | Agent 执行中偏离原始规划 | 执行前让 Worker 复述子任务目标，加入 Plan 一致性检查 |
| **假性分解** | 子任务过于粗糙，无法独立执行 | 设置子任务粒度规则（如：每个子任务 ≤ 5 步可完成）|
| **上下文泄露** | Sub-worker 被喂入过多无关上下文 | 严格按子任务 scope 裁剪 Context |
| **聚合损失** | 各部分产出优秀但汇总后不自洽 | 加入全局一致性校验步骤，让 Plan Agent 做最终审查 |
| **忽略失败反馈** | 失败被静默吞掉，Plan 继续按原路线执行 | 强制 Worker 报告 failure + root cause，触发 Replan |

---

## 与现有框架的映射

| 框架/系统 | Plan-Execute 实现方式 |
|-----------|---------------------|
| **[[Claude_Code_Dynamic_Workflows]]** | Orchestrator Agent 自动生成 Workflow 脚本 → 子 Agent 并行执行 |
| **[[LangGraph]]** | StateGraph 中定义 Plan 节点 → 条件边 → Agent 执行节点 |
| **[[AutoGen]]** | GroupChat Manager 做任务调度，Agent 按角色分工 |
| **[[OpenAI_Agents_SDK]]** | Handoff 机制将子任务分配给 Specialist Agent |
| **[[CrewAI]]** | Process="hierarchical" 模式下 Manager Agent 自动分配任务 |
| **ReAct 手写 Loop** | Step 1: 输出 Plan → Step 2-N: 逐个执行 → 最终 Verify |

---

## 关联连接

- [[Agent_Orchestration_Patterns]] — 五大编排模式中的 Supervisor-Worker
- [[Contract_Driven_Handoffs]] — 层级间的契约确保信息正确传递
- [[Work_Boundary]] — 每层有自己的工作边界
- [[Claude_Code_Dynamic_Workflows]] — 在 Dynamic Workflows 中自动分解
- [[Agent_Loop]] — Plan-Execute 是 Agent Loop 的"规划→行动"阶段的工程细化
- [[Multi_Agent_System]] — 多 Agent 场景下 Plan-Execute 的典型实现路线
- [[Spec_Driven_Development]] — Formal Spec 驱动开发，与 Plan-Execute 互补：Spec 定义"做什么"，Plan 定义"怎么做"
- [[Cost_Aware_Budget_Gates]] — Plan 阶段的成本估算直接影响 Budget Gate 的设置
- [[Claude_Code_Subagent]] — Subagent 作为 Plan-Execute 中 Worker 的执行单元
- [[Tool_Calling]] — Worker 执行子任务时调用的工具链
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源
- [[摘要-agent-loop-guide]] — Agent Loop 指南中的 Plan-Execute 实践参考
