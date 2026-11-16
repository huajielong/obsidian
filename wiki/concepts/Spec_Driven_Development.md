---
title: "Spec-driven Development（规范驱动开发）"
type: concept
tags: [agentic AI, 规范驱动, formal spec, DSPy, 结构化开发, Spec_Kit, Kiro]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
  - "raw/09-archive/The AI Engineering Skills Map 人工智能工程技能图谱.md"
last_updated: 2026-11-10
---

# Spec-driven Development（规范驱动开发）

## 定义

Spec-driven Development（SDD，规范驱动开发）主张**先写规范、再写代码**：规格说明（Spec）是唯一事实源（Single Source of Truth），代码、测试与任务清单都是规范的产物。

> Specifications don't serve code — code serves specifications.

SDD 在 2025 年后成为 AI 编码领域的主流方法论，但"规范"一词在两种不同层次上被使用，需要区分。

## 两种含义辨析

| 层次 | 回答的问题 | 规范形态 | 代表 |
|------|-----------|----------|------|
| **开发方法论层** | 软件开发流程如何组织 | 人类可读、结构化的 spec 文档（用户故事、验收标准、计划、任务） | GitHub Spec Kit、AWS Kiro |
| **任务契约层** | Agent 单次任务的接口如何约束 | 机器可读的 Formal Spec（JSON Schema / Pydantic / DSPy Signature） | [[DSPy]]、Structured Output、Tool Schema |

两层互补：方法论层决定"整个项目怎么推进"，契约层决定"每一步交给 Agent 的输入输出长什么样"。Spec Kit 产出的任务最终仍要靠 JSON Schema 等契约交给 Agent 执行。

## 方法论层：Spec Kit 式工作流

GitHub 于 2025 年 9 月开源 [Spec Kit](https://github.com/github/spec-kit)，把 SDD 固化为一条可执行的命令链，支持 Claude Code、GitHub Copilot、Gemini CLI、Cursor 等 Agent 工具。

### 五阶段

1. **Constitution（项目宪法）** — 定义项目级不可违背的原则：技术偏好、质量门禁、测试要求、禁区。后续所有 spec / plan 都要通过宪法检查。
2. **Specify（做什么）** — 输出 `spec.md`：用户故事（按 P1/P2/P3 排优先级）、验收场景（Given/When/Then）、功能需求（FR-xxx）、成功标准（SC-xxx）、假设与非目标。**此阶段刻意不写技术栈**，避免方案先入为主。
3. **Plan（怎么做）** — 输出 `plan.md`：技术选型、架构、数据模型、接口设计、约束与风险。
4. **Tasks（拆任务）** — 输出 `tasks.md`：按依赖关系拆成 Agent 可逐条执行的小任务，标注可并行项与涉及文件。
5. **Implement（执行）** — Agent 按任务清单实现，每完成一项勾选一项，规范全程可追溯。

### 工件链

```
constitution.md → spec.md → plan.md → tasks.md → code + tests
```

规范不是写完就丢的文档，而是纳入版本控制、随代码一起演进的**活工件**。[[AI_SDLC]] 中的 `intent.md → spec.md → plan.md → PR` 工件链是同一思想在 SDLC 层面的展开。

### 代表实现

- **GitHub Spec Kit** — 开源工具包，以 slash commands（`/speckit.specify`、`/speckit.plan`、`/speckit.tasks`、`/speckit.implement` 等）落地，可接入 [[Claude_Code]] 等 Agent
- **AWS Kiro** — 规范驱动的 Agentic IDE，产物为 `requirements.md`（EARS 语法：WHEN…THE SYSTEM SHALL…）→ `design.md` → `tasks.md`
- **Tessl** — 以 spec 为中心的开发平台，同一思潮的商业化探索

> 说明：本节依据 Spec Kit / Kiro 公开文档整理，暂无对应 raw 源文件。

## 任务契约层：Formal Spec

Spec-driven Development 在 Agent 工程中的狭义用法：**Agent 的任务由 Formal Spec（YAML / JSON Schema / DSPy Signature）定义，而非自由形式的 Prompt**。这使得 Agent 的行为可预测、可验证、可审计。

> Task 由 Formal Spec 定义、不是自由 Prompt。— 进阶 Agentic 概念地图

### 规范是工程师的新工作重心

吴恩达在 [[AI_Engineering_Skills|AI 工程技能图谱]] 中指出：给定清晰的规范，编程智能体的交付能力正在快速提升，因此工程师的工作重心正转向**决定规范里应该写什么**。这需要产品感、业务上下文与客户目标的理解，工程师应从"拿到像素级设计并实现"转向参与塑造构建方案（Shaping the build）。

### 与传统 Prompt 的对比

| 维度 | 自由 Prompt | Spec-driven |
|------|-----------|-------------|
| 定义方式 | 自然语言描述 | 形式化 Schema / 结构化文档 |
| 可验证性 | 模糊、难量化 | 精确、可自动检查 |
| 可复用性 | 低（每次要重写） | 高（Spec 可共享） |
| Agent 自由度 | 高（易越界） | 低（Spec 约束边界） |
| 失败定位 | 只能看最终输出 | 可定位到具体需求条目 |

## 动到哪一层

- **Types（Spec = Code）** — Formal Spec 本身是 [[Work_Boundary]] Types 层的一部分
- **流程层** — 方法论层的 SDD 位于 [[Harness_Engineering]] 的外围流程控制：它规定 Agent 在什么阶段、依据什么工件、产出什么交付物

## 边界与风险

- **Spec Drift（规范漂移）** — 代码改完不回写 spec，规范很快失真；必须把 spec 与代码放在同一 PR 中维护。
- **过度规范化** — 把实现细节全部写进 spec，等于用自然语言重写一遍代码，返工成本高于收益。
- **上游错误放大** — spec 里的错误会被 Agent 忠实且大规模地执行，评审 spec 的优先级高于评审代码。
- **不适用场景** — 探索性原型、一次性脚本、需求高度不确定的早期阶段，vibe coding 反而更快；SDD 适合需求相对明确、需要长期维护的工程。

## 关联连接

- [[AI_SDLC]] — 文档层技术规格：spec.md 与 Formal Spec 互补（前者定"做什么"，后者约束"怎么做"）
- [[AI_Engineering_Skills]] — 「塑造构建方案」技能：规范定义是工程师的新价值重心
- [[Contract_Driven_Handoffs]] — Spec 是契约的延伸
- [[DSPy]] — Spec-driven 的核心框架实现
- [[Work_Boundary]] — Spec 是工作边界的精确定义
- [[Taste_Invariants]] — Spec 可视为 Invariants 的一种形式
- [[Claude_Code_Slash_Commands]] — Spec Kit 以 slash commands 形式接入 Claude Code
- [[Harness_Engineering]] — SDD 属于模型外围的流程与执行控制层
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 核心来源（任务契约层）
- [[摘要-ai-engineering-skills-map]] — 技能图谱来源摘要
