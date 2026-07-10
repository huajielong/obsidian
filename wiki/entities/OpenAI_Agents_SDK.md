---
title: "OpenAI_Agents_SDK"
type: entity
tags: [agent框架, OpenAI, SDK, agent-handoff, production]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-10
---

# OpenAI Agents SDK

OpenAI 官方推出的 Agent SDK，提供 Agent Hand-off + 结构化输出（Structured Outputs）等核心功能。API 设计干净，MIT 许可证。**2026-04 起内建 sandbox（7 个 provider）+ harness 抽象层**，Production coding agent 首次架构健全。

## 核心特性

- **Agent Hand-off**：Agent 之间 1:1 轻量交接
- **Structured Outputs**：结构化输出控制
- **Sandbox**（2026-04 新增）：7 个 provider + harness 抽象层
- **API 干净**：学习曲线低
- **OpenAI 生态**：与 GPT 系列模型深度集成

## 覆盖的编排模式

- [[Agent_Orchestration_Patterns#1 Routing / Handoff|Routing / Handoff]] — 最擅长的模式

## 适用场景

- 已 commit OpenAI 生态
- 需要 Agent 间轻量 Handoff
- Routing 类任务（客户支持路由等）
- Production coding agent（2026-04 起）

## 历史渊源

OpenAI 先发布了 **Swarm**（实验性/教育性，~200 LOC、只有 Agent + handoff 两个概念）作为 Multi-agent mental model 的教学工具，随后在此基础上推出了更完善的 Agents SDK。

## 基本信息

- **License**: MIT
- **GitHub**: https://github.com/openai/openai-agents-python

## 关联连接

- [[OpenAI]] — 模型的开发商和 SDK 的发布者
- [[AutoGen]] — 对话式 Multi-agent，与 SDK 的 Hand-off 路线不同
- [[LangGraph]] — Production 级替代方案（更完善的 checkpointing）
- [[Agent_Orchestration_Patterns]] — SDK 主要服务 Routing/Handoff 模式
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本实体的核心来源
