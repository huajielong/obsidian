---
title: "GLM"
type: entity
tags: [模型, 智谱, 开源, 本地LLM]
sources:
  - raw/01-articles/claude-code-ollama-local-setup.md
  - raw/01-articles/Claude-Code-本地模型接入指南.md
last_updated: 2026-11-02
---

## 定义

GLM 是智谱 AI（Zhipu AI）推出的大语言模型系列。在本知识库收录的 Claude Code 本地化指南中，GLM 被推荐为本地运行 Claude Code 的主力模型：`glm-4.7-flash` 面向 32GB 内存设备（约 19GB 下载），`glm-4.7` 面向 48GB+ 内存设备。

## 关键信息

- **模型家族**：GLM（智谱 AI）
- **本指南涉及的版本**：

| 模型 | 适用内存 | 说明 |
|------|----------|------|
| glm-4.7-flash | 32GB | 指南推荐默认项，约 19GB 下载 |
| glm-4.7 | 48GB+ | 更高内存档位 |

- **部署方式**：`ollama pull glm-4.7-flash`，通过 [[Ollama]] 在本地运行
- **典型用途**：作为 `claude-local` 的默认模型（`claude --model glm-4.7-flash`）
- **信息边界**：模型的具体参数规模、上下文长度与基准成绩未在来源中给出，本页不做推断
- **本机实践备注**：本机实际部署未采用 GLM。因 12GB 显存与已有 Qwen3.6，`claude-local` 使用 Qwen3.6 + [[LlamaCpp|llama.cpp]] + [[Anthropic_Proxy|anthropic-proxy]]（见 [[Claude_Code_本地模型接入]]）；GLM 仍是通用教程的推荐选项

## 关联连接

- [[Ollama]] — GLM 的本地运行工具
- [[Claude_Code]] — 通过 claude-local 使用 GLM 的 Agent 工具
- [[Claude_Code_本地模型接入]] — 接入模式
- [[本地_LLM_推理]] — 本地推理上位概念
- [[Qwen]] — 本机实际采用的本地模型
- [[LlamaCpp]] — 本机推理引擎
- [[Anthropic_Proxy]] — 本机协议转换代理
- [[本地推理性能调优]] — 12GB 显存下的模型选型依据
- [[摘要-claude-code-ollama-local-setup]] — 通用教程来源
- [[摘要-claude-code-本地模型接入指南]] — 本机实施差异来源
