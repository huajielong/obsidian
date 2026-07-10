---
title: "Agent_Observability"
type: concept
tags: [observability, telemetry, tracing, monitoring, production, LLM系统设计]
sources: [raw/01-articles/07-multi-agent-production.zh-Hans.md]
last_updated: 2026-07-10
---

# Agent Observability（智能体可观测性）

## 定义

Agent Observability 是 [[Harness_Engineering]] 的 **第 6 个核心元件**——为 Agent 系统建立 Metrics / Tracing / Logging / Cost Tracking 的可观测层。解决的核心问题：**"当 Agent 做错了，我能知道它为什么做错吗？"**

> 没有 Observability 的 Agent Debug = 黑盒。

## 与 Eval 的区别

| 维度 | Eval Harness | Observability |
|------|-------------|---------------|
| 时间 | **离线**（CI / 开发期） | **在线**（生产运行时） |
| 关心 | "变好了吗？" | "现在怎么了？" |
| 输出 | 分数 / 报告 | Traces / Logs / Metrics |
| 用户 | 开发者（上线前） | 运维 / 开发者（运行时） |

两者互补：Eval 告诉你是否该上线，Observability 告诉你上线后发生了什么。

## Observability 的核心维度

| 维度 | 监控什么 | 工具 |
|------|---------|------|
| **Tracing** | Agent 每一步的完整执行轨迹（LLM call → tool call → result）| Langfuse / Helicone / Arize Phoenix |
| **Logging** | 原始输入输出、错误、异常 | 任一 logging 平台 |
| **Token Counting** | 每次 LLM call 的 input/output token 量 | SDK 内建 + OTel |
| **Cost Tracking** | 每个 session 的累计成本 | 同上 |
| **Latency** | 每个步骤的响应时间 | 同上 |
| **Rate Limiting** | API 限流、退避 | 自定义 |

## 标准：OpenTelemetry GenAI 惯例

认一个可携标准，不被单一工具绑死：

> **OpenTelemetry GenAI semantic conventions**（`gen_ai.*`）—— langfuse / Arize Phoenix / Helicone 都吐 OTel-兼容 span。

OTel-native 推荐：**Arize Phoenix**（★ 10k+）。

## 推荐工具

| 工具 | 定位 | 特点 |
|------|------|------|
| **langfuse** ⭐ | 自架 production observability | OSS、traces + sessions + evals + prompt mgmt。★ 28k+、MIT |
| LangSmith | LangChain/LangGraph 生态 | 商业、全 stack 在 LangChain 上 |
| **Helicone** | 不改程序的快速 instrumentation | proxy 中介、顺便拿 logging + caching。★ 5.7k+ |
| weave (W&B) | ML 实验追踪团队 | W&B tracing + eval，与 wandb 整合 |
| comet-ml/opik | eval + observability 同平台 | 追踪 LLM/Agent + 实验 + 质量检查。★ 19k+ |
| pydantic/logfire | OpenTelemetry 标准 | 建在 OpenTelemetry 上。★ 4k+ |

## 实施路径

1. **快速开始**：Helicone（proxy 中介，不需要改代码）
2. **标准方案**：langfuse（OSS、self-hostable、功能完整）
3. **OTel 原生**：Arize Phoenix
4. **全栈绑定**：LangSmith（如果你在用 LangChain/LangGraph）

## 关联连接

- [[Harness_Engineering]] — Observability 是 Harness 的第 6 个核心元件
- [[Eval_Harness]] — Observability 与 Eval 互补覆盖离线+在线评估
- [[Cost_Optimization]] — Observability 是成本优化的前提（先测量才能优化）
- [[Agent_Loop]] — Agent Loop 的每一步都需要 Observable
- [[Multi_Agent_System]] — Multi-agent 场景下 Observability 更重要（cross-agent trace）
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — 本概念的核心来源（Stage 7 练习 3）
