---
title: "Checkpoint Commit"
type: concept
tags: [Git, 版本控制, AI编程, 最佳实践]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Checkpoint Commit（检查点提交）是一种针对耗时较长的 Agent 任务的提交策略：要求 Agent 在任务的关键节点进行阶段性提交存档，而不是等任务全部完成再提交。

## 关键提交节点

在完成以下关键节点时，执行一次 `git commit`：

1. 完成数据模型/接口定义
2. 完成核心逻辑实现
3. 完成测试编写
4. 完成文档更新

## 约定

- 每个 checkpoint commit 的 message 以 `[WIP]` 开头
- 最终完成后执行 `git commit --amend` 或通过 rebase 整理历史

## 好处

1. **断点恢复**：任务中断时可以从最近的 checkpoint 恢复，而非从头开始
2. **分段审查**：Checkpoint commit 天然成为 code review 的切分点，reviewer 可以分段审查
3. **精准 bisect**：便于 `git bisect` 定位引入问题的具体阶段

## 与 Atomic Commit 的关系

[[Atomic_Commit]] 关注的是语义边界（一个 commit 做一件事），Checkpoint Commit 关注的是进度记录（长任务中的阶段性存档）。两者互补：

- **任务进行中** → Checkpoint Commit 保存现场
- **任务完成后** → Interactive Rebase 整理为 Atomic Commit

## 关联连接

- [[Atomic_Commit]] — 与 Checkpoint Commit 互补的提交原则
- [[Agentic_Coding]] — Checkpoint Commit 的应用场景
- [[Agent_Aware_Commit]] — 提交规范的另一维度
- [[摘要-ai-era-git-management]] — 来源文章
