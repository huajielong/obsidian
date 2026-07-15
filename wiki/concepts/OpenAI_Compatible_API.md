---
title: "OpenAI_Compatible_API"
type: concept
tags: [API, 标准化, LLM, 兼容性]
sources: [raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md]
last_updated: 2026-07-08
---

## 定义

OpenAI 兼容 API（OpenAI-Compatible API）是指遵循 OpenAI 官方 `chat/completions` 接口标准的 API 规范。由于 OpenAI 的 API 已成为 LLM 行业的**事实标准**，大量推理工具和模型提供商（如 Ollama、vLLM、LM Studio、Together AI 等）都实现了这一兼容接口，使得已有 OpenAI 调用代码可以无缝迁移。

## 关键信息

- **端点**：`/v1/chat/completions`
- **请求格式**：与 OpenAI SDK 完全一致的 `messages`、`model`、`max_tokens`、`stream` 等参数
- **流式响应**：返回标准 `choices[0].delta.content` 格式（每个 chunk 的增量文本）
- **非流式响应**：返回完整的 `choices[0].message.content`
- **Ollama 实现**：`api_key` 填任意值即可，Ollama 不验证

### 两种响应模式对比

| 维度 | 流式 (Streaming) | 非流式 (Non-Streaming) |
|------|-------------------|----------------------|
| 响应方式 | 逐 chunk 推送 | 一次性返回 |
| 首字延迟 | 低 | 高 |
| 适用场景 | 实时展示、打字机效果 | 程序内部处理、批处理 |
| 代码复杂度 | 略高（需循环处理） | 简单 |

### Ollama 原生 API vs OpenAI 兼容 API

| 维度 | 原生 API | OpenAI 兼容 API |
|------|----------|-----------------|
| 端点 | `/api/chat` | `/v1/chat/completions` |
| 依赖 | 零依赖（内置库） | 需安装 `openai` Python 包 |
| 迁移成本 | 需单独学习 | 已有 OpenAI 代码几乎无需修改 |
| 模型兼容性 | 更稳定 | 部分模型存在兼容 Bug |

## 知识冲突

- **兼容性普遍性**：虽然 OpenAI 兼容 API 被称为"标准"，但不同工具对同一端口的实现细节存在差异。如 qwen3.5:0.8b 在 Ollama 的 OpenAI 兼容端口下 content 为空，而在原生 API 下正常。说明"兼容"不等于"完全一致"。

## 关联连接
- [[Ollama]] — OpenAI 兼容 API 的主要实现者之一
- [[Qwen]] — 部分 Qwen 模型在此接口下存在已知 Bug
- [[Llama]] — 在此接口下表现稳定
- [[GPT]] — OpenAI 兼容 API 所参照的原始接口定义来源
- [[LiteLLM]] — 统一 LLM API 网关，基于 OpenAI 兼容接口标准
- [[本地_LLM_推理]] — 使用本地推理工具调用 LLM 的实践
