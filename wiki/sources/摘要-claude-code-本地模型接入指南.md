---
title: "摘要-claude-code-本地模型接入指南"
type: source
tags: [来源, Claude Code, llama.cpp, anthropic-proxy, 本地LLM, 本机配置]
sources: [raw/01-articles/Claude-Code-本地模型接入指南.md]
last_updated: 2026-11-02
---

## 核心摘要

本机（COLORFUL P16 Pro IXA1，RTX 5070 Ti Laptop 12GB，i7-14650HX，64GB DDR5，Windows 11）的 Claude Code 本地模型接入实施记录，已完成端到端验证。推荐方案不是 Ollama 直连，而是 **llama.cpp（Qwen3.6，8081）+ anthropic-proxy（8787）** 的两级架构：代理把 Anthropic Messages 请求转换成 OpenAI Chat Completions，再交给 llama.cpp 推理，实测约 65 tok/s；Ollama 直连同一模型仅约 6.6 tok/s，作为备用。日常只需运行 `claude-local`，脚本会自动拉起 Qwen 与代理，普通 `claude` 完全不受影响。文档还记录了代理 `.env` 配置、模型映射、工具调用验证、故障排查、回滚方案，以及与通用教程的实施差异。

## 关键信息

### 三套方案对比

| 方案 | 组成 | 速度 | 状态 |
|------|------|------|------|
| **推荐：claude-local（代理版）** | llama.cpp Qwen3.6（8081）+ anthropic-proxy（8787） | 约 **65 tok/s** | ✅ 已配置并验证 |
| 备用：claude-local-ollama | Ollama 直连 Qwen3.6（11434） | 约 6.6 tok/s | ✅ 可用，但很慢 |
| 普通 claude | Anthropic 官方 | 官方速度 | ✅ 不受影响 |

### 组件与路径

| 组件 | 路径 / 端口 | 作用 |
|------|------------|------|
| Qwen3.6 llama.cpp 服务 | `D:\AI\llama.cpp\start-qwen.bat` → 8081 | 实际推理，约 65 tok/s |
| anthropic-proxy | `D:\AI\anthropic-proxy\anthropic-proxy.exe` → 8787 | Anthropic Messages → OpenAI Chat Completions |
| 代理配置 | `D:\AI\anthropic-proxy\.env` | 上游地址、模型、工具格式 |
| 一键启动 / 停止 | `D:\AI\start-local-ai.bat` / `stop-local-ai.bat` | 同时启停 Qwen + 代理 |
| Claude Code 快速版 | `D:\AI\claude-local.bat` | 自动拉起服务后启动 Claude Code |
| PATH 入口 | `C:\Users\huajielong-win11\bin\claude-local.cmd` | PowerShell / cmd 直接输入 `claude-local` |
| Git Bash 函数 | `C:\Users\huajielong-win11\.bashrc` | Git Bash 直接输入 `claude-local` |
| Ollama 慢速版 | `D:\AI\claude-local-ollama.bat` | 指向 Ollama 11434 |

### anthropic-proxy `.env`

```env
ANTHROPIC_PROXY_UPSTREAM_URL=http://127.0.0.1:8081/v1/chat/completions
ANTHROPIC_PROXY_UPSTREAM_API_KEY=dummy
ANTHROPIC_PROXY_DEFAULT_MODEL=qwen
ANTHROPIC_PROXY_TOOL_FORMAT=native
ANTHROPIC_PROXY_FORCE_MODEL=1
ANTHROPIC_PROXY_LISTEN_ADDR=127.0.0.1:8787
ANTHROPIC_PROXY_REQUEST_TIMEOUT_SEC=600
ANTHROPIC_PROXY_LOG_LEVEL=info
```

- `UPSTREAM_API_KEY=dummy`：代理要求必填；llama.cpp 不校验，填占位值即可
- `TOOL_FORMAT=native`：Qwen3.6 原生工具调用；异常时改 `xml` 并重启代理
- `FORCE_MODEL=1`：Claude Code 发来的任何模型名都映射到 `qwen`
- `LISTEN_ADDR=127.0.0.1:8787`：只监听本机，不对局域网暴露

### 性能对比（同一个 Qwen3.6）

| 引擎 | 生成速度 | prompt 处理 | 说明 |
|------|----------|------------|------|
| Ollama 0.40.13 | 约 6.6 tok/s | 约 0.57 tok/s | 不支持 MoE 专家卸载，整层卸载到 CPU |
| llama.cpp b12017 | 约 65 tok/s | 约 55 tok/s | `--n-cpu-moe 24` + MTP + 32K |
| anthropic-proxy | 基本无额外开销 | — | 只做协议转换 |

> Claude Code 的系统提示 + 工具定义约 2 万 token，所以 prompt 处理速度非常关键：Ollama 的 0.57 tok/s 会让首次请求等很久，llama.cpp 的 55 tok/s 才实用。

### `claude-local` 注入的环境变量

| 变量 | 值 |
|------|-----|
| `ANTHROPIC_BASE_URL` | `http://127.0.0.1:8787` |
| `ANTHROPIC_API_KEY` | `anything` |
| `ANTHROPIC_AUTH_TOKEN` | `anything` |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` | `1` |
| `--model` | `claude-sonnet-4-6`（代理映射到本机 `qwen`） |

### 验证与故障要点

- `claude -p "Say hello in Chinese..."` 返回中文回答
- `/v1/messages` 工具调用测试正确返回 Anthropic `tool_use`（`get_weather` / `{"location":"Beijing"}`）
- `curl http://127.0.0.1:8081/health` 返回 `{"status":"ok"}`；`8787/health` 返回 `ok`
- `/v1/models` 列出 `claude-sonnet-4-6`、`claude-opus-4-8`、`claude-haiku-4-5`（实际都映射到 qwen）
- 常见问题：缺少 `UPSTREAM_API_KEY` 导致代理启动失败；上游地址必须是完整 `/v1/chat/completions` 路径；`--model` 使用 `/v1/models` 列出的 ID；工具调用异常时切换 `TOOL_FORMAT=xml`；`claude -p` 可能卡在无 TTY 的权限确认；普通 `claude` 被污染时用保存/恢复版函数或清除环境变量
- 安全：代理只监听 `127.0.0.1`；不要默认使用 `--dangerously-skip-permissions`

### 与原教程的实施差异

| 原教程 | 本机实施 | 原因 |
|--------|----------|------|
| Step 0–2 安装 Node/Claude/Ollama | 跳过 | 已安装 |
| 用 glm-4.7-flash 等新模型 | 不装新模型，使用现有 Qwen3.6 | 用户明确要求；12GB 显存更适合现有 Qwen |
| Ollama 直连 | 仅作备用（6.6 tok/s） | 实测太慢 |
| 只讲代理概念 | 已配置 anthropic-proxy（8787）并验证 | 端到端可用 |
| 默认 4K 上下文 | 32K | Claude Code 系统提示约 20K token |
| PowerShell 直接改 `$env:` | 保存/恢复版本或 `.bat` | 避免污染普通 `claude` |
| 声称“100% 私有” | 推理本地，但 Claude Code 可能联网 | 避免误解，详见 [[Claude_Code_本地模型接入#知识冲突]] |

## 关联连接

- [[Claude_Code_本地模型接入]] — 本实施记录抽象出的接入模式
- [[Claude_Code]] — 被本地化的终端编码 Agent
- [[LlamaCpp]] — 实际推理引擎
- [[Anthropic_Proxy]] — Anthropic → OpenAI 协议转换代理
- [[Anthropic_Compatible_API]] — 本方案依赖的接口契约
- [[Ollama]] — 备用直连运行时
- [[Qwen]] — 本机实际使用的模型系列
- [[GLM]] — 原教程推荐、但本机未采用的模型
- [[本地_LLM_推理]] — 上位概念
- [[本地推理性能调优]] — 性能数据与调优方法
- [[摘要-claude-code-ollama-local-setup]] — 通用教程来源
- [[摘要-本地模型执行指南]] — 同机模型与调优手册
