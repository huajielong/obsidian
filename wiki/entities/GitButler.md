---
title: "GitButler"
type: entity
tags: [版本控制, VCS, 虚拟分支, a16z, 工具]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

GitButler 是一个构建在 Git 之上的版本控制客户端，提供桌面 GUI 和命令行工具 `but`。其最核心的创新是**虚拟分支（Virtual Branches）**机制：多个分支可以同时处于活跃状态，共享同一个工作目录，而无需 `git worktree`。GitButler 获得了 a16z 领投的 2200 万美元融资，明确定位为"为 AI 驱动开发重新设计的版本控制界面"。

## 关键信息

- **融资情况**：a16z 领投 2200 万美元
- **定位**：为 AI 驱动开发重新设计的版本控制界面
- **底层兼容性**：不替换 Git，底层仍是标准 Git 仓库，兼容所有现有 Git 工具链

- **核心创新：虚拟分支（Virtual Branches）**：
  - 传统 Git：先切分支再做事 → GitButler：先做事再分类
  - 直接修改文件，然后将每个 hunk（代码块）分配给对应的虚拟分支
  - 多个 Agent 可同时写入同一工作目录，按 hunk 粒度自动归类到不同分支

- **对 Agentic Coding 的关键优势**：
  - 脏工作区问题从根源消除：虚拟分支让不同关注点的变更在同一工作目录中保持分离
  - 多 Agent 并发无需 worktree：每个 Agent 会话绑定一个虚拟分支
  - Hunk 级别分配天然产生小而聚焦的提交
  - 提供 `but status --json` 输出，适合 Agent 程序化消费
  - `but branch -a` 创建 Stacked Branches（堆叠分支），自动 rebase
  - 提供内置 hooks 在 Agent 工具调用前后自动触发提交管理

- **关键命令**：
  - `but status --json` — 查看当前工作区状态（JSON 输出）
  - `but commit <branch> -m "<message>" --changes <hunk>` — 将特定 hunk 提交到指定分支
  - `but absorb` — 自动归并到最合适的提交（类似 jj absorb）
  - `but branch -a <base> <new>` — 创建堆叠分支

## 关联连接

- [[Jujutsu]] — 同为适合 Agentic Coding 的新兴 VCS 工具
- [[Virtual_Branch]] — GitButler 的核心创新概念
- [[Stacked_PR]] — GitButler 原生支持的堆叠 PR 工作流
- [[Agentic_Coding]] — GitButler 面向的核心场景
- [[摘要-ai-era-git-management]] — 来源文章
