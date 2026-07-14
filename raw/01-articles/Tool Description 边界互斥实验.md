---
title: Tool Description 边界互斥实验
date: 2026-07-14
tags: [LLM, Tool Calling, Function Calling, Ollama, qwen2.5, prompt engineering]
---

# Tool Description 边界互斥实验

## 问题

在 LLM 工具调用中，当一个系统有多个 tool 时，模型靠 **description** 来判断选哪一个。但如果 description 写得太笼统，不同 tool 的边界就会重叠，小模型尤其容易挑错。

本实验通过三个对比测试，验证 **description 边界互斥** 对工具选择准确性的影响。

## 完整代码

```python
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def make_tools(calendar_desc):
    """根据不同的 calendar description 生成工具列表。"""
    return [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search current or external info not in the prompt.",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Evaluate basic arithmetic with +, -, *, /, parentheses.",
                "parameters": {
                    "type": "object",
                    "properties": {"expression": {"type": "string"}},
                    "required": ["expression"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calendar_lookup",
                "description": calendar_desc,
                "parameters": {
                    "type": "object",
                    "properties": {"date": {"type": "string"}},
                    "required": ["date"],
                },
            },
        },
    ]
```

三个测试通过同一个 `make_tools(calendar_desc)` 工厂函数，只替换 `calendar_lookup` 的 description，其他不变：

| Tool | 固定 description |
|------|----------------|
| `web_search` | "Search current or external info not in the prompt." |
| `calculator` | "Evaluate basic arithmetic with +, -, *, /, parentheses." |
| `calendar_lookup` | **随测试变化** |

### 测试 1：Baseline（好 description + 明确数学题）

- **calendar description**: `"Look up events for a specific date."`
- **提问**: `"What is (19 * 42) - 8?"`
- **预期**: ✅ 选 `calculator`

```python
resp1 = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=make_tools("Look up events for a specific date."),
    messages=[{"role": "user", "content": "What is (19 * 42) - 8?"}]
)
msg1 = resp1.choices[0].message
tc1 = msg1.tool_calls[0]
print(f"LLM 挑了: {tc1.function.name}, args: {json.loads(tc1.function.arguments)}")
# 输出 → LLM 挑了: calculator, args: {'expression': '(19 * 42) - 8'}
```

这是一个明确的算术题，所有 description 都写得清楚，作为对照组确认模型基础能力正常。

### 测试 2：坏 description（太笼统 + 模糊问题）

- **calendar description**: `"日历"` ← 只有两个字，没有说明"查事件"还是"查信息"
- **提问**: `"这周五有什么安排？"`
- **预期**: ⚠️ 可能错选 `web_search`

```python
resp2 = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=make_tools("日历"),
    messages=[{"role": "user", "content": "这周五有什么安排？"}]
)
msg2 = resp2.choices[0].message
tc2 = msg2.tool_calls[0]
print(f"LLM 挑了: {tc2.function.name}, args: {json.loads(tc2.function.arguments)}")
# 输出 → LLM 挑了: web_search, args: {'query': '这周五有什么安排'}
#        （错选 — "日历"太笼统，模型理解为搜索任务）
```

为什么可能错？`"日历"` 没有表达"查询指定日期的事件"这层含义，模型觉得"这周五有什么安排"像是需要搜一下外部信息，就会偏向 `web_search`。

### 测试 3：好 description（边界清晰 + 同样模糊问题）

- **calendar description**: `"查询指定日期的事件"`
- **提问**: `"这周五有什么安排？"`
- **预期**: ✅ 选 `calendar_lookup`

```python
resp3 = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=make_tools("查询指定日期的事件"),
    messages=[{"role": "user", "content": "这周五有什么安排？"}]
)
msg3 = resp3.choices[0].message
tc3 = msg3.tool_calls[0]
print(f"LLM 挑了: {tc3.function.name}, args: {json.loads(tc3.function.arguments)}")
# 输出 → LLM 挑了: calendar_lookup, args: {'date': '2026-07-17'}
#        （选对 — description 边界清晰，模型能正确路由）
```

同样的问题，只改 description 边界——`"查询指定日期的事件"` 与 `"搜索外部信息"`、`"计算表达式"` 天然互斥，模型更容易正确路由。

## 核心结论

```
对比结果
测试 1（math baseline） → calculator
测试 2（坏 desc）       → web_search / calendar_lookup（取决于模型，大概率错）
测试 3（好 desc）       → calendar_lookup
```

| 原则 | 说明 |
|------|------|
| **边界互斥** | 不同 tool 的 description 语义上不能有交叉——"日历"和"搜索"都隐含"查信息"，就会撞 |
| **写给人看 ≠ 写给模型看** | "日历"是人类理解的快捷标签，但对模型来说信息量不够；要写"查询指定日期的事件" |
| **小模型对质量更敏感** | `qwen2.5:3b` 这类小参数模型对 description 的措辞变化反应明显，是测试边界质量的好靶子 |
| **参数优先做测试** | 用工厂函数将变量收拢成一个参数，可以快速做 A/B 对比，排除其他因素的干扰 |

## 实操建议

写 tool description 时的自检清单：

1. **每个 description 是否让模型一眼知道"什么场景用它"？** — 不要用缩写、不要用太泛的词
2. **任意两个 description 拼在一起，语义上有没有模糊地带？** — 有就加限定词
3. **是否包含具体的数据格式或返回值提示？** — 比如"返回 JSON 数组"比"查询信息"好

如果模型在 A/B 测试中仍然选错，把太笼统的那个 description 继续往"它能做什么、不能做什么"的方向细化，直到边界完全互斥为止。
