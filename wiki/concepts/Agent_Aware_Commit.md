---
title: "Agent-Aware Commit"
type: concept
tags: [Git, 版本控制, AI编程, 最佳实践]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Agent-Aware Commit 是为 AI Agent 生成代码设计的提交规范，通过在 Git commit message 中引入结构化元数据（[[Commit_Trailer]]），使 Agent 的决策过程、使用模型和任务背景在版本历史中可见。

## 核心原则

每个 commit 应当能独立描述"做了什么、为什么、上下文是什么"。

## 推荐的 Commit Message 格式

```
<type>(<scope>): <summary>

<正文：描述本次变更的背景与动机>

Agent-Task: <原始任务描述或任务 ID>
Agent-Model: <使用的模型，如 gpt-4o、gemini-2.5-pro>
Agent-Decision: <关键设计决策及理由>
Agent-Limitation: <已知局限或后续 TODO>
```

## 示例

```
feat(auth): implement JWT refresh token rotation

Add sliding-window refresh token support to reduce re-login friction
while maintaining session security.

Agent-Task: PROJ-234 - Add refresh token support to auth service
Agent-Model: gpt-4o
Agent-Decision: Used 7-day sliding window over fixed expiry for better UX;
  refresh tokens stored in httpOnly cookie to prevent XSS access
Agent-Limitation: Redis TTL not yet aligned with token expiry on logout
```

## Trailer 标准字段

上述 `Agent-Task:`、`Agent-Model:` 等字段使用 Git 内置的 commit trailer 机制，由 `git` 原生解析：

| Trailer 字段 | 用途 | 必填 |
|---|---|---|
| `Agent-Task` | 原始任务描述或任务 ID | 推荐 |
| `Agent-Model` | 使用的 AI 模型 | 推荐 |
| `Agent-Decision` | 关键设计决策及理由 | 推荐 |
| `Agent-Limitation` | 已知局限或后续 TODO | 可选 |

## 查询 Trailer

```bash
# 列出所有包含 Agent-Task trailer 的提交
git log --format='%(trailers:key=Agent-Task,valueonly)'

# 按 trailer 过滤提交历史
git log --grep="^Agent-Task:" --all
```

## 工程实施建议

1. 在 Agent 的 system prompt 或 [[AGENT_MD]] 中明确要求上述格式
2. 使用 `commit-msg` hook 校验 agent commit 是否包含必要的 trailer 字段
3. 用类型前缀区分来源：`feat`/`fix`/`refactor` 等遵循 Conventional Commits，agent 生成的提交可额外加 `[AI]` 标签便于过滤

## 关联连接

- [[Commit_Trailer]] — trailer 机制的技术基础
- [[Agentic_Coding]] — Agent-Aware Commit 的应用场景
- [[Atomic_Commit]] — 与 Agent-Aware Commit 互补的提交原则
- [[Checkpoint_Commit]] — Agent 任务中的阶段性提交策略
- [[AGENT_MD]] — 在其中定义提交规范
- [[摘要-ai-era-git-management]] — 来源文章
