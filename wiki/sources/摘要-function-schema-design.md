---
title: "摘要-function-schema-design"
type: source
tags: [来源, 原始文件, Tool Calling, Schema设计, Function Calling]
sources: [raw/01-articles/Function Schema 设计 — Bad Schema 修到 Good.md]
last_updated: 2026-07-15
---

# 摘要：Function Schema 设计 — Bad Schema 修到 Good

## 核心摘要

函数 Schema（Function Calling 参数定义）的质量直接决定 LLM 工具调用的准确性——尤其是在使用小模型时。文章通过 qwen2.5:3b 对比 Bad Schema 与 Good Schema 在同一组查询上的表现差异，总结出 4 个关键改进项（name 具体化、description 写"何时用"、type 用对、加 required+enum）和 5 条黄金规则。核心结论：**写 Schema 的功夫能省下换大模型的钱**——Bad Schema 在小模型上全部失败，而 Good Schema 全部正确。

## 关联连接

- [[Tool_Calling]] — 文章实践内容的本体页面（Schema 设计章节已存在但需大幅扩充）
- [[Prompt_Engineering]] — Schema 的 description 本质是一种"写给模型看的提示词"
- [[Ollama]] — 实验运行环境（qwen2.5:3b）
- [[摘要-llm-tool-calling-practice]] — 同系列练习 1-3（基础 Tool Calling 入门）
- [[摘要-多步骤推理任务-连续-tool-调用]] — 同系列练习 4（多步依赖链）
- [[摘要-tool-error-is-data]] — 同系列练习 5（错误处理），两篇互补
