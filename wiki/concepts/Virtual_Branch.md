---
title: "Virtual Branch"
type: concept
tags: [版本控制, GitButler, 工作流, AI编程]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Virtual Branch（虚拟分支）是 [[GitButler]] 版本控制客户端的核心创新。它允许**多个分支同时处于活跃状态，共享同一个工作目录**，而无需 `git worktree`。虚拟分支机制改变了传统 Git 的工作方式。

## 与传统 Git 的对比

| 维度 | 传统 Git | GitButler 虚拟分支 |
|---|---|---|
| 工作方式 | 先切分支再做事 | 先做事再分类 |
| 分支切换 | 需要 checkout，工作区切换 | 直接修改，按 hunk 归类 |
| 多 Agent 并发 | 需 worktree 或多次 clone | 共享同一工作目录 |
| 变更分类 | 按文件粒度 | 按 hunk（代码块）粒度 |

## 工作原理

1. **直接修改文件**：开发者/Agent 直接在工作目录中修改代码
2. **分配 Hunk**：将每个 hunk（代码块）分配给对应的虚拟分支
3. **提交**：将特定 hunk 提交到指定分支

```bash
# 将 service.ts 提交到 refresh-token 分支
$ but commit feat/refresh-token -m "feat(auth): implement token rotation" --changes g0
```

## 对 Agentic Coding 的意义

1. **脏工作区消除**：不同关注点的变更在目录中保持分离，`git diff` 噪声从根源消除
2. **无 worktree 并发**：多 Agent 写入同一目录，按 hunk 自动归类
3. **天然小提交**：hunk 级别分配产生小而聚焦的提交
4. **程序化交互**：`but status --json` 输出 JSON，适合 Agent 消费

## 关联连接

- [[GitButler]] — 虚拟分支的具体实现
- [[Jujutsu]] — 另一种不同的 VCS 心智模型
- [[Agentic_Coding]] — 虚拟分支解决的核心场景
- [[Stacked_PR]] — 虚拟分支与 Stacked Branches 的关系
- [[摘要-ai-era-git-management]] — 来源文章
