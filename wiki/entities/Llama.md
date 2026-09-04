---
title: "Llama"
type: entity
tags: [模型, Meta, 开源, LLM]
sources: [raw/01-articles/Ollama 本地 LLM 调用实战：四种 API 方式与踩坑记录.md, raw/01-articles/awesome-agentic-ai-zh-stage-01-llm-basics.md, raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md]
last_updated: 2026-08-05
---

## 定义

Llama（Large Language Model Meta AI）是 Meta 推出的开源大语言模型系列，是自托管（self-host）和本地推理场景的生态最广、最主流的开源 LLM 系列。

## 关键信息

- **开发者**：Meta
- **最新活跃版本**：Llama 3.3 70B（截至 2026-05，Llama 4 尚未释出）
- **许可证**：Llama Community License — 开源但有条款限制（如 ≥ 7 亿 MAU 需单独授权）
- **生态地位**：Ollama 预设模型，self-host 入门首选，fine-tune base 的标准选择
- **模型大小示例**：llama3.2:3b 约 2.0 GB
- **CPU 推理速度**：llama3.2:3b 约 8.8 token/s
- **Ollama 兼容性**：原生 API 和 OpenAI 兼容 API 下均可正常工作，无已知兼容问题

### Llama-3.2-3B-Instruct（课程实操示例）

- **命名解读**：`3.2` = 版本号；`3B` = 30 亿参数（很小的模型，Colab 免费版 T4 需换 1B）；`Instruct` = 理解指令并做回复。
- **词汇表（Vocabulary）**：`tokenizer.vocab_size` = **128,000** 个 Token（编号 0~127,999），包罗多语言文字与符号；0 号是感叹号 `!`，最后一个 Token 是中文"锦"。
- **Token 特性**：同一个英文单词在句首（无前导空格）与词中有空格是**不同 Token**（`GOOD` = 19045 vs 1695）；`HI`/`Hi`/`hi` 大小写不同也是不同 Token。
- **实际能力**：能根据输入改变概率分布（`1+1=` → "2" 65.7%；"在二进位中1+1=" → "10" 70.12%）；不设 System Prompt 时会自称 GPT-3.5（身份幻觉）。
- **官方 Chat Template**：通过 `tokenizer.apply_chat_template` 自动包装（system/user/assistant 角色 + 日期等基础信息）。
- **中文能力**：相对一般，容易中英夹杂；Gemma 中文表现更好。

## 关联连接
- [[Ollama]] — 运行 Llama 模型的主要本地推理工具
- [[Qwen]] — 同为 Ollama 生态的另一模型系列（部分版本存在兼容性问题）
- [[OpenAI_Compatible_API]] — Llama 在此接口下表现稳定
- [[Gemma]] — 同为开源模型，课程中对比对象（Gemma 中文/性能更优）
- [[Hugging_Face]] — Llama 模型的托管与下载平台
- [[BPE_Tokenizer]] — Llama 词汇表与 Token 机制
- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — Llama-3.2-3B-Instruct 实操的来源
