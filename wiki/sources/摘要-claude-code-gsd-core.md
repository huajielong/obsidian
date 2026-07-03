---
title: "摘要-GSD Core 开发框架"
type: source
tags: [Claude Code, GSD, 开发框架, 项目管理]
sources: [raw/01-articles/Claude Code/GSD Core安装到Claude Code.md]
last_updated: 2026-07-03
---

# GSD Core：Claude Code 项目开发框架

## 核心主旨

GSD Core 是基于 Claude Code 的全生命周期项目开发框架，从项目初始化、需求讨论、规划、执行、验证到交付，提供完整的 6 步工作流。

## 核心工作流

1. **/gsd-new-project** — 初始化项目，自动启动 4 个并行 researcher agent 研究技术栈
2. **/gsd-discuss-phase** — 讨论 Phase 决策（UI、API、数据库等）
3. **/gsd-plan-phase** — 规划 Phase，拆分成原子 task，Plan Checker 验证
4. **/gsd-execute-phase** — 并行执行，多个 executor 各自 fresh 200K context
5. **/gsd-verify-work** — 验证功能是否正常，自动诊断 + 修复
6. **/gsd-ship** — 推送分支、生成 PR、更新 STATE.md

## 架构特点

- 33 个专门化 Agent（agents/gsd-*.md）
- 60+ 个 GSD 命令（commands/gsd/*.md）
- 运行时 Hooks（context 监控等）
- 支持 Global 和 Local 两种安装模式

## 关联连接
- [[Claude_Code]] — Claude Code 实体
- [[GSD_Core]] — GSD Core 实体
- [[Claude_Code_Workflow]] — Claude Code 工作流方法论
