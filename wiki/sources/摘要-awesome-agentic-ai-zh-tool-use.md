---
title: "摘要-awesome-agentic-ai-zh-tool-use"
type: source
tags: [工具使用, 学习路线, function calling, ReAct, Agent, LLM]
sources: [raw/09-archive/awesome-agentic-ai-zh-stage-03-tool-use.md]
last_updated: 2026-07-10
---

## 核心摘要

该资料是 "awesome-agentic-ai-zh" Agentic AI 系统学习路线图的 **Stage 3——工具使用与第一个 Agent（Tool Use & Hello Agent）**，提供从 LLM 提示工程到 Agent 构建的关键跨越教程。核心涵盖：Agent 的三个最小必要部件（LLM + Tools + Loop）、Function Calling 底层机制、从零实现 ReAct（Thought → Action → Observation）循环、多步骤推理任务拆解、Tool Error 的结构化处理，以及 Function Schema 设计的最佳实践。配有 **6 个动手练习**，覆盖单一工具调用到完整 ReAct Agent 搭建的完整路径。

## 关键提炼

- **Agent 的三部件模型**：🧠 LLM（大脑/推理决策）+ 🔧 Tools（手/对世界行动）+ 🔁 Loop（心跳/ReAct 循环）
- **Function Calling 核心**：定义 tool schema（name + description + parameters）→ LLM 返回 tool_call → 执行工具 → 结果回填 message history
- **ReAct 循环精髓（13 行代码）**：assistant message（含 tool_calls）→ 执行工具 → tool message → 再次调用 LLM → 直到无 tool_calls 结束
- **三大常见踩坑**：忘记追加 assistant message 导致无限循环、tool message 缺 `tool_call_id`、没设 `max_iter` 导致无限调用
- **错误处理哲学**：Production 的 retry 不在 Python 层、而在 LLM 层——工具返回结构化 error dict 让 LLM 自主决定如何恢复
- **Schema 设计 4 项改进**：`name` 要具体、`description` 写"何时用"而非"做什么"、`type` 强制 `number`、加 `required` + `enum`
- **安全底线**：给 agent 工具 = 给它攻击面——致命三角（私密数据 + 不可信内容 + 对外发送能力）→ prompt injection 根因
- **从 Prompt 到 Tool 的分水岭**：当 prompt 到达极限时（需要实时数据、对世界产生作用、多步 Reasoning），就该切换到 Tool Use

## 关联连接

- [[Agent_Loop]] — ReAct 循环是该资料的核心运行机制，定义 Thought → Action → Observation 范式
- [[Chain_of_Thought]] — CoT（纯推理）与 ReAct（推理+行动）是互补范式，Stage 3 进入带行动的推理
- [[Prompt_Engineering]] — 该资料所在路线图的 Stage 2，提示词到达极限时就需要 Tool Use
- [[Harness_Engineering]] — 三层工程 stack 的最外层，Stage 3 工具使用是 Harness 的前置基础
- [[Ollama]] — 本阶段练习默认的本地 LLM 运行环境，默认模型 qwen2.5:3b
- [[Qwen]] — 默认练习模型，tool-use 支援稳定
- [[Anthropic]] — 云端练习路径的 API 提供商（原生 tool use 格式）
- [[OpenAI]] — Function Calling 标准格式的制定者，OpenAI 兼容 API 已成为行业事实标准
- [[OpenAI_Compatible_API]] — Ollama 使用该标准对外暴露接口
- [[本地_LLM_推理]] — 在本地运行 qwen2.5:3b 等小模型进行 tool-use 实验
- [[摘要-awesome-agentic-ai-zh-foundations]] — 本路线图 Stage 0，先修基础
- [[摘要-awesome-agentic-ai-zh-llm-basics]] — 本路线图 Stage 1，LLM 基础
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 本路线图 Stage 2，Prompt 设计
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本路线图 Stage 4，从单 Agent 进入 Multi-agent 框架
