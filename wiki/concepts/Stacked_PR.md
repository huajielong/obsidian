---
title: "Stacked PR"
type: concept
tags: [Git, 版本控制, 代码审查, 工作流]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Stacked PR（堆叠 PR）是一种将大任务拆解为多个按依赖关系层叠的 PR 的工作流。每个 PR 针对前一个 PR 的分支而非 main 分支，形成有序的依赖链。每层 PR 只展示当前层的 diff，reviewer 可以独立审查每一层，合并时按顺序从底部开始依次合入。

## 结构示意

```
main
 └── PR #1：feat(auth): add RefreshToken domain model
       └── PR #2：feat(auth): implement token rotation in AuthService
             └── PR #3：feat(auth): expose POST /auth/refresh endpoint
                   └── PR #4：test(auth): add integration tests
```

## 核心优势

1. **降低审查复杂度**：每层 PR 只展示当前层的 diff，reviewer 可以聚焦审查
2. **并行开发**：底层 PR 在审查中时，上层可以继续开发
3. **精确 CI**：每层 PR 的 CI 针对其实际目标分支运行

## 工具支持

### GitHub gh-stack
GitHub 正在以 `gh-stack` 的形式将 Stacked PR 作为原生特性引入（private preview）：
- PR 头部的 Stack Navigator：在 PR 页面直接看到整条依赖链并在各层之间跳转
- 聚焦 diff：每层 PR 只展示相对于下一层的变更
- 按层运行 CI
- 一键合并整个 stack

### [[Jujutsu]] 原生支持
jj 的提交链天然就是 stacked PR 的工作单元。修改任意一层后，jj 自动 rebase 所有后代，无需手动维护级联关系。

### [[GitButler]] 的 Stacked Branches
通过 `but branch -a` 创建堆叠分支，修改底层分支后上层自动 rebase，GUI 提供可视化 stack 视图。

## 关联连接

- [[GitButler]] — 原生支持 Stacked Branches
- [[Jujutsu]] — 提交链天然支持 Stacked PR
- [[Agent_Aware_Commit]] — 配合 Stacked PR 的提交规范
- [[Monorepo]] — Stacked PR 在 Monorepo 中尤为有价值
- [[摘要-ai-era-git-management]] — 来源文章
