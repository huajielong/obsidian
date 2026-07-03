---
title: "Feature Branch Workflow"
type: concept
tags: [Git, 版本控制, 工作流, 最佳实践]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Feature Branch Workflow（功能分支工作流）是一种 Git 分支管理策略，要求所有功能开发在独立的功能分支上完成，通过 Pull Request 合并到主分支。在 [[Agentic_Coding]] 场景下，这一策略尤为重要——任何 Agent 都不应该有权限直接推送到 `main` 或 `master`。

## Agent 场景下的分支命名规范

```
agent/<task-id>-<brief-description>

# 示例
agent/PROJ-234-refresh-token-rotation
agent/PROJ-301-migrate-postgres-schema
```

## Branch Protection Rules 配置（GitHub 示例）

- Require pull request before merging: ✅
- Require approvals: 1（至少一个人工审查通过）
- Dismiss stale pull request approvals when new commits are pushed: ✅
- Require status checks to pass before merging: ✅
- Restrict who can push to matching branches: 仅允许 CI bot 和指定人员

## Agent 操作规范

1. Agent 每次执行新任务前，从最新的 `main` 切出新分支
2. 任务完成后由 Agent 开 PR，但 merge 动作由人工触发
3. 避免在同一分支上执行多个不相关的 Agent 任务

## 关联连接

- [[Agentic_Coding]] — Feature Branch 在 Agent 场景下的应用
- [[Agent_Aware_Commit]] — 配合 Feature Branch 的提交规范
- [[GitButler]] — 虚拟分支提供另一种并发管理方式
- [[Jujutsu]] — jj 的提交链模型简化分支管理
- [[摘要-ai-era-git-management]] — 来源文章
