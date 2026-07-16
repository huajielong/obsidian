---
title: "微服务与API网关设计"
type: concept
tags: [微服务, API Gateway, 架构, 中间件, 分布式系统, Agent平台]
sources: []
last_updated: 2026-07-16
---

# 微服务与 API 网关设计

## 定义

微服务架构是将应用拆分为一组**独立部署、松耦合、围绕业务能力组织**的服务，每个服务有自己的数据存储、部署管道和扩展策略。API Gateway 是微服务集群的**统一入口层**，负责请求路由、认证授权、限流熔断、协议转换等横切关注点。

在 AI Agent 平台场景中，微服务与 API Gateway 的设计比传统业务系统有更多**特殊性**——需要处理 LLM 的流式响应、Tool Schema 的动态注册、Agent 状态的一致性等 Agent 原生问题。

## 微服务核心概念

### 分解原则

| 原则 | 说明 | Agent 平台示例 |
|------|------|---------------|
| **业务能力拆分** | 按业务领域划分服务边界 | Agent 运行时 / Tool 注册中心 / Memory 服务 |
| **数据库隔离** | 每个服务独立数据存储 | Agent State DB / Tool Schema DB / Memory Store |
| **自治部署** | 服务可独立开发/测试/部署 | 各服务独立 CI/CD Pipeline |
| **通信契约** | 服务间通过 API 契约交互 | OpenAPI / gRPC / 事件 Schema |

### 关键模式

| 模式 | 解决的问题 | Agent 场景应用 |
|------|-----------|---------------|
| **Saga** | 跨服务的分布式事务一致性 | Agent 多步骤执行中跨服务回滚 |
| **CQRS** | 读写分离，查询与命令走不同路径 | Agent 状态写入 Memory vs 检索 Memory |
| **Event Sourcing** | 以事件流存储状态变化 | Agent 执行轨迹的可审计 replay |
| **Sidecar** | 服务外挂通用组件（日志/监控） | Agent 可观测性 Agent Sidecar |
| **Strangler Fig** | 渐进式系统迁移 | 旧系统逐步替换为 Agent 增强的新系统 |

## API Gateway 核心功能

### 通用 API Gateway

| 功能 | 说明 | 示例实现 |
|------|------|---------|
| **请求路由** | 按路径/Header 分发到后端服务 | `/agent/*` → Agent Service |
| **认证授权** | JWT/OAuth/API Key 校验 | 统一鉴权层 |
| **限流熔断** | 防止后端被突发流量打垮 | Token Bucket / Circuit Breaker |
| **协议转换** | REST ↔ gRPC / HTTP ↔ WebSocket | Agent 流式响应转换 |
| **请求聚合** | 合并多个后端请求为一个响应 | BFF (Backend for Frontend) |
| **负载均衡** | 多实例分发 | Round-Robin / Least Connections |

### Agent 场景下 API Gateway 的特殊要求

Agent 平台中的 Gateway 与传统场景有本质差异：

| 传统 Gateway 场景 | Agent 平台特殊场景 |
|-----------------|------------------|
| 请求-响应模式，短连接 | **流式响应**（SSE/WebSocket），长时间连接 |
| 静态路由规则 | **动态路由**——根据 Tool Schema 实时路由 |
| 固定 HTTP Method | **Function Calling 协议**——需理解 LLM 的 Tool 调用格式 |
| 单一 API 版本 | **Schema 版本管理**——Tool 定义持续演进 |
| 简单的请求/响应转换 | **Message 格式转换**——LLM ↔ 后端服务之间的格式桥接 |

#### Agent Gateway 的六个关键设计点

1. **流式代理**：LLM 的 SSE 流式输出需要 Gateway 层透传而非缓冲，否则端到端延迟剧增
2. **Tool Schema 动态注册**：Agent 平台中 Tool 是热注册的，Gateway 需要支持运行时更新路由表
3. **Function Calling 协议适配**：OpenAI 格式 ↔ Anthropic 格式 ↔ 自定义格式之间的翻译层
4. **长连接管理**：Agent 多步执行可能持续数分钟，Gateway 需管理长连接生命周期
5. **速率感知路由**：根据 LLM API 的实时速率限制动态切换供应商（[[Cost_Optimization]] 中的 Model Routing）
6. **调试流量复制**：将生产流量复制到 Staging 环境做 Agent 行为 diff 测试

## Agent 平台典型微服务划分

```
┌─────────────────────────────────────────────────────┐
│                   API Gateway                         │
│          (路由/鉴权/流式代理/Schema转换)               │
└──────┬──────┬──────┬──────┬──────┬──────┬───────────┘
       │      │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼      ▼
   ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────────┐
   │Agent│ │Tool │ │Mem- │ │Skill│ │Auth │ │Eval /  │
   │Run- │ │Reg- │ │ory  │ │Mgr  │ │Svc  │ │Observa-│
   │time │ │istry│ │Svc  │ │     │ │     │ │bility  │
   └────┘ └────┘ └────┘ └────┘ └────┘ └────────┘
       │      │      │      │
       ▼      ▼      ▼      ▼
   ┌────┐ ┌────┐ ┌────┐ ┌────┐
   │LLM │ │Vec │ │Req │ │User│
   │Gate│ │DB  │ │Store│ │DB  │
   └────┘ └────┘ └────┘ └────┘
```

| 服务 | 职责 |
|------|------|
| **Agent Runtime** | Agent Loop 执行引擎、状态管理、上下文组装 |
| **Tool Registry** | 工具注册/发现/版本管理、Schema 校验 |
| **Memory Service** | 长期/短期记忆存储、检索、多租户隔离 |
| **Skill Manager** | Skill 注册/权限/热加载、市场管理 |
| **Auth Service** | 多租户认证、RBAC/ABAC 权限校验 |
| **Eval/Observability** | 执行追踪、Tracing、Token 统计、Eval |

## 高可用设计

### Agent 平台高可用的额外维度

| 维度 | 传统微服务 | Agent 平台 |
|------|-----------|-----------|
| **无状态化** | 水平扩展容易 | Agent 有状态（Memory/Context），需外部化状态 |
| **容错** | 请求重试 | Agent 执行中的部分失败 → 需 Agent Loop 层级重试 |
| **一致性** | 最终一致性即可 | Agent 状态需强一致（否则上下文中断） |
| **降级** | 返回缓存或错误页面 | [[Graceful_Degradation]] — 回退到弱模型/规则 |
| **可观测性** | 请求追踪 | 需 Agent 行为语义追踪（Trial-level tracing） |

### 常见架构模式

- **多活架构**：多数据中心同时服务，Agent 状态通过 CRDT 或一致性哈希同步
- **Cell 架构**：将用户分片到独立 Cell，故障域隔离（类似微信的 SET 化）
- **Backpressure**：当后端 LLM API 过载时，Gateway 层主动降速而非丢弃请求

## 工具生态

| 类别 | 工具 | 适用场景 |
|------|------|---------|
| **API Gateway** | Kong / APISIX / Envoy / Zuul | 通用商用/开源 Gateway |
| **Agent 专用 Gateway** | LiteLLM / OpenRouter / Portkey | LLM 路由 + Fallback + 成本追踪 |
| **服务网格** | Istio / Linkerd | Sidecar 级流量管理 |
| **消息队列** | Kafka / RabbitMQ / NATS | Agent 事件驱动架构 |
| **服务发现** | Consul / etcd / Zookeeper | 动态服务注册发现 |

## 关联连接
- [[Harness_Engineering]] — Agent 平台归属的顶层工程框架
- [[Graceful_Degradation]] — 高可用降级策略
- [[Cost_Optimization]] — Model Routing 与成本优化
- [[Agent_Observability]] — Agent 可观测性与 Tracing
- [[Agent_Loop]] — Agent Runtime 核心执行机制
- [[Claude_Code_Skills]] — Skill 管理服务的上层行为
- [[MCP]] — Tool Registry 的底层通信协议
- [[Memory_Agent]] — Memory 服务的概念基础
- [[OpenAI_Compatible_API]] — 接口兼容标准参考
- [[LiteLLM]] — LLM API 网关实现
