---
title: "本地_LLM_推理"
type: concept
tags: [LLM, 推理, 本地部署, 隐私]
sources:
  - raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md
  - raw/01-articles/claude-code-ollama-local-setup.md
  - raw/01-articles/Claude-Code-本地模型接入指南.md
  - raw/01-articles/本地模型执行指南.md
last_updated: 2026-11-02
---

## 定义

本地 LLM 推理（Local LLM Inference）是指在用户自己的硬件设备上运行大语言模型，而非通过云端 API 调用。这种方式的核心优势是数据隐私——所有输入输出数据均在本地处理，无需上传到第三方服务器。Ollama 是目前最流行的本地 LLM 运行工具之一。

## 关键信息

- **隐私优势**：数据不出本地，适合敏感场景
- **硬件要求**：主要依赖 CPU/GPU，集成显卡通常被 Ollama 自动跳过
- **推理速度**：取决于硬件与推理后端；CPU 推理通常较慢（8-18 token/s 量级），GPU + llama.cpp 可显著提升
- **主流工具**：Ollama、LM Studio、vLLM、llama.cpp
- **API 标准化**：多数工具支持 OpenAI 兼容 API，降低迁移成本

### 常见痛点

1. **编码问题**：Windows 终端默认 GBK 编码与 UTF-8 输出冲突
2. **模型兼容性**：同一工具对不同模型的支持程度不同
3. **下载卡顿**：大模型文件（1-10 GB 不等）下载易受网络波动影响
4. **推理速度**：CPU 推理速度远低于 GPU，响应延迟明显
5. **端口冲突**：多个进程监听同一端口导致启动失败

## 本机硬件与后端选择

本机配置：COLORFUL P16 Pro IXA1，RTX 5070 Ti Laptop 12GB，i7-14650HX（16C/24T），64GB DDR5-5600，Windows 11。

| 后端 | 代表模型 | 本机速度 | 结论 |
|------|----------|----------|------|
| llama.cpp（CUDA b12017） | Qwen3.6-35B-A3B | 约 65 tok/s | 大模型主力 |
| Ollama 0.40.13 | Qwen3.6-35B-A3B | 约 6.6 tok/s | 模型管理 / 翻译 / 小模型 |
| llama.cpp | Gemma 4 12B | 约 34 tok/s | 快速多模态 |

关键原因：Ollama 0.40.x 对 Qwen3.6 / Gemma 4 等新架构不支持 MoE 专家卸载，只能整层卸载到 CPU；llama.cpp 支持 `--n-cpu-moe`、MTP 投机解码与 KV cache 量化，同一 GGUF 可快 6–10 倍。详见 [[本地推理性能调优]]。

## Claude Code 接入本地模型

本地 LLM 不仅能通过 API 被脚本调用，也可以作为 [[Claude_Code]] 这类 Agent 工具的模型后端。做法是通过环境变量把 Anthropic API 端点重定向到本地服务，有两条路径：

| 路径 | 链路 | 本机实测 |
|------|------|----------|
| 代理 + llama.cpp（推荐） | Claude Code → [[Anthropic_Proxy|anthropic-proxy]] 8787 → [[LlamaCpp|llama.cpp]] 8081 | 约 65 tok/s |
| 直连 Ollama | Claude Code → [[Ollama]] 11434 | 约 6.6 tok/s |

代理路径示例：

```bash
ANTHROPIC_BASE_URL=http://127.0.0.1:8787 \
ANTHROPIC_API_KEY=anything \
ANTHROPIC_AUTH_TOKEN=anything \
CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1 \
claude --model claude-sonnet-4-6
```

**通用教程的按内存选型**

| 内存 | 推荐模型 | 定位 |
|------|----------|------|
| ≤16GB | qwen2.5-coder:14b | 轻量代码模型 |
| 32GB | glm-4.7-flash | 推荐默认项，约 19GB 下载 |
| 48GB+ | glm-4.7 | 大内存档位 |

**本机实际（12GB 显存）**

| 资源 | 选择 | 实测 |
|------|------|------|
| RTX 5070 Ti Laptop 12GB + 64GB RAM | Qwen3.6-35B-A3B（Q4_K_M） | 约 65 tok/s，10.8GB 显存 |
| 多模态 / 翻译 | Gemma 4 12B / TranslateGemma 4B | 约 34 / 78 tok/s |

- **优势**：零边际成本、数据不出本机、可离线使用
- **代价**：本地模型能力通常弱于云端模型，推理速度受 RAM/VRAM 限制
- **工程要点**：用 shell 别名（如 `claude-local`）隔离环境变量，避免污染常规 `claude` 配置
- **隐私边界**：模型推理在本地，但 Claude Code 客户端本身可能联网
- 详见 [[Claude_Code_本地模型接入]]；性能调优见 [[本地推理性能调优]]

## 关联连接
- [[Ollama]] — 最流行的本地 LLM 运行工具
- [[Llama]] — 常用的本地推理开源模型
- [[Qwen]] — 常用的本地推理开源模型
- [[OpenAI_Compatible_API]] — 本地推理工具的标准化接口
- [[GPT]] — 大语言模型的基础概念
- [[Claude_Code]] — 可在本地模型上运行的终端编码 Agent
- [[Claude_Code_本地模型接入]] — 环境变量重定向与别名隔离模式
- [[LlamaCpp]] — 本机大模型的主力推理引擎
- [[Anthropic_Proxy]] — Anthropic → OpenAI 协议转换代理
- [[Anthropic_Compatible_API]] — 本地接入所依赖的接口契约
- [[本地推理性能调优]] — 后端选择、量化与显存调优
- [[Gemma]] — Gemma 4 / TranslateGemma 本地模型
- [[GLM]] — 通用教程推荐的本地模型系列
- [[摘要-claude-code-ollama-local-setup]] — 通用安装指南来源
- [[摘要-claude-code-本地模型接入指南]] — 本机代理版实施记录来源
- [[摘要-本地模型执行指南]] — 同机模型与调优手册
