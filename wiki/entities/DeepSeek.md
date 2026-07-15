---
title: "DeepSeek"
type: entity
tags: [公司, 模型, API, 云端, MoE, 推理, Harness, Agent, 招聘, 工程, 后端, 数据]
sources: []
last_updated: 2026-07-15
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

## Harness 团队

DeepSeek 设有专门的 Agent Harness 团队，致力于将模型能力转化为前沿的 Agent 产品与科研突破。团队使命遵循核心公式：

> **Model + Harness = Agent**

### 四个招聘方向

| 方向 | 定位 | 核心要求 |
|------|------|---------|
| **Agent Harness 研究** | 探索 Agent Harness 研究前沿 | 科研经验、0→1 推动能力、Benchmark 设计、实验迭代 |
| **Agent Harness 研发/工程** | 解决下一代 Agent Harness 工程难题 | 技术架构、AI 辅助开发、快速迭代、开发者体验 |
| **Agent Harness 产品** | 定义下一代 Agent 产品形态 | 产品路线图、UX/UI 设计、数据驱动决策、社区运营 |
| **Agent Harness 项目经理**（实习）| 推动项目高效运转 | 沟通协调、进度跟踪、执行力 |

### 技术知识体系

DeepSeek Harness 团队要求全方向成员掌握以下知识：

- **基础机制**：LLM API、KV Cache、Agent Loop、Tool Use、Reasoning、Planning、Skills、MCP、Memory、Subagent、Multi-Agent
- **三层工程模型**：[[Prompt_Engineering]]、[[Context_Engineering]]、[[Harness_Engineering]]
- **进阶机制**：自进化 Agent、超长程任务、沙箱执行、Observability

> 详见 [[摘要-deepseek-harness-team-jd]] — 完整职位描述与知识图谱

## 服务端工程团队

DeepSeek 的服务端工程团队承担与 Harness 团队互补的角色——将模型智能落地为数千万日活用户可用的生产服务。

> **团队使命**：与智能共演化，让工程即作品。
>
> 对内：与资深研究员合作构建提升模型智能边界的工程基建
> 对外：深度参与 AI 产品的创新迭代，让智能触达亿万用户

### 三个方向

| 方向 | 核心职责 | 技术挑战 |
|------|---------|---------|
| **线上核心服务** | 大模型应用与 API 服务架构、性能优化、研发效能工具 | 数千万日活、高吞吐低延迟、可靠性 |
| **Agent 后端** | Agent 执行环境快照、框架集成评测、Agent 数据生成 | 状态持久化、评测自动化、数据反哺模型 |
| **数据仓库** | 数据管道、离线/实时计算、架构稳定性 | 大规模数据处理、流批一体、资源优化 |

### Agent 后端方向：Harness 的工程实现层

Agent 后端方向是三个方向中与 [[Harness_Engineering]] 关系最密切的，涵盖三个独特工程课题：

1. **Agent 执行环境快照系统** — 将 Agent 运行时的完整状态（上下文、工具调用轨迹、中间结果）序列化存储，实现断点续传、回放调试、状态迁移
2. **Agent 框架集成与评测** — 接入各类 Agent 框架，构建高效的评测基础设施
3. **Agent 数据生成** — 用 Agent 执行轨迹作为训练数据反哺模型，实现模型与 Harness 的共同进化

> 详见 [[摘要-deepseek-service-engineer-jd]] — 完整职位描述与三层架构

### 团队对照

| 维度 | Harness 团队 | 服务端工程团队 |
|------|-------------|---------------|
| 聚焦 | Agent 运行时设计 | 基础设施与生产服务 |
| 产出 | Harness 原则、机制、原型 | 在线服务、数据管道、工程平台 |
| 协作对象 | 研究员、产品经理、工程师 | 研究员（对内）、亿万用户（对外） |
| 工程重心 | Loop / Tool / Memory / Subagent | 性能、可靠性、可观测性、可维护性 |

## 关联连接
- [[摘要-ollama-cost-comparison]] — 成本对比实验数据来源
- [[摘要-ollama-style-comparison]] — 风格对比实验数据来源
- [[摘要-deepseek-api-error-handling]] — API 错误处理实战来源
- [[摘要-few-shot-experiment]] — Few-Shot 实验来源
- [[摘要-system-prompt-experiment]] — System Prompt 实验来源
- [[摘要-deepseek-harness-team-jd]] — DeepSeek Harness 团队职位描述与知识要求
- [[摘要-deepseek-service-engineer-jd]] — DeepSeek 服务端工程团队职位描述（线上核心服务/Agent 后端/数据仓库）
- [[Exponential_Backoff]] — 指数退避重试通用实现
- [[BPE_Tokenizer]] — Token 估算方法的底层算法
- [[Ollama]] — 本地对比方案
- [[Doubao]] — 同为云端 API 的竞争对手（豆包更快但输出更短）
- [[Llama]] — 本地模型对比对象
- [[Qwen]] — 本地模型对比对象
- [[OpenAI_Compatible_API]] — DeepSeek 使用的 API 标准
- [[Harness_Engineering]] — Harness Engineering 核心概念
- [[Context_Engineering]] — 三层工程模型的中间层
- [[Prompt_Engineering]] — 三层工程模型的基础层
- [[Agent_Loop]] — Agent 核心运行机制，执行环境快照的关联概念
- [[Eval_Harness]] — Agent 框架集成评测的关联概念
- [[Memory_Agent]] — Agent 状态与记忆持久化
- [[Checkpoint_Commit]] — 类比：版本控制中的快照概念
- [[Agent_Observability]] — 可观测性基础设施
- [[Agent_Interfaces]] — 智能体接口模型（含 Code Sandbox）
- [[摘要-预训练数据工程师-jd]] — 预训练数据工程师 JD，数据供给侧团队
- [[摘要-deepseek-ai-search-jd]] — AI 搜索工程师 JD，检索推理侧团队
- [[AI搜索工程]] — AI 原生搜索工程概念
- [[DeepSeek四份JD全景对比]] — 全部四份 JD 的横向对比分析
