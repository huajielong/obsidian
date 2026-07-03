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

## CLAUDE.md 编写规范（Boris Cherny 风格）

Boris Cherny 推荐在项目中强制维护 CLAUDE.md，作为 AI 的"项目宪法"，杜绝瞎改和过度重构。

### 通用标准版模板（企业/大型TS/团队项目）
```markdown
# CLAUDE.md — Project AI Coding Guidelines

## 1. Core Principles
- Make minimal, focused changes only. No unnecessary refactoring, style tweaking, or unrelated cleanup.
- Preserve existing project architecture, folder structure, coding patterns and tech stack.
- Prioritize correctness, readability, maintainability over clever one-liners.
- Do not break existing features, APIs, interfaces or data formats.

## 2. Code Style & Quality
- Keep code consistent with current project style, indentation, naming convention.
- Avoid magic numbers, hardcoded secrets, raw magic strings.
- Strong type safety first (TypeScript / static type preferred).
- No any abuse, implicit any, unsafe type assertion.

## 3. Feature & Bug Fix Rules
- For new features: Analyze current code flow → design incremental → add tests → keep backward compat.
- For bug fixes: Find root cause → write reproduction → fix edge cases → add regression test.

## 4. Testing & Validation
- Add unit/integration tests for newly added logic.
- Ensure all existing tests pass after modification.
- Run lint, type check, format check before finalizing.

## 5. Refactor Limitation
- Do NOT refactor unrelated files / modules / functions.
- Large-scale refactoring must be requested explicitly.
- Split big tasks into small, incremental steps.

## 6. Command & Tool Rules
- Use existing project scripts / commands.
- Do not install extra dependencies without permission.

## 7. Output Requirement
- Give brief summary of changes after work done.
- List breaking changes / attention points if any.
```

### 精简轻量版（小项目/脚本/个人项目）
```markdown
# CLAUDE.md
## 基础规则
1. 只做最小必要修改，不擅自全局重构、不乱改无关代码。
2. 完全沿用项目现有写法、缩进、命名、代码风格。
3. 保证代码可运行、无语法错误、无明显漏洞。

## 编码要求
1. 逻辑清晰，变量命名易懂，复杂逻辑加简短注释。
2. 杜绝硬编码密钥、明文密码、敏感信息。
3. TS 项目尽量收紧类型，少用 any。

## 功能 & 修复
1. 新增功能：增量开发，不破坏原有逻辑。
2. 修复问题：定位根因，不临时打补丁糊弄。

## 限制
- 不私自安装新依赖、不改构建/配置文件。
- 大规模重构、目录调整、架构改动，必须先询问。

## 交付
每次完成后，简要说明改动内容与注意事项。
```

## CLAUDE.md 配置层级

| 级别 | 路径 | 共享范围 |
|------|------|----------|
| 企业级 | /Library/Application Support/ClaudeCode/CLAUDE.md | 团队共享 |
| 全局级 | ~/.claude/CLAUDE.md | 仅自己 |
| 项目级（共享） | 项目根目录/CLAUDE.md | 团队共享 |
| 项目级（本地） | 项目根目录/CLAUDE.local.md | 仅自己 |
| 目录级 | 子目录下的 CLAUDE.md | 特定模块 |

## 关联连接

- [[Agent_Aware_Commit]] — 应在 AGENT.md 中定义的提交规范
- [[Agentic_Coding]] — AGENT.md 的应用场景
- [[Feature_Branch_Workflow]] — 应在 AGENT.md 中定义的分支策略
- [[Claude_Code_Memory_System]] — Claude Code 中的 Project Memory 即 CLAUDE.md 文件
- [[Claude_Code]] — Claude Code 工具中 AGENT.md/CLAUDE.md 的实践应用
- [[Boris_Cherny]] — 提供 CLAUDE.md 编写规范的行业专家
- [[摘要-ai-era-git-management]] — 来源文章
- [[摘要-claude-code-guide]] — Claude Code 使用指南中的记忆系统说明
- [[摘要-claude-code-boris-cherny]] — Boris Cherny 最佳实践
