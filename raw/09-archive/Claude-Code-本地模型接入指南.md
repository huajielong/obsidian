# Claude Code 本地模型接入指南（本机专用 · 已配置）

> 机型：COLORFUL P16 Pro IXA1 · RTX 5070 Ti Laptop 12GB · i7-14650HX · 64GB DDR5-5600 · Windows 11
> 更新：2026-11-02
> 现状：**已配置完成并通过端到端测试**。`claude-local` 使用现有 Qwen3.6，通过 llama.cpp + anthropic-proxy，约 65 tok/s；没有安装任何新模型；普通 `claude` 不受影响。

---

## 0. 结论

| 方案 | 组成 | 速度 | 状态 |
|---|---|---|---|
| **推荐：claude-local（代理版）** | llama.cpp Qwen3.6（8081）+ anthropic-proxy（8787） | 约 **65 tok/s** | ✅ 已配置并验证 |
| 备用：claude-local-ollama | Ollama 直连 Qwen3.6（11434） | 约 6.6 tok/s | ✅ 可用，但很慢 |
| 普通 claude | Anthropic 官方 | 官方速度 | ✅ 不受影响 |

**已验证：**
- `claude -p "Say hello in Chinese..."` → 返回中文回答；
- `/v1/messages` 工具调用测试 → 正确返回 Anthropic `tool_use`（`get_weather` / `{"location":"Beijing"}`）。

**日常使用：**

```bat
claude-local
```

- 会自动启动 Qwen（8081）和代理（8787），等 Qwen 就绪后进入 Claude Code。
- 停止服务：`D:\AI\stop-local-ai.bat`。
- 也可手动启动：`D:\AI\start-local-ai.bat` → `D:\AI\claude-local.bat`。

---

## 1. 现有文件与组件

### 1.1 模型（全部是已有模型，没有新安装）

| 模型 | 大小 | 角色 |
|---|---|---|
| `qwen3.6:35b-a3b-mtp-q4_K_M` | 22GB | Claude Code 本地模型（编程/Agent） |
| `gemma4:12b` | 8GB | 多模态，不用于 Claude Code |
| `translategemma:4b` / `translategemma-2k` / `translategemma-cpu` | 3.3GB | 翻译 |

### 1.2 运行时与脚本

| 组件 | 路径 | 作用 |
|---|---|---|
| Qwen3.6 llama.cpp 服务 | `D:\AI\llama.cpp\start-qwen.bat` → 8081 | 实际推理，约 65 tok/s |
| anthropic-proxy | `D:\AI\anthropic-proxy\anthropic-proxy.exe` → 8787 | Anthropic Messages → OpenAI Chat Completions |
| 代理配置 | `D:\AI\anthropic-proxy\.env` | 上游地址、模型、工具格式 |
| 一键启动 | `D:\AI\start-local-ai.bat` | 同时启动 Qwen + 代理 |
| 一键停止 | `D:\AI\stop-local-ai.bat` | 停止 Qwen + 代理 |
| Claude Code 快速版 | `D:\AI\claude-local.bat` | 自动拉起 Qwen + 代理，再启动 Claude Code |
| PATH 启动入口 | `C:\Users\huajielong-win11\bin\claude-local.cmd` | PowerShell / cmd 里直接输入 `claude-local` |
| Git Bash 函数 | `C:\Users\huajielong-win11\.bashrc` | Git Bash 里直接输入 `claude-local` |
| Claude Code Ollama 慢速版 | `D:\AI\claude-local-ollama.bat` | 指向 Ollama 11434 |
| 代理手动启动 | `D:\AI\anthropic-proxy\start-proxy.bat` | 只启动代理 |

### 1.3 代理配置 `.env`

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

说明：
- `UPSTREAM_API_KEY=dummy`：代理要求必填；llama.cpp 不校验，填占位值即可。
- `TOOL_FORMAT=native`：Qwen3.6 原生工具调用。如果工具调用异常，改成 `xml` 并重启代理。
- `FORCE_MODEL=1`：Claude Code 发来的任何模型名都映射到 `qwen`。
- 代理只监听 `127.0.0.1`，不对局域网暴露。

---

## 2. 为什么这样最快

同一个 Qwen3.6，不同推理引擎：

| 引擎 | 生成速度 | prompt 处理 | 说明 |
|---|---|---|---|
| Ollama 0.40.13 | 约 6.6 tok/s | 约 0.57 tok/s | 不支持 MoE 专家卸载，整层卸载到 CPU |
| llama.cpp b12017 | 约 65 tok/s | 约 55 tok/s | `--n-cpu-moe 24` + MTP + 32K |
| anthropic-proxy | 基本无额外开销 | — | 只做协议转换 |

Claude Code 的系统提示 + 工具定义约 2 万 token，所以 prompt 处理速度非常关键。Ollama 的 0.57 tok/s 会让首次请求等很久；llama.cpp 的 55 tok/s 才实用。

---

## 3. 日常使用（已配置）

### 3.1 启动（推荐：一条命令）

在任意终端直接运行：

```bat
claude-local
```

- **Git Bash**：`~/.bashrc` 里已定义 `claude-local` 函数（新终端生效，或先 `source ~/.bashrc`）。
- **PowerShell / cmd**：`C:\Users\huajielong-win11\bin\claude-local.cmd` 已在 PATH 中。
- 如果 Qwen（8081）或代理（8787）没启动，`claude-local` 会自动拉起它们（会打开两个窗口），等 Qwen 就绪后进入 Claude Code。
- 首次启动约 10–20 秒。
- 也可以手动启动：先 `D:\AI\start-local-ai.bat`，再 `D:\AI\claude-local.bat`。

脚本会设置：

- `ANTHROPIC_BASE_URL=http://127.0.0.1:8787`
- `ANTHROPIC_API_KEY=anything`
- `ANTHROPIC_AUTH_TOKEN=anything`
- `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`
- `claude --model claude-sonnet-4-6`

代理会把 `claude-sonnet-4-6` 映射到本机 `qwen`。

### 3.2 验证

```bat
curl.exe http://127.0.0.1:8081/health
curl.exe http://127.0.0.1:8787/health
curl.exe http://127.0.0.1:8787/v1/models
```

- 8081 返回 `{"status":"ok"}`。
- 8787 返回 `ok`。
- `/v1/models` 会列出 `claude-sonnet-4-6`、`claude-opus-4-8`、`claude-haiku-4-5`（代理暴露的 Claude 模型 ID，实际都映射到 qwen）。

### 3.3 停止

- 关闭 Claude Code。
- 双击 `D:\AI\stop-local-ai.bat`，或关闭 Qwen / 代理两个窗口。
- 停止后显存释放。

### 3.4 手动启动（可选）

如果不想用一键脚本：

```bat
D:\AI\llama.cpp\start-qwen.bat
D:\AI\anthropic-proxy\start-proxy.bat
```

顺序：先 Qwen，后代理。代理可以在 Qwen 还没加载完时启动，请求会等待。

---

## 4. 备用：Ollama 直连（慢）

如果代理临时不可用，可以：

```bat
D:\AI\claude-local-ollama.bat
```

- 使用 Ollama `qwen3.6:35b-a3b-mtp-q4_K_M`。
- 速度约 6.6 tok/s，prompt 约 0.57 tok/s，只适合短问答/验证通路。
- 普通 `claude` 仍不受影响。

---

## 5. PowerShell / Git Bash 版本

### 5.1 快速版（代理 8787）

PowerShell 安全函数（保存/恢复环境变量，避免污染普通 `claude`）：

```powershell
function claude-local {
    $oldToken = $env:ANTHROPIC_AUTH_TOKEN
    $oldKey   = $env:ANTHROPIC_API_KEY
    $oldUrl   = $env:ANTHROPIC_BASE_URL

    $env:ANTHROPIC_AUTH_TOKEN = "anything"
    $env:ANTHROPIC_API_KEY    = "anything"
    $env:ANTHROPIC_BASE_URL   = "http://127.0.0.1:8787"

    try {
        claude --model claude-sonnet-4-6 @args
    }
    finally {
        $env:ANTHROPIC_AUTH_TOKEN = $oldToken
        $env:ANTHROPIC_API_KEY    = $oldKey
        $env:ANTHROPIC_BASE_URL   = $oldUrl
    }
}
```

Git Bash 别名：

```bash
alias claude-local='ANTHROPIC_API_KEY=anything ANTHROPIC_AUTH_TOKEN=anything ANTHROPIC_BASE_URL=http://127.0.0.1:8787 CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1 claude --model claude-sonnet-4-6'
```

### 5.2 慢速版（Ollama 11434）

```bash
alias claude-local-slow='ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen3.6:35b-a3b-mtp-q4_K_M'
```

---

## 6. 验证清单

- [ ] `start-local-ai.bat` 能启动 Qwen（8081）和代理（8787）
- [ ] 新终端里直接输入 `claude-local` 能启动（Git Bash / PowerShell / cmd）
- [ ] 服务未启动时，`claude-local` 能自动拉起 Qwen + 代理
- [ ] `curl http://127.0.0.1:8081/health` 返回 ok
- [ ] `curl http://127.0.0.1:8787/health` 返回 ok
- [ ] `curl http://127.0.0.1:8787/v1/models` 能看到 `claude-sonnet-4-6`
- [ ] `D:\AI\claude-local.bat` 能启动 Claude Code
- [ ] 问“你好”能正常回答
- [ ] 让 Claude Code 读一个小文件，工具调用正常
- [ ] 普通 `claude` 仍然走 Anthropic
- [ ] `stop-local-ai.bat` 能释放显存
- [ ] 显存不 OOM

---

## 7. 常见问题

### 7.1 代理启动失败：`ANTHROPIC_PROXY_UPSTREAM_API_KEY is required`

- `.env` 必须包含 `ANTHROPIC_PROXY_UPSTREAM_API_KEY=dummy`。
- 代理从当前工作目录读取 `.env`，所以必须用 `start-proxy.bat`（它会 `cd` 到 `D:\AI\anthropic-proxy`）。

### 7.2 代理 8787 正常，但请求失败

- Qwen 8081 没启动：先运行 `start-qwen.bat`，检查 `http://127.0.0.1:8081/health`。
- 上游地址写错：`.env` 里必须是 `http://127.0.0.1:8081/v1/chat/completions`（完整路径）。
- 模型名：代理 `DEFAULT_MODEL=qwen`，与 `llama-server -a qwen` 对齐。

### 7.3 Claude Code 报模型无效

- 使用 `--model claude-sonnet-4-6`（代理 `/v1/models` 里列出的 ID）。
- 代理会把它映射到本机 qwen，不需要真的 Claude 模型。
- 不要用 `--model qwen` 以外未列出的名字；虽然 `FORCE_MODEL=1` 通常会兜底，但用列出的 ID 最稳。

### 7.4 工具调用不工作

- 当前 `.env` 是 `TOOL_FORMAT=native`，已验证 `tool_use` 正常。
- 如果某个模型/版本下 native 不工作：把 `.env` 改成 `ANTHROPIC_PROXY_TOOL_FORMAT=xml`，重启代理。
- 工具调用依赖 Qwen3.6 的 tools 能力；不要用 Gemma 4/TranslateGemma 做 Claude Code。

### 7.5 `claude -p` 被权限拦截 / 一直无输出

- `claude -p "..."` 在无交互模式下可能因为工具权限被拒绝或卡在确认界面；这是 Claude Code 的权限策略，不是代理问题。
- 自动拉起服务后，`claude -p` 如果长时间无输出、GPU 空闲，通常是卡在无 TTY 的权限确认；改用交互式 `claude-local` 即可。
- 日常用交互式 `claude-local`；需要自动化时，按需配置允许的工具/权限。
- 不要默认使用 `--dangerously-skip-permissions`，除非你明确知道风险。

### 7.6 速度慢

- 检查 Qwen 是否走 llama.cpp 8081，而不是 Ollama 11434。
- 关闭 Index-tts2、ChatGPT/Codex、NVIDIA Broadcast。
- 检查 `nvidia-smi` 显存；Qwen 约 10.8GB。
- 上下文不要超过 32K；OOM 时把 `start-qwen.bat` 的 `--n-cpu-moe 24` 改成 28。

### 7.7 普通 `claude` 也连到本地了

- 不要用直接 `$env:` 赋值的 PowerShell 函数；用第 5.1 节的保存/恢复版本或 `.bat`。
- 关闭终端重开，或清除：
  ```powershell
  Remove-Item Env:ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
  Remove-Item Env:ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
  Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
  ```

### 7.8 Python 环境说明

- 配置过程中尝试过 LiteLLM，它升级了全局 Python 包；随后已恢复关键版本（litellm 1.60.2、fastapi 0.104.1、aiohttp 3.14.2、pydantic-settings 2.10.1、rich 14.3.4 等）。
- 最终使用的 anthropic-proxy 是 Go 单文件，不依赖 Python。
- 如果 CrewAI 等项目出现依赖异常，告诉我，我可以把代理相关依赖隔离到虚拟环境。

---

## 8. 回滚

- 不使用 `claude-local`，直接运行普通 `claude` 即可；两者互不影响。
- 停止服务：`D:\AI\stop-local-ai.bat`。
- 删除脚本：`claude-local.bat`、`claude-local-proxy.bat`、`start-local-ai.bat`、`stop-local-ai.bat`。
- 没有安装新模型，不需要卸载模型。
- 代理文件可保留，不占多少空间（约 25MB）。

---

## 9. 与原教程的差异

| 原教程 | 本机中文版 | 原因 |
|---|---|---|
| Step 0–2 安装 Node/Claude/Ollama | 跳过 | 已安装 |
| 用 glm-4.7-flash 等新模型 | 不装新模型，使用现有 Qwen3.6 | 用户明确要求；12GB 显存也更适合现有 Qwen |
| Ollama 直连 | Ollama 直连仅作备用（6.6 tok/s） | 实测太慢 |
| 只讲代理概念 | 已配置 anthropic-proxy（8787）并验证 | 端到端可用 |
| 默认 4K 上下文 | 32K | Claude Code 系统提示约 20K token |
| PowerShell 直接改 `$env:` | 保存/恢复版本或 `.bat` | 避免污染普通 `claude` |
| 声称“100% 私有” | 推理本地，但 Claude Code 可能联网 | 避免误解 |

---

## 10. 参考来源

- anthropic-proxy：https://github.com/thomas-illiet/anthropic-proxy
- Ollama Anthropic 兼容文档：https://docs.ollama.com/api/anthropic-compatibility
- 本机模型与调优：`D:\AI\本地模型执行指南.md`
