---
title: "Developer_Agentic_Workflow"
type: concept
tags: [开发者工作流, 工具链, 场景分类, 最佳实践]
sources: [https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/branches/for-developer.zh-Hans.md]
last_updated: 2026-07-10
---

# 开发者 Agentic AI 工作流

将开发者日常编码工作拆解为 **7 个典型场景**，并为每个场景匹配 AI 工具链的框架。来源于 awesome-agentic-ai-zh 的 for-developer 分支。

## 7 场景分类框架

下表把开发者一天会遇到的场景拆开——每个场景有不同的痛点，AI 工具也不同：

| 场景 | 痛点 | AI 能帮的部分 | 推荐工具链（从轻到重） |
|---|---|---|---|
| **AI 结对编程** | 写到半忘 syntax / 想不到 method 名 | 自动补全 + 改写 + 解释 | Cursor / Copilot → Claude Code |
| **多文件重构** | 改一个 class 怕漏改、跨文件 rename 易错 | batch refactor、改 50 文件仍保持风格一致 | Cursor → Claude Code → codex-delegate |
| **Code review（自己 PR）** | review 自己 diff 看不出问题 | 找 bug/smell、检查 edge case | Claude Code / Cline → Continue(CI) |
| **写测试** | TDD 常忘加 case、coverage 不足 | 从 signature/spec 生成 pytest | Claude Code + Aider |
| **Debug** | log 不够、stack trace 看不懂 | 解释 trace、生成 hypothesis、跑 minimal repro | Claude Code |
| **文档生成** | docstring/README 没人写、refactor 后过期 | 从 code 生成 doc、PR 对应改 doc | Claude Code |
| **CI/团队自动化** | 重复手动跑 review、跨人风格不一 | GitHub Action 自动跑 review/lint | Claude Code Action + Continue |

> **个人 vs 团队**: 前 6 个是个人 daily workflow；最后 1 个（CI）是团队规范。团队 < 5 人时 CI 自动化的 ROI 不高。

---

## Tier 升级路径

从学习成本和 ROI 角度划分的四个层级：

| Tier | 工具 | 适合谁 | 学习成本 |
|---|---|---|---|
| **Tier 0** | Cursor / Copilot / Claude.ai | IDE 内 chat、autocomplete，不自己写 agent | 0（会用编辑器就行） |
| **Tier 1** | Claude Code / Cline / Aider + CLAUDE.md | CLI 接 file system、human-in-the-loop | 1-2 天 |
| **Tier 2** | 自写 Skills + MCP server | 把 dev workflow 包成 skill 给团队共用 | 1 周 |
| **Tier 3** | CI 自动跑 agent + production observability | 进到 Production 化领域 | 数周，需 governance |

> 多数个人开发者可先停在 **Tier 0-1**。升级到 **Tier 2+** 要先确认 ROI——团队够大、流程够重复、事故不可逆才值得 invest。

---

## 3 个具体 Workflow Recipe

### 1. AI 结对编程（每日节奏）

1. 开新 feature → `git checkout -b feature/xxx`
2. 把任务丢给 Claude Code / Cursor，**先让它写 plan**（不直接写 code）
3. Review plan、修正方向 → 才 approve 写 code
4. 写完跑 tests + lint → 自己 review diff（**不要 blind accept**）
5. Commit message 自己写或 prompt 生草稿后改

### 2. Aider git-native 流程（最像"跟 AI pair"）

```bash
aider --model anthropic/claude-sonnet-5
> 帮我把 utils.py 的 parse_date 加上时区参数，默认 UTC
# Aider 会自动编辑 + commit。若不满意：
> /undo  # 退掉最后一次 AI commit
```

### 3. PR 上的 Claude code review（GitHub Action）

配置 `.github/workflows/claude-review.yml`，使用 `anthropics/claude-code-action` 官方 action。抓 git diff → 跑 prompt → 结果 post 回 PR，实现 human + AI 双审。

---

## Anti-patterns（常见踩坑）

| ❌ 不要 | ✅ 改成 |
|---|---|
| 让 AI 直接 push 到 main | 永远 PR → review → merge |
| Blind accept 大规模 refactor diff | 拆成 < 50 LOC 改动，逐个 review |
| 把 .env / API key 丢给 AI 看 | 用工具对应的排除机制（`.cursorignore` / `.aiderignore` / `.claude/settings.json` permissions.deny）|
| 让 AI 在 production code 自由跑 shell | sandbox 限制、permission whitelist |
| 用 AI 生 test 后不检查 assertion | 跑覆盖率 + 故意改一个 bug 看 test 抓不抓得到 |
| 跨多个 commit 才发现方向错 | **plan-first** 模式：先 review plan 再写 code |

---

## 关联链接

- [[Agentic_Coding]] — AI Agent 自主驱动编程的软件开发范式（本框架的上层概念）
- [[Claude_Code_Workflow]] — Claude Code 开发工作流方法论
- [[Claude_Code_Skills]] — Claude Code 技能系统（Tier 2 涉及）
- [[Harness_Engineering]] — Agent 系统工程实践
- [[摘要-awesome-agentic-ai-zh-for-developer]] — 本框架的来源摘要

### 工具实体

- [[Cursor]] — Tier 0 编辑器集成工具
- [[Aider]] — Tier 1 git-native CLI tool
- [[Claude_Code]] — Tier 1-2 核心 coding 助理
- [[Cline]] — Tier 1 VS Code agent
- [[Continue_Dev]] — Tier 3 CI review
- [[OpenHands]] — 自主 agent 替代方案
- [[Goose_AI]] — 多接口自主 agent
- [[Roo_Code]] — VS Code multi-mode agent
- [[Repomix]] — 必备 daily-driver 工具
- [[From_NoCode_To_Agent_Paradigm]] — Agent 范式下开发工作流替代传统无代码搭建
- [[superpowers_obra]] — Skill 参考实现
