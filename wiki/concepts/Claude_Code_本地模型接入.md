---
title: "Claude_Code_本地模型接入"
type: concept
tags: [Claude Code, 本地LLM, Ollama, llama.cpp, anthropic-proxy, 环境变量, 别名]
sources:
  - raw/01-articles/claude-code-ollama-local-setup.md
  - raw/01-articles/Claude-Code-本地模型接入指南.md
  - raw/01-articles/本地模型执行指南.md
last_updated: 2026-11-02
---

## 定义

Claude Code 本地模型接入是指通过 `ANTHROPIC_BASE_URL` 等环境变量，把 Claude Code 原本发往 Anthropic API 的请求重定向到本地模型服务，从而在无云端订阅、数据不出本机的前提下继续使用 Claude Code 的 Agent 能力。常见有两条路径：直连原生 Anthropic 兼容端点（如 Ollama 的 11434），或经协议转换代理（如 [[Anthropic_Proxy|anthropic-proxy]] 的 8787）转接到 [[LlamaCpp|llama.cpp]] 等 OpenAI 兼容后端。典型做法是配合 shell 别名生成第二个命令 `claude-local`，与常规 `claude` 并存。

## 关键信息

### 两条接入路径

| 路径 | 链路 | 本机实测 | 适用场景 |
|------|------|----------|----------|
| **代理 + llama.cpp（推荐）** | Claude Code → anthropic-proxy 8787 → llama.cpp 8081 | 约 **65 tok/s** | 日常编码、Agent |
| 直连 Ollama | Claude Code → Ollama 11434 | 约 6.6 tok/s | 快速验证、低配置环境 |
| 官方云端 | Claude Code → Anthropic API | 官方速度 | 常规使用，不受本地配置影响 |

> 两条本地路径都只替换 [[Claude_Code_Harness|7-Layer Architecture]] 的 L1 Foundation 层；Skills / Hooks / MCP / Subagent 等 Harness 能力保持不变。

### 代理路径的环境变量

```bash
ANTHROPIC_BASE_URL=http://127.0.0.1:8787 \
ANTHROPIC_API_KEY=anything \
ANTHROPIC_AUTH_TOKEN=anything \
CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1 \
claude --model claude-sonnet-4-6
```

| 变量 | 值 | 作用 |
|------|-----|------|
| `ANTHROPIC_BASE_URL` | `http://127.0.0.1:8787` | 指向 anthropic-proxy |
| `ANTHROPIC_API_KEY` | `anything` | 占位 Key，代理不校验 |
| `ANTHROPIC_AUTH_TOKEN` | `anything` | 占位令牌 |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` | `1` | 允许从 `/v1/models` 发现模型 |
| `--model` | `claude-sonnet-4-6` | 代理映射到本机 `qwen` |

### 直连路径的环境变量

```bash
ANTHROPIC_AUTH_TOKEN=ollama \
ANTHROPIC_API_KEY="" \
ANTHROPIC_BASE_URL=http://localhost:11434 \
claude --model qwen3.6:35b-a3b-mtp-q4_K_M
```

| 变量 | 值 | 作用 |
|------|-----|------|
| `ANTHROPIC_BASE_URL` | `http://localhost:11434` | 指向 Ollama |
| `ANTHROPIC_AUTH_TOKEN` | `ollama` | 占位令牌，Ollama 不校验 |
| `ANTHROPIC_API_KEY` | 空字符串 | 清空官方 Key |
| `--model` | Ollama 中已 pull 的模型名 | 本地模型 |

### 为什么用别名而不是全局环境变量

- 常规 `claude` 继续走 Anthropic 云端与订阅，不受影响
- `claude-local` 单独携带本地环境变量，两套配置互不污染
- 所有常规 CLI 参数仍可透传，如 `claude-local --dangerously-skip-permissions`
- PowerShell 推荐用“保存/恢复环境变量”的函数，避免函数执行后污染当前终端
- 可扩展多个别名，分别对应不同本地模型或不同任务场景

### 硬件与模型选型

**通用教程（按内存）**

| 内存 | 推荐模型 | 说明 |
|------|----------|------|
| ≤16GB | `qwen2.5-coder:14b` | 14B 代码模型 |
| 32GB | `glm-4.7-flash` | 指南推荐，约 19GB 下载 |
| 48GB+ | `glm-4.7` | 更高内存档位 |

**本机实际（按显存）**

| 资源 | 选择 | 说明 |
|------|------|------|
| RTX 5070 Ti Laptop 12GB + 64GB RAM | `qwen3.6:35b-a3b-mtp-q4_K_M` | 35.5B MoE，Q4_K_M，约 22GB 文件，运行显存约 10.8GB |
| 多模态 / 翻译 | `gemma4:12b` / `translategemma*` | 不用于 Claude Code 主模型 |
| 最终选择 | **Qwen3.6 + llama.cpp + anthropic-proxy** | 约 65 tok/s；未安装 GLM 新模型 |

> 本机因 12GB 显存与已有 Qwen3.6，未采用通用教程的 `glm-4.7-flash`；这属于本地实施差异，不是模型能力冲突。

### 日常使用（本机已配置）

```bat
claude-local
```

- 自动拉起 Qwen（8081）与代理（8787），等 Qwen 就绪后进入 Claude Code
- 首次启动约 10–20 秒；服务已启动时直接进入
- 停止：`D:\AI\stop-local-ai.bat`，或关闭 Qwen / 代理窗口
- 手动启动：`D:\AI\start-local-ai.bat` → `D:\AI\claude-local.bat`
- Git Bash：`~/.bashrc` 中的 `claude-local` 函数；PowerShell / cmd：PATH 中的 `claude-local.cmd`

### 验证

```bash
curl http://127.0.0.1:8081/health   # {"status":"ok"}
curl http://127.0.0.1:8787/health   # ok
curl http://127.0.0.1:8787/v1/models
```

`/v1/models` 应列出 `claude-sonnet-4-6`、`claude-opus-4-8`、`claude-haiku-4-5`（实际都映射到 qwen）。工具调用测试应返回 Anthropic `tool_use` block。

### 适用场景与边界

- **适合**：隐私敏感代码、离线环境、零边际成本实验、学习 Claude Code 的 Agent 机制
- **边界**：本地模型能力通常弱于云端 Opus/Sonnet；首次拉取模型体积大；推理速度与上下文长度受本机 RAM/VRAM 限制
- **工程边界**：代理只监听 `127.0.0.1`；不要默认使用 `--dangerously-skip-permissions`
- **隐私边界**：模型推理在本地，但 Claude Code 客户端本身可能联网（更新、遥测等）

### 与原教程的实施差异

| 原教程 | 本机实施 | 原因 |
|--------|----------|------|
| Step 0–2 安装 Node/Claude/Ollama | 跳过 | 已安装 |
| 用 glm-4.7-flash 等新模型 | 不装新模型，使用现有 Qwen3.6 | 用户明确要求；12GB 显存更适合现有 Qwen |
| Ollama 直连 | 仅作备用（6.6 tok/s） | 实测太慢 |
| 只讲代理概念 | 已配置 anthropic-proxy（8787）并验证 | 端到端可用 |
| 默认 4K 上下文 | 32K | Claude Code 系统提示约 20K token |
| PowerShell 直接改 `$env:` | 保存/恢复版本或 `.bat` | 避免污染普通 `claude` |
| 声称“100% 私有” | 推理本地，但 Claude Code 可能联网 | 避免误解 |

## 知识冲突

### “100% 私有”的适用范围

- **旧说法（通用教程 `摘要-claude-code-ollama-local-setup`）**：`claude-local` 是“100% free, 100% private, 100% local”。
- **新说法（本机实施记录 `摘要-claude-code-本地模型接入指南`）**：模型推理确实在本地完成，但 Claude Code 本体可能联网（更新、遥测或其他网络请求），因此不应把整个使用过程表述为“100% 私有”。
- **当前处理**：保留双方说法。涉及隐私承诺时采用新说法，仅声明“模型推理在本地”；通用教程的表述视为营销性概括，不作事实承诺。

## 关联连接

- [[Claude_Code]] — 被重定向的 Agent 工具
- [[Ollama]] — 直连路径的本地运行时
- [[LlamaCpp]] — 代理路径的推理引擎
- [[Anthropic_Proxy]] — Anthropic → OpenAI 协议转换代理
- [[Anthropic_Compatible_API]] — 接入所依赖的接口契约
- [[GLM]] — 通用教程推荐模型
- [[Qwen]] — 本机实际使用的模型系列
- [[Gemma]] — 多模态与翻译模型
- [[本地_LLM_推理]] — 上位概念
- [[本地推理性能调优]] — 性能数据与调优方法
- [[摘要-claude-code-ollama-local-setup]] — 通用教程来源
- [[摘要-claude-code-本地模型接入指南]] — 本机实施记录来源
- [[摘要-本地模型执行指南]] — 同机模型与调优手册
- [[OpenAI_Compatible_API]] — 对照：另一种兼容接口标准
- [[Harness_Engineering]] — Claude Code 保留的 Harness 层
- [[Claude_Code_Harness]] — 7-Layer 架构中仅替换 L1 的定位
