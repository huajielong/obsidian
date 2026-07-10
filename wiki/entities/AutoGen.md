---
title: "AutoGen"
type: entity
tags: [agent框架, multi-agent, orchestration, Microsoft, AG2]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-10
---

# AutoGen / AG2

AutoGen 是 Microsoft 推出的对话式 Multi-agent 框架，专注于 Group-Chat、Debate、Peer Review 等模式。其继任者 AG2 在 v0.4 重写为 async-first 架构。

## 核心特性

- **对话式多 Agent**：以 Group-Chat 为核心，Agent 之间自然语言对话
- **GroupChat**：多个 Agent 在同一聊天室中协作
- **Debate / Peer Review**：Agent 互相 critique
- **AG2 v0.4**：重写为 async-first、异步优先架构
- 论文发表于 2023（[Wu et al. 2023](https://arxiv.org/abs/2308.08155)）

## 覆盖的编排模式

- [[Agent_Orchestration_Patterns#4 Supervisor-Worker（Hub-Spoke）|Supervisor-Worker]] — GroupChat 实现
- [[Agent_Orchestration_Patterns#5 Debate / Society（多视角收敛）|Debate/Society]] — 最擅长的模式

## 适用场景

- 多 Agent 辩论 / 脑力激荡
- Peer Review 流程
- 社会模拟（Social Simulation）
- 研究型实验

## ⚠️ 注意事项

- AG2 v0.4 重写后，旧教程多半还在 v0.2
- v0.4 是新架构，留意版本分支
- License: CC-BY-4.0（文件 license）

## 基本信息

- **Stars**: 57k+
- **License**: CC-BY-4.0
- **GitHub**: https://github.com/microsoft/autogen

## 关联连接

- [[Agent_Orchestration_Patterns]] — AutoGen 擅长 Debate/Society 模式
- [[CrewAI]] — 角色驱动框架，与 AutoGen 的对话式不同
- [[LangGraph]] — Production 级替代方案
- [[OpenAI]] — OpenAI Agents SDK 是 Routing/Handoff 路线的代表
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本实体的核心来源
