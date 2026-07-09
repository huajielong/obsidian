---
title: "Doubao"
type: entity
tags: [字节跳动, 模型, API, 云端, 豆包]
sources: [raw/01-articles/05-跨平台成本对比本地vs云端.md, raw/01-articles/07-多模型回答风格对比.md, raw/01-articles/Ollama LLM 实验系列索引.md]
last_updated: 2026-07-09
---

## 定义

豆包（Doubao）是字节跳动推出的对话式 AI 大模型产品，提供云端 API 服务。其 Seed Character 模型以低延迟和高性价比著称，在处理短请求时表现尤为突出。

## 关键信息

- **模型**：Doubao Seed Character（云端对话模型）
- **API 端点**：`https://ark.cn-beijing.volces.com/api/v3`
- **调用方式**：OpenAI 兼容 SDK（`openai` Python 包）

### 性能基准（"你好"级短请求 ×100 次）

| 指标 | 数据 |
|:---|:---:|
| 总耗时 | **45s**（100次，所有模型最快） |
| 平均延迟 | **0.45s/次**（本地模型的 5 倍快） |
| 输出 Token/次 | 15（简洁问候） |
| 每百万次费用 | ~¥58（最便宜） |
| 生成速度 | ~33 tok/s |

### 风格特点

- **极低延迟**：0.45s/次（短请求），适合高频短请求场景（客服、对话）
- **回复简洁**：对简单问候仅返回简短问候
- **性价比最高**：100 次仅 ¥0.006，每百万次 ~¥58
- **条理清晰**：分节论述，语言流畅自然

### 风格对比基准（观点判断类 Prompt）

> 与 llama3.2:3b、qwen3.5:0.8b、DeepSeek V4 Pro 同 Prompt 对比

| 指标 | 豆包 Seed Character |
|:---|:---:|
| 输入 Token | 64 |
| 输出 Token | 730 |
| 中文字数 | 1,195 |
| 延迟 | **10.2s（最快）** |
| 生成速度 | ~72 tok/s（最快） |
| 成本/次 | ~¥0.00006（最低） |
| 回答结构 | 分节论述（支持/反对/判断），条理最清晰 |

## 关联连接
- [[摘要-ollama-cost-comparison]] — 成本对比实验数据来源
- [[摘要-ollama-style-comparison]] — 风格对比实验数据来源
- [[Ollama]] — 本地对比方案（0 直接成本但需硬件）
- [[DeepSeek]] — 同为云端 API 的竞争对手（DeepSeek 回复更长、成本更高）
- [[OpenAI_Compatible_API]] — 豆包使用的 API 标准
