---
title: "摘要-llm-tool-calling-practice"
type: source
tags: [工具调用, function calling, ReAct, 实践, Ollama, qwen2.5, Claude]
sources: [raw/01-articles/LLM工具调用入门实践.md, raw/01-articles/Tool Description 边界互斥实验.md, raw/01-articles/从零实现 ReAct 循环.md, raw/01-articles/多步骤推理任务 — 连续 Tool 调用.md]
last_updated: 2026-07-15
---

## 核心摘要

四篇 LLM Tool Calling 动手实践练习，从入门到多步骤推理链逐步进阶，全部基于本地 Ollama（qwen2.5:3b）+ 云端 Anthropic（Claude Haiku）双平台验证。核心涵盖两种主流工具调用协议（OpenAI 兼容格式 vs Anthropic 原生格式）的对比、Tool Description 质量对路由准确性的实验验证、从零实现 ReAct 循环的完整代码框架、以及多步骤推理链的数据依赖管理。

## 关键提炼

### 两种工具调用协议对比

| 维度 | OpenAI 兼容（Ollama/qwen） | Anthropic 原生（Claude） |
|------|---------------------------|------------------------|
| Schema 结构 | `{"type":"function","function":{name,description,parameters}}` | `{name,description,input_schema}` |
| 参数键名 | `parameters` | `input_schema` |
| 停止原因 | `finish_reason == "tool_call"` | `stop_reason == "tool_use"` |
| 参数提取 | `json.loads(tc.function.arguments)` | `tc.input`（已是对象） |
| 运行方式 | 本地（Ollama + 小模型） | 云端 API |

### Tool Description 边界互斥四原则

1. **边界互斥** — 不同 tool 的 description 语义上不能有交叉（"日历"和"搜索"都隐含"查信息"就会撞）
2. **写给人看 ≠ 写给模型看** — "日历"是人类标签，但模型需要"查询指定日期的事件"
3. **小模型对质量更敏感** — qwen2.5:3b 对 description 措辞变化反应明显
4. **参数优先做 A/B 测试** — 用工厂函数将变量收拢成一个参数，快速对比排除干扰

### ReAct 循环核心规则

1. LLM 输出必须追回 messages — `role: "assistant"` 保留 `content` + `tool_calls`
2. 工具结果必须追回 messages — `role: "tool"` + 匹配的 `tool_call_id`
3. 没有 tool_calls 就是终止 — LLM 不再调用工具时，`msg.content` 即最终答案

### 多步骤推理的关键特征

后一步依赖前一步的输出值作为输入——这是多步骤推理区别于单步调用的关键。四个独特挑战：任务规划、依赖管理、上下文跟踪、错误传播。

## 关联连接

- [[Tool_Calling]] — 工具调用核心概念：两种协议格式对比、Schema 设计、Description 优化四原则
- [[Agent_Loop]] — ReAct 循环是该系列第三个练习的核心运行机制
- [[Ollama]] — 本地实验环境，默认模型 qwen2.5:3b
- [[Qwen]] — 默认练习模型，tool-use 支援稳定
- [[Anthropic]] — 云端练习路径的 API 提供商
- [[OpenAI_Compatible_API]] — Ollama 使用该标准暴露接口
- [[摘要-awesome-agentic-ai-zh-tool-use]] — Stage 3 理论版本，与此实践系列形成理论+动手互补
- [[Orchestration_Code_Examples]] — Multi-agent 编排示例，ReAct 是单 Agent 基础
