---
title: "Tool_Calling"
type: concept
tags: [工具调用, function calling, LLM, Agent, 协议, Schema设计]
sources: [raw/01-articles/LLM工具调用入门实践.md, raw/01-articles/Tool Description 边界互斥实验.md, raw/01-articles/多步骤推理任务 — 连续 Tool 调用.md]
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

## Schema 设计最佳实践

| 改进项 | 说明 |
|--------|------|
| **`name` 要具体** | `get_population` 优于 `get_data` |
| **`description` 写"何时用"而非"做什么"** | "查询城市人口，单位万人"优于"人口查询函数" |
| **`type` 强制 `number`** | 避免 LLM 传字符串导致下游解析异常 |
| **加 `required` + `enum`** | 约束参数取值范围，减少幻觉参数 |
| **参数名自解释** | `city` 优于 `param1`，`expression` 优于 `input` |

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
- [[摘要-awesome-agentic-ai-zh-tool-use]] — Stage 3 理论版本，含 Schema 设计 4 项改进
- [[OpenAI_Compatible_API]] — 已成为行业事实标准的接口规范
- [[Anthropic]] — Anthropic 原生 tool use 格式的提供商
- [[Ollama]] — OpenAI 兼容格式的本地运行环境
- [[Orchestration_Code_Examples]] — Multi-agent 编排中的 Tool Calling 对比
