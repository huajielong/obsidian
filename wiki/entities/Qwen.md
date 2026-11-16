---
title: "Qwen"
type: entity
tags: [模型, 阿里云, 开源, LLM]
sources:
  - raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md
  - raw/01-articles/claude-code-ollama-local-setup.md
  - raw/01-articles/Claude-Code-本地模型接入指南.md
  - raw/01-articles/本地模型执行指南.md
last_updated: 2026-11-02
---

## 定义

Qwen（通义千问）是阿里云推出的开源大语言模型系列，包含从 0.5B 到 72B 不等参数规模的模型，也包含 Qwen3.6-35B-A3B 这类 MoE 架构模型。Qwen 系列在 Ollama / llama.cpp 生态中广泛使用，但部分版本存在 API 兼容性问题。

## 关键信息

- **开发者**：阿里云（Alibaba Cloud）
- **模型范围**：0.5B ~ 72B 参数
- **Ollama 兼容性**：原生 API 正常，但 qwen3.5:0.8b 在 OpenAI 兼容端口下存在 `content` 字段返回空字符串的 Bug
- **模型大小示例**：qwen3.5:0.8b 约 1.0 GB
- **CPU 推理速度**：qwen3.5:0.8b 在 CPU 上约 18.6 token/s
- **本地编码 Agent 选型**：`qwen2.5-coder:14b` 是 ≤16GB 内存设备运行 [[Claude_Code]] 本地模型的推荐档位（见 [[Claude_Code_本地模型接入]]）
- **Qwen3.6-35B-A3B-MTP**：本机主力模型，`qwen3.6:35b-a3b-mtp-q4_K_M`，qwen35moe / 35.5B，Q4_K_M 量化，文件约 22GB，原生上下文 262144，支持文本、图片、tools、thinking，Apache 2.0
- **本机实测性能**：llama.cpp 生成 64.8 tok/s、prompt 54.9 tok/s、32K 上下文、显存 10.8GB；Ollama 0.40.13 直连仅约 6.6 tok/s
- **Claude Code 角色**：作为 `claude-local` 的实际模型，经 [[Anthropic_Proxy]] 映射为 `qwen`；`llama-server -a qwen` 中的 `-a` 即模型别名
- **MoE 特点**：35B 总参数、3B 激活参数（A3B），可在 12GB 显存上通过 `--n-cpu-moe` 专家卸载运行

### 已知兼容问题

qwen3.5:0.8b 在 Ollama 的 OpenAI 兼容 API 下：调用成功、Token 正常消耗、`finish_reason="length"`，但 `content` 字段为空。这是模型与 Ollama 版本间的兼容问题，非代码错误。建议换用 `qwen2.5:3b` 或 `llama3.2:3b`。

## 关联连接
- [[Ollama]] — 运行 Qwen 模型的本地推理工具
- [[Llama]] — 同为 Ollama 生态的另一模型系列
- [[OpenAI_Compatible_API]] — Qwen 在 OpenAI 兼容端口下存在已知 Bug
- [[Claude_Code]] — 可用 qwen2.5-coder:14b 或 Qwen3.6 作为本地模型后端
- [[Claude_Code_本地模型接入]] — 本地接入模式与性能对比
- [[LlamaCpp]] — 本机运行 Qwen3.6 的主力推理引擎
- [[Anthropic_Proxy]] — 把 Claude Code 请求映射到 `qwen` 的代理
- [[本地推理性能调优]] — Qwen3.6 的 MoE 卸载与调参方法
- [[GLM]] — 通用教程推荐的另一模型系列
- [[摘要-claude-code-ollama-local-setup]] — 通用模型选型来源
- [[摘要-claude-code-本地模型接入指南]] — 本机 Qwen3.6 实施记录来源
- [[摘要-本地模型执行指南]] — Qwen3.6 性能数据来源
