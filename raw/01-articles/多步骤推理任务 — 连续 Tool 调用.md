---
title: 多步骤推理任务 — 连续 Tool 调用
date: 2026-07-14
tags: [LLM, ReAct, Tool Calling, Agent, Ollama, qwen2.5, 推理]
---

# 多步骤推理任务 — 连续 Tool 调用

## 场景

三个工具，四步调用，用 ReAct 循环串成一条推理链：

```
get_population("台北")  →  get_population("纽约")
        ↓                       ↓
      250 万                 833 万
        ↓                       ↓
           calculator("250/833")
                 ↓
            0.30012
                 ↓
    convert_to_percentage(0.30012)
                 ↓
             30.01%
```

**问题**：*"找出台北人口，除以纽约人口，再把比例换成百分比。"*

这四个调用分属 **三个不同的工具**，模型需要自己规划"先查什么 → 再算什么 → 最后转格式"的执行顺序。

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
            "description": "查询城市人口数量，单位万人（如台北250万）。支持中文/英文城市名。",
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
            "description": "将小数转换为百分比字符串。输入 0-1 之间的小数，返回如「30.01%」的格式。",
            "parameters": {
                "type": "object",
                "properties": {"value": {"type": "number", "description": "0~1 之间的小数"}},
                "required": ["value"],
            },
        },
    },
]


def get_population(args):
    city = args.get("city", "")
    data = {
        "台北": 250, "Taipei": 250,
        "纽约": 833, "New York": 833,
        "东京": 1400, "Tokyo": 1400,
        "上海": 2500, "Shanghai": 2500,
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
        return f"{value * 100:.2f}%"
    except Exception as e:
        return f"转换错误: {e}"


TOOL_IMPL = {
    "get_population": get_population,
    "calculator": calculator,
    "convert_to_percentage": convert_to_percentage,
}


# ===== ReAct 循环 =====

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

    print(f"\n{'='*50}")
    print(f"Step {step+1}")
    print(f"{'='*50}")
    print(f"💭 Thought: {msg.content or '(无文本推理)'}")

    messages.append({
        "role": "assistant",
        "content": msg.content,
        "tool_calls": msg.tool_calls,
    })

    if not msg.tool_calls:
        print(f"\n✅ 最终答案：{msg.content}")
        break

    for tc in msg.tool_calls:
        tool_name = tc.function.name
        try:
            tool_args = json.loads(tc.function.arguments)
        except json.JSONDecodeError:
            tool_args = {}
        obs = TOOL_IMPL.get(tool_name, lambda _: f"未知工具: {tool_name}")(tool_args)
        print(f"  🛠️  {tool_name}({tool_args})")
        print(f"  👁️  → {obs}")

        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": str(obs),
        })
else:
    print("⏹️ 终止：超过最大步数")
```

---

## 运行示例

```
==================================================
Step 1
==================================================
💭 Thought: 我需要先查询台北和纽约的人口数据。
  🛠️  get_population({'city': '台北'})
  👁️  → 250
  🛠️  get_population({'city': '纽约'})
  👁️  → 833

==================================================
Step 2
==================================================
💭 Thought: 台北250万，纽约833万，现在计算250/833。
  🛠️  calculator({'expression': '250/833'})
  👁️  → 0.3001200480192077

==================================================
Step 3
==================================================
💭 Thought: 得到了0.3001，用 convert_to_percentage 转成百分比。
  🛠️  convert_to_percentage({'value': 0.3001200480192077})
  👁️  → 30.01%

==================================================
Step 4
==================================================
💭 Thought: 所有计算完成，可以回答用户了。

✅ 最终答案：台北人口为250万人，纽约人口为833万人。
台北人口 ÷ 纽约人口 = 250/833 ≈ 0.3001，换算成百分比约为 **30.01%**。
```

---

## 推理链拆解

### 四步推理流水线

| 轮次 | 模型思考（Thought） | 行动（Action） | 观察（Observation） |
|------|-------------------|---------------|-------------------|
| 1 | 需要查两个城市的人口 | `get_population("台北")` → `get_population("纽约")` | 250, 833 |
| 2 | 数据有了，计算比值 | `calculator("250/833")` | 0.30012 |
| 3 | 得到小数，转百分比 | `convert_to_percentage(0.30012)` | 30.01% |
| 4 | 全部完成，给出答案 | （无 tool_calls） | ✅ 终止 |

### 每一步的依赖关系

```
           Step 1                  Step 2              Step 3              Step 4
    ┌─────────────────┐     ┌────────────────┐    ┌──────────────┐     ┌─────────────┐
    │ get_population   │     │   calculator    │    │convert_to_   │     │  Answer      │
    │ ("台北")         │──┬─→│ ("250/833")     │───→│ percentage   │───→│              │
    │ → 250           │  │  │ → 0.30012      │    │ (0.30012)    │    │ "30.01%"     │
    │                 │  │  └────────────────┘    │ → "30.01%"   │     └─────────────┘
    │ get_population   │  │                        └──────────────┘
    │ ("纽约")         │──┘
    │ → 833           │
    └─────────────────┘
```

每个后续步骤都**依赖**前一步的输出值作为输入，这是多步骤推理区别于单步调用的关键。

---

## 什么是多步骤推理？

对比之前的练习：

| 练习 | 场景 | 调用次数 | 关键特征 |
|------|------|---------|---------|
| 练习 1 | 单工具、单次调用 | 1 次 | 测试模型能否识别需要调用工具 |
| 练习 2 | 三工具、边界互斥 | 1 次 | 测试 description 质量对路由的影响 |
| 练习 3 | ReAct 循环框架 | 2-3 次 | 用原生 tool calling 驱动循环 |
| **练习 4** | **多步骤推理链** | **3-5 次** | **后一步依赖前一步的输出** |

多步骤推理的独特挑战在于：

1. **任务规划** — 模型需要先想清楚整体步骤，再逐步执行
2. **依赖管理** — 第 N 步的输出是第 N+1 步的输入
3. **上下文跟踪** — 模型必须在对话历史中记住中间结果
4. **错误传播** — 任何一步出错，后面的结果全部偏离

---

## 核心设计要点

### 1. 多工具 vs 单一工具

与练习 3 相比，练习 4 把 `calculator` 拆成了两个功能：
- `calculator`：纯计算
- `convert_to_percentage`：格式转换

这样强制模型在"计算"和"格式化"之间显式切换，增加推理链长度。

### 2. 三个工具的 description 互斥检查

| 工具 | description | 边界风险 |
|------|-----------|---------|
| `get_population` | "查询城市人口数量" | 只跟"查"相关，不涉及计算或格式 |
| `calculator` | "计算数学表达式" | 只跟"算"相关，不涉及查数据或格式化 |
| `convert_to_percentage` | "将小数转换为百分比" | 只跟"转格式"相关，不涉及查或算 |

三个 description 各司其职，语义边界完全互斥。

### 3. 与练习 1 的不同

练习 1 是"调了工具就直接结束"，练习 4 是"调了工具 -> 拿到结果 -> 再调下一个工具 -> 再拿结果 -> ..."，本质区别在于 **调用之间有数据依赖**。

---

## 扩展思路

### 复杂数据流

```
get_population("台北") → 250  ─┐
                                ├─→ calculator("250/833") → 0.3001 → convert(0.3001) → "30.01%"
get_population("纽约") → 833  ─┘
```

也可以扩展为：
```
get_population("台北") → 250
get_population("东京") → 1400
calculator("1400/250") → 5.6
format("东京是台北的5.6倍")
```

### 更多步骤的推理链

变一：**三步变五步**
```
get_population(A) → get_population(B) → calculator(A/B) → convert() → 输出表格
```

变二：**跨领域数据**
```
search("台北 2024 GDP") → search("纽约 2024 GDP") → calculator(GDP_A/GDP_B) → format()
```

变三：**有条件的推理**
```
get_population("台北") → 如果 > 300 → call tool A；否则 → call tool B
```

---

## 与现实 Agent 的关系

多步骤推理是现实 Agent 的核心能力。举几个例子：

| 现实 Agent | 推理链 |
|-----------|--------|
| **客服 Agent** | 查询用户信息 → 查订单 → 查物流 → 计算退款金额 → 生成回复 |
| **数据分析 Agent** | 查数据库 → 运行统计 → 生成图表 → 写结论 |
| **代码 Agent** | 搜索 API 文档 → 写代码 → 运行测试 → 读报错 → 修复 |

所有这些场景都可以抽象为：**工具1 → 工具2 → 工具3 → ... → 答案**，与练习 4 的模式完全一致。

---

## 小结

多步骤推理是将简单工具组合成复杂能力的桥梁。核心模式：

- ReAct 循环驱动每一步
- 工具间形成**数据依赖链**
- 模型的 `Thought` 负责规划路由
- 对话历史中的 `Observation` 是数据传递的介质

> **单个工具是手脚，多个工具的推理链才是大脑。**
