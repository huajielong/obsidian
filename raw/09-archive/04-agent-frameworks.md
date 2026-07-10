# Stage 4 — Agent 框架（Agent Frameworks）

> **來源**: https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/stages/04-agent-frameworks.md
> **作者**: WenyuChiou
> **抓取日期**: 2026-07-10

> **繁體中文** | [简体中文](./04-agent-frameworks.zh-Hans.md) | [English](./04-agent-frameworks.en.md)

⏱ **時間估算**：2-3 週（約 10-15 小時）

> 💡 用語不熟（framework / supervisor / worker / handoff⋯）→ 翻 [`resources/glossary.md`](../resources/glossary.md)。

> 📋 **本章組成**：學習目標 → 進入條件 → 必修閱讀 →〔可選 · 概念地圖：multi-agent intro + 進階 tool patterns〕→ 動手練習 → 精選 Projects → 自我檢查
> 🔑 **關鍵名詞**：見 [`resources/glossary.md`](../resources/glossary.md)（framework / agent loop / handoff / supervisor 等收在 2、4）

你已經從零打造過一個 ReAct agent（Stage 3）。現在來看 framework 到底幫你做了什麼。**挑一個深入學**，其他的瀏覽過去就好，知道什麼時候該換。

## 📌 學習目標

完成這個 stage 後你會：
- 比較 5 個主流 agent framework（LangGraph、AutoGen、CrewAI、Smolagents、OpenAI Agents SDK）
- 替任務挑出對的 framework
- 用兩個 framework 各做一次同樣的 agent，親身感受差異
- 看出什麼時候該丟掉 framework、自己寫

## 🚪 進入條件

你應該已經：
- 跑完 Stage 3 的全部 5 個 hello-X projects
- 從零寫過 ReAct（練習 3）
- 對 async Python 上手（framework 大量依賴 async）

## 📚 必修閱讀

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 什麼時候用 framework、什麼時候直接用 raw API
2. [**LangChain — Conceptual Guide: Agents**](https://python.langchain.com/docs/concepts/agents/) — agent 的抽象概念
3. [**Best Multi-Agent Frameworks 2026 comparison**](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — 當前市場定位
4. **挑一個 framework 的 Quickstart** — 選 LangGraph 或 CrewAI，把官方教學從頭跑到尾

## 🤔 什麼是 multi-agent framework？

### 兩個維度先分清楚（workflow vs agent / single vs multi）

要看懂 multi-agent framework 之前、有一個有用的釐清方式——把 **workflow vs agent** 跟 **single vs multi LLM** 當成兩個正交維度。Anthropic「Building Effective Agents」原文的核心區分是 workflow（固定 code path）vs agent（LLM 自主決定 next step）；我們把它跟 single/multi 疊起來看 4 個象限：

| | **Workflow**<br>（你寫好的 code path） | **Agent**<br>（LLM 動態決定下一步） |
|---|---|---|
| **Single LLM** | 線性 pipeline、無分支判斷 | 一個 LLM + ReAct loop、自己 plan + adapt<br>（**Stage 3 寫的就是這個**） |
| **Multi LLM** | 預設 routing（譬如「銷售問題 → agent A、技術問題 → agent B」） | 2+ agent 互相 handoff、orchestrator 動態分配<br>（**本 stage 主題**） |

**為什麼這個區分有用**：production 場景大多落在「single agent workflow」+「single agent」象限——多數任務根本不需要 multi-agent。**真正需要 multi-agent framework 的是右下角象限**——LLM 自主性高 + 多角色協作。但實作上四個象限的邊界有時模糊（LangGraph 的 conditional edge 可以同時看成 workflow routing 跟 agent 動態決策）、不要把這個 matrix 當互斥分類。

### Single-agent vs multi-agent — 一張對照表先看清楚差異

| 維度 | **Single-agent**（你 Stage 3 寫過了） | **Multi-agent system** |
|---|---|---|
| **架構** | 一個 LLM + ReAct loop + 若干 tools | 2+ LLM、各有角色（researcher / writer / critic ...）、orchestrator 協調 |
| **怎麼決策** | 同一個 LLM 從頭想到尾 | 角色拆分 + handoff、不同 LLM instance 看不同視角 |
| **State 管理** | 線性 message history | shared state / message passing / checkpoint |
| **適合場景** | 邏輯線性、tool < 20-30 個、單一目標 | 任務可分解、需要 perspective diversity、長 workflow、平行化 |
| **Debug 成本** | 低（單一 loop 可以一路 trace） | 高（cross-agent 互動、error propagation 難定位） |
| **Token 成本** | 1x | 通常 **3-10x**（每個 sub-agent 都有自己的 prompt + thinking + tool call）|
| **Latency** | 低 | 高（除非 sub-agent 平行跑） |

### 什麼時候**真的**需要 multi-agent（不要硬上）

**Multi-agent 不是 default、是 last resort**。**Anthropic 跟 Cognition 兩家 frontier lab 在 2024-2025 都明白寫過：90% 用例其實不該用 multi-agent。** 硬上會付三個代價：**3-10× token、debug 痛苦、context fragmentation**——context 被切散在多個 agent、彼此看不到全貌。

| 立場 | 來源 | 核心論點 |
|---|---|---|
| **Anthropic** | [Building Effective Agents (2024)](https://www.anthropic.com/engineering/building-effective-agents)、[How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/built-multi-agent-research-system) | 多數場景 simple workflow + single agent 就夠；multi-agent 只在「**研究型 / 並行探索**」任務真的有幫助 |
| **Cognition** | [Don't Build Multi-Agents (2025)](https://cognition.ai/blog/dont-build-multi-agents) | multi-agent 的 context fragmentation 嚴重、shared state 維護痛苦；先窮盡 single-agent + long-context 才考慮 |

需要 multi-agent 通常是這 4 個信號之一：

| 信號 | 描述 | 對應 pattern |
|---|---|---|
| **1. 任務天然分解** | 大任務有清楚的子步驟、step-by-step 完成 | Sequential / Planner-Executor |
| **2. Token explosion** | single agent prompt 塞不下所有 tool description / context | Supervisor-Worker（分流給 sub-agent）|
| **3. 角色衝突** | 同一個 LLM 既當 writer 又當 critic 會 self-justify | Debate / Peer review |
| **4. 平行加速** | 3 個 research 子任務同時跑、wall-clock 1/3 | Parallel / Map-Reduce 變種 |

### Multi-agent 經典 pattern（按複雜度排序）

| Pattern | 複雜度 | 什麼樣 | 經典場景 | 代表 framework / paper |
|---|---|---|---|---|
| **1. Routing / Handoff** | ⭐ | agent 之間 1:1 handoff、無中央 orchestrator | customer support routing、context switch | [OpenAI Swarm](https://github.com/openai/swarm)、[OpenAI Agents SDK](https://github.com/openai/openai-agents-python) |
| **2. Sequential**<br>（Planner → Executor） | ⭐⭐ | planner 規劃多步驟 + executor 執行 | 多步驟自動化、code generation | LangGraph、[ChatDev paper](https://arxiv.org/abs/2307.07924) |
| **3. Parallel**<br>（平行加速） | ⭐⭐⭐ | N 個 agent 同時跑、結果 aggregate | research / map-reduce 任務、wall-clock 1/N | LangGraph parallel branches、CrewAI parallel tasks |
| **4. Supervisor-Worker**<br>（hub-spoke） | ⭐⭐⭐ | 1 主 + N worker、主分配 + 整合 | 任務拆解、報告整合 | LangGraph、AutoGen GroupChat |
| **5. Debate / Society**<br>（多視角收斂） | ⭐⭐⭐⭐ | 2+ agent 互相 critique 或角色扮演 | research、judgment task、social simulation | AutoGen GroupChat、[CAMEL paper](https://arxiv.org/abs/2303.17760)、[Generative Agents paper](https://arxiv.org/abs/2304.03442) |

### Framework 的工作

Framework 把上面這 5 個 pattern 的 orchestration boilerplate（roles、handoff、state、retry、checkpoint、HITL pause）抽出來、讓你只寫角色定義跟任務描述。

## 🛠 進階 tool patterns

Framework 提供的三種進階 tool pattern——這三個都需要 framework 抽象層才寫得乾淨：

| Pattern | 解決什麼問題 | 代表實作 |
|---|---|---|
| **Dynamic tool selection** | 工具 > 30 個時、`tools=[...]` 塞不下 prompt | LlamaIndex tool router — embedding-based 路由 |
| **Tool composition / chaining** | tool A output → tool B input、不要 LLM 中間 narrative | LangGraph state graph、CrewAI sequential tasks |
| **Tool-augmented retrieval** | tool 本身是 RAG search → 回結果再 reason | LangGraph 直接把 retriever 包成 tool node |

## 🛠 動手練習

### 練習 1：同一個 agent、兩個 framework
用 LangGraph 和 CrewAI 各做一次同樣的簡單 agent（搜尋 + 摘要）。

### 練習 2：多 agent 角色分配
用 CrewAI 做一個 2-3 個 agent、各自有不同角色一起完成同一個任務的 demo。

### 練習 3：圖式 workflow
用 LangGraph 做一個有分支邏輯跟 human-in-the-loop checkpoint 的 workflow。

### 練習 4：CodeAct vs JSON tool
用 Smolagents 做一個會寫 Python 程式碼當作 action 的 agent（CodeAct pattern）。

### 練習 5：型別安全 agent
用 Pydantic AI 做一個會回傳結構化輸出的 agent。

## 🎯 精選 Projects

按用途分 5 類、16 個項目：

| 分類 | Project | 適合誰 |
|---|---|---|
| **Production 級** | LangGraph, Semantic Kernel, Agno, Microsoft Agent Framework | Production multi-agent + 稽核軌跡 |
| **快速雛形 / 多 agent** | CrewAI, AutoGen/AG2, OpenAI Agents SDK, deepagents, OpenAI Swarm, Strands Agents (AWS) | 角色驅動快速雛形 |
| **特殊路線** | Smolagents (CodeAct), Pydantic AI, Letta (MemGPT) | CodeAct / typed / memory-first |
| **特化** | LlamaIndex Agents, agentscope, LangChain | 文件密集型 / 視覺化 debug |
| **基礎設施** | litellm | 跨 provider 切換 |
