---
title: "OpenRouter"
type: entity
tags: [工具, LLM, 路由, API]
sources: []
last_updated: 2026-07-10
---

## 定义

OpenRouter 是一个**统一的 LLM API 路由与网关服务**，提供对多个模型供应商的统一接口，支持自动 Model Routing、智能价格优化、以及 Fallback 降级机制。

## 关键信息

- **核心功能**: 统一 API 入口访问多种 LLM 模型
- **自动路由**: 根据价格、延迟、可用性智能选择最优模型
- **Fallback**: 模型不可用时自动路由到备选模型
- **价格透明**: 显示各模型的实时定价
- **应用场景**: [[Graceful_Degradation]] 优雅降级的实现方式之一

## 关联连接

- [[Graceful_Degradation]] — 作为 Fallback 路由的实现方式
- [[Cost_Optimization]] — Model Routing 是成本优化的重要策略
- [[OpenAI_Compatible_API]] — OpenRouter 兼容此标准
