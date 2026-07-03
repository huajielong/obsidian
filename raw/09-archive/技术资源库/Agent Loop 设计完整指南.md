---
title: "Agent Loop 设计完整指南"
source: "feishu/wiki/技术资源库"
node_token: "ArjLwFI5RibQh5kpmf6c1U1Yndg"
obj_token: "KoDedCpAIok55nxT3crcL4CunZf"
export_date: "2026-07-03"
---

# Agent Loop 设计完整指南

## 📌 概述

Agent Loop 是让 AI 智能体自主完成任务的核心机制。它将大模型从"文本生成器"升级为"能完成任务的执行系统"。

**核心思路：** 让 Agent 自主完成任务循环（执行→验证→下一任务），通过明确的"完成+验证"判断机制实现可靠交付。

---

## 🎯 核心定义

### 什么是 Agent Loop？

Agent Loop = 调用模型 → 判断是否要用工具 → 执行工具 → 把结果回喂给模型 → **重复**

直到模型认为信息足够，输出最终答案为止。

### 基础范式：ReAct 循环

最早由 Yao et al. 于 2022 年提出：

```Plain Text
Thought → Action → Observation → Thought → Action → ...

```

**核心特征：**

- 推理（Reasoning）与行动（Acting）交错执行
- 每次行动后都会观察结果，再决定下一步

---

## 📜 演进历程

| 年份 | 关键演进 | 来源 |
|-|-|-|
| **2022** | ReAct 循环（基础框架） | [论文原文](https://arxiv.org/abs/2210.03629) |
| **2023** | Plan-and-Execute（规划-执行分离） | [LangChain 官方博客](https://www.langchain.com/blog/plan-and-execute-agents) |
| **2023** | Reflexion（自我反思机制） | [论文原文](https://arxiv.org/abs/2303.11366) |
| **2024-2026** | 生产级闭环系统（八步完整循环） | OpenClaw、Quest、悟空等实战系统 |

---

## 🔧 生产级标准化循环（八步法）

### 完整闭环流程

```Plain Text
Plan（规划）→ Decompose（拆解）→ Retrieve（检索） 
→ Act（执行）→ Verify（验证）→ Critique（审查） 
→ Repair（修复）→ Commit（提交）

```

### 各阶段说明

| 阶段 | 职责 | 输入 | 输出 |
|-|-|-|-|
| **Plan** | 制定整体计划 | TaskSpec + ExecutionContext | Plan |
| **Decompose** | 任务拆解 | Plan + ExecutionContext | List |
| **Retrieve** | 检索相关信息 | List + ExecutionContext | EvidenceBundle |
| **Act** | 执行具体操作 | List + EvidenceBundle | ExecutionOutputs |
| **Verify** | 验证结果质量 | ExecutionOutputs + TaskSpec | VerificationVerdict |
| **Critique** | 分析失败原因 | ExecutionOutputs + Verdict | CritiqueDiagnosis |
| **Repair** | 修复问题 | ExecutionOutputs + Diagnosis | ExecutionOutputs |
| **Commit** | 提交最终结果 | ExecutionOutputs + TaskSpec | AgentResult |

### 状态机形式化定义

Agent Loop 是一个有限状态机：

```TypeScript
L = (S, s₀, Σ, δ, F)

S = {PLAN, DECOMPOSE, RETRIEVE, ACT, VERIFY, CRITIQUE, REPAIR, COMMIT, FAIL, HALT}
s₀ = PLAN
F = {COMMIT, FAIL, HALT}

```

关键状态转换：

- `δ(VERIFY, quality_gate_fail) = CRITIQUE`
- `δ(CRITIQUE, diagnosis_complete) = REPAIR`
- `δ(REPAIR, repair_success) = VERIFY`
- `δ(VERIFY, quality_gate_pass) = COMMIT`

---

## 🛠️ 实战案例分析

### 1. OpenClaw - 三层架构

**核心特性：**

- 三层关注点分离（外层战略、中层协调、内层感知）
- 双重队列管理（Global + Session）
- 七重容错策略
- 沙箱隔离机制
- 8+ 生命周期 Hook 点

**详细文档**（51CTO，2026-03-29）

### 2. Quest - 自主编程闭环

**核心流程：** Spec → Coding → Verify

- **Spec 阶段**：生成技术规格书（功能描述、验收标准、技术约束、测试要求）
- **Coding 阶段**：根据 Spec 自主实现，无需用户监督
- **Verify 阶段**：自动运行测试，未通过则进入下一轮迭代

**对抗模型"退缩"倾向：**

- 模型面对复杂任务倾向于模糊回答或询问更多信息
- Quest 通过架构设计推动模型完成完整任务链路

**详细案例**（掘金，2026-01-21）

### 3. 悟空Agent - 可收敛循环

**核心原则：可收敛**

```Python
class AgentLoop:
    def __init__(self, max_iterations: int = 20):
        self.max_iterations = max_iterations
        self.progress_tracker = ProgressTracker()
    
    def run(self, task: Task) -> Result:
        for i in range(self.max_iterations):
            # 1. 规划下一步
            plan = self.think(task, self.progress_tracker.history)
            
            # 2. 检测是否在原地打转
            if self.progress_tracker.is_stalled(plan):
                return self.escalate_or_pivot(task)
            
            # 3. 执行并观察结果
            result = self.act(plan)
            observation = self.observe(result)
            
            # 4. 判断是否达成目标
            if self.is_task_complete(task, observation):
                return self.package_deliverable(task, observation)
            
            # 5. 更新进度追踪
            self.progress_tracker.record(plan, result, observation)
        
        # 超过最大轮次，交还给人
        return self.handover(task)

```

**关键特性：**

- 进度追踪（防止原地打转）
- 迭代上限（防止无限循环）
- 优雅降级（超限后转人工）

**详细说明**（今日头条，2026-03-25）

### 4. OpenHarness - 六阶段闭环

**流程：**

1. 感知与理解：解析任务意图
2. 决策与工具调用生成：生成结构化指令
3. 权限校验与安全拦截：安全检查
4. 工具执行与环境交互：原子性操作
5. 结果回收与状态观测：捕获环境变化
6. 反馈注入与下一轮决策：继续循环

**文档链接**（CSDN，2026-04-09）

---

## 📊 工程化关键技术

### 1. 上下文管理

**分层结构：**

```Plain Text
┌────────────────────────────────────┐
│ Layer 1: Working Memory (近期原文) │ ← 最近 N 轮完整保留
├────────────────────────────────────┤
│ Layer 2: Episodic Memory (中期摘要)│ ← 关键事件压缩存储
├────────────────────────────────────┤
│ Layer 3: Semantic Memory (长期事实)│ ← 结构化存储，按需检索
└────────────────────────────────────┘

```

**动态压缩策略：**

- 模型自主判断何时压缩总结
- 非机械式"保留最近 N 轮"
- 基于多因素触发（轮数阈值、上下文长度、阶段切换）

### 2. 失败处理

**失败分类：**

| 类型 | 场景 | 策略 |
|-|-|-|
| **Transient** | 网络抖动、限流、超时 | 指数退避重试 |
| **Recoverable** | 接口不可用、模型超载 | 切换备用方案 |
| **Fatal** | 权限拒绝、参数非法 | 早停并上报人工 |

**终止条件多维度判断：**

| 维度 | 触发条件 | 处理方式 |
|-|-|-|
| 任务完成 | LLM 显式输出"完成"标记 | 进入结果汇总 |
| 步数上限 | step ≥ max_steps | 强制中止 + 摘要返回 |
| 时间上限 | duration ≥ max_time | 强制中止 + 摘要返回 |
| 死循环检测 | 相同 Action 连续多次 | 触发 Replan 或上报 |
| Token 预算 | total_tokens ≥ budget | 上下文压缩或终止 |
| 显式失败 | 关键 Action 返回不可恢复错误 | 降级或人工介入 |

### 3. 控制理论应用

**PID 控制器：**

```TypeScript
u(k) = K_p · e(k) + K_i · Σe(j) + K_d · (e(k) - e(k-1))

```

其中：

- `e(k)` = 质量误差（目标质量 - 当前质量）
- `u(k)` = 修复行动强度
- `K_p`（比例）：根据当前误差调整
- `K_i`（积分）：累积误差推动升级
- `K_d`（微分）：预防震荡

**质量演化模型：**

```Plain Text
y(k+1) = y(k) + G · u(k) + w(k)

```

- `G` = 修复增益（每次修复的预期改进比例）
- `w(k)` \~ N(0, σ²) = 过程噪声（模型随机性）

### 4. 状态持久化

**必要性：**

- 长任务 Agent 需要支持从中断点恢复
- 防止进程异常导致整个会话作废

**最小可行方案：**

- 每完成一个 Action，持久化 `(step_id, state_snapshot, decision_log)`
- 重启时按 step_id 倒序找最近有效快照恢复执行

---

## 🎓 你提到的"工具链组合"解读

### 概念对应关系

```Plain Text
规划 → PRD → 调研 → 构建 → 审查 → 测试

```

这个思路是对 **Plan-and-Execute 范式**在软件工程领域的具体化：

| 范式阶段 | 工具链组合 | 说明 |
|-|-|-|
| **Plan** | 规划 → PRD | 明确目标和验收标准 |
| **Execute** | 调研 → 构建 | 收集信息并实现功能 |
| **Verify** | 审查 → 测试 | 验证质量并确保符合要求 |
| **Loop** | 验证未通过 → 修复 → 再验证 | 持续迭代直到达标 |

### 关键点

1. **"完成+验证"判断机制**：

   - 需要明确的验收标准（Acceptance Criteria）
   - 自动化验证（测试、lint、规范检查）
   - 验证失败后自动进入修复流程
2. **工具链组合优势**：

   - 每个步骤都有独立工具支持
   - 标准化的工作流
   - 便于并行化和复用

---

## 📚 核心参考资源

### 必读文献

1. **Chapter 15: The Agent Loop — Bounded Control, Verification, and Failure Recovery**

   - 最权威的工程化定义
   - 数学化描述（有限状态机、PID 控制）
   - 生产级实践指导
2. **AI Agent 的 Loop 设计:范式、上下文与失败处理的工程权衡**

   - 最完整的方法论梳理
   - Loop 范式选择指南
   - 上下文管理策略
   - 失败恢复实践
3. **AI应用的下半场：Agent Looping**

   - 单智能体 vs 多智能体舰队模式
   - 开放循环 vs 闭环循环
   - 2026 生产级框架推荐（LangGraph、CrewAI、AutoGen）

### 实战案例

1. **OpenClaw Agent Loop核心引擎**

   - 三层架构详解
   - 七重容错策略
   - Plugin Hook 机制
2. **从结对到自主：让AI交付可运行的工程成果**

   - Quest 的自主编程实践
   - Spec 驱动开发流程
   - 对抗模型退缩倾向
3. **悟空Agent的真正价值：把LLM变成可治理的执行系统**

   - 可收敛循环设计
   - 进度追踪机制
   - 原地打转检测

---

## 🎯 实践建议

### 1. Loop 范式选择

| 任务特征 | 推荐范式 |
|-|-|
| 短链路、确定性高 | ReAct |
| 多步骤、可拆分 | Plan-and-Execute + Replan |
| 有明确成败判断 | 引入 Reflexion 自校验 |
| 复杂协同任务 | Hierarchical / Multi-Agent |

### 2. 闭环 vs 开放循环

| 类型 | 特点 | 适用场景 |
|-|-|-|
| **开放循环** | 高创新、高成本 | 科研探索、创新实验 |
| **闭环循环** | 高可靠、可落地 | 商业落地、业务自动化 |

**生产环境推荐：** 闭环循环

- 目标 + 步骤 + 评估关卡 + 停止条件
- 成本可控、输出稳定

### 3. 避坑指南

| 问题 | 表现 | 解决方案 |
|-|-|-|
| 上下文窗口耗尽 | Loop 次数多、工具输出长 | 摘要返回、分层管理、任务拆分 |
| 模型选错工具 | 工具描述不清或重叠 | 写清适用场景、避免相似描述 |
| 无限循环 | 陷入两个状态反复跳转 | 设置迭代上限、检测原地打转 |
| 任务发散 | 从简单任务越做越偏 | 明确目标约束、定期审查进度 |

---

## 🔗 外部资源

### 学术论文

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

### 官方文档

- [LangChain Plan-and-Execute Agents](https://www.langchain.com/blog/plan-and-execute-agents)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

### 社区资源

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw Discord](https://discord.com/invite/clawd)

---

*最后更新：2026-06-13整理者：大龙虾*
