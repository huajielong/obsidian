---
title: Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录
date: 2026-07-08
tags:
  - ollama
  - python
  - llm
  - api
  - 踩坑
---

## 背景

想在本地跑 LLM，又不想把数据送到云端，Ollama 是目前最省心的选择。本文记录从零开始用 Python 调用 Ollama 本地模型的完整过程：四种 API 调用方式、Windows 下的编码坑、模型兼容性问题。

## 环境

| 项目 | 值 |
|------|-----|
| OS | Windows 11 |
| Ollama | 0.31.1 |
| 模型 | qwen3.5:0.8b (1.0 GB) → llama3.2:3b (2.0 GB) |
| API 地址 | `http://localhost:11434` |
| 推理设备 | CPU only（集成显卡 Intel UHD 自动跳过） |

---

## 一、四种 API 调用方式

Ollama 提供两套 API：**原生 API**（`/api/chat`）和 **OpenAI 兼容 API**（`/v1/chat/completions`），每套都支持流式和非流式，共四种组合。

### 准备工作

```python
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import urllib.request
import json

OLLAMA_BASE = "http://localhost:11434"
MODEL = "llama3.2:3b"
```

> === GBK 编码修复 ===
>
> Windows 终端默认编码是 GBK，Python 的 `print()` 遇到 emoji 或中文混合输出时会抛 `UnicodeEncodeError`。`sys.stdout.reconfigure(encoding="utf-8")` 强制 stdout 使用 UTF-8 输出，一劳永逸。

### 方式 1：原生 API — 非流式

最基础的用法，请求发出去等完整回复回来再处理。

```python
payload = {
    "model": MODEL,
    "messages": [{"role": "user", "content": "用一句话介绍你自己。"}],
    "stream": False,
}
req = urllib.request.Request(
    f"{OLLAMA_BASE}/api/chat",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode("utf-8"))

print(f"回复: {result['message']['content']}")
print(f"Token: 输入={result['prompt_eval_count']}, 输出={result['eval_count']}")
```

**特点：** 纯内置库，零依赖。一次请求拿到完整 JSON，适合简单脚本。

---

### 方式 2：原生 API — 流式

`stream=True`，Ollama 逐行返回 JSON，每行一个 chunk。

```python
payload = {
    "model": MODEL,
    "messages": [{"role": "user", "content": "从 1 数到 5，每行一个数字。"}],
    "stream": True,
}
req = urllib.request.Request(
    f"{OLLAMA_BASE}/api/chat",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req) as resp:
    for line in resp:
        if not line.strip():
            continue
        chunk = json.loads(line.decode("utf-8"))
        delta = chunk.get("message", {}).get("content", "")
        print(delta, end="", flush=True)
        if chunk.get("done"):
            print()
            stats = {
                "总耗时": f"{chunk.get('total_duration', 0) / 1e9:.2f}s",
                "Token 数": f"输入={chunk.get('prompt_eval_count')}, 输出={chunk.get('eval_count')}",
                "速率": f"{chunk.get('eval_count', 0) / (chunk.get('total_duration', 1) / 1e9):.1f} token/s",
            }
            print(f"[统计] {stats}")
```

**特点：** 也是内置库。逐行解析，边生成边显示；最后一个 chunk 的 `done: true` 携带完整统计信息。

---

### 方式 3：OpenAI 兼容 API — 非流式

Ollama 还提供与 OpenAI SDK 完全兼容的接口，已有 OpenAI 调用的代码几乎无需修改。

```bash
pip install openai
```

```python
from openai import OpenAI

client = OpenAI(base_url=f"{OLLAMA_BASE}/v1", api_key="ollama")

r = client.chat.completions.create(
    model=MODEL,
    max_tokens=200,
    messages=[{"role": "user", "content": "用一句话介绍你自己。"}],
)

content = r.choices[0].message.content
print(f"回复: {content}")
print(f"使用模型: {r.model}")
print(f"Token 用量: {r.usage}")
```

**特点：** 接口与 OpenAI 官方 API 一致，迁移成本最低。`api_key` 填任意值即可，Ollama 不验证。

---

### 方式 4：OpenAI 兼容 API — 流式

```python
stream = client.chat.completions.create(
    model=MODEL,
    max_tokens=200,
    messages=[{"role": "user", "content": "背诵一首唐诗的五言绝句。"}],
    stream=True,
)

for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

**特点：** 与 OpenAI SDK 流式接口完全一致，每个 chunk 的 `choices[0].delta.content` 就是增量文本。

---

### 四种方式对比

| 方式 | 依赖 | 响应方式 | 典型场景 |
|------|------|----------|----------|
| 原生非流式 | 内置库 | 一次性 | 简单对话、批处理 |
| 原生流式 | 内置库 | 逐行 JSON | 实时展示、进度条 |
| OpenAI 非流式 | openai 库 | 一次性 | 已有 OpenAI 代码的迁移 |
| OpenAI 流式 | openai 库 | 流式 chunk | ChatGPT 风格的打字机效果 |

---

## 二、踩坑记录

### 坑 1：Windows GBK 编码 → UnicodeEncodeError

**现象：** 脚本输出 emoji（✅、✨）或中英文混合时崩溃。

```
UnicodeEncodeError: 'gbk' codec can't encode character '✅'
```

**原因：** Windows 终端默认编码是 GBK，不包含 emoji 字符。

**解决方案：** 脚本开头加入：

```python
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

`errors="replace"` 保证即使有无法编码的字符也能用 `?` 替代而不是崩溃。

---

### 坑 2：qwen3.5:0.8b 的 OpenAI 兼容 Bug

**现象：** 原生 API 正常回复，但 OpenAI 兼容接口调用成功、Token 正常消耗、`finish_reason="length"`，**`content` 字段却为空**。

```
回复:
使用模型: qwen3.5:0.8b
Token 用量: {'prompt_tokens': 30, 'completion_tokens': 4066, 'total_tokens': 4096}
```

**原因：** qwen3.5:0.8b 这个模型在 Ollama 的 OpenAI 兼容端口下有兼容性问题，`content` 返回空字符串。这是 **模型与 Ollama 版本之间的兼容问题**，不是代码问题。

**解决方案：** 换模型。实测 `llama3.2:3b` 和 `qwen2.5:3b` 均能正常工作。

```bash
ollama pull llama3.2:3b
```

---

### 坑 3：Ollama 端口冲突

**现象：** 启动 Ollama 时提示 `port 11434 already in use`。

**原因：** 后台已经有一个 ollama 进程在运行（可能是 Ollama 桌面应用和服务进程重复了）。

**解决方案：** 在 Git Bash 中用 `taskkill` 注意参数格式：

```bash
# Git Bash 中必须用 //F 而非 /F，否则 /F 会被当作路径
taskkill //F //IM ollama.exe
taskkill //F //IM "ollama app.exe"
```

> 在 Git Bash 中，`/F` 会被识别为文件系统路径，要用 `//F` 绕过。

---

### 坑 4：Ollama pull 下载卡在 94-96%

**现象：** 下载 `llama3.2:3b` 到 1,926 MB / 2.0 GB 时速度骤降至 ~18 KB/s，最终卡住不动。

**原因：** 网络波动或镜像服务器不稳定。

**解决方案：** 直接 Ctrl+C 中断重试，Ollama 支持断点续传。重新 `ollama pull llama3.2:3b` 会从暂停处继续。

---

### 坑 5：推理速度

| 模型 | 大小 | 速度 | 备注 |
|------|------|------|------|
| qwen3.5:0.8b | 1.0 GB | ~18.6 token/s | CPU 推理，响应慢 |
| llama3.2:3b | 2.0 GB | ~8.8 token/s | 参数更多，速度更慢 |

CPU 推理，集成显卡被 Ollama 自动跳过。想要快还是得上 GPU。

---

## 三、完整脚本

最终整合版见同级目录下的 `ollama_demo.py`，包含了上述四种调用方式和检查逻辑。直接运行：

```bash
python ollama_demo.py
```

前提是 Ollama 已在 `localhost:11434` 运行且已拉取 `llama3.2:3b` 模型。

---

## 总结

1. **Ollama 提供了两套 API**：原生 API（零依赖）和 OpenAI 兼容 API（方便迁移）。
2. **Windows 下编码是最隐蔽的坑**——不是 LLM 本身的错，但足够让新手崩溃。
3. **模型兼容性不可忽视**——同属 Ollama 生态，不同模型对同一端口的支持程度不同。遇到奇怪问题先换模型试试。
4. **流式 vs 非流式**没有优劣之分，流式适合实时展示，非流式适合程序内部处理。

---

**参考链接：**
- [Ollama API 文档](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
