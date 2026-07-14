---
title: "mattpocock/skills 中文速查表"
type: synthesis
tags: [skills, claude-code, agent-engineering, cheat-sheet]
sources: []
last_updated: 2026-07-14
---

# mattpocock/skills 中文速查表

> 来源：<https://github.com/mattpocock/skills>（15 万+ Star）— Matt Pocock 开源的 Claude Code Skills 集合，含工程开发与日常生产力两大类。

---

## 一、初始化（先跑这个）

| Skill | 什么时候用 | 怎么写提示 | 常见坑 |
|-------|-----------|-----------|--------|
| `/setup-matt-pocock-skills` | **第一次在新仓库启用前**，初始化 issue tracker、标签体系、文档存储位置 | `/setup-matt-pocock-skills` → 按提示选 tracker（GitHub/Local/Linear）和标签方案 | ❌ 不跑 setup 就直接用 `/triage` `/to-issues`，标签体系会不一致 |
| `/ask-matt` | **不知该用哪个 skill**，让 AI 做路由推荐 | "帮我看看该用哪个 skill：我想给用户模块加个搜索功能" | ❌ 问太模糊会推荐不准，建议带一句场景描述 |

---

## 二、方案定义与分解

| Skill | 什么时候用 | 怎么写提示 | 常见坑 |
|-------|-----------|-----------|--------|
| `/to-prd` | **想法需沉淀为正式需求文档**，把零散对话合成 PRD 并提交为 Issue | 先聊清楚需求，然后敲：`/to-prd` | ❌ **不要在空对话里直接敲** — 没有素材可提炼，产出会很空 |
| `/to-issues` | **已有 PRD/方案**，拆成可独立执行的 vertical slice 任务 | 生成 PRD 后直接敲：`/to-issues` | ❌ 切成**水平切片**（先 schema → 再 API → 再 UI）是错的；每个 issue 必须是端到端完整功能块 |
| `domain-modeling`（自动触发） | **需明确领域术语、实体关系、边界上下文**时触发。也用于 `/grill-with-docs` 内部 | 说"我们来理一下支付模块的领域模型"时自动激活 | ❌ 只做一次不维护。它产出 `CONTEXT.md` + ADR，需持续更新 |
| `codebase-design`（自动触发） | **设计/重构模块时**，按"小接口、大功能"的深模块（deep module）原则指导 | 说"设计这个模块的接口"时自动触发 | ❌ 核心概念来自《A Philosophy of Software Design》，团队不熟悉该理念则建议难落地 |

---

## 三、方案挑战与审查

| Skill | 什么时候用 | 怎么写提示 | 常见坑 |
|-------|-----------|-----------|--------|
| `/grill-me` | **动笔写代码前**，让 AI 对方案做全面压力测试，逐个追问直至所有分支明确 | `/grill-me` → 粘贴方案想法，或描述"我想加个团队看板" | ❌ **觉得"被问太多"就跳过** — 问题越多说明盲点越多；一般 16-50 个问题 |
| `/grill-with-docs` | **有架构文档/ADR 时**，基于规范做反驳式审查 | `/grill-with-docs` → 它自动找 docs 和 ADR，再结合方案提问 | ❌ **没文档就跑这个** — 会退化成 `/grill-me`，失去"基于文档"的价值 |
| `code-review`（自动触发） | **提交代码审查**时，按"标准维度"和"规范维度"双线并行审查 | 创建 PR 或说"帮我 review 这段代码"时自动触发 | ❌ 跑并行子代理消耗 token 较多，小改动可能不划算 |

---

## 四、开发与调试

| Skill | 什么时候用 | 怎么写提示 | 常见坑 |
|-------|-----------|-----------|--------|
| `tdd`（自动触发） | **写新功能**，严格按「红→绿→重构」循环，一次做一个 vertical slice | 说"用 TDD 实现这个功能"时自动启动 | ❌ **跳过红阶段直接写代码** — 本质是纪律训练，不按流程走就失去意义 |
| `prototype`（自动触发） | **快速验证想法/数据模型/UI 方案**，做一次性原型（非生产代码） | 说"帮我 prototype 一下这个思路" | ❌ **拿原型当生产代码用** — 特意做成 disposable，用完就扔 |
| `diagnosing-bugs`（自动触发） | **遇难复现 Bug 或性能回退**，系统化诊断 | 说"帮我诊断这个 Bug"或"这个接口突然变慢了" | ❌ **跳过回归测试** — 诊断循环最后一步是"确保不再出现"，跳过等于白做 |
| `resolving-merge-conflicts`（自动触发） | **Git merge/rebase 产生冲突时**自动介入 | 检测到冲突时自动触发 | ❌ 解决完冲突前不要塞新需求 |

---

## 五、代码架构改进

| Skill | 什么时候用 | 怎么写提示 | 常见坑 |
|-------|-----------|-----------|--------|
| `/improve-codebase-architecture` | **觉代码在腐烂**，扫描全库找"加深"机会，生成可视化 HTML 报告 | `/improve-codebase-architecture` | ❌ 报告是 HTML 文件，需要在浏览器中打开查看；不看报告就没意义 |

---

## 六、交接与知识管理

| Skill | 什么时候用 | 怎么写提示 | 常见坑 |
|-------|-----------|-----------|--------|
| `/handoff` | **会话结束时**，把上下文压成"交接单"给下次会话或另一个 agent | 会话末尾敲：`/handoff` | ❌ **不带文件路径和验证命令** — 必须含：已完成/进行中/阻塞项/下一步/关键文件/回归测试命令 |
| `/teach` | **跟 AI 学新技能/概念**，跨多会话持续学习 | `/teach` → 告诉它想学什么 | ❌ 不告诉它已知水平 — 会从最基础开始讲 |
| `research`（自动触发） | **调研技术问题**，基于一手资料输出带引用的 Markdown | "帮我调研一下 xx 技术方案的现状" | ❌ 不给调研范围 → 产出篇幅失控；最好指定"重点看 3-5 个权威来源" |

---

## 七、Issue 管理

| Skill | 什么时候用 | 怎么写提示 | 常见坑 |
|-------|-----------|-----------|--------|
| `/triage` | **新 issue 堆积时**，分类、打标签、排优先级 | `/triage` | ❌ **没先跑 `/setup` 就 triage** — 标签词汇表不一致会越分越乱 |

---

## 八、辅助 & 杂项

| Skill | 什么时候用 | 怎么写提示 | 常见坑 |
|-------|-----------|-----------|--------|
| `/writing-great-skills` | **想自己写 skill** 时的参考指南 | `/writing-great-skills` | ❌ 写成一大段原则而没有触发条件和输出模板 |
| `git-guardrails-claude-code`（自动生效） | **防止 AI 误执行危险 git 命令**（`push --force`、`reset --hard`、`clean -fd`） | 自动生效 | ❌ 确实需要强制推送时得先关闭 |
| `setup-pre-commit`（自动触发） | **配置 pre-commit hooks**（Husky + lint-staged + Prettier + 类型检查 + 测试） | "帮我配一下 pre-commit" | ❌ 跟已有 CI/CD 可能冲突，配之前先检查 |
| `scaffold-exercises`（自动触发） | **创建练习目录结构**（章节、问题、解答） | "帮我搭一个 TypeScript 练习题脚手架" | ❌ 使用频率低，容易忘 |
| `migrate-to-shoehorn`（自动触发） | **把测试中 `as` 断言迁移到 `@total-typescript/shoehorn`** | 特化工具，仅限用 shoehorn 的项目 | ❌ 非通用技能 |

---

## 推荐使用流程

```
┌──────────────┐    ┌──────────┐    ┌────────────┐    ┌───────────┐
│ /grill-me     │ →  │ /to-prd   │ →  │ /to-issues  │ →  │ tdd       │
│ （压力测试）    │    │ （写文档）  │    │ （拆任务）    │    │ （开发）    │
└──────────────┘    └──────────┘    └────────────┘    └───────────┘
                                                        ↓
                                               ┌───────────────┐
                                               │ code-review    │
                                               │ diagnosing-    │
                                               │ bugs           │
                                               └───────────────┘
```

每次关键里程碑做 `/grill-with-docs` 或 `/improve-codebase-architecture`，会话结束时跑 `/handoff`。

---

## 一句话总结

| Skill | 一句话 |
|-------|-------|
| `/setup-*` | 用之前先铺路 |
| `/ask-matt` | 不知道该用啥？问它 |
| `/to-prd` | 把聊天变文档 |
| `/to-issues` | 把文档变任务 |
| `domain-modeling` | 让术语不再打架 |
| `codebase-design` | 设计深模块 |
| `/grill-me` | 写代码前先被拷问 |
| `/grill-with-docs` | 带着规范来拷问 |
| `code-review` | 双线并行审查 |
| `tdd` | 红-绿-重构 |
| `prototype` | 快速验证，用完就扔 |
| `diagnosing-bugs` | 系统化杀 Bug |
| `resolving-merge-conflicts` | 专治合并冲突 |
| `/improve-*architecture` | 治代码腐朽 |
| `/handoff` | 下班前写好"交接单" |
| `/teach` | 跟 AI 学新东西 |
| `research` | 带引号的调研 |
| `/triage` | 给 Issue 排队 |
| `/writing-great-skills` | 教你写 skill |
| `git-guardrails` | 防手滑误操作 |
| `setup-pre-commit` | 一键配好 git hooks |

---

## 关联连接

- [[Claude_Code_Skills]] — Claude Code 技能系统架构与扩展机制
- [[Claude_Code_Subagent]] — Claude Code 原生 Multi-Agent 机制
- [[Claude_Code_Slash_Commands]] — Claude Code 斜杠命令体系
- [[Developer_Agentic_Workflow]] — 开发者 Agentic AI 工作流框架
- [[Harness_Engineering]] — Agent 约束与反馈回路的系统工程
- [[Spec_Driven_Development]] — 规范驱动开发，与 `/to-prd` + `/to-issues` 理念一致
