---
title: "Gemma"
type: entity
tags: [模型, Google, 开源, LLM]
sources:
  - raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md
  - raw/09-archive/【生成式人工智慧與機器學習導論2025】第 2 講：上下文工程 (Context Engineering) — AI Agent 背後的關鍵技術.md
  - raw/01-articles/本地模型执行指南.md
  - raw/01-articles/Claude-Code-本地模型接入指南.md
last_updated: 2026-11-02
---

## 定义

**Gemma** 是 Google 开源的轻量级大语言模型系列（区别于 Google 闭源的 Gemini 产品线）。课程演示中以其 **Gemma-3-4B-it** 作为作业模型：性能优于 Meta Llama 第三代，中文能力更好，较少出现 Llama 那种中英夹杂的表述。本机还使用 **Gemma 4 12B** 做快速多模态，以及 **TranslateGemma 4B** 变体做中英翻译。

## 关键信息

- **开发者**：Google
- **开源属性**：权重公开可下载（完整训练细节不公开，严格来说不算完全开源）。
- **命名解读**：`Gemma-3-4B-it` —— 3 = 系列版本，4B = 40 亿参数，`it` = instruction-tuned（理解指令并回复）。
- **课程中的角色**：李宏毅《生成式人工智慧與機器學習導論2025》作业一指定模型——把演示用的 Llama 换成 `google/gemma-3-4b-it` 即可跑通聊天机器人。
- **第 2 讲工具调用演示**：李宏毅用 **Gemma 2 9B**（`pipeline` 加载）在 Colab 演示 Tool Calling——通过 `<tool>` / `<tool_output>` 文本标记协议 + 开发者 `eval()` 循环真正驱动 `multiply`/`divide` 工具，并指出 Gemma 没有独立 tool role、工具输出需用专属标记避免被误判为用户消息。
- **特点（课程观察）**：比 Llama 3 代晚出、性能更好；中文能力较强、不轻易中英夹杂。
- **与 Gemini 的区别**：Gemma 开源可自托管；Gemini 是 Google 的闭源商业模型（通过网页/API 交互）。
- **Gemma 4 12B（本机）**：`gemma4:12b`，gemma4 / 11.9B，Q4_K_M，文件约 8GB，原生上下文 262144，支持文本、图片、音频、tools、thinking；llama.cpp 实测生成 33.8 tok/s、prompt 171 tok/s、32K 上下文、显存 7.9GB
- **TranslateGemma 4B（本机）**：gemma3 / 4.3B，Q4_K_M，3.3GB；`translategemma-2k` 为 GPU 版（约 78 tok/s，3.6GB），`translategemma-cpu` 为 CPU 版（0 显存，约 22 tok/s）；上下文固定 2048，需配合专用翻译提示词
- **Claude Code 边界**：Gemma 4 / TranslateGemma 不作为 Claude Code 主模型；工具调用主模型是 [[Qwen|Qwen3.6]]

## 关联连接

- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — 本实体的来源（作业一：Gemma-3-4B-it）
- [[摘要-hung-yi-lee-上下文工程-第2讲]] — 本实体工具调用演示（Gemma 2 9B + eval 循环）的来源
- [[Llama]] — 同为开源模型，课程中的对比对象（Llama 用于课堂演示、Gemma 用于作业）
- [[Hugging_Face]] — Gemma 在 HF 平台发布/下载
- [[本地_LLM_推理]] — 开源权重可本地部署推理
- [[Ollama]] — 本地运行 Gemma 等模型的工具
- [[LlamaCpp]] — 本机运行 Gemma 4 的推理引擎
- [[本地推理性能调优]] — Gemma 4 / TranslateGemma 的显存与参数调优
- [[摘要-本地模型执行指南]] — 同机 Gemma 4 / TranslateGemma 性能数据来源
- [[摘要-claude-code-本地模型接入指南]] — 同机组件清单来源
