---
title: "AGENT.md"
type: concept
tags: [AI编程, 规范, 最佳实践]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

AGENT.md 是 AI Agent 在项目中的行为规范入口文件，应当包含所有 VCS 相关约定。Agent 在每次任务开始时都会读取并遵循该文件，是让团队规范真正生效的最低成本方式。

## 推荐的 Git 相关内容

```markdown
## Git Workflow

### Branch Naming
- Use `agent/<task-id>-<description>` for all agent-initiated branches
- Never commit directly to `main` or `develop`

### Commit Guidelines
- Follow Conventional Commits: https://www.conventionalcommits.org
- Each commit must be atomic: one logical change, buildable and testable in isolation
- Include Agent-Task, Agent-Decision trailers in commit body

### PR Process
- Open PR against `main` using the agent PR template
- Ensure all CI checks pass before requesting review
- Do not self-approve or merge your own PRs
```

## 工程实施建议

1. 将 `AGENT.md` 放置在项目根目录
2. 在 Agent 的 system prompt 中指定 `AGENT.md` 为启动时必读文件
3. 将 VCS 规范（分支命名、提交格式、PR 流程）统一写入此文件
4. 在 `AGENT.md` 中同时定义 CI 命令的使用范围

## 关联连接

- [[Agent_Aware_Commit]] — 应在 AGENT.md 中定义的提交规范
- [[Agentic_Coding]] — AGENT.md 的应用场景
- [[Feature_Branch_Workflow]] — 应在 AGENT.md 中定义的分支策略
- [[Claude_Code_Memory_System]] — Claude Code 中的 Project Memory 即 CLAUDE.md 文件
- [[Claude_Code]] — Claude Code 工具中 AGENT.md/CLAUDE.md 的实践应用
- [[摘要-ai-era-git-management]] — 来源文章
- [[摘要-claude-code-guide]] — Claude Code 使用指南中的记忆系统说明
