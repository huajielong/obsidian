---
title: "摘要-多步骤推理任务-连续-tool-调用"
type: source
tags: [来源, 原始文件, Tool Calling, ReAct, 推理链]
sources: [raw/01-articles/多步骤推理任务 — 连续 Tool 调用.md]
last_updated: 2026-07-15
---

## 核心摘要

本文是一篇**多步骤推理与连续 Tool Calling** 的动手实践记录。使用 qwen2.5:3b 本地模型（通过 Ollama 的 OpenAI 兼容 API）完成"查台北人口 → 查纽约人口 → 计算比值 → 转百分比"四个串行依赖步骤。核心发现：小模型倾向于**并行预测所有 tool_calls**，导致下游工具（如 `convert_to_percentage`）在上游计算（`calculator`）尚未完成时就被调用，产生基于猜测的错误结果。文章提出四种解决方案：加大模型、强化 System Prompt、优化 Description 暗示依赖关系、以及**代码层依赖拦截**。

## 关联连接

- [[Tool_Calling]] — 多步调用的依赖链是本篇的核心扩展
- [[Agent_Loop]] — 手写 ReAct 循环的完整代码参考
- [[Ollama]] — 本地运行环境（Ollama + qwen2.5:3b）
- [[Qwen]] — 实际测试的模型（qwen2.5:3b）
- [[摘要-llm-tool-calling-practice]] — 同系列前序实践，本文是该系列的延续
