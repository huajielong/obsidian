---
title: "摘要-AI-Native-SDLC-Playbook"
type: source
tags: [来源, Anthropic, AI-Native SDLC, 软件工程, Claude Code, Harness Engineering]
sources: [raw/09-archive/The AI-Native SDLC playbook  Claude by Anthropic.md]
last_updated: 2026-09-04
---

# AI-Native SDLC Playbook（Anthropic 官方智能体化软件生命周期手册）

## 核心摘要

Anthropic Applied AI 团队发布的 **AI-Native SDLC（AI 原生软件生命周期）Playbook**。核心论点：当「代码不再是瓶颈」（Build 阶段被 agentic coding 压缩到小时级）后，瓶颈转移到 Build 左右两侧仍以**人类速度**运行的 Plan / Review-Test / Deploy，因此**传统 SDLC 需要和实现阶段同等程度的改造**——审查队列、审批关卡与治理成本必须跟上 agent 的产出速度。

AI-native SDLC 把传统**线性**流程改造为**闭环循环（loop）**，AI 嵌入每个阶段；每个阶段结束时向版本控制提交一份**下一阶段可直接读取的工件（artifact）**，以自动化交接与触发下一个 play。六个阶段依次提交：`intent.md`（Plan）→ `spec.md`（Design）→ `plan.md`（Build）→ 代码 diff + 测试（Build/Test）→ PR 及其评审结论（Deploy）→ 事件记录（Maintain）→ 再生成新的 `intent.md`……**提交链即审计追踪**：谁要求了什么、agent 产出了什么、谁批准了什么。人类始终对需要判断力的决策负责，注意力从「逐行盯 agent 编辑」转移到关卡处「review agent 标记过的工件」。

手册把每阶段落地为一个个 **play**，每个 play 统一包含：变更内容 / 起步（Prerequisites + Infrastructure）/ 实施步骤 / 治理考量 / 度量方式（领先指标 + 滞后指标），并给出依赖图。

- **来源**：https://claude.com/blog/the-ai-native-sdlc-playbook （Anthropic Claude 官方博客，Applied AI 团队）
- **剪藏日期**：2026-09-04

## 六阶段转换对照

| 阶段 | 传统 SDLC | AI-native SDLC |
|------|----------|----------------|
| **Plan** | 委员会收集需求，workshop + 层层签核，手工撰写 | Claude 直接从源头综合痛点，写入人类可读、机器可执行的 `intent.md` |
| **Design** | 分析师写 spec、设计师再解析 | 需求与设计压缩进**一次** agent 会话，由编码为 skills 的 brand/security/compliance/UX 标准约束，git 版本化 |
| **Build** | 测试与代码手写、文档事后补 | AI 生成测试与代码；制度知识维护为版本化的 `CLAUDE.md` 与 skills |
| **Test** | 阶段边界 QA 关卡 | 持续 evals 织入实现过程 |
| **Deploy** | 人类逐行 review，治理靠（常不一致的）评审循环 | 多层 agentic review，人审保留给受监管/关键代码；治理以 hooks 作为审批门、在 AI 行动时强制 |
| **Maintain** | 人类盯生产 bug | agents 监控线上部署；控制带被突破即诊断并写回新的 `intent.md` |

贯穿右栏的主线是**提交的工件**：早期阶段以 `.md` 文件为主（产品负责人与 agent 都能读写同一文件）；从 Build 起工件是代码及其记录。

## 六阶段 Plays 精要

### Plan — 捕获为 intent.md
起点可以是人 brainstorm、已有 ticket、或事件告警（Stage 6）。发起人用自己的话描述问题 → Claude 追问澄清（范围/用户/约束/成功标准）→ 按组织模板产出 `intent.md`（问题 / 预期结果 / 受影响用户与系统 / 约束 / 开放问题）→ 产品负责人 review 修正后提交到共享 intent home（单产品通常是产品仓库里的 `intent/` 目录）。非工程师可经 connector（GitHub）让 Claude 代提交，不必会用 git。**度量**：领先 = 首次对话到 committed `intent.md` 的时长（周→小时，读 git 历史）；滞后 = intent 存活率（被接受进入 Design vs 被关闭）+ intent 在首个 spec 提交后的改动次数。

### Design — 需求与设计合并为一次会话
Claude 读已接受的 `intent.md`，在组织 skills 约束下产出需求与设计 spec（`spec.md`），并**显式标记关切领域**（analyst 会升级的那些点）；产品负责人 review 但不撰写。前端工作可从 `intent.md` 在 Claude Design 出 mock、迭代后再交给 Claude Code 构建。spec 与 intent 成对提交，记录「要了什么、决定了什么」。先手跑，再固化为组织级斜杠命令，最终让 intent 仓库的 merge 成为触发、非交互 job 自动产出 spec 的 PR。**度量**：领先 = intent 提交到 spec 提交间隔；滞后 = Build 开始后的需求返工量（spec.md 晚于首个 plan.md 的提交数）。

### Build — 没有已接受的 plan 不实现
- **Plan Mode 作为默认起点**：工程师在 plan mode（只读、不能改文件）中把 `spec.md` 交给 Claude 产出实现计划，追问「可能破坏什么 / 哪步最险 / 放弃了哪些选项」，迭代到「从未见过对话的人也能照 plan 实现」，提交 `plan.md` 进入审计链；实现偏离时同 commit 更新 plan（可用 hook 强制同步）。
- **Auto Mode**：当 guardrails 成熟（tuned `CLAUDE.md` + 编码政策的 skills + 阻断危险动作的 hooks + Claude 可跑的测试套件），auto-accept 成为 routine 工作的默认——配合 worktrees 支持并行与自主闭环。
- **CLAUDE.md**：把新人第一天需要知道的命令/约定/架构/「Claude 常犯的错」固化为文件，`/init` 生成、<1 页、全员共享、按代码评审演进；「同一个错犯两次 → 写进 CLAUDE.md」。
- **Skills（制度知识）**：需要一致执行的制度知识写成 `.claude/skills/<name>/SKILL.md`（何时触发放 frontmatter、做什么放正文），随仓库或 plugin 分发；政策变更由 owner 签收，工程师下一 session 自动拿到新版本。
- **Hooks（构建期护栏）**：skills 是顾问性控制，hooks 是背后的**确定性层**——阻断受保护路径编辑、编辑后自动跑 formatter/linter、把凭据挡在 diff 外；policy「必须无条件成立」时用 hook 背书。
- **并行会话与 subagents**：一个工程师在多个 git worktree 上跑多个 Claude Code 实例（彼此隔离，工程师是唯一共享点）；重复性工作（如 verifier「跑 app 验证行为」）打包为 `.claude/agents/*.md` 定义的 subagent，各有独立 context 与工具边界。

### Test — 给 Claude 反馈回路 + 持续 evals
- 每个 session 自检自己的工作：把「验证」收敛成单命令（`make test`），`CLAUDE.md` 写明命令与健康输出范例，「done」= 跑过验证并粘贴输出。UI 工作用浏览器/截图工具做视觉闭环。修 bug：**先写失败测试 → commit → 再让 Claude 修**，并用「禁止 fix 任务改测试文件」的 hook 保护回路不被削弱。
- **持续 evals（CI）**：收集 20–50 个真实任务 + 期望结果写成 eval；在 CI 定时 + 对 `CLAUDE.md`/skills/hooks 每次变更时回归运行——**配置 agent 的"代码"和它写的代码一样要回归测试**；pass-rate 作为 merge check；每个生产事故写成 eval 永久留存。

### Deploy — 双向评审 + 治理即行动
- **AI 进 PR review loop**：Claude 既评审别人的 PR、也被评审。`REVIEW.md` 定义评审 pass（bugs / security / compliance-against-spec&plan）、Important vs Nit 与上限；作者或 reviewer `@claude` 即让 Claude 处理意见并推送修复；同一错误第二次出现时回写 `CLAUDE.md`。技术负责人每月调参、限制 Nit 噪音。**职责分离**：写代码的 agent 无法批准自己的 PR，分支保护仍要求 code owner 人审。
- **Hooks 作为审批门**：构建期 hooks 是 guardrail（allow/block，无人在环）；release gate 需要 allow/**ask**/**block**——暂停动作直到指定的人批准。团队 hooks 放 `.claude/settings.json`；不可协商 hooks 放平台托管的 **managed settings**（工程师无法关闭）。每次 allow/block 决策带时间戳记日志。
- **CI/CD 集成**：`claude -p` 非交互式跑 judgment 步骤（triaging 失败 build / 总结 flaky test / 草拟 changelog / 处理 review 意见）；一切写入经 branch protection 走 PR，agent 无直通 main 的路径；执行沙箱化、短时 scoped token、无常驻生产凭据；部署能力经 **MCP** 暴露为工具（deploy/status/rollback），按环境分级自治；**rollback 是最常演练的路径**。
- **受监管企业的 managed settings 示例**：permissions deny/allow + disableBypassPermissionsMode + sandbox（域白名单、凭据文件/环境变量封锁）+ allowManagedHooksOnly + strictKnownMarketplaces + allowManagedMcpServersOnly + requiredMinimumVersion——把 agent 机器锁进组织批准的安全边界。

### Maintain — 闭环（无人在调用路径上）
- **Closing the loop**：确定性检测脚本（rolling mean/std + Western Electric 规则）盯生产指标（CI 失败率 / 5xx / PR cycle time）。**σ 分级**：1σ 只记日志、2σ 只读诊断、3σ 才可行动——且只能开 PR 进 review gate 或触发预批准 runbook。诊断写成 `intent.md`（含异常与证据/预期结果/受影响系统/开放问题）重新进入 Plan。统计无状态、非交互，一个 loop 可以无人启动地开始与结束。
- **Claude Security（定时代码库扫描）**：连 GitHub 仓库后由 Anthropic 托管跑（用 Claude Mythos 5），每个 finding 先验证并附置信度；bounded 补丁经 Claude Code on the web review 后走 PR gate，跨服务/架构级问题写成 `intent.md`；dismissal 必须带理由；扫描历史即审计记录。是静态分析与依赖扫描的补充（覆盖需要上下文判断的漏洞）。
- **Claude Tag（值班）**：让 Claude 以自己身份成为 Slack incident channel 成员，第一时间响应；任何人可在频道内引导/操作；经 MCP 验证指标回到基线并在 thread 确认，post-mortem 写入版本化 lessons 文件。**频道即审计追踪**。小修复走 PR gate，大问题写成 `intent.md` 喂给 Plan。

## 治理与度量的总体原则
- 每个阶段以提交一个版本控制工件收尾，下一阶段读它开始——**提交链 = 审计链**。
- 控制机制三元组：**Skills**（顾问性控制 → 让违规罕见）+ **Hooks**（确定性控制 → 让违规几乎不可能）+ **审批门**（人在关键路径上做判断）。另加 branch protection（agent 无直通 main 路径）与托管 managed settings（不可绕过）。
- 度量一律「领先指标 + 滞后指标」配对，全部可从 git 历史 / PR 元数据 / CI 日志 / incident tracker / OpenTelemetry 导出中直接读取，不靠主观感受。
- 治理记录（spec 的 prompt、生效的 skill 版本、hook 决策、triaging 决定）全部进版本控制与日志。

## 关联连接

- [[AI_SDLC]] — 本文档对应的核心概念页（六阶段闭环 + 工件链 + 治理三层）
- [[Anthropic]] — 发布方（Applied AI 团队），Claude Security / Claude Tag / Claude Design / Cowork 等产品线
- [[Claude_Code]] — Build（plan mode/auto mode）/ Deploy（@claude 修复、CI 非交互式）/ Maintain（headless 调用）的核心执行工具
- [[Claude_Security]] — Anthropic 定时代码扫描产品（Maintain 阶段 play）
- [[Claude_Tag]] — Anthropic Slack 值班 Agent（Maintain 阶段 play）
- [[Harness_Engineering]] — 治理/控制机制所属的工程范式
- [[System_of_Record]] — Legacy 系统 vs markdown 工件的「单一事实来源」取舍（sidebar）
- [[Claude_Code_Hooks]] — allow/ask/block 审批门与构建期护栏
- [[Claude_Code_Skills]] — 制度知识编码为 skill（顾问性控制）
- [[Claude_Code_Subagent]] — 并行会话与 verifier 型 subagent
- [[Eval_Harness]] — 持续 evals / agent 配置回归测试
- [[AI驱动的CICD]] — Claude 非交互式进 CI/CD 管线
- [[Agent_Loop]] — Maintain 闭环与总循环
- [[Agent_Observability]] — OpenTelemetry 导出会话/hook 决策日志
- [[MCP]] — 部署能力与遗留系统经 MCP 暴露为工具
- [[Spec_Driven_Development]] — spec.md 与 Formal Spec 的互补
- [[Contract_Driven_Handoffs]] — 工件交接即契约驱动交接
- [[Developer_Agentic_Workflow]] — 开发者工作流的组织级视角
