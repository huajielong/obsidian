---
title: "Orchestration_Code_Examples"
type: concept
tags: [multi-agent, orchestration, 代码示例, LangGraph, CrewAI, AutoGen, OpenAI, 实战]
sources: [raw/01-articles/04-agent-frameworks.md]
last_updated: 2026-07-14
---

# 编排编程示例

## 概览

同一个 Multi-agent 场景——**Research → Write → Review** 三步骤流水线——在不同框架中的实现对比。这不仅是学 API，更是理解每种框架的"编排哲学"。

### 场景需求

1. **Researcher**：搜索给定主题的关键信息，输出结构化摘要
2. **Writer**：根据摘要撰写一篇博客文章
3. **Critic**：评审文章，给出改进建议
4. 全部使用 GPT-4o，但 Framework 路线可以轻松换成混合 provider

---

## 1. 纯 Python（无框架 — 基线版）

不依赖任何框架，用 dict + for loop 手工实现。适合理解编排的本质，也适合极简单的流水线。

```python
import json
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPTS = {
    "researcher": "你是一个研究员。请搜索并整理指定主题的关键信息，以 JSON 格式输出：标题、要点列表、关键数据。",
    "writer": "你是一个科技写手。根据研究员提供的信息，撰写一篇 500 字的博客文章。直接输出文章正文。",
    "critic": "你是一个严谨的编辑。评审下面的博客文章，列出 3 个改进点和一个总体评分（1-10）。",
}

def call_llm(system_prompt, user_input):
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
    )
    return resp.choices[0].message.content

# --- 编排逻辑：顺序执行，结果传递 ---
topic = "AI Agent 的安全对齐技术"

research = call_llm(SYSTEM_PROMPTS["researcher"], topic)
print("=== Research ===")
print(research)

article = call_llm(SYSTEM_PROMPTS["writer"], research)
print("\n=== Article ===")
print(article)

review = call_llm(SYSTEM_PROMPTS["critic"], article)
print("\n=== Review ===")
print(review)

# 输出：3-10x 的成本差来自哪里？这里每次 call_llm 都完整传入了全部上下文
```

**优缺点**：
- ✅ 零依赖，逻辑完全透明
- ✅ 适合 2-3 步的简单流水线
- ❌ 没有 state 管理，错误处理需手写
- ❌ 没有 retry/fallback/tracing
- ❌ 并行需要手动 `threading` / `asyncio`

---

## 2. LangGraph（图式编排 — Production 首选）

以 **StateGraph** 为核心，节点是 Agent/工具，边是条件路由。天然支持 checkpointing、分支、循环。

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# --- 1. 定义 State ---
class AgentState(TypedDict):
    topic: str
    research: str      # Researcher 输出
    article: str       # Writer 输出
    review: str        # Critic 输出
    accepted: bool     # Review 是否通过

# --- 2. 定义节点函数 ---
def researcher(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o")
    msg = llm.invoke([
        SystemMessage(content="你是研究员。整理指定主题的关键信息，用 JSON 格式输出：标题、要点、关键数据。"),
        HumanMessage(content=state["topic"]),
    ])
    return {"research": msg.content}

def writer(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o")
    msg = llm.invoke([
        SystemMessage(content="你是科技写手。根据信息撰写 500 字博客文章。"),
        HumanMessage(content=state["research"]),
    ])
    return {"article": msg.content}

def critic(state: AgentState) -> dict:
    llm = ChatOpenAI(model="gpt-4o")
    msg = llm.invoke([
        SystemMessage(content="你是编辑。评审文章，返回 JSON：{score:int, improvements:[str], accepted:bool}"),
        HumanMessage(content=state["article"]),
    ])
    return {"review": msg.content}

def decide_next(state: AgentState) -> Literal["writer", "__end__"]:
    """条件边：review 不通过则返回 writer 修改"""
    if state.get("accepted", False):
        return "__end__"
    return "writer"

# --- 3. 构建图 ---
builder = StateGraph(AgentState)

builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("critic", critic)

builder.set_entry_point("researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "critic")
builder.add_conditional_edges("critic", decide_next)  # 循环：critic → writer

# --- 4. 编译并运行 ---
graph = builder.compile()
result = graph.invoke({"topic": "AI Agent 的安全对齐技术"})

# --- 5. 查看结果 ---
print(result["article"])   # 最终文章
print(result["review"])    # 评审意见
# graph.get_state(...).values 可随时 checkpoint 回放
```

**关键差异**：
- **State** 是显式类型，所有节点通过 dict 通信 → 类型安全
- **条件边** `decide_next` 实现 review 不通过 → 回 writer 修改的循环
- `graph.invoke()` 是一次完整执行，`graph.get_state()` 可回放任意历史步骤
- 加 `checkpointer` 参数即可开启 checkpointing / time-travel debug

---

## 3. CrewAI（角色驱动 — 快速雏形首选）

定义 Agent 角色（role/goal/backstory）+ Task 委托，框架自动处理结果传递。

```python
from crewai import Agent, Task, Crew

# --- 1. 定义 Agent（角色驱动）---
researcher = Agent(
    role="高级研究员",
    goal="找出指定主题的关键信息和最新动态",
    backstory="你是一个经验丰富的技术研究员，擅长快速掌握新技术领域。",
    model="gpt-4o",
)

writer = Agent(
    role="科技写手",
    goal="用生动易懂的语言撰写技术博客",
    backstory="你是一个技术博客作者，擅长将复杂概念转化为读者喜爱的文章。",
    model="gpt-4o",
)

critic = Agent(
    role="资深编辑",
    goal="确保文章质量和准确性",
    backstory="你是业界知名的技术编辑，对文章质量和事实准确性要求极高。",
    model="gpt-4o",
)

# --- 2. 定义 Task（自动委托）---
research_task = Task(
    description="研究 AI Agent 的安全对齐技术，输出关键信息和框架对比",
    expected_output="结构化的研究摘要，包含关键概念、主要方法和挑战",
    agent=researcher,
)

write_task = Task(
    description="基于研究结果撰写一篇 500 字的技术博客",
    expected_output="一篇完整的技术博客文章",
    agent=writer,
)

review_task = Task(
    description="评审博客文章，给出改进建议和评分",
    expected_output="包含评分和改进点的评审报告",
    agent=critic,
)

# --- 3. 定义 Crew（编排流水线）---
crew = Crew(
    agents=[researcher, writer, critic],
    tasks=[research_task, write_task, review_task],  # 按顺序执行
    verbose=True,
)

# --- 4. 一次运行 ---
result = crew.kickoff()
print(result)
```

**关键差异**：
- 不写 state 管理、不画 graph——**声明式**：定义 Agent（谁）→ 定义 Task（做什么）→ 组装 Crew（顺序）
- Agent 的 `backstory` 是独特的"角色人格"设定
- `verbose=True` 打印中间步骤
- 按 `tasks` 列表顺序执行，每个 task 的 `agent` 自动接收上一步输出

---

## 4. AutoGen（对话式编排 — Debate / Peer Review 专长）

Agent 在 GroupChat 中以自然语言对话——不是"函数调用函数"，而是"人跟人聊天"。

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    # --- 模型客户端（可混用不同 provider）---
    model_client = OpenAIChatCompletionClient(model="gpt-4o")

    # --- 定义 Agent ---
    researcher = AssistantAgent(
        name="Researcher",
        system_message="你是研究员。研究指定主题，输出结构化摘要。",
        model_client=model_client,
    )

    writer = AssistantAgent(
        name="Writer",
        system_message="你是科技写手。根据研究结果撰写博客文章。输出文章后说'文章完成'。",
        model_client=model_client,
    )

    critic = AssistantAgent(
        name="Critic",
        system_message="你是编辑。评审文章并给出改进建议。如果文章已通过，说'文章通过'。",
        model_client=model_client,
    )

    # --- 组队：RoundRobin 轮流发言 ---
    team = RoundRobinGroupChat(
        participants=[researcher, writer, critic],
        termination_condition=TextMentionTermination("文章通过"),
    )

    # --- 开始对话 ---
    result = await team.run(task="主题：AI Agent 的安全对齐技术")

    for message in result.messages:
        print(f"\n[{message.source}]: {message.content}")

asyncio.run(main())
```

**关键差异**：
- **不是流水线**——Agent 在 Chat Room 里轮流发言，像 Slack 群聊
- `TextMentionTermination("文章通过")`：Critic 说出关键词即终止——自然语言边界
- 天然适合 Debate / Brainstorming / Peer Review
- `RoundRobinGroupChat` 是 1 种模式，还有 `SelectorGroupChat`（LLM 选择谁发言）

---

## 5. OpenAI Agents SDK（Handoff 式编排 — 轻量交接）

Agent 之间通过 `handoffs` 参数 1:1 交接——我干完 → 交给你。

```python
from agents import Agent, Runner

# --- 定义 Agent（带 handoff 参数）---
researcher = Agent(
    name="Researcher",
    instructions="你是研究员。研究指定主题，输出结构化摘要。",
    model="gpt-4o",
)

writer = Agent(
    name="Writer",
    instructions="你是科技写手。根据研究结果撰写博客文章。",
    model="gpt-4o",
    handoffs=[],  # Writer 可以 handoff 给 Critic
)

critic = Agent(
    name="Critic",
    instructions="你是编辑。评审文章并给出改进建议。",
    model="gpt-4o",
)

# --- 编排：在 orchestrator 中控制交接逻辑 ---
import asyncio

async def main():
    topic = "AI Agent 的安全对齐技术"

    # Step 1: Researcher
    research_result = await Runner().run(
        researcher, topic
    )
    research_output = research_result.final_output
    print(f"[Researcher]\n{research_output}")

    # Step 2: 将研究结果传给 Writer
    write_result = await Runner().run(
        writer, f"请根据以下信息撰写博客：\n{research_output}"
    )
    article_output = write_result.final_output
    print(f"\n[Writer]\n{article_output}")

    # Step 3: 将文章传给 Critic
    review_result = await Runner().run(
        critic, f"请评审以下文章：\n{article_output}"
    )
    print(f"\n[Critic]\n{review_result.final_output}")

asyncio.run(main())

# --- 更高级：让 Agent 自主 handoff（无需 orchestrator 控制）---
# researcher.handoffs = [writer]
# writer.handoffs = [critic]
# Runner().run(researcher, "AI Agent 的安全对齐技术")
# → Researcher 完事自动 handoff 给 Writer → Writer 完事自动 handoff 给 Critic
```

**关键差异**：
- Runtime 层处理 Agent 的 `handoffs`——Agent 可以在运行时**自主决定**交给谁
- `Runner().run()` 是顶级入口，返回 `final_output`
- Handoff 是最轻量的编排模式：无 state graph、无 Chat Room、无 Crew
- 适合 Routing 类任务（客户支持分流、Context 切换）

---

## 横向对比

| 维度 | 纯 Python | LangGraph | CrewAI | AutoGen | OpenAI SDK |
|------|-----------|-----------|--------|---------|------------|
| **代码量** | ~40 行 | ~60 行 | ~50 行 | ~50 行 | ~45 行 |
| **编排范式** | 手写顺序 | State Graph | 声明式角色 | GroupChat 对话 | Handoff 接力 |
| **State 管理** | 变量传递 | 显式 TypedDict | 隐式 task 委托 | Chat History | Runner 返回值 |
| **类型安全** | ❌ | ✅ TypedDict | ❌ script 式 | ❌ 动态 | ❌ 动态 |
| **循环/分支** | 手写 if/for | 条件边 + 循环 | ❌ 不支持 | 对话可回环 | 需 orchestrator |
| **Checkpoint** | ❌ | ✅ built-in | ❌ | ❌ | ❌ |
| **并行** | ❌ 手写 | ✅ parallel 节点 | ✅ parallel tasks | ❌ RoundRobin | ❌ 需手动 |
| **跨 provider** | ✅ 手写 | ✅ LangChain | ✅ model 参数 | ✅ 插件式 client | ❌ OpenAI 限定 |
| **学习曲线** | 最低 | 最高 | 低 | 中 | 中低 |
| **一句话定位** | 理解编排本质 | Production 级稽核 | 3 行搭雏形 | 多 Agent 辩论 | 轻量 Handoff |

---

## 如何选？

- **快速验证想法** → CrewAI（~20 行完成）
- **需要条件循环/长 Workflow** → LangGraph（条件边 + checkpointing）
- **需要多视角 Debate/Brainstorm** → AutoGen（GroupChat 自然语言）
- **轻量 Routing/Handoff** → OpenAI Agents SDK（"干完交给你"）
- **不需要任何框架** → 纯 Python（简单流水线、不想引入依赖）
- **想看到框架到底帮你省了什么** → 先写纯 Python 版本，再对比任何一个框架——你就理解了

## 关联连接

- [[Agent_Orchestration_Patterns]] — 5 种经典编排模式的抽象描述
- [[Multi_Agent_System]] — 何时该用 Multi-agent 的决策框架
- [[LangGraph]] — 图式编排框架的实体页面
- [[CrewAI]] — 角色驱动框架的实体页面
- [[AutoGen]] — 对话式编排框架的实体页面
- [[OpenAI_Agents_SDK]] — Handoff 式编排框架的实体页面
- [[Agent_Loop]] — Single-agent ReAct 循环（Multi-agent 的前置基础）
- [[Harness_Engineering]] — Multi-agent 的 Production 化工程基础
