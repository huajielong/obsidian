---
title: "Anthropic_Compatible_API"
type: concept
tags: [API, Anthropic, 兼容接口, 协议转换, Claude Code]
sources: [raw/01-articles/Claude-Code-本地模型接入指南.md, raw/01-articles/claude-code-ollama-local-setup.md]
last_updated: 2026-11-02
---

## 定义

Anthropic 兼容 API（Anthropic-Compatible API）是指以 Anthropic Messages API 的请求/响应格式为契约的接口实现，使 Claude Code 等 Anthropic 客户端可以把 `ANTHROPIC_BASE_URL` 指向非 Anthropic 后端。它有两种典型实现：服务端原生实现 Anthropic Messages 协议，或通过协议转换代理把 Anthropic 请求翻译成 OpenAI Chat Completions。

## 关键信息

### 两种实现路径

| 路径 | 代表 | 链路 | 特点 |
|------|------|------|------|
| 原生兼容 | Ollama 的 Anthropic compatibility | Claude Code → Ollama 11434 | 部署简单，无额外进程；后端性能取决于 Ollama |
| 协议转换代理 | [[Anthropic_Proxy]] | Claude Code → 8787 → llama.cpp 8081 | 可接任意 OpenAI 兼容后端；多一层进程，但性能更好 |

### 核心契约

- **端点**：`POST /v1/messages`
- **鉴权**：`x-api-key` / `anthropic-version` 等 Anthropic 头；本地后端通常不校验，填占位值
- **消息结构**：`system` + `messages`（role / content blocks）
- **工具调用**：`tools` 定义 → 响应中的 `tool_use` block；工具结果回传为 `tool_result`
- **模型名**：客户端传 Claude 模型 ID，代理或后端映射到本地模型

### Claude Code 的接入变量

| 变量 | 作用 |
|------|------|
| `ANTHROPIC_BASE_URL` | 指向兼容端点 |
| `ANTHROPIC_AUTH_TOKEN` | 占位令牌 |
| `ANTHROPIC_API_KEY` | 官方 Key；本地场景可置空或占位 |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` | 允许从 `/v1/models` 发现模型 |

### 协议差异与转换损耗

Anthropic Messages 与 OpenAI Chat Completions 在以下方面不同，代理需要做映射：

- system prompt 的位置（Anthropic 顶层 `system` vs OpenAI messages 中的 system role）
- 工具调用格式（`tool_use` / `tool_result` vs `tool_calls` / `tool` role）
- 停止原因、流式事件、内容块类型
- Anthropic 特有功能（如 prompt caching、thinking blocks）在转换后可能丢失或被忽略

### 验证方法

```bash
curl http://127.0.0.1:8787/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: anything" \
  -d '{"model":"claude-sonnet-4-6","max_tokens":256,
       "messages":[{"role":"user","content":"调用 get_weather 查询北京天气"}],
       "tools":[{"name":"get_weather","description":"查询天气",
                 "input_schema":{"type":"object","properties":{"location":{"type":"string"}}}}]}'
```

预期响应包含 `tool_use` block（`name=get_weather`，`input={"location":"Beijing"}`）。

### 边界

- 兼容层保证的是**协议形状**，不保证模型能力、上下文长度或工具调用可靠性
- 本地模型能力弱于云端 Claude；复杂 Agent 任务仍需验证
- 代理只监听本机时，隐私边界是“推理本地”，但客户端本身可能联网

## 关联连接

- [[Claude_Code_本地模型接入]] — 主要应用场景
- [[Anthropic_Proxy]] — 协议转换实现
- [[Ollama]] — 原生 Anthropic 兼容实现
- [[LlamaCpp]] — OpenAI 兼容上游
- [[OpenAI_Compatible_API]] — 对照：OpenAI 兼容接口标准
- [[Claude_Code]] — 客户端
- [[Claude_Code_Harness]] — 仅替换 L1 模型层
- [[摘要-claude-code-本地模型接入指南]] — 来源
- [[摘要-claude-code-ollama-local-setup]] — 直连方案来源
