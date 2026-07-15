---
title: 从零实现 ReAct 循环
date: 2026-07-14
tags: [LLM, ReAct, Tool Calling, Agent, Ollama, qwen2.5, OpenAI]
---

# 从零实现 ReAct 循环

## 什么是 ReAct？

**ReAct** = **Rea**soning + **Act**ing，由 Shunyu Yao 等人在 2022 年提出（[*ReAct: Synergizing Reasoning and Acting in Language Models*](https://arxiv.org/abs/2210.03629)）。

这是 LLM Agent 最经典的架构模式——让模型在循环中交替进行：

```
Thought（思考）→ Action（行动）→ Observation（观察）→ 循环 → Answer（答案）
```

| 阶段 | 做什么 | 谁在做 |
|------|--------|--------|
| **Thought** | 分析当前状态，决定下一步 | LLM |
| **Action** | 调用工具获取外部信息 | LLM 选择 → 系统执行 |
| **Observation** | 将工具结果反馈给模型 | 系统 |
| **循环** | 信息不足就再来一轮 | 共同完成 |
| **Answer** | 足够信息时给出最终答案 | LLM |

---

## 完整代码

```python
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


# ===== 工具定义 =====

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持 +、-、*、/ 和括号。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '250 / 833'"
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_population",
            "description": "查询城市人口（单位：万人）。例如：台北返回250表示250万人。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，支持中文（台北）或英文（Taipei）"
                    }
                },
                "required": ["city"],
            },
        },
    },
]


def calculator(args):
    expression = args.get("expression", "")
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"


def get_population(args):
    city = args.get("city", "")
    data = {
        "台北": 250, "Taipei": 250, "taibei": 250,
        "纽约": 833, "New York": 833, "new york": 833,
        "东京": 1400, "Tokyo": 1400, "tokyo": 1400,
    }
    return data.get(city, "未知")


TOOL_IMPL = {
    "calculator": calculator,
    "get_population": get_population,
}


# ===== ReAct 主循环 =====

messages = [
    {
        "role": "system",
        "content": (
            "你是一个工具调用专家。请按照 ReAct 模式思考："
            "先调用工具获取所有所需信息，获取结果后再进行计算或总结。"
            "确保在回答前获取所有必要的数据。"
        ),
    },
    {"role": "user", "content": "台北人口除以纽约人口？"},
]

for step in range(5):
    response = client.chat.completions.create(
        model="qwen2.5:3b",
        tools=TOOLS,
        messages=messages,
    )
    msg = response.choices[0].message

    print(f"\n{'='*40}\nStep {step+1}")
    print(f"💭 Thought: {msg.content or '(无文本推理)'}")

    messages.append({
        "role": "assistant",
        "content": msg.content,
        "tool_calls": msg.tool_calls,
    })

    if not msg.tool_calls:
        print(f"\n✅ 最终答案：{msg.content}")
        break

    for tool_call in msg.tool_calls:
        tool_name = tool_call.function.name
        tool_args = {}

        try:
            tool_args = json.loads(tool_call.function.arguments)
            observation = TOOL_IMPL[tool_name](tool_args)
        except json.JSONDecodeError:
            observation = f"❌ 参数解析失败: {tool_call.function.arguments}"
        except KeyError:
            observation = f"❌ 未知工具: {tool_name}"
        except Exception as e:
            observation = f"❌ 工具执行错误: {str(e)}"

        print(f">>> Action: {tool_name}({tool_args}) → 👁️ Observation: {observation}")

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(observation),
        })

else:
    print("\n⏹️ 终止：超过最大步数")
```

---

## 运行示例

```
========================================
Step 1
💭 Thought: 我需要先查询台北和纽约的人口数据，然后才能进行计算。
>>> Action: get_population({'city': '台北'}) → 👁️ Observation: 250
>>> Action: get_population({'city': '纽约'}) → 👁️ Observation: 833

========================================
Step 2
💭 Thought: 台北人口250万，纽约人口833万，现在计算250/833。
>>> Action: calculator({'expression': '250/833'}) → 👁️ Observation: 0.3001200480192077

========================================
Step 3
💭 Thought: 计算结果约为0.30，可以回答了。
✅ 最终答案：台北人口除以纽约人口约为 0.30（即约30.0%）。
```

整个过程跨了 **3 轮对话**：

| 轮次 | Thought | Action | Observation |
|------|---------|--------|-------------|
| 1 | 需要查两个城市人口 | `get_population(台北)` + `get_population(纽约)` | 250, 833 |
| 2 | 数据到手，计算除法 | `calculator(250/833)` | 0.3001… |
| 3 | 拿到结果，输出答案 | （无 tool_calls） | ✅ 终止 |

---

## 代码详解

### 1. 工具定义（TOOLS）

每个工具用 OpenAI 兼容的 Function Calling schema 描述：

```python
{
    "type": "function",
    "function": {
        "name": "get_population",      # 工具名称（LLM 按这个选）
        "description": "查询城市人口",  # 关键字段！LLM 靠它判断"该不该用这个工具"
        "parameters": { ... },         # 参数结构
    },
}
```

> **注意**：`description` 写得越清楚，LLM 选得越准——尤其是多个工具时，边界要互斥。

### 2. 工具实现（TOOL_IMPL）

```python
TOOL_IMPL = {
    "calculator": calculator,        # name → callable 的映射
    "get_population": get_population,
}
```

工具函数接收 `args`（已解析好的字典），返回字符串或可转字符串的值。

### 3. ReAct 循环

循环体分为三个子阶段：

**阶段 1：LLM 思考**
```python
response = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=TOOLS,
    messages=messages,
)
msg = response.choices[0].message
```
传入完整对话历史和工具列表，LLM 决定是调用工具还是直接回答。

**阶段 2：执行工具**
```python
for tool_call in msg.tool_calls:
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    observation = TOOL_IMPL[tool_name](tool_args)
```
遍历所有 `tool_calls`（支持并行），解析参数、执行函数。

**阶段 3：反馈 Observation**
```python
messages.append({
    "role": "assistant",
    "content": msg.content,          # 保留 Thought
    "tool_calls": msg.tool_calls,    # 保留 Action 选择
})
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,    # 关联到对应的 tool_call
    "content": str(observation),     # 结果文本
})
```

两个 append 缺一不可：
- `role: "assistant"` — 让模型看到自己上一轮的推理
- `role: "tool"` — 让模型看到工具执行结果

---

## 为什么老代码看似单步也能走？

你可能会想："如果我一步就把两个城市人口都查到再算，不就一轮解决了吗？"

答案在 **TOOLS schema 的 `description`** 里。如果工具描述写得足够清晰，LLM 可以在单次调用中同时查多个 city（一次返回多个 `tool_calls`）。但这依赖于：

- 工具本身的语义是否允许多次调用
- 模型的容量和上下文长度
- description 是否暗示了"可以一次查多个"

本练习中 LLM 选了分步走（先查两个城市 → 再算），这是它自己的策略选择——ReAct 允许模型自由决定何时调用、调用几次。

---

## 两种实践路径的对比

练习 3 经历了两次迭代，对比一下：

| 对比维度 | 文本协议版 | 原生 Tool Calling 版（最终方案） |
|----------|-----------|-------------------------------|
| **工具选择** | LLM 输出 `Action: 工具名: 参数` 文本行 | LLM 返回结构化 `tool_calls` |
| **Observation 格式** | 拼成 `"Observation: ..."` 纯文本 | `role: "tool"` + `tool_call_id` |
| **解析方式** | 手写字符串 `startswith` / `split` | 框架自动解析 `tool_calls` |
| **多工具并行** | 需自己从文本里分拆 | 原生支持，一次返回多个 |
| **可靠性** | 小模型容易格式出偏差（`Action:` 少空格等） | 协议级保证，格式稳定 |
| **依赖** | 仅 OpenAI SDK | 仅 OpenAI SDK |
| **代码量** | ~55 行（含解析逻辑） | ~50 行（更精简） |

文本解析版（旧）的 Action 行：
```
Action: calculator: 250/833
```
需要手写：
```python
for line in output.split("\n"):
    if line.startswith("Action:"):
        _, rest = line.split("Action:", 1)
        name, _, input = rest.partition(":")
```

原生版（新）直接：
```python
for tc in msg.tool_calls:
    name = tc.function.name
    args = json.loads(tc.function.arguments)
```

**推荐原生方式**——格式稳定、支持并行、代码更少。

---

## 核心要点总结

### 三条规则

1. **LLM 输出必须追回 messages** — `role: "assistant"` 保留 `content` + `tool_calls`
2. **工具结果必须追回 messages** — `role: "tool"` + 匹配的 `tool_call_id`
3. **没有 tool_calls 就是终止** — LLM 不再调用工具时，`msg.content` 即最终答案

### 一张流程图

```
┌──────────────────────────────────────────┐
│          User Query                       │
│  "台北人口除以纽约人口？"                    │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│        LLM 思考 (Thought)                 │
│  "需要查两个城市的人口"                     │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│        Action: get_population            │
│        台北 → 250, 纽约 → 833             │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│      Observation 反馈给 LLM               │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│        LLM 思考 (Thought)                 │
│  "已获取数据，计算 250/833"               │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│        Action: calculator                │
│        250/833 → 0.3001                   │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│        LLM 思考 (Thought)                 │
│  "数据足够，可以回答"                      │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│        Answer (无 tool_calls)            │
│  "约 0.30（即 30%）"                      │
└──────────────────────────────────────────┘
```

### 与 Framework 方案的比较

| 维度 | 本实现 | LangChain / LangGraph |
|------|--------|----------------------|
| **代码量** | ~50 行 | 依赖安装 + 大量样板 |
| **可读性** | 看一遍就懂 | 多层抽象 |
| **灵活性** | 随意改 | 受框架约束 |
| **错误处理** | 手写 | 内置重试 |
| **生产就绪** | 否（教学用途） | 是（流式、追踪） |

---

## 扩展思路

基于这个基础框架，可以进一步添加：

1. **更多工具** — 搜索、数据库查询、文件读写
2. **记忆持久化** — 把 `messages` 存到磁盘或向量数据库
3. **Flow Engineering** — 让 LLM 先生成计划再执行（Plan-then-Execute）
4. **多模型切换** — 小模型做路由、大模型做推理
5. **流式输出** — 实时显示 Thought 过程

---

## 小结

ReAct 的核心就是一个 `for` 循环 + 原生 `tools` 参数，没有任何神秘之处。理解了它，LangChain 等框架的 Agent 对你来说就不再是黑盒了。

> 与其学框架的抽象层，不如先手写 50 行理解本质。
