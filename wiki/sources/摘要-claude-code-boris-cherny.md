---
title: "摘要-Claude Code Boris Cherny 最佳实践"
type: source
tags: [Claude Code, Boris Cherny, 最佳实践, Opus]
sources: [raw/01-articles/Claude Code/Boris Cherny 公开 · Claude Code + Opus 4.7 最佳实践.md]
last_updated: 2026-07-03
---

# Boris Cherny Claude Code 最佳实践

## 核心主旨

Boris Cherny 公开的 Claude Code + Opus 4.7 最佳实践速查清单，包含核心配置、CLAUDE.md 规范、工作流、指令话术、避坑规则。

## 核心配置

- 固定模型：**Claude Opus 4.7**
- 全局 xhigh 推理强度：`claude config set effort xhigh`
- 开启深度思考模式
- 严格模式：`claude config set strict true`

## CLAUDE.md 规范

Boris 所有项目强制维护 CLAUDE.md，本质是给 AI 一份"项目宪法"：
- 定义项目架构、代码风格、目录规范、禁用写法
- 约定测试规则、错误处理、日志规范、PR 标准
- 防止 AI 瞎改、过度重构

提供了完整的**通用标准版**和**精简轻量版**两套 CLAUDE.md 模板。

## 效率策略

1. **多会话并行**：功能开发 + 代码审查 + 技术调研各一个会话
2. **完全放弃手写代码**：全部由 AI 生成，人只做决策、评审、架构、验收
3. **高频小提交**：日均 20-30 个小 PR/提交

## 避坑规则

- 不要用 low/medium effort 做复杂业务
- 不要不给上下文就丢模糊需求
- 禁止一次性重构整个项目
- 修改后必须人工关键逻辑复核

## 关联连接
- [[Claude_Code]] — Claude Code 实体
- [[AGENT_MD]] — AI Agent 行为规范入口文件
- [[Boris_Cherny]] — Boris Cherny 人物实体
