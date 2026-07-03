---
title: "GSD Core"
type: entity
tags: [Claude Code, 开发框架, 项目管理, OpenGSD]
sources: [raw/01-articles/Claude Code/GSD Core安装到Claude Code.md]
last_updated: 2026-07-03
---

# GSD Core

## 定义

GSD Core（Get Stuff Done Core）是基于 Claude Code 的全生命周期项目开发框架，由 OpenGSD 社区维护。它提供了从项目初始化到交付的完整 6 步工作流，深度融合了 Agent 协同能力。

- **GitHub**：https://github.com/open-gsd/gsd-core
- **安装**：`npx @opengsd/gsd-core@latest`

## 核心工作流

| 步骤 | 命令 | 说明 |
|------|------|------|
| 1. 初始化 | `/gsd-new-project` | 4 并行 researcher agent 研究技术栈 |
| 2. 讨论 | `/gsd-discuss-phase N` | 讨论 UI/API/数据库等决策 |
| 3. 规划 | `/gsd-plan-phase N` | 拆原子 task，Plan Checker 验证 |
| 4. 执行 | `/gsd-execute-phase N` | 并行 executor（各 200K fresh context） |
| 5. 验证 | `/gsd-verify-work N` | 自动诊断 + 修复 |
| 6. 交付 | `/gsd-ship N` | 推送分支、生成 PR |

## 架构特点

- 33 个专门化 Agent 定义
- 60+ GSD 命令
- 运行时 Hooks（context 监控等）
- 支持 Global（一次安装全局可用）和 Local（项目级隔离）

## 关联连接
- [[Claude_Code]] — Claude Code 实体
- [[摘要-claude-code-gsd-core]] — GSD Core 源摘要
- [[Claude_Code_Workflow]] — 工作流方法论
