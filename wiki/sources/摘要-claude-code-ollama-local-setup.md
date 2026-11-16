---
title: "摘要-claude-code-ollama-local-setup"
type: source
tags: [来源, Claude Code, Ollama, 本地LLM, 安装指南]
sources: [raw/01-articles/claude-code-ollama-local-setup.md]
last_updated: 2026-11-02
---

## 核心摘要

一份五步操作指南，演示如何在完全本地、无需 Anthropic 订阅的情况下运行 Claude Code：先安装 Node.js 与 Claude Code，再安装 Ollama 并按内存容量拉取模型（≤16GB 用 `qwen2.5-coder:14b`，32GB 用 `glm-4.7-flash`，48GB+ 用 `glm-4.7`），最后用 shell 别名 `claude-local` 注入 `ANTHROPIC_BASE_URL=http://localhost:11434` 等环境变量，把 Claude Code 的模型请求重定向到本地 Ollama。核心设计是用别名隔离环境变量，让常规 `claude` 命令继续走 Anthropic 云端，同时新增一个 `claude-local` 命令，两套配置互不干扰。指南覆盖 macOS/Linux、Windows Git Bash 与 PowerShell 三种配置方式，并强调所有常规 CLI 参数仍然可用。

## 关键信息

### 安装步骤

| 步骤 | 操作 | 验证 |
|------|------|------|
| 0 | 安装 Node.js LTS（https://nodejs.org） | `node --version` |
| 1 | `npm install -g @anthropic-ai/claude-code` | `claude --version` |
| 2 | 安装 Ollama（macOS/Linux 用安装脚本，Windows 用安装包） | `ollama --version` |
| 3 | 按内存选择并拉取模型 | `ollama list` / 模型可调用 |
| 4 | 在 shell 配置中创建 `claude-local` 别名 | `source ~/.bashrc` 或重开终端 |
| 5 | 运行 `claude-local` | 本地模型响应 |

### RAM → 模型选型

| 内存 | 模型 | 拉取命令 | 备注 |
|------|------|----------|------|
| ≤16GB | qwen2.5-coder:14b | `ollama pull qwen2.5-coder:14b` | 14B 代码模型 |
| 32GB | glm-4.7-flash | `ollama pull glm-4.7-flash` | 指南推荐，约 19GB 下载 |
| 48GB+ | glm-4.7 | `ollama pull glm-4.7` | 更高内存档位 |

### claude-local 的环境变量

| 变量 | 值 | 作用 |
|------|-----|------|
| ANTHROPIC_AUTH_TOKEN | ollama | 占位令牌，Ollama 不校验 |
| ANTHROPIC_API_KEY | 空字符串 | 清空官方 Key |
| ANTHROPIC_BASE_URL | http://localhost:11434 | 把请求指向本地 Ollama |
| --model | glm-4.7-flash | 指定本地模型 |

### 跨平台配置

| 平台 | 配置文件 | 写法 |
|------|----------|------|
| macOS/Linux | `~/.bashrc` 或 `~/.zshrc` | `alias claude-local='...'` + `source` |
| Windows Git Bash | `~/.bashrc` | 同一行 alias，重开终端或 `source` |
| Windows PowerShell | `$PROFILE` | `function claude-local { ... @args }` |

> PowerShell 的配置必须写入 `$PROFILE` 文件，直接在窗口里执行不会持久化。

## 关联连接

- [[Claude_Code]] — 被本地化的终端编码 Agent
- [[Ollama]] — 本地模型运行时
- [[GLM]] — 指南推荐的主力本地模型系列
- [[Qwen]] — 16GB 以下内存的推荐模型系列（qwen2.5-coder:14b）
- [[Claude_Code_本地模型接入]] — 本指南抽象出的接入模式
- [[本地_LLM_推理]] — 本地推理的总体概念
- [[OpenAI_Compatible_API]] — 对照：另一种兼容接口标准
