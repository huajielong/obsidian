# Stage 3 — 工具使用与第一个 Agent（Tool Use & Hello Agent）

> [繁體中文](./03-tool-use-and-hello-agent.md) | **简体中文** | [English](./03-tool-use-and-hello-agent.en.md)

⏱ **时间估算**：2-3 周（约 10-20 小时）

> 👋 **从 [Stage 2](02-prompt-engineering.zh-Hans.md) 来的**：你会写结构化 prompt、会用 few-shot 跟 CoT 解推理题了——这 10-20 小时：让 LLM 学会用工具、从零写出你的第一个 ReAct Agent。**直接从这里开始的**：先确认你会在 Stage 1 的 API 调用基础上，理解 function calling 的参数格式——做不到请先回 [Stage 2](02-prompt-engineering.zh-Hans.md)。

> 💡 用语不熟（tool / function calling / ReAct / agent loop ...）→ 翻 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)。

**预设模型**：Ollama `qwen2.5:3b`（tool-use 支援稳定，1.9 GB）

---

## 📌 学习目标

走完这个阶段后你会：

1. 理解为什么 LLM **需要** tools——有文字以外的任务 LLM 无法处理
2. 定义 tool schema，并让 LLM 呼叫它（function calling）
3. 从零（不靠任何 framework）写出**单步 ReAct Agent**
4. 写出**多步 ReAct Agent**，并让它自己判断何时该停
5. 区分哪些问题该用 tool use、哪些纯 prompt 就够

---

## 🚪 进入条件

你应该已经：

- 会调用 LLM API（Stage 1）
- 会解析 / 遍历 API 响应
- 了解基本的 prompt 设计技巧（Stage 2）

---

## 🧠 核心概念：AI / LLM / Agent 的区别

| 词 | 是什么 | 例子 |
|---|---|---|
| **AI** | 整个学科 | ML、DL、LLM、RL 都是子领域 |
| **LLM** | 文字→文字的单一模型 | GPT-5、Claude、Llama 3、Qwen |
| **Agent** | LLM + 工具 + loop 的**系统** | Cursor、Claude Code、Hermes Agent |

### Agent 的 3 个最小必要部件

| 部件 | 角色 | 学习阶段 |
|---|---|---|
| 🧠 **LLM（大脑）** | 推理 / 决策 / 自然语言 | Stage 1 |
| 🔧 **Tools（手）** | 对世界做事（call API、跑 code、查资料） | **本 Stage** |
| 🔁 **Loop（心跳）** | 想 → 做 → 看结果 → 再想（ReAct） | **本 Stage 练习 3** |

### 经典范式对照

| 范式 | 说明 | 学习位置 |
|---|---|---|
| **CoT（思维链）** | LLM 写出推理过程再给答案 | Stage 2 |
| **ReAct（Reasoning + Acting）** | Thought → Action → Observation 循环 | **Stage 3 练习 3** |
| **Reflection** | 跑完一轮后让 LLM 批改自己 | Stage 3 反思 |
| **Planning（任务分解）** | 大任务拆成子任务 | Stage 4 |

---

## 📚 必修阅读

1. [**Anthropic — Tool Use**](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) ⭐⭐⭐⭐⭐ — **官方 tool use 指南**、带 interactive 演示、用 service / function / parameter 三层结构定义工具
2. [**anthropics/courses — Tool Use**](https://github.com/anthropics/courses) ⭐⭐⭐⭐ ★ 21k+ — Jupyter notebook 交互式动手练习，含「multi tool」与「chain tool calls」
3. [**ReAct: Synergizing Reasoning and Acting in Language Models**](https://arxiv.org/abs/2210.03629) ⭐⭐⭐⭐⭐ — Yao et al. 2022，**奠基论文**，提出 Thought → Action → Observation 循环，建议读 **3-5 页 Introduction + 第 4 页 ReAct 方法**
4. [**OpenAI — Function Calling**](https://platform.openai.com/docs/guides/function-calling) ⭐⭐⭐ — OpenAI 接口指南，看清楚 **`tools` 参数格式与 `.tool_calls` 响应结构**
5. [**Build an agent from scratch**](https://shafiqulai.github.io/blogs/blog_3.html) ⭐⭐⭐ — **从零打造 agent 的故事式导览**，适合听完 ReAct 论文后当补充

---

## 🛠 动手练习（6 个）

所有练习的 starter 模板见 `examples/stage-3/` 目录：

### 练习 1：Function Calling（一个工具、一次调用）

- **目标**：给 LLM 一个天气 API 工具 + 问题「台北现在有下雨吗？」，观察它返回 tool_call 而非文字回答
- **Path A（Ollama）**：OpenAI-compatible schema，需包 `{"type":"function", "function":{...}}`
- **Path B（Anthropic）**：原生格式 `tools=[{name, description, input_schema}]`
- **关键差异**：Anthropic 的 `.input` 是 dict（自动 parse）；OpenAI/Ollama 的 `.function.arguments` 是 JSON string
- **目录**：`examples/stage-3/01-function-calling/`

```python
# Ollama 路径（OpenAI 兼容格式）
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "城市名称，如 台北"}
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "台北现在有下雨吗？"}],
    tools=tools,
    tool_choice="auto"
)

msg = response.choices[0].message
print("Assistant:", msg.content)
print("Tool calls:", msg.tool_calls)
```

### 练习 2：多工具选择

- **目标**：给 LLM 三个工具（搜索、计算器、日历），看它怎么挑
- **核心 lesson**：`description` 边界要互斥，小模型对 description 质量比 Claude 更敏感

**三个工具示例**：
| 工具 | 用途 |
|------|------|
| `web_search(query)` | 搜索网络信息 |
| `calculator(expression)` | 执行数学计算 |
| `get_calendar_events(date)` | 查询日历事件 |

- **目录**：`examples/stage-3/02-multi-tool-selection/`

### 练习 3：从零实现 ReAct（不用 framework）

- **目标**：用 50-80 行 Python 写 Thought → Action → Observation 循环
- **核心代码（13 行精华）**：

```python
messages = [{"role": "user", "content": "台北人口除以纽约人口？"}]
for step in range(5):  # max_iter = 5
    r = client.chat.completions.create(
        model="qwen2.5:3b",
        tools=TOOLS,
        messages=messages
    )
    msg = r.choices[0].message
    messages.append({
        "role": "assistant",
        "content": msg.content,
        "tool_calls": msg.tool_calls
    })
    if not msg.tool_calls:
        print(f"✅ 收尾：{msg.content}")
        break
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        obs = TOOL_IMPL[tc.function.name](**args)
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": obs
        })
```

- **3 个常见踩坑**：
  1. 忘记把 assistant response 加回 messages → loop forever
  2. `tool` message 没带 `tool_call_id` → LLM 无法配对结果
  3. 没设 `max_iter` → 无限呼叫

- **目录**：`examples/stage-3/03-react-from-scratch/`（含 mock-based test.py）

### 练习 4：多步骤推理任务

- **目标**：需要连续呼叫 3-5 次 tool 的任务（如：「找出台北人口，除以纽约人口，再把比例换成百分比」）
- **核心概念**：跟练习 3 同一个 loop，只是跑久一点
- **观察重点**：qwen2.5:3b 可能漏步骤，Claude Haiku 较稳
- **目录**：`examples/stage-3/04-multi-step-reasoning/`

### 练习 5：错误处理

- **目标**：让某个工具失败（网络错误、输入无效），看 agent 能否恢复
- **核心 lesson**：tool error 回传**结构化 dict**、不要 `raise`
- **关键心态转换**：Production 的 retry 不在 Python 层、而在 LLM 层

```python
def get_weather(location: str) -> dict:
    try:
        # 模拟 API 调用
        if location == "火星":
            return {"error": True, "reason": "不支持的 locations"}
        return {"temperature": 25, "conditions": "晴"}
    except Exception as e:
        return {"error": True, "reason": str(e)}
```

- **目录**：`examples/stage-3/05-error-handling/`

### 练习 6：Function schema 设计（坏 schema 修到好）

- **目标**：先给烂 schema → 观察 LLM 选错 → 逐项修正
- **4 个改进方向**：
  1. `name` 改具体（`search` → `web_search_by_keyword`）
  2. `description` 写「何时用」而非「做什么」
  3. `type` 改 `number` 而非 `string`（强制类型）
  4. 加 `required` + `enum`（减少幻觉）
- **目录**：`examples/stage-3/06-schema-design/`

---

## ⚠️ 安全：给 agent 工具 = 给它攻击面

**致命三角（lethal trifecta）**：

1. 能访问私密数据
2. 会接触不可信内容（可能藏指令）
3. 能对外发送东西

根因是 **prompt injection**——LLM 分不清哪些是你下的指令、哪些是不可信数据夹带的。

**防御清单**：
| 措施 | 说明 |
|------|------|
| 最小权限 | 只给 agent 完成当前任务最少的工具 |
| 手动确认 | 每步操作前请求用户确认 |
| 沙箱执行 | 在隔离环境中运行代码（容器 / VM） |
| 内容审计 | 记录所有 tool 调用日志，定期审查 |

---

## 🔗 关联资源

| 项目 | 路径 |
|------|------|
| 练习 1 | `examples/stage-3/01-function-calling/` |
| 练习 2 | `examples/stage-3/02-multi-tool-selection/` |
| 练习 3 | `examples/stage-3/03-react-from-scratch/` |
| 练习 4 | `examples/stage-3/04-multi-step-reasoning/` |
| 练习 5 | `examples/stage-3/05-error-handling/` |
| 练习 6 | `examples/stage-3/06-schema-design/` |

### 学习路径地图

```
Stage 0 (Foundations) → Stage 1 (LLM Basics) → Stage 2 (Prompt Engineering) 
→ Stage 3 (Tool Use & Hello Agent) ← 你在这里
    ↓
Stage 4 (Multi-Step Agent) → Stage 5 (Agentic RAG) → Stage 6 (Production Agent)
```

---

## 📖 反思（Reflection）概念

ReAct 是 agent 的**基础**范式。更进一步的技术是 **Reflection**——跑完一轮后让 LLM 批改自己的输出：

```
Action → Observation → Thought → Action → Observation
                                            ↓ (反思)
                                   批改前一次 Action 的质量
                                            ↓
                                   更好的 Action → 更好的 Observation
```

这也是 Stage 4 的前置概念。

---

> Continue to [Stage 4 — 多步骤 Agent（Multi-Step Agent）](04-multi-step-agent.zh-Hans.md)
