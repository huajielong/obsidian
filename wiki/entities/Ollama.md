---
title: "Ollama"
type: entity
tags: [工具, 本地LLM, API, 开源]
sources:
  - raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md
  - raw/01-articles/claude-code-ollama-local-setup.md
  - raw/01-articles/Claude-Code-本地模型接入指南.md
  - raw/01-articles/本地模型执行指南.md
last_updated: 2026-11-02
---

## 定义

Ollama 是一款本地大语言模型运行工具，提供简洁的 API 接口让用户在自己的硬件上运行和管理 LLM 模型，无需将数据上传到云端。它支持多种开源模型（如 Llama、Qwen、Mistral 等），并提供原生 API 与 OpenAI 兼容 API 两套接口。

## 关键信息

- **默认端口**：`localhost:11434`
- **API 体系**：原生 API（`/api/chat`）、OpenAI 兼容 API（`/v1/chat/completions`），以及供 Claude Code 使用的 Anthropic 兼容接口（见 [[Anthropic_Compatible_API]]）
- **原生 API 特点**：零依赖，使用 Python 内置库（`urllib`）即可调用，支持流式（`stream=True`）与非流式两种模式
- **OpenAI 兼容 API 特点**：与 OpenAI SDK 完全兼容，`api_key` 填任意值即可（Ollama 不验证）
- **流式模式下**：原生 API 逐行返回 JSON，每行一个 chunk；OpenAI 兼容接口返回标准 `choices[0].delta.content` 格式
- **最后一个 chunk**：携带 `done: true` 标记和完整统计信息（总耗时、Token 数、生成速率）
- **模型管理**：通过 `ollama pull <模型名>` 拉取模型，支持断点续传
- **Claude Code 后端**：设置 `ANTHROPIC_BASE_URL=http://localhost:11434` 后，[[Claude_Code]] 的模型请求可重定向到 Ollama，实现全本地编码 Agent（见 [[Claude_Code_本地模型接入]]）

### 已知问题

1. **Windows GBK 编码**：终端默认编码为 GBK，输出 emoji 或中英文混合时触发 `UnicodeEncodeError`。需在 Python 脚本开头加入 `sys.stdout.reconfigure(encoding="utf-8")`
2. **端口冲突**：后台 Ollama 进程重复时触发 `port 11434 already in use`。Git Bash 下用 `taskkill //F //IM ollama.exe`（双斜杠绕过路径解析）
3. **某些模型兼容性**：部分模型（如 qwen3.5:0.8b）在 OpenAI 兼容端口下存在 `content` 返回空字符串的 Bug
4. **下载卡顿**：`ollama pull` 可能在 94-96% 卡住，直接 Ctrl+C 中断重试即可（支持断点续传）

### 作为 Claude Code 的本地模型后端

Ollama 可作为 [[Claude_Code]] 的本地模型运行时：通过环境变量把 Anthropic API 端点指向 `localhost:11434`，并指定已拉取的模型。

```bash
ANTHROPIC_AUTH_TOKEN=ollama \
ANTHROPIC_API_KEY="" \
ANTHROPIC_BASE_URL=http://localhost:11434 \
claude --model qwen3.6:35b-a3b-mtp-q4_K_M
```

- 按内存选模型：≤16GB → `qwen2.5-coder:14b`；32GB → `glm-4.7-flash`；48GB+ → `glm-4.7`
- 推荐用别名 `claude-local` 隔离环境变量，保留原 `claude` 命令
- **性能边界**：本机实测 Ollama 0.40.13 运行 Qwen3.6 约 6.6 tok/s，明显慢于 [[LlamaCpp]] 的约 65 tok/s；日常建议用 [[Anthropic_Proxy]] + llama.cpp，Ollama 直连作为备用
- 该接入模式详见 [[Claude_Code_本地模型接入]]

### 性能与运维注意（本机）

- **新架构效率**：Ollama 0.40.x 对 Qwen3.6 / Gemma 4 等新架构不支持 MoE 专家卸载，只能整层卸载到 CPU；同一 GGUF 用 llama.cpp 可快 6–10 倍
- **定位**：Ollama 更适合模型管理、翻译模型（TranslateGemma）和小模型；大模型优先 [[LlamaCpp]]
- **模型目录**：`OLLAMA_MODELS=D:\Ollama\models`；应用 `settings.models` 也指向 D 盘（托盘程序会覆盖环境变量）
- **Windows junction 问题**：Ollama 0.40.x 读取 junction 模型目录有 bug；应让 `settings.models` 指向真实目录
- **环境变量**：`OLLAMA_CONTEXT_LENGTH=32768`、`OLLAMA_FLASH_ATTENTION=1`、`OLLAMA_KV_CACHE_TYPE=q8_0`
- **不要删除模型**：`qwen3.6:35b-a3b-mtp-q4_K_M`、`gemma4:12b`、`translategemma:4b` 被 llama.cpp 启动脚本引用；重新拉取导致 blob hash 变化时，用 `ollama show <模型名> --modelfile` 更新脚本 `-m`

## 四种 API 调用方式对比

| 方式 | 依赖 | 响应方式 | 典型场景 |
|------|------|----------|----------|
| 原生非流式 | 内置库 | 一次性 JSON | 简单对话、批处理 |
| 原生流式 | 内置库 | 逐行 JSON | 实时展示、进度条 |
| OpenAI 非流式 | openai 库 | 一次性 | 已有 OpenAI 代码的迁移 |
| OpenAI 流式 | openai 库 | 流式 chunk | ChatGPT 风格的打字机效果 |

## 关联连接
- [[摘要-ollama-local-llm-python]] — Ollama Python API 调用实战来源
- [[摘要-ollama-experiment-index]] — 实验系列综合数据来源
- [[Llama]] — Ollama 支持的主流开源模型之一
- [[Qwen]] — Ollama 支持的另一个主流模型系列
- [[OpenAI_Compatible_API]] — Ollama 提供的 OpenAI 兼容接口
- [[GPT]] — 通用大语言模型概念
- [[Claude_Code]] — 可通过 Ollama 在本地运行的终端编码 Agent
- [[Claude_Code_本地模型接入]] — 环境变量重定向与别名隔离模式
- [[LlamaCpp]] — 本机大模型的主力推理后端（比 Ollama 快 6–10 倍）
- [[Anthropic_Compatible_API]] — Ollama 提供的 Anthropic 兼容接口
- [[本地推理性能调优]] — 后端选择与显存调优方法
- [[GLM]] — 指南推荐的本地模型系列
- [[摘要-claude-code-ollama-local-setup]] — Claude Code + Ollama 本地化安装指南来源
- [[摘要-claude-code-本地模型接入指南]] — 本机代理版实施记录来源
- [[摘要-本地模型执行指南]] — 同机模型与调优手册
