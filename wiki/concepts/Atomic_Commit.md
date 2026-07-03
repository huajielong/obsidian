---
title: "Atomic Commit"
type: concept
tags: [Git, 版本控制, 最佳实践]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Atomic Commit（原子提交）是一种 Git 提交策略，核心定义是：一个 commit 只表达一个**可解释、可回滚、可验证**的语义变化，且在该 commit 节点上代码可以编译、测试可以通过。

## 在 Agentic Coding 场景下的重要性

Agent 执行长任务时，往往将多个不相关的修改混入同一次提交，Atomic Commit 是对抗这种熵增的直接手段：

1. **可回滚性**：保持每个 commit 可独立回滚，降低 Agent 引入问题时修复成本
2. **可审查性**：Reviewer 按 commit 逐步理解变更，不必面对巨型 diff
3. **可定位性**：`git bisect` 的定位精度直接取决于 commit 粒度

## 切分原则

这里的 Atomic 不是"一行一提交"，而是按**逻辑关注点**切分：

### 好的切分
```
feat(auth): add RefreshToken domain model and repository interface
feat(auth): implement JWT refresh token issuance in AuthService
feat(auth): expose POST /auth/refresh endpoint
test(auth): add unit tests for refresh token rotation logic
```

### 反例
```
feat(auth): implement refresh token    ← 所有改动压成一个 commit
```

## 与 Checkpoint Commit 的关系

[[Checkpoint_Commit]] 关注的是**进度记录**（长任务中的阶段性存档），Atomic Commit 关注的是**语义边界**（一个 commit 做一件事）。两者互补：Checkpoint Commit 在任务进行中保存现场，最终通过 Interactive Rebase 整理为一组语义清晰的 Atomic Commit。

## 在 Agent 系统提示中引导

```
When implementing a feature, break your work into atomic commits:
- Each commit must represent exactly one logical change
- Each commit must leave the codebase in a buildable, testable state
- Do not mix refactoring with feature changes in the same commit
- Do not mix changes to multiple unrelated modules in the same commit
```

## Monorepo 中的 Atomic Commit 边界

在 [[Monorepo]] 中，"一件事"需要更明确的定义。修改共享 library 的同时必须同步更新消费方——这些修改在逻辑上是不可分割的，可以放在同一个 commit 中。

## 关联连接

- [[Checkpoint_Commit]] — 长任务中的阶段性存档，与 Atomic Commit 互补
- [[Agentic_Coding]] — Atomic Commit 在 Agent 场景中的特殊重要性
- [[Agent_Aware_Commit]] — 提交规范的另一维度
- [[Monorepo]] — Monorepo 中的 Atomic Commit 边界问题
- [[摘要-ai-era-git-management]] — 来源文章
