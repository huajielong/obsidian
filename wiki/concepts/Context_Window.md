---
title: "Context_Window"
type: concept
tags: [LLM基础, context window, 上下文, token]
sources: [raw/01-articles/awesome-agentic-ai-zh-stage-01-llm-basics.md]
last_updated: 2026-07-10
---

# Context Window（上下文视窗）

Context Window（上下文视窗）是 **LLM 单次推理能"看到"的最大 token 数量上限**。它决定了模型在生成回复时能同时参考多少对话历史、文档内容或外部信息。

## 主流模型 Context Window 对比（2026 年）

| 模型家族 | Context Window 上限 | 换算中文字数（约） |
|---------|:------------------:|:-----------------:|
| **Claude**（Anthropic） | 1M tokens（Sonnet 5/Opus 4.8） | ~50 万中文字 |
| **Gemini**（Google） | 2M tokens（Pro 系列） | ~100 万中文字 |
| **GPT**（OpenAI） | ~400k tokens | ~20 万中文字 |
| **Kimi**（Moonshot） | 1M+ tokens | ~50 万中文字 |
| **Qwen3**（阿里云） | 128k+ tokens | ~6 万中文字 |
| **DeepSeek V3** | 128k tokens | ~6 万中文字 |

> ⚠️ 中文效率注意：由于 Tokenizer 对中文的处理效率较低（约 1 字 ≈ 2 token，而非英文的 1 词 ≈ 1 token），中文实际可容纳内容量约为英文的 1/2~1/3。详见 [[BPE_Tokenizer]]。

## 实际影响

- **大窗口 ≠ 更好**：超过一定阈值后，模型对窗口中间内容的"注意力"会衰减，长上下文中的关键信息可能被忽略
- **成本线性增长**：input token 数直接影响 API 费用（多数模型按 token 计费）
- **任务类型选择**：整本书分析需要 1M+ 窗口（Gemini/Kimi）；常规对话 32k~128k 已足够
- **Agent 场景**：多轮对话 + 工具调用结果会快速消耗窗口，需结合 [[Context_Engineering]] 管理

## 关联连接

- [[BPE_Tokenizer]] — Tokenizer 效率差异导致中英文实际可容纳量不同
- [[Temperature_Parameter]] — 与 Context Window 并列的三大核心参数之一
- [[GPT]] — GPT 系列的上下文窗口限制
- [[Context_Engineering]] — 如何在有限的上下文窗口中高效组织信息
- [[摘要-awesome-agentic-ai-zh-llm-basics]] — 来源资料
