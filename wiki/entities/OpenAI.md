---
title: "OpenAI"
type: entity
tags: [公司, OpenAI, GPT, API]
sources: [raw/01-articles/awesome-agentic-ai-zh-stage-01-llm-basics.md]
last_updated: 2026-07-10
---

## 定义

OpenAI 是美国 AI 研究公司，GPT（Generative Pre-trained Transformer）系列模型的开发商。其旗舰模型 GPT-5.5/GPT-5.6 preview 在通用任务、function calling 和生态系统广度方面具有显著优势。OpenAI 还推出了 [[Codex]] 编码智能体，并推广了 [[Harness_Engineering]] 概念。

## 关键信息

- **旗舰模型**（2026-06）：
  - **GPT-5.6 preview** — 最新旗舰（限量预览）
  - **GPT-5.5** — 当前主力版本
- **Context Window**：~400k tokens（约 20 万中文字）
- **API 标准**：OpenAI 兼容 API 已成为 LLM 行业事实标准接口规范，被 Ollama、DeepSeek、vLLM 等广泛采用
- **生态优势**：SDK 整合最深、function calling 框架最成熟、GPTs 插件生态最广

### 模型系列

| 等级 | 特点 | 典型用途 |
|:----|:-----|:---------|
| GPT-5 系列 | 通用旗舰，function calling 最强 | 广度查询、函数调用、插件生态 |
| o-series | 推理增强系列（o1/o3） | 复杂推理、数学、科学 |
| GPT-4o 系列 | 多模态，性价比平衡 | 视觉理解、实时对话 |

## 计价原则

OpenAI 按 per-token 计费：
- **Input tokens**：发给模型的内容（system prompt + 对话历史 + 示例）
- **Output tokens**：模型生成的回复
- 按 token 单价 × 数量累计，各模型档次不同

## 关联连接

- [[GPT]] — OpenAI 的核心 LLM 产品系列
- [[Codex]] — OpenAI 编码智能体
- [[OpenAI_Agents_SDK]] — OpenAI 官方 Agent SDK，提供 Agent Hand-off + 结构化输出
- [[Harness_Engineering]] — OpenAI 于 2026-02 正式推广的工程范式
- [[OpenAI_Compatible_API]] — OpenAI 定义的 API 标准已成为行业事实标准
- [[摘要-awesome-agentic-ai-zh-llm-basics]] — 来源资料
