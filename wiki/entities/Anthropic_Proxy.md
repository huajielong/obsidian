---
title: "Anthropic_Proxy"
type: entity
tags: [工具, 代理, Anthropic, OpenAI, 协议转换, 本地LLM]
sources: [raw/01-articles/Claude-Code-本地模型接入指南.md]
last_updated: 2026-11-02
---

## 定义

anthropic-proxy 是一个 Go 单文件代理，把 Anthropic Messages API 请求转换为 OpenAI Chat Completions 请求，再转发给本地 OpenAI 兼容后端（如 llama.cpp）。本机用它把 Claude Code 接到 Qwen3.6：Claude Code → `127.0.0.1:8787`（代理）→ `127.0.0.1:8081`（llama.cpp）。

## 关键信息

- **来源**：https://github.com/thomas-illiet/anthropic-proxy
- **形态**：Go 单文件可执行程序，约 25MB，不依赖 Python
- **本机路径**：`D:\AI\anthropic-proxy\anthropic-proxy.exe`
- **监听**：`127.0.0.1:8787`，只对本机开放
- **协议转换**：Anthropic Messages ↔ OpenAI Chat Completions；保留 `tool_use` / `tool_result` 语义
- **配置（`.env`）**：

| 变量 | 本机值 | 作用 |
|------|--------|------|
| `ANTHROPIC_PROXY_UPSTREAM_URL` | `http://127.0.0.1:8081/v1/chat/completions` | 上游 OpenAI 兼容端点（必须完整路径） |
| `ANTHROPIC_PROXY_UPSTREAM_API_KEY` | `dummy` | 必填占位值；llama.cpp 不校验 |
| `ANTHROPIC_PROXY_DEFAULT_MODEL` | `qwen` | 默认模型名，与 `llama-server -a qwen` 对齐 |
| `ANTHROPIC_PROXY_TOOL_FORMAT` | `native` | 工具调用格式；异常时改 `xml` |
| `ANTHROPIC_PROXY_FORCE_MODEL` | `1` | 把任意 Claude 模型名映射到 `qwen` |
| `ANTHROPIC_PROXY_LISTEN_ADDR` | `127.0.0.1:8787` | 监听地址 |
| `ANTHROPIC_PROXY_REQUEST_TIMEOUT_SEC` | `600` | 请求超时 |

- **模型发现**：`/v1/models` 列出 `claude-sonnet-4-6`、`claude-opus-4-8`、`claude-haiku-4-5`，实际都映射到本机 qwen
- **健康检查**：`GET /health` 返回 `ok`
- **启动**：`start-proxy.bat`（会 `cd` 到代理目录，确保读到 `.env`）
- **注意**：`.env` 从当前工作目录读取；直接双击 exe 可能读不到配置

## 关联连接

- [[Anthropic_Compatible_API]] — 代理实现的接口契约
- [[Claude_Code_本地模型接入]] — 使用场景
- [[LlamaCpp]] — 上游推理引擎
- [[Ollama]] — 另一种上游后端
- [[Claude_Code]] — 客户端
- [[本地_LLM_推理]] — 上位概念
- [[摘要-claude-code-本地模型接入指南]] — 来源
