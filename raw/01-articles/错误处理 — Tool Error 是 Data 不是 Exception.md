---
title: 错误处理 — Tool Error 是 Data 不是 Exception
date: 2026-07-15
tags: [LLM, ReAct, Tool Calling, Agent, Error Handling, Ollama, qwen2.5]
---

# 错误处理 — Tool Error 是 Data 不是 Exception

## 核心观念翻转

```python
# ❌ Bad：raise 中断 loop，LLM 没机会 recover
def fetch_weather(city):
    if network_failed():
        raise Exception("network timeout")

# ✅ Good：return dict，LLM 看到结构化错误后自己决定怎么办
def fetch_weather(city):
    if network_failed():
        return {"error": "network timeout",
                "category": "transient",
                "retry_hint": "try again in 1s"}
```

| 维度 | ❌ Bad（raise / 字符串） | ✅ Good（结构化 dict） |
|------|------------------------|----------------------|
| **发生错误时** | 中断循环 | 返回数据给 LLM |
| **谁决定重试** | Python 层（try/except） | **LLM 层**（看到 retry_hint 后自主决策） |
| **recover 机会** | 无，直接 crash | 有，LLM 可以重试/改 query/放弃 |
| **信息量** | "failed"（看不明白） | `category` + `retry_hint`（LLM 可理解） |
| **小模型友好** | ❌ | ✅ 结构化文本比"failed"好得多 |

> **Production 的 retry 不在 Python 层、而在 LLM 层——这是 Stage 3 练习 5 的 mental flip。**

---

## 完整代码

```python
import json
import random
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# ===== 模拟一个"会失败"的天气工具 =====

REQUEST_COUNT = 0


def fetch_weather(args: dict) -> dict:
    """模拟网络不稳定的天气 API。

    返回 dict 而非直接返回字符串 / 抛异常——
    这是本练习的核心设计理念：error 也是 data。
    """
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    city = args.get("city", "未知")
    roll = random.random()

    # 40% 概率成功
    if roll < 0.4:
        return {
            "city": city,
            "forecast": "rain" if random.random() > 0.5 else "sunny",
            "temperature_c": random.randint(18, 35),
            "status": "ok",
        }

    # 40% 概率 transient（可重试）错误
    if roll < 0.8:
        return {
            "error": "网络连接超时，无法连接到天气服务",
            "category": "transient",
            "retry_hint": "稍后重试，可等待 1-2 秒",
            "status": "error",
        }

    # 20% 概率 fatal（不可重试）错误
    return {
        "error": f"城市 '{city}' 不在服务覆盖范围内",
        "category": "fatal",
        "retry_hint": "请检查城市名称是否正确，或尝试其他城市",
        "status": "error",
    }


def calculator(args: dict) -> str:
    """计算器（辅助工具，不会报错）"""
    expr = args.get("expression", "")
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return json.dumps({"error": f"表达式无效: {e}", "category": "fatal"},
                          ensure_ascii=False)


# ===== 工具 schema =====

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_weather",
            "description": "查询城市实时天气。注意：该服务可能因网络问题暂时不可用，此时可以稍后重试。",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名称"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持 +、-、*、/、括号。",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
]

TOOL_IMPL = {
    "fetch_weather": fetch_weather,
    "calculator": calculator,
}


# ===== ReAct 循环 =====

messages = [
    {
        "role": "system",
        "content": (
            "你是一个智能助手，可以调用工具获取信息。\n"
            "工具调用可能返回错误，请根据错误信息判断：\n"
            "  - 如果错误是 transient（暂时性），可以稍后重试\n"
            "  - 如果错误是 fatal（致命性），不要重试，告诉用户原因\n"
            "  - 如果返回了 retry_hint，请参考提示决定下一步"
        ),
    },
    {"role": "user", "content": "台北今天天气如何？如果查不到，告诉我原因。"},
]

RETRY_LIMIT = 3
retry_counts: dict[str, int] = {}

for step in range(8):
    response = client.chat.completions.create(
        model="qwen2.5:3b",
        tools=TOOLS,
        messages=messages,
    )
    msg = response.choices[0].message

    print(f"\n{'='*60}")
    print(f"Step {step + 1}")
    print(f"{'='*60}")
    print(f"💭 Thought: {msg.content or '(无文本推理)'}")

    if msg.tool_calls:
        print("Action:")
        for tc in msg.tool_calls:
            print(f"    Tool: {tc.function.name}")
            print(f"    Args: {tc.function.arguments}")
    else:
        print(f"\n✅ Final Answer: {msg.content}")
        break

    messages.append({
        "role": "assistant",
        "content": msg.content,
        "tool_calls": msg.tool_calls,
    })

    for tc in msg.tool_calls:
        tool_name = tc.function.name
        try:
            tool_args = json.loads(tc.function.arguments)
        except json.JSONDecodeError:
            tool_args = {}

        # 业务层 retry 配额检查
        retry_counts[tool_name] = retry_counts.get(tool_name, 0) + 1
        if retry_counts[tool_name] > RETRY_LIMIT:
            obs = json.dumps({
                "error": f"工具 {tool_name} 已重试 {RETRY_LIMIT} 次仍失败",
                "category": "fatal",
                "retry_hint": "请放弃使用此工具",
            }, ensure_ascii=False)
        else:
            obs_raw = TOOL_IMPL[tool_name](tool_args)
            # ⭐ 核心：error dict 也是 string 化接回 LLM
            obs = json.dumps(obs_raw, ensure_ascii=False) if isinstance(obs_raw, dict) else str(obs_raw)

        print(f"    Result: {obs}")
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": obs,
        })
else:
    print("⏹️ 终止：超过全局最大步数 (8)")
```

---

## 运行示例

### 场景 A：首次失败 → LLM 自动重试 → 成功

```
============================================================
Step 1
============================================================
💭 Thought: 我需要查询台北的天气。
Action:
    Tool: fetch_weather    Args: {"city": "台北"}
Result: {"error": "网络连接超时，无法连接到天气服务",
         "category": "transient",
         "retry_hint": "稍后重试，可等待 1-2 秒",
         "status": "error"}

============================================================
Step 2
============================================================
💭 Thought: 网络超时了，错误是 transient，我可以再试一次。
Action:
    Tool: fetch_weather    Args: {"city": "台北"}
Result: {"city": "台北", "forecast": "rain",
         "temperature_c": 24, "status": "ok"}

============================================================
Step 3
============================================================
💭 Thought: 成功获取到天气数据，台北现在是雨天 24°C。

✅ Final Answer: 台北今天下雨，气温 24°C，记得带伞。
```

### 场景 B：连续 3 次 transient 后强制终止

```
============================================================
Step 1~3
============================================================
（连续 3 次 fetch_weather 都返回 transient error）
LLM 每次看到 error 都决定重试

Step 4
============================================================
💭 Thought: 我再试一次。
Action:
    Tool: fetch_weather    Args: {"city": "台北"}
Result: ⛔ 超过 retry 上限 (3次)，强制终止
    → {"error": "工具 fetch_weather 已重试 3 次仍失败",
       "category": "fatal",
       "retry_hint": "请放弃使用此工具，尝试其他方法"}

============================================================
Step 5
============================================================
💭 Thought: 这个工具已经重试多次仍然失败，错误变成 fatal 了，
            我告诉用户查不到天气的原因。

✅ Final Answer: 抱歉，天气服务目前不稳定，重试 3 次后仍无法获取
                 台北天气数据，请稍后再试。
```

### 场景 C：fatal error 不重试

```
============================================================
Step 1
============================================================
💭 Thought: 我需要查询台北的天气。
Action:
    Tool: fetch_weather    Args: {"city": "台北"}
Result: {"error": "城市 '台北' 不在服务覆盖范围内",
         "category": "fatal",
         "retry_hint": "请检查城市名称是否正确"}

============================================================
Step 2
============================================================
💭 Thought: 这是 fatal 错误，重试也没用，我应该告诉用户。

✅ Final Answer: 台北不在当前天气服务的覆盖范围内，无法查询天气。
```

---

## 设计详解

### 错误类型的结构化设计

```python
# ✅ Good：三种错误类型各有明确语义
{
    "status": "ok",            # 成功
    "forecast": "rain",
    "temperature_c": 24,
}

{
    "error": "网络连接超时",     # transient — 可重试
    "category": "transient",
    "retry_hint": "稍后重试",
}

{
    "error": "城市不在覆盖范围",  # fatal — 不要重试
    "category": "fatal",
    "retry_hint": "检查城市名称",
}
```

### 两层 Retry 机制

```
┌──────────────────────────────────────────────┐
│  Layer 1：LLM 层（业务语义层）              │
│  LLM 看到 category + retry_hint →           │
│  自主决定重试 / 改参数 / 放弃                │
├──────────────────────────────────────────────┤
│  Layer 2：Python 层（安全护栏层）            │
│  retry_counts[name] > RETRY_LIMIT →          │
│  强制返回 fatal，LLM 必须终止               │
└──────────────────────────────────────────────┘
```

- **LLM 层**：做"值不值得重试"的判断——机器说是 transient，但已经试了 2 次，LLM 可能选择换城市而不是继续重试
- **Python 层**：做"不能再重试了"的硬拦停——防止无限循环

### 为什么不能 raise？

```python
# ❌ 错误的设计
def fetch_weather(args):
    if network_failed():
        raise ConnectionError("timeout")  # ← 循环崩溃，LLM 根本没看到错误

try:
    obs = fetch_weather(args)            # ← 这里就炸了
except Exception:
    obs = "failed"                       # ← LLM 看到"failed"，不知道怎么处理
```

```python
# ✅ 正确的设计
def fetch_weather(args):
    if network_failed():
        return {"error": "timeout", "category": "transient", "retry_hint": "retry"}

obs = fetch_weather(args)                # ← 永远不 crash
# obs 传给 LLM → LLM 看到结构化 dict → 自己决定下一步
```

### 为什么不能只 return 字符串 "failed"？

小模型看到 `"failed"` 不知道：

- 是什么失败了？（网络？参数？权限？）
- 能不能重试？（transient？fatal？）
- 重试要改什么？（等 1 秒？改城市名？）

结构化 dict 解决了所有问题——字段名本身就是提示词。

---

## 与练习 4 的对比

| 对比维度 | 练习 4（多步骤推理） | 练习 5（错误处理） |
|---------|-------------------|------------------|
| **核心挑战** | 工具间的数据依赖链 | 工具返回错误时的 recovery |
| **工具行为** | 一直正常，永远返回成功 | 可能失败，返回结构化 error dict |
| **模型需要** | 规划能力（先做什么后做什么） | 判断能力（该重试还是放弃） |
| **关键代码** | `obs = fn(args)` | `{"error": ..., "category": ...}` |
| **护栏** | max_steps | max_steps + retry_limit |

---

## 四种错误回传方式的对比

```python
# 1. ❌ raise Exception
raise ConnectionError("timeout")       # ← 循环崩溃，最差方案

# 2. ❌ 无信息字符串
return "failed"                        # ← LLM 看不懂，不知道怎么 recover

# 3. ⚠️ 有信息字符串
return "网络超时，请重试"               # ← LLM 能看懂但无法结构化解析

# 4. ✅ 结构化 dict
return {"error": "网络超时",           # ← LLM 能看懂每个字段
        "category": "transient",       #     可以直接判断是否该重试
        "retry_hint": "稍后重试"}
```

| 方案 | LLM 能否 recover | 信息量 | 可扩展性 | 推荐 |
|------|-----------------|--------|---------|------|
| raise Exception | ❌ 崩溃 | 低 | 低 | ❌ |
| `return "failed"` | ❌ 看不懂 | 极低 | 低 | ❌ |
| `return "网络超时"` | 🟡 可能 | 中 | 低 | ⚠️ |
| `return {...}` | ✅ 完全可理解 | 高 | 高 | ✅ **推荐** |

---

## 工程经验

### 三层错误处理架构

| 层级 | 职责 | 示例 |
|------|------|------|
| **工具层** | 返回结构化 dict，不 raise | `return {"error": "...", "category": "transient"}` |
| **LLM 层** | 看 dict 判断是否重试 | "这是 transient，再试一次" |
| **Python 层** | 兜底护栏 | retry_limit, max_steps |

### 什么时候 LLM 层 vs Python 层管

| 场景 | 谁管 | 判断依据 |
|------|------|---------|
| 同一工具连续失败 | **LLM 层** | 看到 category=transient，自己决定再试 |
| 超过重试配额 | **Python 层** | retry_counts > LIMIT，强制 fatal |
| 用户输入无效 | **LLM 层** | 看到 category=fatal，告诉用户 |
| 全局死循环 | **Python 层** | max_steps 兜底 |
| 是否换参数重试 | **LLM 层** | 根据 retry_hint 改 query |
| 是否彻底放弃 | **LLM 层** | 综合判断后输出 Answer |

---

## 小结

练习 5 的核心就一句话：

> **Tool Error 是 Data 不是 Exception。**

| 旧观念 | 新观念 |
|--------|--------|
| 工具出错了 → raise | 工具出错了 → return dict |
| Python 层 try/except → retry | LLM 层看 category → 决定 retry/放弃 |
| `return "failed"` | `return {"error":"...","category":"transient","retry_hint":"..."}` |
| retry 是基础设施问题 | retry 是业务语义问题 |

**这个 mental flip 是 Agent 工程从"函数调用"走向"LLM 驱动"的关键一步。**
