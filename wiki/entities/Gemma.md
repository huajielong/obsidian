---
title: "Gemma"
type: entity
tags: [模型, Google, 开源, LLM]
sources: [raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md, raw/09-archive/【生成式人工智慧與機器學習導論2025】第 2 講：上下文工程 (Context Engineering) — AI Agent 背後的關鍵技術.md]
last_updated: 2026-08-05
---

## 定义

**Gemma** 是 Google 开源的轻量级大语言模型系列（区别于 Google 闭源的 Gemini 产品线）。课程演示中以其 **Gemma-3-4B-it** 作为作业模型：性能优于 Meta Llama 第三代，中文能力更好，较少出现 Llama 那种中英夹杂的表述。

## 关键信息

- **开发者**：Google
- **开源属性**：权重公开可下载（完整训练细节不公开，严格来说不算完全开源）。
- **命名解读**：`Gemma-3-4B-it` —— 3 = 系列版本，4B = 40 亿参数，`it` = instruction-tuned（理解指令并回复）。
- **课程中的角色**：李宏毅《生成式人工智慧與機器學習導論2025》作业一指定模型——把演示用的 Llama 换成 `google/gemma-3-4b-it` 即可跑通聊天机器人。
- **第 2 讲工具调用演示**：李宏毅用 **Gemma 2 9B**（`pipeline` 加载）在 Colab 演示 Tool Calling——通过 `<tool>` / `<tool_output>` 文本标记协议 + 开发者 `eval()` 循环真正驱动 `multiply`/`divide` 工具，并指出 Gemma 没有独立 tool role、工具输出需用专属标记避免被误判为用户消息。
- **特点（课程观察）**：比 Llama 3 代晚出、性能更好；中文能力较强、不轻易中英夹杂。
- **与 Gemini 的区别**：Gemma 开源可自托管；Gemini 是 Google 的闭源商业模型（通过网页/API 交互）。

## 关联连接

- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — 本实体的来源（作业一：Gemma-3-4B-it）
- [[摘要-hung-yi-lee-上下文工程-第2讲]] — 本实体工具调用演示（Gemma 2 9B + eval 循环）的来源
- [[Llama]] — 同为开源模型，课程中的对比对象（Llama 用于课堂演示、Gemma 用于作业）
- [[Hugging_Face]] — Gemma 在 HF 平台发布/下载
- [[本地_LLM_推理]] — 开源权重可本地部署推理
- [[Ollama]] — 本地运行 Gemma 等模型的工具
