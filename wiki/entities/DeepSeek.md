---
title: "DeepSeek"
type: entity
tags: [公司, 模型, API, 云端, MoE, 推理]
sources: [raw/01-articles/05-跨平台成本对比本地vs云端.md, raw/01-articles/07-多模型回答风格对比.md, raw/01-articles/Ollama LLM 实验系列索引.md, raw/01-articles/awesome-agentic-ai-zh-stage-01-llm-basics.md, raw/01-articles/DeepSeek-API-错误处理实战.md, raw/01-articles/Few-Shot-实验对比.md, raw/01-articles/System-Prompt-实验对比.md]
last_updated: 2026-07-10
---

## 定义

DeepSeek（深度求索）是中国 AI 公司，提供高性能大语言模型 API 服务。其模型系列涵盖通用对话（V3/V4）和推理增强（R1）两条产品线。采用 MoE（混合专家）架构，以高性价比和长上下文窗口著称，是同级别英文模型中 token 单价最低的选择之一。

## 模型系列

| 模型 | API 名称 | Context | 定位 |
|:----|:--------|:-------:|:----|
| **V4 Flash** | `deepseek-chat`（V4 经济型）| 128k | 日常对话，性价比最高 |
| **V4 Pro** | `deepseek-chat`（V4 高性能）| 128k | 复杂推理与生成 |
| **V3** | `deepseek-chat`（旧版通用）| 128k | 通用对话 |
| **R1** | `deepseek-reasoner` | 128k | 推理增强，数学/代码/逻辑

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

- **辩论式结构**：擅长模拟"正方 vs 反方"的辩论赛结构，立场鲜明、层层递进
- 回复详尽（对简单问候也会输出完整自我介绍）
- 上下文窗口大，适合长文本生成
- 输出质量高，适合生产环境

### 风格对比基准（观点判断类 Prompt）

> 与 llama3.2:3b、qwen3.5:0.8b、豆包 Seed Character 同 Prompt 对比

| 指标 | DeepSeek V4 Pro |
|:---|:---:|
| 输入 Token | 37 |
| 输出 Token | 1,246 |
| 中文字数 | 1,353 |
| 延迟 | **25.4s** |
| 生成速度 | ~49 tok/s |
| 成本/次 | ~¥0.0003 |
| 回答结构 | 正反辩论式+折中方案 |

> ⚠️ **模型版本说明**：实验七使用 DeepSeek V4 Pro，实验五使用 V4 Flash。两者分别侧重复杂推理和性价比，性能基准数据不同属正常现象。

## API 错误处理行为

DeepSeek API 使用 OpenAI 兼容接口，但错误处理行为与 OpenAI 有重要差异：

### 认证错误
- **异常类型**: `openai.AuthenticationError` (HTTP 401)
- **错误码**: `invalid_request_error`
- **处理策略**: 不可恢复的 FatalError，不应放入重试循环

### 输入超长行为（关键差异 ⚠️）
> **DeepSeek 不会抛出 `context_length_exceeded` 错误。** 当输入超出上下文窗口时，它选择**静默截断**并返回空内容（`finish_reason: "length"`），而不是像 OpenAI 那样抛异常拒绝请求。

这意味着：
1. 不能依赖 API 来告诉你输入太长
2. 需要在客户端做 prompt 长度预检
3. 需要对空响应做兜底处理

### 推荐的 Token 预检
```python
def estimate_tokens(text: str) -> int:
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    ascii_chars = len(text) - chinese_chars
    return chinese_chars // 2 + ascii_chars // 4
```

### 重试策略
| 错误类型 | DeepSeek 行为 | 处理策略 |
|---------|--------------|---------|
| 无效 API Key | `AuthenticationError` (401) | 不重试，提示用户检查 Key |
| 输入超长 | 不抛异常，返回空内容 | 客户端预检 Token；空响应兜底 |
| 网络超时 | `ReadTimeout`/`APITimeoutError` | 指数退避重试（最多 3~5 次） |
| 限流 (429) | `RateLimitError` | 指数退避重试 |
| 服务端 5xx | `APIStatusError` | 指数退避重试 |

> **教训**: 永远不要假设 API 会帮你发现所有问题。客户端要做好预检、分类重试和兜底。

> 详见 [[Exponential_Backoff]] — 指数退避重试的通用实现

## 关联连接
- [[摘要-ollama-cost-comparison]] — 成本对比实验数据来源
- [[摘要-ollama-style-comparison]] — 风格对比实验数据来源
- [[摘要-deepseek-api-error-handling]] — API 错误处理实战来源
- [[摘要-few-shot-experiment]] — Few-Shot 实验来源
- [[摘要-system-prompt-experiment]] — System Prompt 实验来源
- [[Exponential_Backoff]] — 指数退避重试通用实现
- [[BPE_Tokenizer]] — Token 估算方法的底层算法
- [[Ollama]] — 本地对比方案
- [[Doubao]] — 同为云端 API 的竞争对手（豆包更快但输出更短）
- [[Llama]] — 本地模型对比对象
- [[Qwen]] — 本地模型对比对象
- [[OpenAI_Compatible_API]] — DeepSeek 使用的 API 标准
