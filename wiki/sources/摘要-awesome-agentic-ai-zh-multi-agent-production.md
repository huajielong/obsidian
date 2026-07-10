---
title: "摘要-awesome-agentic-ai-zh-multi-agent-production"
type: source
tags: [multi-agent, production, harness-engineering, eval, observability, cost-optimization]
sources: [raw/01-articles/07-multi-agent-production.zh-Hans.md]
last_updated: 2026-07-10
---

# 摘要：Multi-Agent & Production — awesome-agentic-ai-zh Stage 7

> 来源：https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/stages/07-multi-agent-production.zh-Hans.md
> 原始素材已归档至：[[摘要-awesome-agentic-ai-zh-multi-agent-production]]（原始素材在 raw/09-archive/）

本 Stage 是 awesome-agentic-ai-zh 学习路线的**最终章**，覆盖三大主题：**Multi-agent 协作 → Harness Engineering（8 核心元件）→ Production 化部署**。

## 核心产出

### 1. 三层工程分工

| 层级 | 工程对象 | 对应 Stage |
|------|---------|-----------|
| Prompt Engineering | 送进 LLM 的字符串 | Stage 2 |
| Context Engineering | 窗口里装的信息（RAG/Memory） | Stage 6 |
| **Harness Engineering** | 模型外围的执行与控制层 | **本 Stage（核心）** |

### 2. Harness 的 8 个核心元件

| # | 元件 | 说明 | 对应练习 |
|---|------|------|---------|
| 1 | **Agent Loop** | LLM → Tool → Result → LLM 循环 | 练习 1 辩论 |
| 2 | **Tool Registry** | 动态 tool dispatch、permission gate、sandbox | — |
| 3 | **Context Manager** | message history 管理、context window 控制 | 练习 4 SDK |
| 4 | **Safety Layer** | permission prompts、sandboxed exec | — |
| 5 | **Retry / Recovery** | tool fail 处理策略 | 练习 4 SDK |
| 6 | **Telemetry / Observability** | metrics、logging、token counting、trace | 练习 3 |
| 7 | **Eval Harness** | regression test、quality gate、A/B test | 练习 2 |
| 8 | **Cost / Latency** ⭐ | prompt caching、model routing、batching | 练习 6 |

### 3. 反馈循环四时机

| 时机 | 白话 | 工程形式 |
|------|------|---------|
| 工具返回值 | 工具吐回的信息本身就是反馈 | 把错误信息写清楚 |
| 执行中插话 | 在两次思考间调整方向 | 中途注入消息（steering）|
| 单轮结束验收 | 独立验收者比对目标 | Evaluator Agent |
| 外层 Loop | 目标导向重跑 | `/goal`、cron |

### 4. Cost / Latency 优化技术（2026 必修）

| 技巧 | 节省幅度 | 2026 支持状态 |
|------|---------|-------------|
| Prompt Caching | ~90% | Anthropic/OpenAI/Gemini 全支持 |
| Model Routing / Cascade | 50-90% | RouteLLM / OpenRouter 内建 |
| Thinking Budget | 可控 | Claude/Gemini API 参数 |
| Batching | 高吞吐 | vLLM / production inference |
| Semantic Caching | 相似 query 复用 | GPTCache / Helicone |

### 5. ⚠️ UC Berkeley Reward-Hacking 警告（2026-04）

8 个主流 Agent Benchmark（SWE-bench / WebArena / OSWorld / GAIA / Terminal-Bench 等）**全部可被 automated scanning agent reward-hack 到接近 100%**。结论：永远不要只看 leaderboard 数字，跑自己的 hold-out test 才是唯一可靠方法。

### 6. Multi-Agent Pattern

文章重申了 [[Agent_Orchestration_Patterns#五大编排模式|五大编排模式]]，并补充了 Production 层面的判断：**不是 default，而是 last resort**，硬上会付出 3-10× Token 和 Debug 痛苦。

### 7. 工具推荐

按场景分类的入口选择：
- 第一个 Multi-agent → **crewAI**
- 加 Eval → **promptfoo**
- 加 Observability → **langfuse**
- Production 升级 → **LangGraph + BentoML**
- 自架 LLM → **vLLM**
- Fine-tune → **LLaMA-Factory**

> 💡 **关键名词**：multi-agent / orchestration / handoff / eval / observability / harness（模型外围的执行与控制层）

## 关联连接

- [[Harness_Engineering]] — 本 Stage 的核心主题（需大幅扩充 8 元件 + 反馈循环 + 成本优化）
- [[Multi_Agent_System]] — Multi-agent 决策框架与 Production 注意事项
- [[Agent_Orchestration_Patterns]] — 五大编排模式详解
- [[Eval_Harness]] — Agent Eval 标准化方法（本 Stage 新概念）
- [[Agent_Observability]] — Tracing / Logging / Telemetry（本 Stage 新概念）
- [[Cost_Optimization]] — Prompt caching / Model routing / Batching（本 Stage 新概念）
- [[Agent_Loop]] — Agent Loop 设计从 ReAct 到 production 级闭环
- [[Agentic_Coding]] — AI Agent 自主驱动编程
- [[Claude_Code_Harness]] — Claude Code 作为 Reference Harness 实现
- [[摘要-awesome-agentic-ai-zh-foundations]] → [[摘要-awesome-agentic-ai-zh-llm-basics]] → [[摘要-awesome-agentic-ai-zh-prompt-engineering]] → [[摘要-awesome-agentic-ai-zh-tool-use]] → [[摘要-awesome-agentic-ai-zh-agent-frameworks]] → [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] → [[摘要-awesome-agentic-ai-zh-memory-rag]] → **本页面** — 路线图 Stage 0→1→2→3→4→5→6→**7 全部收录完成**
