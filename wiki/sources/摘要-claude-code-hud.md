---
title: "摘要-claude-hud 状态监控插件"
type: source
tags: [Claude Code, 插件, 监控, 工具]
sources: [raw/01-articles/Claude Code/Claude Code 必装插件：claude-hud 让你的 AI 编程效率翻倍.md]
last_updated: 2026-07-03
---

# claude-hud：Claude Code 状态监控插件

## 核心主旨

claude-hud 是 Claude Code 的终端状态监控插件，在终端底部实时显示上下文占用、配额消耗、工具活动等关键指标，让 AI 编程从"黑盒"变"透明箱"。

## 核心功能

- **Context 进度条**：上下文窗口占用百分比（>70% 变黄，>90% 变红）
- **Usage 配额消耗**：API 配额使用率 + 重置倒计时
- **Weekly 周配额**：更长远规划 AI 使用策略
- **工具活动追踪**（可选）：实时显示 Claude Code 正在调用的工具
- **Agent 与 Todo 状态**（可选）：子代理并行工作状态和耗时

## 三个预设方案

- **Minimal**：仅模型名称 + 上下文进度
- **Essential**：核心指标 + Git 状态 + 工具活动（日常推荐）
- **Full**：所有模块全开（复杂项目调试）

## 实战建议

超过 50% 上下文占用时执行 `/clear`，避免 AI 回答质量骤降。

## 关联连接
- [[Claude_Code]] — Claude Code 实体
- [[Claude_Code_Slash_Commands]] — 斜杠命令体系
