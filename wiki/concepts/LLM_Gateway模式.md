---
title: "LLM Gateway 模式"
type: concept
tags: [LLM, API网关, 路由, 企业架构, HarnessEngineering]
sources: [raw/01-articles/llm-gateway-pattern.md]
last_updated: 2026-07-22
---

## 概述

LLM Gateway 是企业级 LLM 应用基础设施的核心组件，充当 AI 应用与各类 LLM 模型之间的**统一接入层**。在 [[Harness_Engineering]] 框架中，它属于 Harness 层的网络基础设施——解决多模型管理、流量治理、安全管控、成本追踪等共性问题。

## 核心职责

| 职责 | 说明 | 关键技术 |
|------|------|---------|
| **统一路由** | 将请求分发到最优模型（按能力/成本/延迟路由） | Model Routing、Fallback Chain、A/B Test |
| **流量治理** | 限流、熔断、重试、负载均衡 | Rate Limiting、Circuit Breaker、Retry with Backoff |
| **安全管控** | API Key 管理、鉴权、审计、数据脱敏 | RBAC/ABAC、PII Detection、Audit Log |
| **成本追踪** | Token 计量、费用分摊、预算告警 | Token Counting、Cost Attribution、Budget Alert |
| **可观测性** | Tracing、监控、评估数据采集 | OpenTelemetry、Langfuse 集成、Eval Data Pipeline |
| **协议适配** | 统一 OpenAI 兼容格式，适配不同厂商协议 | OpenAI Compatible API、Adapter Pattern |

## 架构位置

LLM Gateway 在企业 LLM 技术栈中的位置：

```
应用层 (Agent / Chatbot / RAG 应用)
       ↓
LLM Gateway ← 统一接入层（路由/限流/鉴权/成本）
       ↓
模型层 (Claude / GPT / Qwen / 本地模型)
       ↓
基础设施层 (Kubernetes / GPU 集群)
```

## 开源方案

| 方案 | 特点 | 适用场景 |
|-----|------|---------|
| **LiteLLM** | 100+ 模型兼容、内建路由/费用追踪/护栏 | 中小团队快速接入 |
| **OpenRouter** | 托管服务、按量付费、模型统一接入 | 无需自建基础设施 |
| **Kong + AI Gateway** | 企业级 API 网关 + AI 插件 | 已有 Kong 基础设施的企业 |
| **Portkey** | AI Gateway + Observability + Guardrails | 需要完整治理栈的团队 |
| **自建 Gateway** | 完全可控、深度定制 | 大规模/高安全要求的企业 |

## 在 DevOps AI 场景中的价值

LLM Gateway 是 [[摘要-devops-ai-architect-xiamen]] 中"企业级 LLM 应用基础设施"职责的核心组件：

- **DevOps Agent 场景**：多个 Agent（CICD Agent、排障 Agent、代码审查 Agent）共享 Gateway 进行模型路由和成本分摊
- **工具链集成**：Gateway 作为 MCP Server 的接入点，统一管控 Tool Calling 的鉴权和限流
- **混合部署**：企业内部敏感数据走私有化部署模型，非敏感场景用云端模型，Gateway 透明路由

## 关联连接

- [[Harness_Engineering]] — LLM Gateway 是 Harness 层基础设施的核心组件
- [[MCP]] — Gateway 可承载 MCP Server 的鉴权和流量治理
- [[微服务与API网关设计]] — 通用 API Gateway 在 LLM 场景的演进
- [[Cost_Optimization]] — Gateway 是成本追踪和模型路由优化的物理载体
- [[Agent_Observability]] — Gateway 采集的 Trace 数据是可观测性的重要来源
- [[Agent沙箱工程]] — Gateway 是沙箱环境与外部模型通信的安全边界
- [[摘要-devops-ai-architect-xiamen]] — DevOps AI 架构师 JD 中该模式的落地场景
