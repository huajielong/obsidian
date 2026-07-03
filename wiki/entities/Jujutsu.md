---
title: "Jujutsu"
type: entity
tags: [版本控制, VCS, jj, Google, 工具]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Jujutsu（命令行工具为 jj）是由 Google 工程师 Martin von Zweigbergk 开发的版本控制系统。它使用 Git 仓库作为存储后端，完全兼容 Git 生态，但在心智模型上做了根本性的重新设计——以"变更"而非"提交"为中心。目前已在 Google 内部大规模使用。

## 关键信息

- **开发者**：Martin von Zweigbergk（Google 工程师）
- **兼容性**：以 Git 仓库为存储后端，完全兼容 Git 生态，可使用 `jj git init --colocate` 在现有 Git 仓库中启用
- **核心创新**：
  - **工作区即提交（Working Copy as a Commit）**：工作区始终是一个提交（标记为 @），文件改动实时反映，永不丢失未保存工作
  - **Change ID vs Commit ID 双标识符**：Change ID 是稳定的字母标识符，无论修改多少次都不变；Commit ID 是内容哈希，内容变化即改变
  - **冲突为一等公民**：冲突存储在提交对象中，rebase 遇到冲突不会中止，可随时回来解决
  - **操作日志**：每条命令都留下操作日志，`jj op undo` 可撤销任意操作，相当于无限 undo

- **对 Agentic Coding 的关键优势**：
  - 脏工作区自动记录，Agent 的探索过程不会丢失
  - `jj split` 和 `jj absorb` 让拆分和重新归类变更极低成本
  - 自动 rebase 后代，Agent 修改历史提交无需手动维护提交链
  - `jj log` 提交图直观展示变更关系

## 关联连接

- [[GitButler]] — 同为适合 Agentic Coding 的新兴 VCS 工具
- [[Agentic_Coding]] — jj 的设计对 AI Agent 编程场景尤其友好
- [[Virtual_Branch]] — GitButler 的虚拟分支概念，与 jj 不同思路
- [[摘要-ai-era-git-management]] — 来源文章
