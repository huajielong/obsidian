---
title: "Tool_Calling"
type: concept
tags: [工具调用, function calling, LLM, Agent, 协议, Schema设计]
sources: [raw/01-articles/LLM工具调用入门实践.md, raw/01-articles/Tool Description 边界互斥实验.md, raw/01-articles/多步骤推理任务 — 连续 Tool 调用.md, raw/01-articles/错误处理 — Tool Error 是 Data 不是 Exception.md, raw/01-articles/Function Schema 设计 — Bad Schema 修到 Good.md]
last_updated: 2026-07-15
---

# Tool Calling（工具调用）

## 定义

Tool Calling（又称 Function Calling）是 LLM 自主选择调用外部工具/函数的核心机制——模型不仅生成文本，还能根据对话上下文判断是否需要调用工具，并以结构化格式返回调用参数。这是 LLM 从"只会说话"进化为"能动手"的分水岭，也是 [[Agent_Loop|ReAct 循环]] 中 Action 阶段的技术基础。

## 两种主流协议格式

| 维度 | OpenAI 兼容格式 | Anthropic 原生格式 |
|------|----------------|-------------------|
| **Schema 结构** | `{"type":"function","function":{name,description,parameters}}` | `{name,description,input_schema}` |
| **参数键名** | `parameters` | `input_schema` |
| **停止原因** | `finish_reason == "tool_call"` | `stop_reason == "tool_use"` |
| **参数提取** | `json.loads(tc.function.arguments)` | `tc.input`（已是对象） |
| **消息结构** | 流式函数调用 | content block 数组 |
| **代表实现** | OpenAI GPT、Ollama、大多数开源模型 | Claude 系列 |

### OpenAI 兼容格式示例

```python
tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询城市目前天气（晴/雨/阴），回传短字符串。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
            },
            "required": ["city"],
        },
    },
}

# 调用
resp = client.chat.completions.create(model="gpt-4o", tools=[tool], ...)
tc = resp.choices[0].message.tool_calls[0]
name = tc.function.name                     # "get_weather"
args = json.loads(tc.function.arguments)    # {"city": "台北"}
```

### Anthropic 原生格式示例

```python
tool = {
    "name": "get_weather",
    "description": "查询城市目前天气（晴/雨/阴），回传短字符串。",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名称"},
        },
        "required": ["city"],
    },
}

# 调用
resp = client.messages.create(model="claude-haiku-4-5", tools=[tool], ...)
tc = [b for b in resp.content if b.type == "tool_use"][0]
name = tc.name                               # "get_weather"
args = tc.input                              # {"city": "台北"}（已解析）
```

## Tool Description 优化四原则

高质量的 `description` 直接决定 LLM 在多工具场景中的路由准确性：

| 原则 | 说明 | 反例 | 正例 |
|------|------|------|------|
| **边界互斥** | 不同 tool 的 description 语义不能交叉 | "日历" vs "搜索"→都隐含"查信息" | "查询指定日期的事件" vs "搜索当前外部信息" |
| **写给人看 ≠ 写给模型看** | 人类标签的信息量不够模型判断 | "日历"（两字） | "查询指定日期的事件" |
| **小模型更敏感** | qwen2.5:3b 对措辞变化反应明显 | 笼统描述 → 路由错误 | 精确描述 → 路由正确 |
| **参数优先 A/B 测试** | 用工厂函数收拢变量，快速对比 | 手动改多处 | `make_tools(calendar_desc)` 一行切换 |

### Description 三要素

```
"查询指定日期的事件"
  ↑ 动词       ↑ 对象     ↑ 限定
```

| 要素 | 作用 | 正例 |
|------|------|------|
| **动词**（做什么） | 明确行为类型 | "查询""搜索""计算" |
| **对象**（对什么做） | 明确作用对象 | "事件""表达式""城市人口" |
| **限定**（边界在哪） | 缩小范围、避免重叠 | "指定日期""当前外部" |

### 自检清单

1. 每个 description 是否让模型一眼知道"什么场景用它"？
2. 任意两个 description 拼在一起，语义上有没有模糊地带？
3. 是否包含动词开头？
4. 是否包含输入输出的提示（如"返回 JSON 数组"）？
5. 小模型实测验证过了吗？

## 多步调用的依赖链

当多个 Tool Call 之间存在**数据依赖关系**时，模型可能不按依赖顺序执行——尤其是小模型。

### 数据依赖链模式

```
Step 1: get_population("台北")    →  250      ← 无依赖
Step 2: get_population("纽约")    →  833      ← 无依赖（可与 Step 1 并行）
Step 3: calculator("250/833")     →  0.3001   ← 依赖 Step 1 & 2 的结果
Step 4: convert_to_percentage(0.3001) → 30.01% ← 依赖 Step 3 的结果
```

### 小模型的"跳跃"问题

由于 OpenAI 兼容协议支持单次返回多个 `tool_calls`，小模型（如 qwen2.5:3b）倾向于"一股脑全预测出来"，导致：

```
查台北 → 查纽约 → convert_to_percentage(0.3)  ← ❌ 还没算呢！
```

`convert_to_percentage` 被提前调用，用猜测值 `0.3` 而非真实计算结果 `0.30012`，且后续即使 `calculator` 返回正确结果，模型也**不会重新调用**转换工具。

### 依赖链的调用时序约束

| 类型 | 能否并行 | 示例 |
|------|---------|------|
| **独立工具** | ✅ 可并行调用 | 多个 `get_population` 查询不同城市 |
| **数据依赖工具** | ❌ 必须串行 | `calculator` 必须等人口数据 |
| **链式依赖工具** | ❌ 必须按序 | `convert_to_percentage` 必须等 `calculator` |

### 缓解方案

| 方案 | 适用场景 |
|------|---------|
| **加大模型**（7b/14b） | 一次性解决，大模型规划更准确 |
| **System Prompt 强调顺序** | 零成本改进，如"未计算前不得调用 convert_to_percentage" |
| **调整 description 暗示依赖** | 巧妙方案，如"接收计算结果作为输入" |
| **代码层拦截** | 检测到前置依赖未满足时拒绝执行 |

> **核心经验**：小模型做多步骤推理，必须在代码层做依赖校验，不能全指望模型自己规划。详细代码示例见 [[摘要-多步骤推理任务-连续-tool-调用]]。

## Schema 设计深度指南

> **写 Schema 的功夫能省下换大模型的成本。** 相同 Bad Schema 在 Claude 上可能还能猜对，在 qwen2.5:3b 上几乎必错。如果 Production 打算用小模型节省成本，Schema 质量就是必须补的欠债。

### 4 个关键改进项

| 改进项 | Bad | Good |
|--------|-----|------|
| **name 带领域信息** | `convert`（笼统） | `convert_temperature`（带领域信息） |
| **description 写"何时用"** | `"Convert a value."`（像注释） | `"当用户要求温度转换时使用"`（路由判断条件） |
| **type 用对** | `value: string` | `value: number` |
| **required + enum** | 无 required, `unit: string` | `required: ["value","unit"]`, `unit: enum["celsius","fahrenheit"]` |

### 问题 1：Name 笼统

```
Bad:  "name": "convert"
      → LLM 看到"温度转换"不知道 convert 跟它有啥关系
Good: "name": "convert_temperature"
      → LLM 看到"温度"就匹配上了
```

更致命的是——太笼统的 name 会**污染整个工具集的选择**。实测中 BAD schema 的 `convert` 导致天气查询也失败（LLM 无法做出路由决策）。

### 问题 2：Description 写得像函数注释

```
Bad:  "description": "Convert a value."
      → LLM："转换什么值？什么时候用？跟问题有什么关系？"

Good: "description": "当用户要求在不同温度单位（摄氏/华氏）之间转换时使用"
      → LLM："这个匹配！用户问的就是温度转换"
```

**把 description 想成路由判断条件**——LLM 看到用户问题，拿 description 逐一比对，第一个命中率最高的就是正确工具。详见 [[Tool_Calling#Description 三要素|Description 优化四原则]]。

### 问题 3：Type 全用 string

```
Bad:  "value": {"type": "string"}    → LLM 传 "100"（字符串）
Good: "value": {"type": "number"}    → LLM 传 100（数字）
```

BAD schema 传了 `"100"` 字符串——函数内用 `float()` 转换所以没崩，但如果 value 带单位如 `"100°F"`，`float()` 就会报错。

### 问题 4：没写 Required + 没写 Enum

```
Bad:  没写 required → LLM 可能跳过某些参数
     unit: string（无约束） → LLM 自由发挥，传了 "Fahrenheit" "Celsius"

Good: required: ["value", "unit"] → LLM 知道必须传这两个
     unit: enum["celsius", "fahrenheit"] → 只能传小写标准名
```

实际运行中 BAD schema 传的 `"Fahrenheit"` 和 `"Celsius"` 最典型——LLM 按口语习惯首字母大写，没有 enum 约束就没人阻止它。

### 5 条黄金规则

| 规则 | 说明 |
|------|------|
| **1. Name 带领域信息** | `convert` → `convert_temperature` |
| **2. Description 写"何时用"** | 不是写"做什么"，是写"什么场景下 LLM 该选我" |
| **3. Type 用对** | number / boolean / enum / array，不要全 string |
| **4. Required + Enum** | required 防止漏传，enum 防止非法值 |
| **5. Error 回传 dict** | 见下方 [[Tool_Calling#错误处理模式\|错误处理模式]] |

### 5 个常见 Anti-Pattern

| # | Anti-Pattern | 坏例子 | 好例子 |
|---|-------------|--------|--------|
| 1 | 所有参数塞到 "data" 对象 | `data: {"type": "string"}` | 展开成独立字段 |
| 2 | 被动语态 | `"The temperature is converted"` | 祈使句 |
| 3 | 参数名缩写 | `"val"`, `"tmp"` | `"value"`, `"temperature"` |
| 4 | Enum 值跟用户说法脱节 | `enum: ["c", "f"]` | `enum: ["celsius", "fahrenheit"]` |
| 5 | 不写 required | 自由发挥 | `required: ["value", "unit"]` |

### 小模型 vs 大模型的 Schema 敏感度

相同 Bad Schema 在不同模型上的表现差异：

| 模型 | 结果 |
|------|------|
| **qwen2.5:3b** | ❌ 温度转换全部失败（大小写问题）+ 天气查询也不调用工具 |
| **qwen2.5:14b** | 🟡 可能好一些，但仍然受 enum 缺失影响 |
| **Claude Haiku** | 🟡 可能传正确的单位名（大小写碰运气） |
| **GPT-4 / Claude Sonnet/Opus** | ✅ 基本能猜对大小写和类型 |

> **Bad Schema 在很多大模型上被"猜对"了，这掩盖了 Schema 设计问题。** 如果 Production 打算用小模型节省成本，Schema 质量就是必须补的欠债。

### 实际运行对比速览

| 问题 | BAD Schema | GOOD Schema |
|------|-----------|-------------|
| 100°F → °C | ❌ `convert("Fahrenheit")` 失败两次 | ✅ `convert_temperature(fahrenheit)` → 37.8°C |
| 37°C → °F | ❌ `convert("Celsius")` 失败 | ✅ `convert_temperature(celsius)` → 98.6°F |
| 北京天气 | ❌ 空回答，未调用任何工具 | ✅ `get_weather("北京")` → 晴，30°C |

## 错误处理模式

> **Tool Error 是 Data 不是 Exception。** 这是 Agent 工程从"函数调用"走向"LLM 驱动"的关键一步。

### 核心观念翻转

工具函数出错时，不应抛出 Exception 中断循环，而应返回结构化 dict——让 LLM **自己看到错误信息后自主决策**重试/改参数/放弃。

```python
# Bad：raise 中断 loop，LLM 没机会 recover
def fetch_weather(city):
    if network_failed():
        raise Exception("network timeout")

# Good：return dict，LLM 看到结构化错误后自己决定怎么办
def fetch_weather(city):
    if network_failed():
        return {"error": "network timeout",
                "category": "transient",
                "retry_hint": "try again in 1s"}
```

### 结构化错误设计

```python
# 成功
{"status": "ok", "forecast": "rain", "temperature_c": 24}

# transient — 可重试（LLM 可自主选择重试）
{"error": "网络连接超时", "category": "transient", "retry_hint": "稍后重试"}

# fatal — 不可重试（LLM 应直接放弃）
{"error": "城市不在覆盖范围", "category": "fatal", "retry_hint": "检查城市名称"}
```

### 两种 Retry 机制

```
Layer 1：LLM 层（业务语义层）
  LLM 看到 category = transient → 自主决定重试
  LLM 看到 category = fatal    → 直接放弃

Layer 2：Python 层（安全护栏层）
  retry_counts[name] > RETRY_LIMIT(3)
  → 强行返回 fatal，LLM 必须终止
```

**关键区别**：Production 的 retry 不在 Python 层、而在 LLM 层——这个 mental flip 是核心。

### 四种错误回传方式对比

| 方案 | LLM 能否 recover | 信息量 | 推荐 |
|------|-----------------|--------|------|
| raise Exception | ❌ 崩溃 | 低 | ❌ |
| `return "failed"` | ❌ 看不懂 | 极低 | ❌ |
| `return "网络超时"` | 🟡 可能 | 中 | ⚠️ |
| `return {dict}` | ✅ 完全可理解 | 高 | ✅ |

结构化 dict 的字段名本身就是提示词——LLM 看字段名就知道含义。小模型尤其受益于此。

### 三层错误处理架构

| 层级 | 职责 | 示例 |
|------|------|------|
| **工具层** | 返回结构化 dict，不 raise | `return {"error":"...","category":"transient"}` |
| **LLM 层** | 看 dict 判断是否重试 | "这是 transient，再试一次" |
| **Python 层** | 兜底护栏 | retry_limit=3, max_steps=8 |

决策分配表：

| 场景 | 谁管 | 判断依据 |
|------|------|---------|
| 同一工具连续失败 | **LLM 层** | 看到 category=transient，自己决定再试 |
| 超过重试配额 | **Python 层** | retry_counts > LIMIT，强制 fatal |
| 用户输入无效 | **LLM 层** | 看到 category=fatal，告诉用户 |
| 全局死循环 | **Python 层** | max_steps 兜底 |
| 是否换参数重试 | **LLM 层** | 根据 retry_hint 改 query |
| 是否彻底放弃 | **LLM 层** | 综合判断后输出 Answer |

## 与 Agent Loop 的关系

Tool Calling 是 [[Agent_Loop|ReAct 循环]] 中 Action 阶段的技术基础：

```
Thought（分析）→ Action（Tool Calling）→ Observation（工具结果反馈LLM）→ 循环 → Answer
```

- LLM 在 Thought 阶段决定"是否需要调用工具"
- Action 阶段通过 Tool Calling 协议选择工具、构造参数
- Observation 阶段将工具结果写回消息历史供下一轮推理

## 关联连接

- [[Agent_Loop]] — ReAct 循环依赖 Tool Calling 实现 Action 阶段
- [[摘要-llm-tool-calling-practice]] — 本概念的核心来源（动手实践系列）
- [[摘要-多步骤推理任务-连续-tool-调用]] — 多步骤 Tool Calling 数据依赖链实践
- [[摘要-tool-error-is-data]] — Tool Error 作为结构化 Data 返回的错误处理范式（练习 5）
- [[摘要-function-schema-design]] — Bad Schema 到 Good Schema 的 4 项改进与 5 条黄金规则
- [[摘要-awesome-agentic-ai-zh-tool-use]] — Stage 3 理论版本，含 Schema 设计 4 项改进
- [[OpenAI_Compatible_API]] — 已成为行业事实标准的接口规范
- [[Anthropic]] — Anthropic 原生 tool use 格式的提供商
- [[Ollama]] — OpenAI 兼容格式的本地运行环境
- [[Orchestration_Code_Examples]] — Multi-agent 编排中的 Tool Calling 对比
