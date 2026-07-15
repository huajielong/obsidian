---
title: "Cost_Optimization"
type: concept
tags: [cost, latency, optimization, production, prompt-caching, model-routing, LLM系统设计]
sources: [raw/01-articles/07-multi-agent-production.zh-Hans.md]
last_updated: 2026-07-10
---

# Cost / Latency Optimization（成本与延迟优化）

## 定义

Cost / Latency Optimization 是 [[Harness_Engineering]] 的 **第 8 个核心元件**——Production Agent 跑久了，**Cost / Latency 两条线会吃掉大半预算与用户体验**。2024-2026 前沿模型已将成本优化作为 First-class API Feature，**会用 = 省 50-90% Cost / Latency**。

**核心公式**：Agent Cost = Σ（每次 LLM Call 的 Token × Price）× Call Count

因此优化方向有三：
1. **降每次成本**（Prompt Caching / Model Routing）
2. **减调用次数**（Batching / Semantic Caching）
3. **提单次效率**（Thinking Budget / Speculative Decoding）

## 优化技术总览

| 技巧 | 节省机制 | 2026 状态 | 省多少 |
|------|---------|-----------|-------|
| **Prompt Caching** | 重复 prefix（system prompt、long context）一次计费，后续 cache hit 折扣 | Anthropic / OpenAI / Gemini 全支持，自动或手动标记 | ~90% |
| **Model Routing / Cascade** | 简单 query → 小 model，难 query → frontier model | RouteLLM / OpenRouter production 内建 | 50-90% |
| **Thinking Budget** | reasoning model 可控 thinking token 上限 | Claude / Gemini API 参数、o-series 默认高 | 可控 |
| **Speculative Decoding** | 小 model 预测 N token、大 model 一次验证 | vLLM / TGI 内建 | 2-3× 速度 |
| **Batching** | 多 query 并行处理，GPU 利用率高 | vLLM、production inference layer | 高吞吐 |
| **Semantic Caching** | 相似 query 共享回答（not just exact match） | GPTCache / Helicone 内建 | 不定 |

## 分层实践路径

### Track A：使用 CLI Agent 的人
- 在 Claude Code / Cursor 启用 prompt caching（daily session 省 50-90%）
- RouteLLM / OpenRouter 动态切换 model（简单 → Haiku/Flash，困难 → Opus/Pro）
- Claude API 用 `thinking_budget` 参数控 reasoning model 的 token 上限

### Track B：自己写 Agent 的人
- 自架 cascade router（query embedding → classifier → model 对应）
- 在 Agent Loop 内监控 token cost，超 budget 自动降级
- 部署时整合 semantic cache 层
- Helicone / langfuse 等平台已内建这些能力，不用自己写

## 工具推荐

| 工具 | 用途 | 特点 |
|------|------|------|
| **RouteLLM** | Model routing / cascade | 开源、简单 query → 小 model |
| **OpenRouter** | Model routing | 商业、统一 API 网关 |
| **GPTCache** | Semantic caching | 开源、相似 query 共享回答 |
| **Helicone** | Cost tracking + caching | Proxy 中介、不绑 framework |
| **langfuse** | Cost tracking + eval + obs | OSS、功能完整 |

## 与 Harness 其他元件的关系

- [[Agent_Observability]] → Cost Tracking：先测量才能优化
- [[Eval_Harness]] → 质量门禁：降成本不能降质量，Eval 把关
- [[Harness_Engineering]] → 整体架构建模：成本是 8 个核心元件之一

> 💡 **Cost Optimization 是 2024-2026 的 Production 必修课**——Promp Caching 90% 降本 + Model Routing 50-90% 降本，组合使用几乎能消除 Production Agent 的成本壁垒。

## 关联连接

- [[Harness_Engineering]] — Cost/Latency 是 Harness 第 8 个核心元件
- [[Agent_Observability]] — Cost Tracking 是 Observability 的核心维度
- [[Eval_Harness]] — 降本不能降质，Eval 是质量门禁
- [[Agent_Loop]] — Agent Loop 的每一步都消耗 token
- [[Multi_Agent_System]] — Multi-agent 的 3-10× token 成本更需要优化
- [[Prompt_Engineering]] — 更好的 prompt 也是降本手段（减少 retry）
- [[LiteLLM]] — 统一 API 网关，内建 Model Routing + Cost Tracking
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — 本概念的核心来源（Stage 7 练习 6）
