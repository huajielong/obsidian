---
title: "AI-Native SDLC（AI 原生软件生命周期）"
type: concept
tags: [AI-SDLC, AI-Native SDLC, 软件开发流程, 文档驱动, spec, intent, plan, 评审门控, 闭环, agentic coding]
sources: [raw/09-archive/The AI-Native SDLC playbook  Claude by Anthropic.md]
last_updated: 2026-09-04
---

# AI-Native SDLC（AI 原生软件生命周期）

> 本页原以「AI-SDLC（文档驱动的 AI 软件生命周期）」记录。2026-09 摄入 Anthropic《The AI-Native SDLC playbook》后，扩展为完整六阶段闭环视图；原「intent.md → spec.md → 开发实现」文档驱动流程是其在 Plan/Design/Build 阶段的骨架。

## 定义

AI-Native SDLC（又称 **Agentic SDLC** / AI SDLC / agentic software development）是对传统软件生命周期的再设计：把「**Plan → Design → Build → Test → Deploy → Maintain**」六阶段的**线性**流程改造为**闭环循环（loop）**，AI 嵌入每个阶段，并在每阶段结束时向版本控制提交一份**下一阶段可直接读取的工件（artifact）**，实现自动化交接与触发。它结合了传统 SDLC 的控制目标（问责与把关）与新的执行方式（agent 产出 + 人在关卡把关）。

**为什么需要它**：当 agentic coding 把 Build 从周/月压缩到小时，**代码不再是瓶颈**——瓶颈移到仍以人类速度运行的 Plan / Review-Test / Deploy，而按人类产出规模设计的审查队列与治理关卡无法跟上 agent 的产出速度（安全团队就是典型：要么 review 排队，要么代码带病上线）。因此流程本身必须经历与实现阶段同等的改造。

核心流转（每阶段提交工件、工件触发下一阶段）：

```
intent.md（Plan）→ spec.md（Design）→ plan.md（Build）→ 代码 diff + 测试 → PR + 评审结论（Deploy）→ 事件记录（Maintain）→ 新的 intent.md …
```

## 六阶段转换对照

| 阶段 | 传统 SDLC | AI-native SDLC |
|------|----------|----------------|
| **Plan** | 委员会收集需求、workshop、手工撰写 | Claude 从源头综合痛点写入 `intent.md`（人类可读、机器可执行） |
| **Design** | 分析师写 spec、设计师再解析 | 需求+设计压缩进一次 agent 会话，由 skills 标准约束，git 版本化 |
| **Build** | 手写代码测试、文档后补 | AI 生成代码测试；制度知识 = 版本化 `CLAUDE.md` + skills |
| **Test** | 阶段边界 QA 关卡 | 持续 evals 织入实现过程 |
| **Deploy** | 人逐行 review、治理靠评审循环 | 多层 agentic review，人审留给受监管/关键代码；hooks 在行动时强制治理 |
| **Maintain** | 人盯生产 | agents 监控线上；控制带被突破 → 诊断写回新 `intent.md` |

## 工件链（Artifact Chain）：提交链即审计链

每个阶段结束时提交一个版本控制工件，下一阶段读它开始：

| 阶段 | 提交的工件 | 触发 |
|------|-----------|------|
| Plan | `intent.md`（问题/预期结果/受影响用户与系统/约束/开放问题） | 被产品负责人接受（merge 或 closing review）→ 进入 Design |
| Design | `spec.md`（与 intent 成对提交） | 被产品负责人批准 → 触发 Build 的 plan mode |
| Build | `plan.md` + 代码 diff + 测试 | plan 被工程师接受后实现；merged PR → 触发管线 |
| Test | CI/持续 evals 结果 | — |
| Deploy | PR + review findings | merged → 部署 |
| Maintain | 事件记录（incident record） | 控制带被突破 → 写回新的 `intent.md`，循环继续 |

早期阶段以 `.md` 文件为主要工件，因为**产品负责人和 agent 都能读写同一文件**；从 Build 起工件是代码及其记录。**提交链 = 审计轨迹**：谁要求什么（intent）、agent 产出什么（spec/plan/diff）、谁批准（merge/close review）。人类对需要判断力的决策负责，注意力集中在关卡处 review agent 标记过的内容，而非从零启动每个阶段。

## 六阶段机制精要

### Plan — 捕获为 intent.md
起点：人 brainstorm、ticket、或事件告警。发起人用自己的话描述问题 → Claude 追问澄清 → 按模板产出 `intent.md` → 产品负责人修正后提交到共享 intent home（单产品通常是仓库内 `intent/` 目录）。非工程师可经 connector（GitHub）让 Claude 代提交，无需会用 git。

### Design — 需求与设计合并为一次会话
Claude 读已接受的 `intent.md`，在组织 skills（brand/security/compliance/UX）约束下产出 `spec.md` 并**标记关切领域**；产品负责人 review 但不撰写。前端可从 Claude Design 出 mock 再交给 Claude Code 构建。先手跑 → 固化为组织斜杠命令 → 最终以 intent 的 merge 为触发器、非交互 job 自动产出 spec 的 PR。

### Build — 没有已接受的 plan 不实现
- **Plan mode 作为默认起点**：只读规划，产出实现计划 → 追问风险 → 迭代到「没见过对话的人也能照做」→ 提交 `plan.md`；实现偏离时同步更新 plan（可用 hook 强制）。
- **Auto mode**：guardrails 成熟后 routine 工作默认 auto-accept，配合 worktree 并行。
- **CLAUDE.md**：把命令/约定/架构/常见错误固化为 <1 页文件，每个 session 读取；错两次 → 写进去。
- **Skills**：需一致执行的制度知识写成 `.claude/skills/<name>/SKILL.md`，政策变更由 owner 签收。
- **Hooks**：确定性护栏——阻断受保护路径、自动 lint/format、凭据挡在 diff 外。
- **并行会话与 subagents**：多个 git worktree × Claude Code 实例并行；重复工作打包为 `.claude/agents/*.md` subagent（verifier 等）。

### Test — 反馈回路 + 持续 evals
每个 session 自检（单命令测试/构建/截图 diff，「done」= 跑过验证）；修 bug 先写失败测试并用 hook 禁止改测试。**持续 evals**：20–50 个真实任务写成 eval，CI 定时 + 对 CLAUDE.md/skills/hooks 变更回归运行，pass-rate 作 merge check，生产事故写成 eval 永久留存——agent 的配置和它写的代码一样要回归测试。

### Deploy — 双向评审 + 治理即行动
- `REVIEW.md` 定义评审 pass（bugs/security/compliance-vs-spec&plan）；`@claude` 处理 review 意见并推送修复；错两次回写 CLAUDE.md；人审聚焦意图与风险；**写代码的 agent 无法批准自己的 PR**（职责分离，分支保护仍要 code owner 人审）。
- Hooks 作审批门：allow/ask/block；团队 hooks 在 `.claude/settings.json`，不可协商 hooks 走托管 managed settings。
- CI/CD：`claude -p` 非交互式跑判断步骤，一切写入走 PR、无直通 main 路径；执行沙箱化、无生产凭据；部署能力经 MCP 暴露、按环境分级自治；rollback 是最常演练的路径。

### Maintain — 闭环（无人在调用路径上）
确定性检测脚本（rolling mean/std + Western Electric）盯生产指标，σ 分级（1σ 记日志 / 2σ 只读诊断 / 3σ 经 PR 或预批准 runbook 行动）；诊断写成 `intent.md` 重回 Plan。代表产品：[[Claude_Security]]（定时代码扫描）与 [[Claude_Tag]]（Slack 值班）。

## spec.md：技术规格文档

### 来源

由 AI 基于**已审核通过的 intent.md** 自动生成；人类再对 spec.md 内容做评审、修正，确认后进入后续开发环节。spec.md 不直接来源于口头需求，而是「已达成一致的业务意图」的设计落地。在完整 Playbook 中，spec 受组织 skills 约束、标记关切领域、与 intent 成对提交。

### 核心内容

1. **业务目标** — 对齐 intent.md 的原始诉求，明确要解决什么问题
2. **功能规格** — 具体功能清单、输入输出、交互行为、业务规则
3. **非功能规格** — 性能、安全、兼容性、报错处理、边界条件
4. **数据设计** — 涉及的数据结构、字段、存储、流转逻辑
5. **依赖项** — 外部依赖、接口、第三方组件、环境约束
6. **验收标准** — 可验证的验收用例，用来判断功能是否完成
7. **遗留问题** — 尚未确定、需要后续讨论的点

### 作用

1. **消除歧义** — 将模糊的业务意图转化为清晰、可执行的技术设计
2. **开发依据** — 后续可基于 spec.md 生成代码、测试用例（以及 plan.md）
3. **评审载体** — 人和 AI 共同校验设计是否符合原始业务意图
4. **变更留痕** — Git 版本管理，留存设计变更历史，用于回溯审计

## plan.md：实现计划工件（Playbook 新增）

介于 spec 与代码之间的一等工件：由 Claude 在 plan mode 中产出，命名将改变的文件、工作顺序、风险（含被放弃的选项）与证明方式（测试）。**批准前不允许生成代码**——plan mode 本身强制这一点（agent 在 plan 被接受前不能编辑文件）。提交后加入审计链，PR review 时以 diff 对照 plan 检查；实现偏离时须同步更新 plan。

## 评审门控：流程的一等公民

intent.md、spec.md、plan.md 都必须「评审通过」才能进入下一阶段；接受/批准/关闭决策以 git merge 或 close review 的形式记录，成为审计轨迹的一部分。评审是人与 AI 共同校验「产物是否忠实于上游意图」的关卡，把问题拦截在编码之前，而非事后返工。随自动化成熟，每个被接受的工件会**自动触发**下一阶段（accepted intent → design、approved spec → plan mode、merged PR → pipeline），人工逐步退到「只审 agent 标记过的东西」。

## 控制机制：治理三层

AI-native SDLC 的治理 = 三层机制叠加，让人审只保留在真正需要判断力的地方：

1. **Skills（顾问性控制）** — 让违规**罕见**：制度知识随代码写作时被应用；不强制，但使违规成为少数情况。触发与版本都在 session traces 中留痕。
2. **Hooks（确定性控制）** — 让违规**几乎不可能**：在 agent 每个动作前 allow/ask/block，无条件政策用 hook 背书（如阻断生产部署、禁止 fix 任务改测试）。决策带时间戳记日志。
3. **审批门（人在环）** — 需要判断力的动作暂停等人批准：code owner 的分支保护、release manager 授权、受监管路径的保护。写代码的 agent 无法批准自己的产物（职责分离）。

配套：branch protection（agent 无直通 main 路径）+ 平台托管 managed settings（工程师不可绕过：sandbox、凭据封锁、仅允许托管 hooks/MCP、严格 marketplace、最低版本）。

**度量原则**：一律「领先指标 + 滞后指标」配对，且可从 git 历史 / PR 元数据 / CI 日志 / incident tracker / OpenTelemetry 导出中直接读取。

## 与相关概念的边界

- spec.md 是**人类可读的 Markdown 技术规格文档**；[[Spec_Driven_Development]] 中的 Formal Spec（YAML / JSON Schema / DSPy Signature）是**可机读的任务契约**。两者互补：spec.md 在文档层消除「做什么」的歧义，Formal Spec 在任务/接口层精确约束「怎么做」。
- 对 [[Agent_First_Engineering]] 而言，AI-Native SDLC 是其一种具体编排形态——人定需求（intent.md）、人做评审，AI 产出设计与实现（spec.md → plan.md → 代码）。
- spec.md/plan.md 作为阶段间的交接物，是 [[Contract_Driven_Handoffs]] 的文档层实例：上游承诺工件，下游按工件验证。
- 与 [[AI驱动的CICD]]：AI-Native SDLC 把 Claude 非交互式嵌入 CI/CD（Deploy play 是其在 DevOps 的展开）；CICD 是生命周期中的执行管道，而非流程本身。
- 与 [[Claude_Code_Workflow]] / [[GSD_Core]]：同类全生命周期 AI 开发框架对照——GSD 以命令/Agent 驱动，AI-SDLC 以**文档工件驱动 + 关卡触发**。
- [[System_of_Record]]：过渡期需为每类工件声明「单一事实来源」——仓库（markdown 为权威）或 legacy 系统（Jira/ServiceNow 为权威，markdown 为工作副本，经 MCP 读写），Linkage 是两者的最低公约数。

## 关联连接

- [[Spec_Driven_Development]] — spec.md 是文档层的规格；Formal Spec 是可机读契约，二者互补
- [[Contract_Driven_Handoffs]] — 阶段间工件交接 = 契约驱动交接，评审 = 接受度 Gate
- [[Agent_First_Engineering]] — AI-Native SDLC 是 Agent-First「人定目标做审核、AI 做设计实现」的一种文档驱动编排
- [[Agent_As_Judge]] — spec/PR 评审是质量保障门控，可引入 Agent-as-Judge 自动化校验
- [[GSD_Core]] — 同类全生命周期 AI 开发框架对照：GSD 以命令/Agent 驱动，AI-SDLC 以文档工件驱动
- [[AGENT_MD]] — 同为流程规范文档工件：AGENT.md/CLAUDE.md 约束行为边界，spec.md/plan.md 约束交付物
- [[System_of_Record]] — spec.md 在开发阶段充当「知识权威来源」；过渡期单一事实来源决策
- [[Harness_Engineering]] — 评审门控、hooks、skills、evals 都是约束 Agent 输出的控制机制
- [[Agentic_Coding]] — AI-Native SDLC 所属的总体范式
- [[Claude_Code]] — Plan mode/auto mode/subagent/hooks 的载体工具
- [[Claude_Code_Hooks]] — 治理三层的确定性控制（allow/ask/block）
- [[Claude_Code_Skills]] — 治理三层的顾问性控制
- [[Claude_Security]] — Maintain 阶段 hosted 定时代码扫描
- [[Claude_Tag]] — Maintain 阶段 Slack 值班
- [[Eval_Harness]] — Test 阶段持续 evals / agent 配置回归测试
- [[AI驱动的CICD]] — Deploy 阶段非交互式 CI/CD 展开
- [[Agent_Loop]] — Maintain 阶段闭环的循环机制
- [[摘要-ai-native-sdlc-playbook]] — 来源摘要（Anthropic Playbook）
- [[摘要-agent-first-engineering]] — Agent-First 7 步实操对照
