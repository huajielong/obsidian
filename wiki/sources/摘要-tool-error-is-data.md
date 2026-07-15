---
title: "摘要-tool-error-is-data"
type: source
tags: [来源, 原始文件, Tool Calling, 错误处理, ReAct]
sources: [raw/01-articles/错误处理 — Tool Error 是 Data 不是 Exception.md]
last_updated: 2026-07-15
---

# 摘要：Tool Error 是 Data 不是 Exception

## 核心摘要

Tool Calling 中工具函数的错误处理应将错误作为**结构化 dict 返回**而非抛出 Exception，让 LLM 自己能根据错误类型（transient/fatal）自主决策重试或放弃。文章通过 qwen2.5:3b 运行的 ReAct 循环代码，展示了 transient（暂时性，可重试）和 fatal（致命性，不可重试）两类错误的完整 recovery 流程，并设计了"LLM 层 → Python 层"两层 retry 机制。核心观念翻转：**retry 是业务语义问题，不是基础设施问题**。

## 关联连接

- [[Tool_Calling]] — 文章实践内容的本体页面（错误处理章节）
- [[Agent_Loop]] — ReAct 循环中 Act→Observation 阶段的错误处理设计
- [[Ollama]] — 实验运行环境（qwen2.5:3b）
- [[摘要-多步骤推理任务-连续-tool-调用]] — 同系列练习 4（多步依赖链），本文为练习 5
- [[摘要-llm-tool-calling-practice]] — 同系列练习 1-3
