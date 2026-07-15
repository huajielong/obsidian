---
title: Tool Description 边界互斥实验
date: 2026-07-14
tags: [LLM, Tool Calling, Function Calling, Ollama, qwen2.5, Prompt Engineering]
---

# Tool Description 边界互斥实验

## 问题

在 LLM 工具调用中，当系统有多个 tool 时，模型靠 **description** 来判断应该用哪一个。description 写得好不好，直接影响模型能否正确路由到正确的工具。

核心假设：**description 写得越像"给人读的 docstring"，模型越容易挑错；边界越互斥，模型选得越准。** 小模型（如 qwen2.5:3b）对 description 质量尤其敏感。

本实验通过三个对比测试，验证这一假设。

---

## 完整代码

```python
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def make_tools(calendar_desc):
    """根据不同的 calendar description 生成工具列表。
    
    只有 calendar_lookup 的 description 变化，
    其余工具完全不变——确保实验控制变量。
    """
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


# ===== 工具集固定不变 =====
# 三个工具中只有 calendar_lookup 的 description 随测试变化
# web_search 和 calculator 始终不变

# ===== 测试 1：好 description + 明确数学题（baseline）=====
print("=" * 60)
print("测试 1：好 description + 明确数学题")
print("  calendar = 'Look up events for a specific date.'")
print("  提问   = 'What is (19 * 42) - 8?'")
print("  预期   → calculator")
print("-" * 60)

resp1 = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=make_tools("Look up events for a specific date."),
    messages=[{"role": "user", "content": "What is (19 * 42) - 8?"}]
)
msg1 = resp1.choices[0].message
if msg1.tool_calls:
    tc1 = msg1.tool_calls[0]
    print(f"LLM 挑了: {tc1.function.name}, args: {json.loads(tc1.function.arguments)}")
else:
    tc1 = None
    print(f"LLM 直接回答了: {msg1.content}")
print()


# ===== 测试 2：坏 description（太笼统）+ 模糊问题 =====
print("=" * 60)
print("测试 2：坏 description + 模糊问题")
print("  calendar = '日历'（仅两个字，与 web_search 语义重叠）")
print("  提问   = '这周五有什么安排？'")
print("  预期   → 可能错选 web_search（因为「日历」没说明具体用途）")
print("-" * 60)

resp2 = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=make_tools("日历"),
    messages=[{"role": "user", "content": "这周五有什么安排？"}]
)
msg2 = resp2.choices[0].message
if msg2.tool_calls:
    tc2 = msg2.tool_calls[0]
    print(f"LLM 挑了: {tc2.function.name}, args: {json.loads(tc2.function.arguments)}")
else:
    tc2 = None
    print(f"LLM 直接回答了: {msg2.content}")
print()


# ===== 测试 3：好 description（边界清晰）+ 同样模糊问题 =====
print("=" * 60)
print("测试 3：好 description + 同样模糊问题")
print("  calendar = '查询指定日期的事件'（边界与 web_search 互斥）")
print("  提问   = '这周五有什么安排？'")
print("  预期   → calendar_lookup")
print("-" * 60)

resp3 = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=make_tools("查询指定日期的事件"),
    messages=[{"role": "user", "content": "这周五有什么安排？"}]
)
msg3 = resp3.choices[0].message
if msg3.tool_calls:
    tc3 = msg3.tool_calls[0]
    print(f"LLM 挑了: {tc3.function.name}, args: {json.loads(tc3.function.arguments)}")
else:
    tc3 = None
    print(f"LLM 直接回答了: {msg3.content}")
print()


# ===== 结论对比 =====
print("=" * 60)
print("对比结果")
print("=" * 60)
print(f"测试 1（math baseline） → {tc1.function.name if tc1 else '直接回答'}")
print(f"测试 2（坏 desc）      → {tc2.function.name if tc2 else '直接回答'}")
print(f"测试 3（好 desc）      → {tc3.function.name if tc3 else '直接回答'}")
print()
print("如果测试 2 挑了 web_search 而测试 3 挑了 calendar_lookup，")
print("就说明 description 边界互斥直接影响小模型的工具选择。")
print("如果两者一样，试试把 calendar 坏 description 改得更模糊（比如 '信息'）再跑。")
```

---

## 实验设计

三个 tool，通过工厂函数 `make_tools(calendar_desc)` 只更改 `calendar_lookup` 的 description，其他工具完全不变：

| Tool | 固定 description |
|------|----------------|
| `web_search` | "Search current or external info not in the prompt." |
| `calculator` | "Evaluate basic arithmetic with +, -, *, /, parentheses." |
| `calendar_lookup` | **随测试变化**（见下方） |

### 测试 1：Baseline

| 项 | 值 |
|----|----|
| calendar description | `"Look up events for a specific date."` |
| 提问 | `"What is (19 * 42) - 8?"` |
| 预期 | ✅ `calculator` |

明确数学题 + 所有 description 写得清楚 → 作为对照组确认模型基础能力正常。

**执行结果示例：**
```
LLM 挑了: calculator, args: {'expression': '(19 * 42) - 8'}
```

### 测试 2：坏 description

| 项 | 值 |
|----|----|
| calendar description | `"日历"`（只有两个字，语义太笼统） |
| 提问 | `"这周五有什么安排？"` |
| 预期 | ⚠️ 可能错选 `web_search` |

为什么可能错？`"日历"` 没有表达"查询特定日期的事件"这层含义。模型看到"这周五有什么安排"觉得像是需要搜索外部信息，而 `web_search` 的 description 正好是"Search...external info"，就撞上了。

**执行结果示例（错误情况）：**
```
LLM 挑了: web_search, args: {'query': '这周五有什么安排'}
```
**执行结果示例（正确情况）：**
```
LLM 挑了: calendar_lookup
```
如果结果正确，说明模型仍然从参数名 `date` 推断出了用途——这时需要把坏 description 改得更模糊（如 `"信息"`）再试。

### 测试 3：好 description

| 项 | 值 |
|----|----|
| calendar description | `"查询指定日期的事件"` |
| 提问 | `"这周五有什么安排？"` |
| 预期 | ✅ `calendar_lookup` |

同样的问题、同样的工具集，只改了 description——`"查询指定日期的事件"` 与 `"搜索外部信息"`、`"计算表达式"` 语义天然互斥，模型更容易正确路由。

**执行结果示例：**
```
LLM 挑了: calendar_lookup, args: {'date': '2026-07-17'}
```

---

## 核心发现

### 对比表格

| 测试 | description | 提问 | 可能结果 | 原因 |
|------|-----------|------|---------|------|
| 1（baseline） | 好（具体） | 明确数学题 | ✅ calculator | 匹配清晰 |
| 2（坏 desc） | `"日历"`（笼统） | 模糊问题 | ⚠️ web_search | 语义重叠 |
| 3（好 desc） | 好（边界互斥） | 同模糊问题 | ✅ calendar_lookup | 边界清晰 |

### 四原则

| 原则 | 说明 |
|------|------|
| **边界互斥** | 不同 tool 的 description 语义上不能有交叉——"日历"和"搜索"都隐含"查信息"，就会撞 |
| **写给人看 ≠ 写给模型看** | "日历"是人类理解的快捷标签，但对模型来说信息量不够；要写成"查询指定日期的事件" |
| **小模型对质量更敏感** | qwen2.5:3b 这类小参数模型对 description 的措辞变化反应明显，是测试边界质量的好靶子 |
| **参数优先做 A/B 测试** | 用工厂函数将变量收拢成一个参数，可以快速对比、排除干扰 |

---

## 一个好的 description 应该包含什么？

```
"查询指定日期的事件"
  ↑ 动词       ↑ 对象     ↑ 限定
```

三要素：

| 要素 | 反例 | 正例 |
|------|------|------|
| **动词**（做什么） | "日历"（名词） | "查询""搜索""计算" |
| **对象**（对什么做） | "信息"（太宽泛） | "事件""表达式""城市人口" |
| **限定**（边界在哪） | 缺少限定 | "指定日期""当前外部" |

---

## 实操自检清单

写完 tool 的 description 后，逐一检查：

1. **每个 description 是否让模型一眼知道"什么场景用它"？**
   - 不要用缩写、单个名词、太泛的词

2. **任意两个 description 拼在一起，语义上有没有模糊地带？**
   - 有就加限定词，直到边界完全互斥

3. **是否包含动词开头？**
   - "搜索...""计算...""查询..."比名词标签更清晰

4. **是否包含输入输出的提示？**
   - 如"返回 JSON 数组""单位：万人"——帮助模型理解返回值格式

5. **小模型实测验证过了吗？**
   - 用工厂函数做 A/B 对比，问模糊问题，看是否选错

---

## 扩展：如果模型仍然选错怎么办？

如果 A/B 测试中好 description 仍然选错：

1. **把 bad description 改得更模糊** — `"日历"` → `"信息"` → `"东西"`，逐步降低信息量，看模型在哪个阈值崩溃
2. **把 good description 加更多细节** — `"查询指定日期的事件"` → `"按日期查询日历事件（会议/约会/节假日），返回事件标题列表"`
3. **交换测试问题** — 用明确的关键词测试，看模型是 description 问题还是参数名/工具名误导
4. **换更大的模型** — 如果 qwen2.5:3b 不行，试 qwen2.5:7b 或 14b，验证是否真的是小模型敏感

---

## 小结

Description 不是写给人看的注释，而是模型判断"该用哪个工具"的核心依据。写得太笼统，多个工具的语义边界就会重叠，小模型尤其容易跑偏。

> 写 tool description 的黄金法则是：**假设模型只看得懂 description，看不懂 tool name**——你写对了吗？
