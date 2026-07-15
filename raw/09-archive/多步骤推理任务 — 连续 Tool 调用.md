---
title: 多步骤推理任务 — 连续 Tool 调用
date: 2026-07-15
tags: [LLM, ReAct, Tool Calling, Agent, Ollama, qwen2.5, 推理]
---

# 多步骤推理任务 — 连续 Tool 调用

## 场景

找出台北人口 → 查出纽约人口 → 计算比值 → 转为百分比。

理想情况下，ReAct 循环会按顺序走 5 步：

```
Step 1: Thought → get_population("台北")          → 250
Step 2: Thought → get_population("纽约")          → 833
Step 3: Thought → calculator("250/833")           → 0.3001
Step 4: Thought → convert_to_percentage(0.3001)   → 30.01%
Step 5: Thought → Final Answer
```

---

## 完整代码

```python
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# ===== 三个工具 =====
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_population",
            "description": "查询城市人口数量，单位万人（如台北250万）。",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名称，支持中文和英文"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持 +、-、*、/、括号和小数。",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string", "description": "如 '250/833'"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_to_percentage",
            "description": "将小数转换为百分比字符串。输入 0-1 之间的小数，返回如 '30.01%' 的格式。",
            "parameters": {
                "type": "object",
                "properties": {"value": {"type": "number", "description": "0~1 之间的小数，如 0.30012"}},
                "required": ["value"],
            },
        },
    },
]


def get_population(args):
    city = args.get("city", "")
    data = {
        "台北": 250, "Taipei": 250, "taibei": 250,
        "纽约": 833, "New York": 833, "new york": 833,
        "东京": 1400, "Tokyo": 1400, "tokyo": 1400,
        "上海": 2500, "Shanghai": 2500, "shanghai": 2500,
    }
    return str(data.get(city, "未知"))


def calculator(args):
    expr = args.get("expression", "")
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"计算错误: {e}"


def convert_to_percentage(args):
    value = args.get("value", 0)
    try:
        value = float(value)
        return f"{value * 100:.2f}%"
    except Exception as e:
        return f"转换错误: {e}"


TOOL_IMPL = {
    "get_population": get_population,
    "calculator": calculator,
    "convert_to_percentage": convert_to_percentage,
}


# ===== ReAct 主循环 =====

messages = [
    {
        "role": "system",
        "content": (
            "你是一个数据分析助手。请严格按 ReAct 模式工作：\n"
            "1. 先调用工具获取所有必要数据\n"
            "2. 获取数据后进行计算\n"
            "3. 计算完成后进行格式转换\n"
            "4. 最后给出完整答案"
        ),
    },
    {"role": "user", "content": "找出台北人口，除以纽约人口，再把比例换成百分比。"},
]

for step in range(6):
    response = client.chat.completions.create(
        model="qwen2.5:3b",
        tools=TOOLS,
        messages=messages,
    )
    msg = response.choices[0].message

    print("\n" + "=" * 60)
    print(f"Step {step + 1}")
    print("=" * 60)
    print(f"Thought: {msg.content or '(无文本推理)'}")

    if msg.tool_calls:
        print("Action:")
        for tc in msg.tool_calls:
            print(f"    Tool: {tc.function.name}")
            print(f"    Args: {tc.function.arguments}")

    messages.append({
        "role": "assistant",
        "content": msg.content,
        "tool_calls": msg.tool_calls,
    })

    if not msg.tool_calls:
        print(f"\nFinal Answer: {msg.content}")
        break

    print("Observation:")
    for tc in msg.tool_calls:
        tool_name = tc.function.name
        try:
            tool_args = json.loads(tc.function.arguments)
        except json.JSONDecodeError:
            tool_args = {}
        obs = TOOL_IMPL.get(tool_name, lambda _: f"未知工具: {tool_name}")(tool_args)
        print(f"    Tool: {tool_name}")
        print(f"    Args: {tool_args}")
        print(f"    Result: {obs}")

        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": str(obs),
        })
else:
    print("终止：超过最大步数")
```

---

## 理想运行示例

```
============================================================
Step 1
============================================================
Thought: 我需要先查询两个城市的人口数据。
Action:
    Tool: get_population
    Args: {"city": "台北"}
Observation:
    Tool: get_population
    Args: {"city": "台北"}
    Result: 250

============================================================
Step 2
============================================================
Thought: 台北人口250万，现在查询纽约。
Action:
    Tool: get_population
    Args: {"city": "纽约"}
Observation:
    Tool: get_population
    Args: {"city": "纽约"}
    Result: 833

============================================================
Step 3
============================================================
Thought: 两个城市人口都查到了，现在计算比值 250/833。
Action:
    Tool: calculator
    Args: {"expression": "250/833"}
Observation:
    Tool: calculator
    Args: {"expression": "250/833"}
    Result: 0.3001200480192077

============================================================
Step 4
============================================================
Thought: 得到了0.3001，现在转为百分比。
Action:
    Tool: convert_to_percentage
    Args: {"value": 0.3001200480192077}
Observation:
    Tool: convert_to_percentage
    Args: {"value": 0.3001200480192077}
    Result: 30.01%

============================================================
Step 5
============================================================
Thought: 所有计算完成，可以给出最终答案。

Final Answer: 台北人口为250万人，纽约人口为833万人。
台北人口 ÷ 纽约人口 = 250/833 ≈ 0.3001，换算为百分比约为 30.01%。
```

---

## 小模型的局限性

> ⚠️ **重要实况**：qwen2.5:3b 等小模型在实际运行中**可能不会按顺序执行**。

### 实际运行时可能发生的"跳跃"现象

```
============================================================
Step 1
============================================================
Thought: 我需要先查台北和纽约的人口，然后计算比值，再转百分比。
Action:
    Tool: get_population          ← ✅ 正确查台北
    Args: {"city": "台北"}
    Tool: get_population          ← ✅ 正确查纽约
    Args: {"city": "纽约"}
    Tool: convert_to_percentage   ← ❌ 还没算呢！模型猜了个值
    Args: {"value": 0.3}
```

### 为什么会出现这个问题？

| 原因 | 说明 |
|------|------|
| **并行调用** | OpenAI 协议支持一次返回多个 `tool_calls`，小模型倾向于"一股脑全预测出来" |
| **缺乏规划约束** | 没有明确的依赖链提示，模型不知道"必须等 calculator 结果才能转格式" |
| **小模型容量有限** | qwen2.5:3b 在复杂多步骤规划上不如 7b/14b 或 GPT/Claude |

### 影响

如果 `convert_to_percentage(0.3)` 在 `calculator("250/833")` 之前被调用：

```
Result: 30.00%    ← ❌ 基于猜测值 0.3，不是真实计算结果 0.30012
```

后续 `calculator` 虽然会返回正确结果，但模型**不会重新调用** `convert_to_percentage`，导致最终答案里的百分比是错的。

### 解决方案

| 方案 | 适用场景 |
|------|---------|
| **加大模型**（7b/14b） | 一次性解决方案，大模型规划更准确 |
| **System Prompt 强调顺序** | 无成本改进，如"未计算前不得调用 convert_to_percentage" |
| **调整 description 增加依赖暗示** | 巧妙方案，如给 convert_to_percentage 加一句"接收计算结果作为输入" |
| **代码层拦截** | 检测到 convert_to_percentage 的输入不是来自 calculator 时，拒绝执行 |

---

## 推理链的依赖关系

### 理想 vs 实际的执行路径

```
理想路径（顺序执行）：
    查台北 → 查纽约 → 计算比值 → 转百分比 → 答案

实际可能路径（小模型并行推测）：
    查台北 ──────────→ 转百分比(0.3)   ← ❌ 超前执行
    查纽约 ──→ 计算 ──→ (百分比已做过，不再重做)
                      ↓
                    答案中百分比错误
```

### 三种工具的调用时序约束

| 工具 | 前置依赖 | 能否并行 |
|------|---------|---------|
| `get_population("台北")` | 无 | ✅ 可与其他 `get_population` 并行 |
| `get_population("纽约")` | 无 | ✅ 可与其他 `get_population` 并行 |
| `calculator("250/833")` | **两个人口值** | ❌ 必须等人口数据 |
| `convert_to_percentage(0.3001)` | **计算器结果** | ❌ 必须等 calculator |

并行安全的工具：`get_population` 之间
串行必须的工具：`calculator` 和 `convert_to_percentage`

---

## 与现实场景的联系

多步骤推理是小模型 Agent 落地的关键瓶颈：

| 场景 | 对推理链的依赖 | 小模型风险 |
|------|---------------|-----------|
| **数据分析** | 查数据 → 清洗 → 计算 → 绘图 | 中间步骤顺序错乱 |
| **自动客服** | 查用户 → 查订单 → 查物流 → 生成回复 | 调错工具导致答非所问 |
| **代码生成** | 理解需求 → 查 API → 写代码 → 测试 | 顺序依赖断裂 |

**核心经验：小模型做多步骤推理，一定要在代码层面做依赖校验，不能全指望模型自己规划。**

---

## 小结

练习 4 展示了多步骤推理任务的核心模式——**数据依赖链**——同时也暴露了小模型在这个场景下的典型局限。

| 层面 | 要点 |
|------|------|
| **设计意图** | 连续 5 步、3 个不同工具、串行依赖 |
| **理想情况** | 模型按顺序执行，每一步依赖上一步的输出 |
| **实际情况（小模型）** | 可能并行预测所有步骤，导致中间值被跳过 |
| **教训** | 代码层需要做依赖校验，不能全信模型规划 |

> **让大模型做规划，让小模型做执行——但就算是小模型执行，也要有护栏。**
