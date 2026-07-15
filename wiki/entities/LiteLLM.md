---
title: "LiteLLM"
type: entity
tags: [LLM, AI网关, 路由, API, 开源, AI_Gateway]
sources: []
last_updated: 2026-07-15
---

# LiteLLM — 统一 LLM API 网关

## 定义

LiteLLM 是由 **BerriAI** 开发的开源 AI 网关（AI Gateway），GitHub 22k+ ★。其核心定位是：**通过统一的 OpenAI 兼容 API 接口，让开发者无缝调用 100+ 主流大语言模型**。它同时提供轻量级 Python SDK 和企业级代理服务器（Proxy Server）两种使用方式，覆盖从个人开发到生产部署的全场景需求。

## 核心功能

### 🔌 统一 API 层

LiteLLM 将不同厂商的 SDK、认证方式、请求格式和错误类型全部抽象为 OpenAI 兼容格式。切换模型只需改一行 `model` 参数：

```python
from litellm import completion

# OpenAI
response = completion(model="openai/gpt-4o", messages=[...])

# Anthropic — 完全相同的写法
response = completion(model="anthropic/claude-sonnet-4-20250514", messages=[...])

# Ollama 本地模型
response = completion(model="ollama/qwen3", messages=[...])
```

### 🎯 100+ 模型提供商

覆盖几乎所有主流模型平台：

| 类型 | 提供商 |
|------|--------|
| **闭源 API** | OpenAI、Anthropic、Google Gemini、Mistral、Cohere、DeepSeek、Groq |
| **云平台** | AWS Bedrock、AWS Sagemaker、Azure OpenAI、Azure AI、Vertex AI |
| **本地推理** | Ollama、vLLM、LM Studio |
| **开源平台** | Hugging Face、Replicate、Together AI、NVIDIA NIM |
| **国内平台** | 阿里 Dashscope（通义千问）、百度文心 |

支持端点：`/chat/completions`、`/embeddings`、`/images`、`/audio`、`/batches`、`/rerank`、`/a2a`、`/messages` 等。

### 📦 两种使用方式

#### 方式一：Python SDK

```bash
pip install litellm
```

```python
from litellm import completion, acompletion

# 同步调用
response = completion(model="openai/gpt-4o", messages=[{"role": "user", "content": "你好"}])

# 流式响应
response = completion(model="openai/gpt-4o", messages=messages, stream=True)
for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)

# 异步批量
tasks = [acompletion(model=model, messages=msg) for msg in message_list]
results = await asyncio.gather(*tasks)
```

#### 方式二：AI Gateway 代理服务器

```bash
uv tool install 'litellm[proxy]'
litellm --model gpt-4o
```

之后任何 OpenAI 客户端只需改 `base_url` 指向代理：

```python
import openai
client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
response = client.chat.completions.create(model="gpt-4o", messages=[...])
```

### 🔀 智能路由与负载均衡

- **故障自动转移**：Azure 异常时自动切换到 AWS Bedrock
- **延迟优先路由**：自动选择响应最快的模型部署
- **成本优化**：根据预算自动分配请求到不同价位模型
- **重试/回退**：内置指数退避重试和 Fallback 机制

### 🔐 企业级管理

| 功能 | 说明 |
|------|------|
| **虚拟密钥** | 按团队/用户生成密钥，设置预算、速率限制和模型白名单 |
| **费用追踪** | 多租户成本追踪，按项目/用户统计消费 |
| **访问控制** | 细粒度鉴权和授权 |
| **管理面板** | 内置 Admin Dashboard UI |
| **审计日志** | 记录每次调用的密钥、模型、延迟、Token 数 |

### 🛡️ 护栏（Guardrails）

集成 **Aporia、Lakera、Presidio** 等护栏服务，在请求前后进行内容验证和安全过滤。

### 📊 可观测性

- **OpenTelemetry 原生支持**：通过 `otel` 回调导出 GenAI 语义化追踪
- **第三方集成**：[[langfuse]]、Helicone、Datadog、MLflow、Lunary、Phoenix、Promptlayer 等
- **Prometheus + Grafana**：提供 23 项核心指标监控

### 🤖 Agent & MCP 支持

- **A2A 协议**：支持 [[LangGraph]]、Vertex AI Agent Engine、Azure AI Foundry、Bedrock AgentCore、Pydantic AI
- **MCP Gateway**：LiteLLM 可作为 MCP Gateway，将 [[MCP]] 服务器工具连接到任意 LLM

## SDK vs 代理服务器对比

| 对比维度 | Python SDK | AI Gateway（代理服务器） |
|---------|-----------|------------------------|
| **适用场景** | 项目直接集成 | 集中式网关服务 |
| **使用者** | 开发者 | GenAI/ML 平台团队 |
| **核心功能** | 路由、重试/回退、异常处理、回调 | 鉴权、多租户费用管理、虚拟密钥、管理面板 |
| **部署方式** | `pip install` | Docker / Kubernetes |

## 同类对比

| 项目 | 核心优势 | 局限 | 适用场景 |
|-----|---------|------|---------|
| **LiteLLM** | 模型最多，企业级功能完善 | 配置相对复杂 | 多平台混合/企业级部署 |
| [[OpenRouter]] | 托管服务，开箱即用 | 不支持自托管 | 个人/小团队快速试用 |
| Portkey | 护栏 + 提示管理 | 社区规模较小 | 企业级治理 |
| [[LangChain]] | 工作流编排能力强 | 学习曲线陡峭 | AI 应用流程设计 |

## 许可证

- **开源版**：MIT 许可证（SDK 和代理服务器非企业版代码）
- **企业版**：SSO、审计日志、SLA 支持等付费功能
- **稳定版**：使用 `-stable` 标签的 Docker 镜像，经过 12 小时压力测试后发布

## 关联连接

- [[Harness_Engineering]] — LiteLLM 是 Harness Engineering 中"模型接入层"的关键工具实例
- [[OpenAI_Compatible_API]] — 统一使用 OpenAI 兼容接口标准
- [[OpenRouter]] — 同类托管的 LLM 路由服务，可做功能对比
- [[MCP]] — LiteLLM 可作为 MCP Gateway 运行
- [[Cost_Optimization]] — 智能路由与成本优化策略
- [[Graceful_Degradation]] — Fallback 降级机制的工程实现
- [[Agent_Observability]] — 可观测性与监控集成
- [[langfuse]] — LiteLLM 的原生可观测性集成之一
- [[Claude_Code]] — 可通过 LiteLLM 代理调用不同模型
- [[Ollama]] — 可通过 LiteLLM 统一管理本地模型
