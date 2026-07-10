---
title: "Continue"
type: entity
tags: [工具, CodeReview, CI, VS Code, 开源]
sources: [https://github.com/continuedev/continue, https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/branches/for-developer.zh-Hans.md]
last_updated: 2026-07-10
---

# Continue

> ★ 33k+ · Apache-2.0 · [GitHub](https://github.com/continuedev/continue)

**source-controlled AI checks** 工具，可以在 CI 强制执行代码审查。代表 **"团队/governance"** 角度的 coding agent。

## 核心定位

- **核心差异**: 代码审查规则可源码管控（source-controlled）
- **CI 集成**: 可在 GitHub Action 中自动运行 AI code review
- **团队视角**: 适合团队规范化 AI 使用，跨人风格一致

## 适用场景

- **Per PR 自动 code review**：团队协作中抓 git diff → 跑 prompt → post 回 PR
- **CI 自动化**：配合 Claude Code Action 实现 human + AI 双审
- **适合团队规模 > 5 人**，需要统一 code review 标准

## 关联链接

- [[Claude_Code]] — Anthropic AI coding 助理（可与 Continue 配合）
- [[Cline]] — VS Code autonomous agent（同为 VS Code 生态）
- [[Roo_Code]] — VS Code multi-mode agent
- [[Developer_Agentic_Workflow]] — 开发者工作流场景分类
- [[Harness_Engineering]] — Agent 系统工程实践（CI review 属于 harness 层）
- [[Agentic_Coding]] — AI 自主编程范式
