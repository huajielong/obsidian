---
title: "LlamaCpp"
type: entity
tags: [工具, 推理引擎, 本地LLM, CUDA, 开源]
sources: [raw/01-articles/Claude-Code-本地模型接入指南.md, raw/01-articles/本地模型执行指南.md]
last_updated: 2026-11-02
---

## 定义

llama.cpp 是 Georgi Gerganov 发起的 C/C++ 大语言模型推理引擎，直接加载 GGUF 量化模型文件，支持 CPU/GPU 混合推理与 OpenAI 兼容的 HTTP Server。本机使用 CUDA 版 b12017 运行 Qwen3.6 与 Gemma 4，是本机本地推理的主力后端。

## 关键信息

- **本机版本**：CUDA 版 b12017，路径 `D:\AI\llama.cpp\b12017`
- **服务形态**：`llama-server.exe` 提供 HTTP 服务与自带聊天界面
- **端口分配**：Qwen 8081、Gemma 8082；健康检查 `/health`；OpenAI 兼容接口 `/v1`
- **模型复用**：直接读取 Ollama 下载的 GGUF blob，无需重复下载模型
- **性能优势**：同一 Qwen3.6，llama.cpp 约 65 tok/s，Ollama 0.40.13 约 6.6 tok/s；Gemma 4 约 34 vs 5.3 tok/s
- **关键能力**：
  - `--n-cpu-moe`：MoE 专家按层卸载到 CPU，是 12GB 显存跑 35B MoE 的关键
  - `--spec-type draft-mtp`：MTP 投机解码，实测 45.6 → 64.8 tok/s
  - `-ctk/-ctv q8_0`：KV cache 量化
  - `--mmproj`：Gemma 4 视觉投影
  - `--jinja`：启用模型自带 chat template
- **启动脚本**：`D:\AI\llama.cpp\start-qwen.bat` / `start-gemma.bat` / `stop-llama.bat`
- **限制**：启动脚本写死了 Ollama blob 路径；模型 hash 变化后需用 `ollama show --modelfile` 更新 `-m`

## 关联连接

- [[本地推理性能调优]] — 参数调优方法论
- [[Ollama]] — 模型来源与备用运行时
- [[Qwen]] — Qwen3.6 主力模型
- [[Gemma]] — Gemma 4 / TranslateGemma
- [[Claude_Code_本地模型接入]] — Claude Code 的本地推理后端
- [[Anthropic_Proxy]] — 协议转换层
- [[本地_LLM_推理]] — 上位概念
- [[摘要-本地模型执行指南]] — 来源
- [[摘要-claude-code-本地模型接入指南]] — 来源
