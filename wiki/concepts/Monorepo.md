---
title: "Monorepo"
type: concept
tags: [代码管理, 架构, 版本控制]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Monorepo（单仓库策略）是一种将多个项目或服务的代码放在同一个版本控制仓库中的策略。在 [[Agentic_Coding]] 场景下，Monorepo 展现出显著优势，因为 Agent 可以在单次上下文窗口内完整追踪一个用户动作从 UI 到数据库的完整链路。

## Monorepo 对 Agentic Coding 的优势

### 1. 完整的跨服务上下文
Agent 无需在多个仓库之间跳转，可以在一次任务中同步修改 API 定义和对应的客户端调用，保证接口一致性。这类修改在 polyrepo 中需要多个协调的 PR，Agent 往往无法独立完成。

### 2. 大规模重构与迁移
Monorepo 让 Agent 能够可靠地执行影响范围广的重构，如修改共享 utility 函数签名后同时更新所有调用方。

### 3. 依赖图可见性
配合 Monorepo 工具（如 [[Nx]]、[[Turborepo]]），Agent 可以查询"修改了 package A 之后，哪些 package 受到影响"，精确决定需要运行哪些测试。

## Monorepo 下的 VCS 挑战

### 并发冲突风险
所有 Agent 共享同一个仓库，公共文件（`package.json`、共享类型定义、配置文件）的冲突概率远高于 polyrepo。应对手段：
- `git worktree` 或 [[GitButler]] 虚拟分支
- 每个 Agent 任务独立的隔离工作区

### PR Diff 容易变大
涉及共享 package 的修改可能产生较大的 diff。[[Stacked_PR]] 在 Monorepo 中尤为有价值。

### CI 范围界定
需要配合依赖图工具实现"只跑受影响 package 的测试"。在 `AGENT.md` 中明确说明适合 Agent 本地运行的 CI 命令：

```
### CI Commands for Agents
# 只运行受当前变更影响的 package 的测试
nx affected --target=test
turbo run test --filter='[HEAD^1]'

# 全量检查由 CI 执行，不建议 Agent 本地全量运行
```

### Atomic Commit 边界
修改共享 library 的同时必须同步更新消费方——这些修改在逻辑上不可分割，可以放在同一个 [[Atomic_Commit]] 中。

## 关联连接

- [[Atomic_Commit]] — Monorepo 中的透明提交边界
- [[Agentic_Coding]] — Monorepo 对 AI 编程的核心优势
- [[Stacked_PR]] — Monorepo 中尤其有价值的 PR 策略
- [[GitButler]] — 虚拟分支解决 Monorepo 并发冲突
- [[摘要-ai-era-git-management]] — 来源文章
