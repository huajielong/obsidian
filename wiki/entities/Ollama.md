---
title: "Ollama"
type: entity
tags: [工具, 本地LLM, API, 开源]
sources: [raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md]
last_updated: 2026-07-08
---

## 定义

Ollama 是一款本地大语言模型运行工具，提供简洁的 API 接口让用户在自己的硬件上运行和管理 LLM 模型，无需将数据上传到云端。它支持多种开源模型（如 Llama、Qwen、Mistral 等），并提供原生 API 与 OpenAI 兼容 API 两套接口。

## 关键信息

- **默认端口**：`localhost:11434`
- **API 体系**：原生 API（`/api/chat`）和 OpenAI 兼容 API（`/v1/chat/completions`）
- **原生 API 特点**：零依赖，使用 Python 内置库（`urllib`）即可调用，支持流式（`stream=True`）与非流式两种模式
- **OpenAI 兼容 API 特点**：与 OpenAI SDK 完全兼容，`api_key` 填任意值即可（Ollama 不验证）
- **流式模式下**：原生 API 逐行返回 JSON，每行一个 chunk；OpenAI 兼容接口返回标准 `choices[0].delta.content` 格式
- **最后一个 chunk**：携带 `done: true` 标记和完整统计信息（总耗时、Token 数、生成速率）
- **模型管理**：通过 `ollama pull <模型名>` 拉取模型，支持断点续传

### 已知问题

1. **Windows GBK 编码**：终端默认编码为 GBK，输出 emoji 或中英文混合时触发 `UnicodeEncodeError`。需在 Python 脚本开头加入 `sys.stdout.reconfigure(encoding="utf-8")`
2. **端口冲突**：后台 Ollama 进程重复时触发 `port 11434 already in use`。Git Bash 下用 `taskkill //F //IM ollama.exe`（双斜杠绕过路径解析）
3. **某些模型兼容性**：部分模型（如 qwen3.5:0.8b）在 OpenAI 兼容端口下存在 `content` 返回空字符串的 Bug
4. **下载卡顿**：`ollama pull` 可能在 94-96% 卡住，直接 Ctrl+C 中断重试即可（支持断点续传）

## 四种 API 调用方式对比

| 方式 | 依赖 | 响应方式 | 典型场景 |
|------|------|----------|----------|
| 原生非流式 | 内置库 | 一次性 JSON | 简单对话、批处理 |
| 原生流式 | 内置库 | 逐行 JSON | 实时展示、进度条 |
| OpenAI 非流式 | openai 库 | 一次性 | 已有 OpenAI 代码的迁移 |
| OpenAI 流式 | openai 库 | 流式 chunk | ChatGPT 风格的打字机效果 |

## 关联连接
- [[Llama]] — Ollama 支持的主流开源模型之一
- [[Qwen]] — Ollama 支持的另一个主流模型系列
- [[OpenAI_Compatible_API]] — Ollama 提供的 OpenAI 兼容接口
- [[GPT]] — 通用大语言模型概念
