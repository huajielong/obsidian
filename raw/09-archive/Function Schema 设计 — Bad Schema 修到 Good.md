---
title: Function Schema 设计 — Bad Schema 修到 Good
date: 2026-07-15
tags: [LLM, Tool Calling, Function Calling, Schema Design, Prompt Engineering, Ollama, qwen2.5]
---

# Function Schema 设计 — Bad Schema 修到 Good

## 核心观念

写 schema 的功夫能省下换大 model 的成本。小 model 对 schema 质量比大 model 敏感——相同 bad schema 在 Claude 上可能还能猜对、在 qwen2.5:3b 上几乎必错。

**Production 想用便宜 model？schema 必须写到能上线跑的程度。**

---

## 完整代码

```python
import sys
import json
from openai import OpenAI

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# ============================================================
# Bad Schema（故意写烂）
# ============================================================
BAD_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "convert",
            "description": "Convert a value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "string"},
                    "unit": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"},
                },
                "required": ["city"],
            },
        },
    },
]

# ============================================================
# Good Schema（4 处改进）
# ============================================================
GOOD_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "convert_temperature",
            "description": "当用户要求在不同温度单位（摄氏/华氏）之间转换时使用。传入温度数值及其当前单位，自动转换到另一个单位。",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "待转换的温度数值，如 100、-5、37.5",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度值的当前单位：celsius（摄氏度）或 fahrenheit（华氏度）",
                    },
                },
                "required": ["value", "unit"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市实时天气状况，包括天气描述和温度（摄氏度）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"},
                },
                "required": ["city"],
            },
        },
    },
]


# ============================================================
# 工具实现
# ============================================================

def convert_temperature(args) -> str:
    value = args.get("value", 0)
    unit = args.get("unit", "celsius")
    try:
        value = float(value)
        if unit == "celsius":
            result = value * 9 / 5 + 32
            return f"{value}°C = {result:.1f}°F"
        elif unit == "fahrenheit":
            result = (value - 32) * 5 / 9
            return f"{value}°F = {result:.1f}°C"
        else:
            return json.dumps({
                "error": f"不支持的温度单位: {unit}",
                "category": "fatal",
                "retry_hint": "请使用 celsius 或 fahrenheit",
            })
    except (ValueError, TypeError) as e:
        return json.dumps({"error": f"温度值无效: {e}", "category": "fatal"})


def get_weather(args) -> str:
    city = args.get("city", "")
    data = {"台北": "阴天，22°C", "北京": "晴，30°C", "上海": "小雨，26°C"}
    return json.dumps(data.get(city, f"{city}：未知"))


TOOL_IMPL = {
    "convert": convert_temperature,
    "convert_temperature": convert_temperature,
    "get_weather": get_weather,
}


def run_test(label: str, tools, query: str):
    messages = [{"role": "user", "content": query}]
    resp = client.chat.completions.create(
        model="qwen2.5:3b",
        tools=tools,
        messages=messages,
    )
    msg = resp.choices[0].message
    print(f"\n{'='*60}")
    print(f"{label}: {query}")
    print(f"{'='*60}")

    if msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"  name: {tc.function.name}")
            print(f"  args: {tc.function.arguments}")
            tool_fn = TOOL_IMPL.get(tc.function.name)
            if tool_fn:
                result = tool_fn(json.loads(tc.function.arguments))
                print(f"  结果: {result}")
    else:
        print(f"  直接回答: {msg.content}")
    print()
    return msg


# ============================================================
# 对比测试
# ============================================================

QUERIES = [
    "100华氏度等于多少摄氏度？",
    "把 37 摄氏度转成华氏度",
    "北京天气怎么样？",
]

for q in QUERIES:
    print(f"\n{'#'*60}\n# 问题: {q}\n{'#'*60}")
    run_test("[BAD]", BAD_SCHEMA, q)
    run_test("[GOOD]", GOOD_SCHEMA, q)
```

---

## 实际运行结果对比

### 测试 1："100华氏度等于多少摄氏度？"

```
[BAD Schema]
  name: convert
  args: {"unit":"Fahrenheit","value":"100"}
  结果: ❌ 不支持的温度单位: Fahrenheit

  name: convert               ← 又试了一次，还是错
  args: {"unit":"Celsius","value":"100"}
  结果: ❌ 不支持的温度单位: Celsius


[GOOD Schema]
  name: convert_temperature
  args: {"value":100,"unit":"fahrenheit"}
  结果: ✅ 100.0°F = 37.8°C
```

**问题诊断**：BAD schema 没有 `enum` 约束，LLM 传了大写的 "Fahrenheit" 和 "Celsius"，而且传的 value 是字符串 `"100"`。还因为 name 太笼统、不确定该选哪个工具，所以试了两次。

### 测试 2："把 37 摄氏度转成华氏度"

```
[BAD Schema]
  name: convert
  args: {"unit":"Celsius","value":"37"}
  结果: ❌ 不支持的温度单位: Celsius

[GOOD Schema]
  name: convert_temperature
  args: {"unit":"celsius","value":37}
  结果: ✅ 37.0°C = 98.6°F
```

**问题诊断**：BAD schema 同样的问题——传了首字母大写的 "Celsius"（无 enum 约束），value 是字符串 `"37"`。

### 测试 3："北京天气怎么样？"（对照组）

```
[BAD Schema]
  finish_reason: stop
  直接回答: （空回答）

[GOOD Schema]
  name: get_weather
  args: {"city":"北京"}
  结果: ✅ "晴，30°C"
```

**问题诊断**：BAD schema 中 `get_weather` 的 description 是 `"查询城市天气"`，写得太简略。LLM 看到模型里有 `convert`（"Convert a value."）和 `get_weather`（"查询城市天气"），两个 description 都模糊——结果 LLM 直接放弃调用任何工具。

---

## 4 个关键差异

| | Bad | Good |
|---|-----|------|
| **1. name** | `convert`（笼统） | `convert_temperature`（带领域信息） |
| **2. description** | `"Convert a value."`（像注释） | `"当用户要求温度转换时使用"`（写何时用） |
| **3. type** | `value: string` | `value: number` |
| **4. required + enum** | 无 required, `unit: string` | `required: ["value","unit"]`, `unit: enum[...]` |

### 问题 1：Name 笼统

```
Bad:  "name": "convert"
      → LLM 看到"温度转换"不知道 convert 跟它有啥关系
Good: "name": "convert_temperature"
      → LLM 看到"温度"就匹配上了
```

运行中 BAD schema 的 LLM 甚至对天气问题也失败了——`convert` 太通用，扰乱了整个工具集的选择。

### 问题 2：Description 写得像函数注释

```
Bad:  "description": "Convert a value."
      → LLM："转换什么值？什么时候用？跟问题有什么关系？"

Good: "description": "当用户要求在不同温度单位（摄氏/华氏）之间转换时使用"
      → LLM："这个匹配！用户问的就是温度转换"
```

**把 description 想成路由判断条件**——LLM 看到用户问题，拿 description 逐一比对，第一个命中率最高的就是正确工具。

### 问题 3：Type 全用 string

```
Bad:  "value": {"type": "string"}    → LLM 传 "100"（字符串）
Good: "value": {"type": "number"}    → LLM 传 100（数字）
```

实际结果：BAD schema 传了 `"100"`，而函数内部用 `float()` 转换所以没崩——但如果 value 类型是 string 且带单位"100°F"，`float()` 就会报错。

### 问题 4：没写 Required + 没写 Enum

```
Bad:  没写 required → LLM 可能跳过某些参数
     unit: string（无约束） → LLM 自由发挥，传了 "Fahrenheit" "Celsius"

Good: required: ["value", "unit"] → LLM 知道必须传这两个
     unit: enum["celsius", "fahrenheit"] → 只能传小写标准名
```

实际运行中 BAD schema 传的 `"Fahrenheit"` 和 `"Celsius"` 就是最典型的后果——LLM 按口语习惯首字母大写，而没有 enum 约束就没人阻止它。

---

## 5 条黄金规则

| 规则 | 说明 |
|------|------|
| **1. Name 带领域信息** | `convert` → `convert_temperature` |
| **2. Description 写"何时用"** | 不是写"做什么"，是写"什么场景下 LLM 该选我" |
| **3. Type 用对** | number / boolean / enum / array，不要全 string |
| **4. Required + Enum** | required 防止漏传，enum 防止非法值 |
| **5. Error 回传 dict** | 参考练习 5，不 raise、不 return "failed" |

详细说明见 `resources/schema-design-cheatsheet.md`。

---

## 5 个常见 Anti-Pattern

| # | Anti-Pattern | 坏例子 | 好例子 |
|---|-------------|--------|--------|
| 1 | 所有参数塞到 "data" 对象 | `data: {"type": "string"}` | 展开成独立字段 |
| 2 | 被动语态 | `"The temperature is converted"` | 祈使句 |
| 3 | 参数名缩写 | `"val"`, `"tmp"` | `"value"`, `"temperature"` |
| 4 | Enum 值跟用户说法脱节 | `enum: ["c", "f"]` | `enum: ["celsius", "fahrenheit"]` |
| 5 | 不写 required | 自由发挥 | `required: ["value", "unit"]` |

---

## 小模型 vs 大模型

相同 bad schema，不同模型的表现：

| 模型 | 结果 |
|------|------|
| **qwen2.5:3b** | ❌ 温度转换全部失败（大小写问题） + 天气查询也不调用工具 |
| **qwen2.5:14b** | 🟡 可能好一些，但仍然受 enum 缺失影响 |
| **Claude Haiku** | 🟡 可能传正确的单位名（大小写碰运气） |
| **GPT-4** | ✅ 基本能猜对大小写和类型 |

> **Bad schema 在很多大模型上被"猜对"了，这掩盖了 schema 设计问题。如果 production 打算用小模型节省成本，schema 质量就是必须补的欠债。**

---

## 小结

```python
# Bad — qwen2.5:3b 全部失败
{"name": "convert",
 "description": "Convert a value.",
 "parameters": {"value": {"type": "string"}, "unit": {"type": "string"}}}

# Good — 三个测试全部正确
{"name": "convert_temperature",
 "description": "当用户要求温度转换时使用",
 "parameters": {
     "value": {"type": "number"},
     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}},
 "required": ["value", "unit"]}
```

**实际运行结果速览：**

| 问题 | BAD Schema | GOOD Schema |
|------|-----------|-------------|
| 100°F → °C | ❌ `convert("Fahrenheit")` 失败两次 | ✅ `convert_temperature(fahrenheit)` → 37.8°C |
| 37°C → °F | ❌ `convert("Celsius")` 失败 | ✅ `convert_temperature(celsius)` → 98.6°F |
| 北京天气 | ❌ 空回答，未调用任何工具 | ✅ `get_weather("北京")` → 晴，30°C |

> **写 schema 的功夫能省下换大 model 的成本——这是最便宜的"模型升级"。**
