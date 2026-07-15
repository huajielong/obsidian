---
title: LLM 工具调用入门实践
date: 2026-07-14
tags: [LLM, AI, Tool Calling, Function Calling, Ollama, Claude, OpenAI]
---

# LLM 工具调用（Tool Calling）入门实践

## 概述

大语言模型（LLM）的**工具调用**能力（又称 Function Calling）是其核心能力之一——模型不仅生成文本，还能根据对话上下文自主选择调用外部工具（API/函数），从而获取实时数据、执行操作或与环境交互。

本文通过两个并行的练习脚本，展示两种主流工具调用协议的使用方式：

- **OpenAI 兼容格式**（通过本地 Ollama 调用 `qwen2.5:3b`）
- **Anthropic 原生格式**（通过 Anthropic SDK 调用 `claude-haiku-4-5`）

## 场景：查询天气

两个脚本都相同的功能：

1. 定义一个 `get_weather` 工具，接收 `city` 参数
2. 问模型："台北现在有下雨吗？"
3. 模型应该**自主决定**调用 `get_weather` 工具，而不是直接回答
4. 验证工具调用的参数正确性

---

## 脚本 1：OpenAI 兼容格式（Ollama 本地运行）

```python
# 需要：pip install openai
# 前置：ollama pull qwen2.5:3b && ollama serve
import sys, json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

### 工具 Schema

OpenAI 兼容格式需要在工具定义外套一层 `{"type": "function", "function": {...}}`：

```python
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询城市目前天气（晴/雨/阴），回传一个短字符串。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称（如「台北」）"},
            },
            "required": ["city"],
        },
    },
}
```

### 调用与验证

```python
resp = client.chat.completions.create(
    model="qwen2.5:3b",
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "台北现在有下雨吗？"}],
)

msg = resp.choices[0].message
assert msg.tool_calls, "预期 LLM 会选择调用 tool"
tc = msg.tool_calls[0]
assert tc.function.name == "get_weather"
args = json.loads(tc.function.arguments)
assert args.get("city")
print(f"✅ 通过 — 选了 get_weather、city='{args['city']}'")
```

**关键点：**
- 响应中的 `finish_reason` 为 `tool_call` 而非 `stop`
- 工具调用参数在 `msg.tool_calls[0].function.arguments` 中（JSON 字符串）
- 本地运行依赖 Ollama，推荐 `qwen2.5:3b`（作者注：tool-use 稳定性高于 `gemma4`）

---

## 脚本 2：Anthropic 原生格式

```python
# 需要：pip install anthropic
# 环境变量：export ANTHROPIC_API_KEY=sk-ant-...
import anthropic

client = anthropic.Anthropic()
```

### 工具 Schema

Anthropic 原生格式更简洁，不需要外层包装，直接定义 `name`、`description`、`input_schema`：

```python
weather_tool = {
    "name": "get_weather",
    "description": "查询城市目前天气（晴/雨/阴），回传一个短字符串。",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名称（如「台北」）"},
        },
        "required": ["city"],
    },
}
```

### 调用与验证

```python
resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "台北现在有下雨吗？"}],
)

assert resp.stop_reason == "tool_use"
tool_calls = [b for b in resp.content if b.type == "tool_use"]
assert tool_calls[0].name == "get_weather"
assert tool_calls[0].input.get("city")
print(f"✅ 通过 — 选了 get_weather、city='{tool_calls[0].input['city']}'")
```

**关键点：**
- `stop_reason` 为 `tool_use`（异于 OpenAI 的 `tool_call`）
- 工具调用在 `resp.content` 列表中，`type == "tool_use"` 的 block 即为调用
- 参数直接以对象形式存在 `tool_calls[0].input`，不需要 `json.loads` 解析

---

## 两种格式对比

| 维度 | OpenAI 兼容（Ollama） | Anthropic 原生 |
|------|----------------------|----------------|
| **依赖** | `openai` 包 | `anthropic` 包 |
| **模型** | qwen2.5:3b（本地） | claude-haiku-4-5（云端） |
| **Schema 结构** | 套一层 `{type:"function", function:{...}}` | 直接 `{name, description, input_schema}` |
| **参数名** | `parameters` | `input_schema` |
| **停止原因** | `finish_reason == "tool_call"` | `stop_reason == "tool_use"` |
| **调用参数提取** | `json.loads(tc.function.arguments)` | `tc.input`（已是对象） |
| **运行方式** | 本地（需要 GPU/CPU） | 云端 API |
| **API Key** | 虚拟值 `"ollama"` | 真实 `ANTHROPIC_API_KEY` |

## 小结

这两个练习展示了 LLM 工具调用的核心模式：

1. **定义工具**：告诉模型有哪些可用工具、参数结构
2. **模型自主决策**：不强制调用，让模型根据用户意图判断是否需要工具
3. **解析调用结果**：提取工具名称和参数，执行真实逻辑（示例中未实现真实天气查询，仅验证了调用本身）

工具调用是 Agent 系统的基石——通过它，LLM 从"只会说话"进化为"能动手"。
