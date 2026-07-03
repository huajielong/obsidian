---
title: "OpenClaw"
type: entity
tags: [AI Agent, 开源平台, Skills, 插件]
sources: [raw/01-articles/OpenClaw信息库/]
last_updated: 2026-07-03
---

# OpenClaw

## 定义

OpenClaw 是一个开源的 AI Agent 平台/工具，具备插件化 Skills 系统、Context 引擎、Session 管理、多模型支持等能力。截至 2026 年 3 月，其 Skills 生态超过 1700+。

- **官网**：https://openclaw.ai/
- **GitHub**：https://github.com/openclaw/openclaw
- **文档**：https://docs.openclaw.ai
- **插件市场**：https://clawhub.ai

## 关键特性

### Skills 插件生态
- 四种安装方式：ClawHub CLI / openclaw CLI / 手动 / GitHub
- 必装 Top 10：skill-vetter、tavily-search、agent-browser、summarize、self-improving-agent 等
- 分类：安全保障、信息检索、浏览器自动化、创意娱乐、运维必备

### Session v2.0
- 子会话池架构：主会话 + 多个子会话并行处理
- 性能提升：并发响应时间降低 62%，内存占用降低 43%
- 上下文继承机制

### ContextEngine 可插拔
- v2026.3.7 引入，全生命周期钩子（bootstrap/ingest/assemble/compact/afterTurn）
- 可插拔的记忆系统

### 变现生态
代部署（500-1500元/单）、模板售卖（49-299元）、培训课程、企业服务（5000-20000元/单）

## 关联连接
- [[摘要-openclaw-info]] — OpenClaw 信息库汇总
- [[Agent_Loop]] — Agent Loop 核心概念
- [[Harness_Engineering]] — 驾驭工程体系
