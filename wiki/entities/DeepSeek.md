---
title: "DeepSeek"
type: entity
tags: [公司, 模型, API, 云端, MoE]
sources: [raw/01-articles/05-跨平台成本对比本地vs云端.md, raw/01-articles/07-多模型回答风格对比.md, raw/01-articles/Ollama LLM 实验系列索引.md]
last_updated: 2026-07-09
---

## 定义

DeepSeek（深度求索）是中国 AI 公司，提供高性能大语言模型 API 服务。其 DeepSeek V4 Flash 模型采用 MoE（混合专家）架构，以高性价比和长上下文窗口著称。

## 关键信息

- **模型**：DeepSeek V4 Flash（云端 MoE）
- **API 端点**：`https://api.deepseek.com`
- **调用方式**：OpenAI 兼容 SDK（`openai` Python 包）
- **非高峰时段价格**：9:00~12:00 / 14:00~18:00 外为优惠时段
- **高峰时段价格**：上述时段内价格翻倍

### 性能基准（"你好"级短请求 ×100 次）

| 指标 | 数据 |
|:---|:---:|
| 总耗时 | 265s（100次） |
| 平均延迟 | 2.65s/次 |
| 输出 Token/次 | 144（回复详尽） |
| 每百万次费用 | ~¥290 |
| 生成速度 | ~54 tok/s |

### 风格特点

- 回复详尽（对简单问候也会输出完整自我介绍）
- 上下文窗口大，适合长文本生成
- 输出质量高，适合生产环境

## 关联连接
- [[Ollama]] — 本地对比方案
- [[Doubao]] — 同为云端 API 的竞争对手（豆包更快但输出更短）
- [[Llama]] — 本地模型对比对象
- [[Qwen]] — 本地模型对比对象
- [[OpenAI_Compatible_API]] — DeepSeek 使用的 API 标准
