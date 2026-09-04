---
title: "Hugging_Face"
type: entity
tags: [平台, 开源模型, 数据集, 工具, 社区]
sources: [raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md]
last_updated: 2026-08-05
---

## 定义

**Hugging Face** 是 AI 领域最大的开源模型与数据集托管平台，被形容为"模型的 Facebook"——每个模型都有说明页、下载次数与按赞数。公司最初想做聊天机器人（logo 是一个笑脸 + 一双手），后来转型成为开源模型/数据集的集散地，并开发了被广泛使用的 **Transformers** 套件。

## 关键信息

- **定位**：开源模型与数据集平台，开发者发布开源模型的首选去处。
- **核心工具**：**Transformers** 套件——通用模型运行库，无论模型当初用什么框架（PyTorch / JAX）训练，只要上传到 HF 即可用 Transformers 运行。
- **生态价值**：
  - 一个平台覆盖模型的"下载—运行—对比"，极大降低开源模型使用门槛。
  - 配合 Google Colab（云端 notebook）可免费/低成本跑开源模型演示。
- **使用流程（课程实操）**：
  1. 注册并获取 **Hugging Face Token**（认证凭证，注意：这里的 Token 指凭证，与生成式 AI 的 Token 是不同概念）。
  2. 申请目标模型使用权限（如 Meta Llama 需填表授权，获批可能等数小时）。
  3. 用 Transformers 的 `AutoTokenizer` / `AutoModel` / `pipeline` 加载并运行。
- **对比**：比 [[Ollama]] 等更"通用、弹性高"，所有 HF 模型保证可用；其他工具（如 Ollama）在特定场景更高效。

## 关联连接

- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — 本实体的来源
- [[Llama]] — HF 上的代表性开源模型（meta-llama/Llama-3.2-3B-Instruct）
- [[Gemma]] — HF 上的另一开源模型（google/gemma-3-4b-it）
- [[Mistral]] — HF 上的开源模型发布方
- [[Transformer_Architecture]] — Transformers 套件之名源自 Transformer 架构
- [[本地_LLM_推理]] — 通过 HF 下载模型到本地/云端推理的路线
- [[Ollama]] — 本地 LLM 运行的另一工具路线（对比）
