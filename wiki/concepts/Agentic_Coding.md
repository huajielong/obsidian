---
title: "Agentic Coding"
type: concept
tags: [AI编程, 软件开发, 范式, AGI]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Agentic Coding（AI Agent 驱动编程）是一种软件开发范式，其中 AI Agent（如 Claude Code、Cursor、TRAE 等）在无人监督或少量监督的情况下，自主地编写、修改和重构代码。与传统 AI 辅助编程（如代码补全）不同，Agentic Coding 中的 Agent 可以连续执行跨多文件、跨模块的复杂开发任务。

## 核心特征

- **自主执行**：Agent 可以在无人监督的情况下连续修改数十个文件，跨越数分钟到数小时
- **并发协作**：多个 Agent 实例可以同时在同一个代码仓库中并行工作
- **任务粒度不匹配**：一个自然语言描述的任务可能对应上百次文件操作
- **决策黑盒**：Agent 的中间推理过程传统上不会留在 Git 历史中，只有最终代码变更可见

## 带来的 Git 版本控制挑战

Agentic Coding 打破了传统 Git 的基本假设——"一个开发者的一次有意图的决策"：

1. **意图缺失**：Git 只记录 diff，Agent 的推理过程、prompt 依据和设计决策不会被自动记录
2. **脏工作区**：Agent 探索过程快速分散，临时文件、格式化变更和业务修改混在一起
3. **语义合并**：Git merge 只做文本校验，多 Agent 并发时"无冲突合并"不等于"语义正确"
4. **巨型提交**：Agent 倾向于产出巨型 diff，导致审查、回滚和 bisect 定位全部失效

## 应对策略

- 建立 [[Agent_Aware_Commit]] 规范，通过 commit trailer 记录 Agent 决策
- 采用 [[Checkpoint_Commit]] 策略在关键节点存档
- 通过 [[Atomic_Commit]] 保证每个提交的语义清晰
- 使用 [[Virtual_Branch]]（如 [[GitButler]]）或 [[Jujutsu]] 等更适合 Agent 的 VCS 工具
- 维护 [[AGENT_MD]] 作为 Agent 行为规范文件

## 关联连接

- [[Agent_Aware_Commit]] — 为 Agentic Coding 设计的提交规范
- [[Jujutsu]] — 以变更为中心的 VCS，天然适合 Agent 工作流
- [[GitButler]] — 虚拟分支机制，解决多 Agent 并发问题
- [[Monorepo]] — 单仓库策略对 Agentic Coding 的优势
- [[摘要-ai-era-git-management]] — 来源文章
- [[摘要-agentic-ai-roadmap]] — Agentic AI 从零到入门的系统学习路线
