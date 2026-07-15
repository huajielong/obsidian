---
title: "Eval_Harness"
type: concept
tags: [eval, harness-engineering, quality, production, agent, CI]
sources: [raw/01-articles/07-multi-agent-production.zh-Hans.md]
last_updated: 2026-07-10
---

# Eval Harness（评估框架）

## 定义

Eval Harness 是 [[Harness_Engineering]] 的 **第 7 个核心元件**——为 Agent 系统建立自动化评估流水线的工程实践。它解决的核心问题是：**"我怎么知道我的 Agent 真的变好了？"**

## 核心定位

Eval Harness ≠ Benchmark。Benchmark 告诉你"这个模型在标准化测试上的排名"，Eval Harness 告诉你"我的 Agent 在我的场景上表现得怎么样"。

> ⚠️ **2026-04 UC Berkeley 发现 8 个主流 Agent Benchmark 全部可被 Reward-Hacking 到接近 100%**（SWE-bench / WebArena / OSWorld / GAIA / Terminal-Bench 等）。永远不要只看 Leaderboard 数字。

## 评估层次

| 层次 | 评估什么 | 方法 | 谁用 |
|------|---------|------|------|
| **单元评估** | 单次 LLM call 的输出质量 | promptfoo 配置、LLM-as-judge | 开发期 |
| **轨迹评估** | 整个 Agent 执行轨迹（plan → tool → result 链条） | trajectory analysis、pass^k | 开发期 |
| **任务评估** | Agent 是否完成了真实任务 | 任务完成率（success rate）、hold-out test | CI / 上线前 |
| **生产评估** | Production 中 Agent 的表现 | 用户反馈、cost tracking、drift detection | 生产期 |

## Benchmark Landscape（2026-05 SOTA）

| Benchmark | 领域 | 2026 SOTA | 领先 Model |
|-----------|------|-----------|------------|
| SWE-bench Verified | 软工 / code agent | 88.6% | Claude Opus 4.8 |
| Terminal-Bench | terminal 任务 | 领先 | Claude Opus 4.8 |
| GAIA | general assistant | 74.6% | Claude Sonnet 4.5 (HAL) |
| WebArena | web 导航 | 68.7% | — |
| OSWorld | OS-level 桌面控制 | 76.26% (superhuman) | OpenAI CUA |
| τ-bench | tool use 多轮对话 | （较难 hack）| Anthropic / OpenAI |
| RE-bench | research engineering | （较难 hack）| Frontier model |

## ⚠️ Reward-Hacking 风险

UC Berkeley RDI (2026-04-12) 系统性 audit 了 8 个主流 Benchmark，**每个都能被 automated scanning agent 绕过**——Agent 实际没有 solve 任何 task，却拿到接近 100% 分数。

### 如何避免被 Benchmark 欺骗

| 做法 | 推荐度 |
|------|--------|
| 只看 Leaderboard Top | ❌ |
| 看 task-level success rate breakdown | ✅ |
| **跑自己的 hold-out test set** | ✅✅ **最可靠** |
| 看 trajectory / log 是否真的解了 task | ✅ |
| 看多个 benchmark + 自己 use case | ✅ |

**哪些 benchmark 较难 hack**：
- **τ-bench** — 多轮对话 + tool use，reward function 较密集
- **RE-bench** — research engineering 真实任务
- **你自己的 production eval set** ⭐ 永远最可靠

## Production 评估纪律

1. 不要把外部 Benchmark 数字当 Ground Truth
2. **自己的 eval set（内部 hold-out test）** 才是上线依据
3. 每次 Model Upgrade → 跑内部 eval set，不看厂商公布数字
4. 用 [[promptfoo]] / [[langfuse]] 把 eval 自动化，每次 Deploy 都跑

## Evaluation 进阶指标

- **pass^k**：同一题连续 k 次都对的概率 = 可靠度，不是只看过一次
- **τ²-bench**：τ-bench 的进阶版，更严格的多轮 tool use 评估

## 失败模式分类（MAST）

多 Agent 系统的失败有现成词汇：**MAST**（arXiv 2503.13657），14 种失败模式分 3 类——用这个框架结构化地报告和修复 Multi-agent 失败。

## 推荐工具

| 工具 | 定位 | 特点 |
|------|------|------|
| **promptfoo** ⭐ | Eval 标准化 | YAML config、跨模型比较、CI 整合、★ 22k+ |
| **langfuse** ⭐ | Eval + Observability | OSS、tracing + eval + prompt mgmt、★ 28k+ |
| openai/evals | OpenAI 专属 | ★ 18k+ |
| lm-evaluation-harness | 学术 Benchmark | MMLU/HellaSwag/GSM8K、★ 12k+ |

## 关联连接

- [[情感智能数据工程]] — 情感温度评测数据层：以人类情感认知为基准，通过 Badcase 挖掘与归因分析，提升 AI 在情感陪伴与角色扮演场景中的互动真实感与沉浸度
- [[AI创作数据工程]] — 创作审美评测数据层：将人类审美标准转化为可操作的评测体系与数据管线，驱动模型在文学创作与实用写作领域的能力提升
- [[专业领域数据工程]] — 专业领域评测数据层：通过领域专家判断力构建评测体系与高质量数据，将人类专业知识注入模型；覆盖小语种/医学/法律等学科
- [[Agent数据产品工程]] — 评测数据桥梁层：通过评测体系设计与数据生产管线构建，连接产品体验与模型能力；聚焦办公/生活/搜索等通用场景
- [[Agent能力工程]] — 能力构建层：通过 RL 环境构建、评测任务设计和能力短板补齐，系统性地提升模型 Agent 能力
- [[Harness_Engineering]] — Eval Harness 是 Harness 的第 7 个核心元件
- [[Agent_Observability]] — Eval + Observability 构成 Production Agent 的可观测性底座
- [[Cost_Optimization]] — Eval 帮助发现成本异常
- [[Agent_Loop]] — Agent Loop 的每个环节都可以被 Eval 覆盖
- [[Multi_Agent_System]] — Multi-agent 场景下 Eval 更关键（3-10× token 成本）

- [[后训练研究]] — 内容来源：后训练评测是 Eval Harness 的重要应用场景，定义评测内容和标准

- [[多模态理解研究]] — 评测内容来源：多模态评测需要运行在 Eval_Harness 之上，定义多模态场景的评测标准
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — 本概念的核心来源（Stage 7 练习 2 + Benchmark 章节）
