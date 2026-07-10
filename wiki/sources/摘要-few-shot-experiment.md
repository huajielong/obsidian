---
title: "摘要-few-shot-experiment"
type: source
tags: [来源, few-shot, prompt-engineering, deepseek, llama, ollama]
sources: [raw/01-articles/Few-Shot-实验对比.md]
last_updated: 2026-07-10
---

## 核心摘要

Few-Shot 系统性实验：对比 deepseek-v4-pro 云端强模型与 llama3.2:3b 本地弱模型在意图分类和 JSON 结构化提取任务上的 few-shot 效果差异。核心发现：Few-shot 对小模型更有效（llama 3B 提升 +10%），而强模型 0-shot 已接近天花板。另发现 qwen3.5:0.8b 通过 Ollama OpenAI 兼容接口返回空内容的兼容性问题。

## 关联连接

- [[Few_Shot_Prompting]] — 实验数据补充
- [[DeepSeek]] — 实验使用的云端模型
- [[Llama]] — 实验使用的本地弱模型
- [[Qwen]] — 实验中暴露兼容性问题的模型
- [[Ollama]] — 本地推理框架
- [[Prompt_Engineering]] — Few-shot 是提示词工程核心技术之一
- [[摘要-deepseek-api-error-handling]] — 同为 DeepSeek API 实验系列
- [[摘要-system-prompt-experiment]] — 同为 DeepSeek API 实验系列
