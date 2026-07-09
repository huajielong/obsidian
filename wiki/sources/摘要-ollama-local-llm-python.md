---
title: "摘要-ollama-local-llm-python"
type: source
tags: [来源, ollama, python, llm, api]
sources: [raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md]
last_updated: 2026-07-08
---

## 核心摘要

本文详细记录了在 Windows 环境下使用 Python 调用 Ollama 本地模型的完整实践。介绍了四种 API 调用方式（原生 API 流式/非流式、OpenAI 兼容 API 流式/非流式），并深入剖析了 Windows 平台下的五大常见陷阱：GBK 编码导致的 UnicodeEncodeError、qwen3.5 模型在 OpenAI 兼容端口下的 content 空值 Bug、Ollama 端口冲突、模型下载卡在 94-96% 以及 CPU 推理速度瓶颈。文章提供了一套从零开始的完整解决方案，强调模型兼容性测试的重要性。

## 关联连接
- [[Ollama]] — 本地 LLM 运行工具
- [[Qwen]] — 通义千问模型系列（阿里出品）
- [[Llama]] — Meta 开源大语言模型系列
- [[OpenAI_Compatible_API]] — OpenAI 兼容 API 标准及其在 LLM 生态中的角色
