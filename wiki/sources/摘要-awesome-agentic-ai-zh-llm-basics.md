---
title: "摘要-awesome-agentic-ai-zh-llm-basics"
type: source
tags: [LLM, API, 学习路线, token, context window]
sources: [raw/01-articles/awesome-agentic-ai-zh-stage-01-llm-basics.md]
last_updated: 2026-07-10
---

## 核心摘要

该资料是 "awesome-agentic-ai-zh" Agentic AI 系统学习路线图的 **Stage 1——LLM 基础（LLM Basics）**，涵盖从零开始使用 LLM API 的所有必要基础知识。核心内容包括：LLM 三大核心概念（token、context window、temperature）的原理解释与实际影响、主流 LLM 家族对比（美系商业前沿 3 家、中国商业+开源 7 家、西方开源 4 家）、第一次 API 调用的完整代码实践、跨供应商比较方法、错误处理与指数退避重试、以及本地 LLM（Ollama）部署入门。每个练习均配有 Ollama（本机免费）和 Anthropic（云端品质）双路径可运行代码。

## 关键提炼

- **三大核心概念**：token（计费与长度基本单位）、context window（单次能处理的 token 上限）、temperature（输出随机性控制参数 0.0~1.0）
- **Next-token prediction 机制**：LLM 核心动作为预测下一个 token 的概率分布并抽样，temperature 与 top_p 控制如何重塑该分布
- **LLM 家族全景（2026-05 快照）**：Claude/GPT/Gemini 三大美系前沿 + DeepSeek/Kimi/Hunyuan/MiniMax 等中国商业 + Qwen/GLM/Yi 等开源 + Llama/Gemma/Mistral/Phi 等西方自托管
- **API 调用双模式**：Ollama 使用 OpenAI 兼容 SDK（`base_url="http://localhost:11434/v1"`），Anthropic 使用独立 SDK（`anthropic` 包）
- **成本对比方法论**：本机 Ollama $0/次但有延迟成本（CPU ~5-30s/次），云 API 按 token 计费但速度快 5-15 倍
- **生产 vs 学习决策**：学习/实验/debug 全用本机 Ollama，生产场景才考虑云 API

## 关联连接

- [[Context_Window]] — LLM 上下文视窗概念详解
- [[BPE_Tokenizer]] — 底层分词算法解释 token 中文效率差异
- [[Temperature_Parameter]] — 温度参数控制输出确定性
- [[Prompt_Engineering]] — 本路线图 Stage 2，提示词工程进阶
- [[Ollama]] — 本机练习默认的 LLM 运行环境
- [[Anthropic]] — 云端练习路径的 API 提供商
- [[OpenAI]] — GPT 模型家族开发商
- [[Llama]] — Meta 开源 LLM 系列
- [[DeepSeek]] — 中国高性价比 LLM API
- [[Qwen]] — 阿里云通义千问开源系列
- [[摘要-awesome-agentic-ai-zh-foundations]] — 本路线图 Stage 0，先修基础
