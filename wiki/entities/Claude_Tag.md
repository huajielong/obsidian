---
title: "Claude Tag"
type: entity
tags: [Anthropic, Slack, 值班, 事件响应, Agent]
sources: [raw/09-archive/The AI-Native SDLC playbook  Claude by Anthropic.md]
last_updated: 2026-09-04
---

# Claude Tag

## 定义

Anthropic 推出的**值班/事件响应 Agent**（Slack 公测中）：让 Claude 以**自己的身份**成为工作频道（Slack/Teams 等）的成员，事件一来就有「第一响应者」自动接单，无需人等 3 a.m. 告警。响应过程本身成为循环与记忆的一部分。

## 关键信息

- **触发方式**：incident channel 消息、ticket 上 @（经 MCP）、频道内直接提问。
- **能力**：在频道内即时响应、诊断；任何团队成员都能引导与操作（可并行验证假设、探索方案、实时调查）；经 MCP 访问外部系统验证指标已回到基线并在 thread 中确认；把 post-mortem 写入**版本化的 lessons 文件**，供未来调查读取。
- **处置分级**：小型有界修复 → 以 PR 形式走 review gate；更大的问题 → 写成 `intent.md` 从 Plan 阶段重新进入 [[AI_SDLC]]——**loop 开始自我喂食**。
- **审计性**：请求、诊断、人类授权、修复都留在 incident 发生的频道里——**频道即审计追踪**。
- **Institutional knowledge**：对话与事后总结留在频道，形成未来 incident 可读的组织记忆。

## 在 AI-Native SDLC 中的位置

Maintain 阶段「Claude on call」play——与 deterministic 检测脚本（closing the loop）互补：脚本覆盖「控制带被突破」这类指标事件，Claude Tag 覆盖「从 IM/工单到达」这类通道事件；两者都把发现写回 `intent.md`。

## 关联连接

- [[Anthropic]] — 开发商（Claude Tag 是其产品线之一）
- [[AI_SDLC]] — 所属的 AI 原生软件生命周期（Maintain 阶段 play）
- [[Claude_Code]] — 走 PR review gate 时的执行工具
- [[MCP]] — 访问指标/工单/部署系统的通道
- [[Slack]] — 主要运行载体（IM 通道即 agent 界面）
- [[Agent_Observability]] — 值班响应的会话留痕
- [[摘要-ai-native-sdlc-playbook]] — 来源
