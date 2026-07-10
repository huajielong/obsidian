---
title: "Claude Code Dynamic Workflows"
type: concept
tags: [Claude Code, Dynamic Workflows, 编排, Opus, 多Agent]
sources: 
  - raw/01-articles/05-claude-code-ecosystem.md
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-10
---

# Claude Code Dynamic Workflows（动态工作流）

## 定义

Dynamic Workflows 是 Opus 4.8+ 引入的新机制——让 Claude **自己生成一份 Workflow 脚本，再自己执行**。它建立在 [[Claude_Code_Subagent|Subagent]] 之上：Workflow 脚本去 Orchestrate 一群 Subagent，实现**确定性**的 Loop / 并行 Fan-out / 验证阶段。

## 名字的矛盾

这个名字本身暗含了 Workflow vs Agent 区分的坍塌：

- **Workflow** = 人预先写死的 Code Path（按 Anthropic Building Effective Agents 的定义）
- **Agent** = LLM 在 Runtime 自主决定下一步

Dynamic Workflows 是——**Agent（Claude）在 Runtime 自己决定任务怎么拆，再产出 JavaScript Orchestration Script，丢给独立 Runtime 执行**。人没有写那个 Workflow，是 Agent 写的。它同时是 Agent（谁决定）也是 Workflow（怎么跑）。

## 核心机制：Context Offloading

关键不在并行、在 **Context Offloading**。一般 Subagent / Skill 的每个中间结果都回到 Claude 的 Context Window。Dynamic Workflows 的 Loop、分支、中间结果**全留在 Script 变量里**——只有最终 Verified 答案回到 Context。这是它能跑"几十万行 Codebase 迁移"的原因——因为中间几百次 Agent 调用的杂讯不会塞爆 Context。

## 与 Subagent 的差别

| 维度 | Subagent | Dynamic Workflows |
|------|---------|-------------------|
| 步骤谁决定 | 你手动派，一次一个 | Claude 自己写出多步骤脚本 |
| 控制流 | Model 即兴决定下一步 | 脚本里是**确定性**的 Loop / 并行 / 验证 |
| 适合 | 少数几个并行子任务 | 大型、要穷举或多阶段验证 |
| 关系 | — | DW **建在 Subagent 之上** |

## 什么时候用

- **✅ 用**：要穷举 + 对抗式验证（找完所有 Bug、每个 Finding 再派独立 Agent 反驳）、一次性大迁移、跨多文件同样转换的 Pipeline
- **❌ 别用**：只是想叫一两个 Agent 并行做点事 → 留在 Subagent 即可；小任务直接一条 Prompt 更省

## 核心 Pattern

- **Adversarial Verify**：并行 N 个独立 Skeptic，每个被要求 REFUTE 某个 Claim，若多数 Refute 则 Kill
- **Loop-until-dry**：对未知规模的问题（Bug/Issues），持续 Spawn 寻找直到 K 轮无新发现
- **Judge Panel**：N 个独立解决方案，并行 Judge 评分后合成最优

## 规模上限与质量机制

| 指标 | 数值（官方文档证实） |
|------|-------------------|
| 同时最大 Agent 数 | **16**（不是"几百个同时跑"）|
| 单次 Run 累计上限 | **1,000** 个（防 Runaway）|
| 触发方式 | (1) Prompt 含 `workflow` (2) Saved Command (3) `/effort ultracode` |
| 平台 | Claude Code only（CLI / Desktop / IDE / Agent SDK v2.1.154+）|
| 不是 | Raw API（没有 `/v1/workflows` endpoint）|

**质量机制 — Adversarial Propose / Refute / Converge**：
1. 独立 Agent 各攻一角（Propose）
2. 其他 Agent 试图反驳（Refute）
3. 迭代到收敛（Converge）
4. Merge 前验证

## 什么不是（诚实限制）

| 误解 | 事实 |
|------|------|
| 是通用 Workflow 引擎（如 Airflow / n8n）| ❌ 人不画 DAG，是 Agent 写 Code |
| 无限并行 | ❌ 16 concurrent / 1,000 total per run |
| 已 GA（General Availability）| ❌ Research Preview，定价/可用性可能变 |
| 更多 Subagent = 更高正确率 | ❌ Reliability 提升主要来自"不确定时 Abstain" |
| 免费 | ❌ Token 用量"substantially more" |
| 解决 Dispatch Problem | ❌ "何时该 Fan-out vs 一次仔细做"仍靠 Claude Runtime 判断 |

## 注意

DW 会 Spawn 大量 Agent、消耗大量 Token，不是万灵丹——需权衡 Token Cost 与收益。建议先用 Scoped Task 抓 Consumption 再决定是否采用。

## 关联连接

- [[Claude_Code_Subagent]] — DW 建立在 Subagent 之上
- [[Claude_Code]] — DW 的宿主环境
- [[Claude_Code_Harness]] — 7-Layer Architecture
- [[Harness_Engineering]] — DW 属于 Harness Engineering 范畴
- [[Agent_Orchestration_Patterns]] — Orchestrator-Workers 模式的具体实现
- [[Work_Boundary]] — DW 中 Subagent 的工作边界管理
- [[Agent_As_Judge]] — Adversarial Propose/Refute 质量机制
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 核心来源
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — Opus 4.8 DW 模块补充来源
