---
title: "Agent 评测 Benchmark Landscape"
type: synthesis
tags: [eval, benchmark, agent评测, SWE-bench, GAIA, AgentBench, 评估对比]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-multi-agent-production.md
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-22
---

# Agent 评测 Benchmark Landscape

## 概述

Agent 评测 Benchmark 是衡量 AI Agent 在真实任务场景中能力的标准化测试体系。与传统的 NLP Benchmark（如 MMLU、GSM8K）不同，Agent Benchmark 评估的是**多轮交互、工具调用、规划执行与环境反馈**的综合能力。

> ⚠️ **2026-04 UC Berkeley RDI 发现 8 个主流 Agent Benchmark 全部可被 Reward-Hacking 到接近 100%**。评测数字不等于真实能力，理解每个 Benchmark 的定位、设计和漏洞，比记住排名数字更重要。

本页系统梳理当前主要 Agent 评测基准，以便在 [[Eval_Harness]] 的框架下做选型参考。

---

## Benchmark 全景总览

### 主表：当前主流 Agent Benchmark

| Benchmark | 领域 | 发布年份 | 2026 SOTA | 领先模型 | 核心评估维度 | 是否可 Hack |
|-----------|------|---------|-----------|----------|-------------|:----------:|
| **[[SWE-bench]]** | 软件工程 | 2023→2024 | 88.6% | Claude Opus 4.8 | 真实 GitHub Issue → Patch | ⚠️ 可 Hack |
| **GAIA** | 通用助手 | 2023 | 74.6% | Claude Sonnet 4.5 (HAL) | 多步推理 + 工具调用 | ⚠️ 可 Hack |
| **AgentBench** | 多维度 Agent | 2023 | ~65%* | GPT-4 / Claude 3.5 | 8 场景综合能力 | 部分可 Hack |
| **WebArena** | Web 导航 | 2024 | 68.7% | — | 开放 Web 任务执行 | ⚠️ 可 Hack |
| **OSWorld** | OS 桌面操控 | 2024 | 76.26% | OpenAI CUA | 桌面 GUI 操作 | ⚠️ 可 Hack |
| **Terminal-Bench** | 终端任务 | 2025 | 领先 | Claude Opus 4.8 | Shell/CLI 任务 | ⚠️ 可 Hack |
| **τ-bench (τ²-bench)** | Tool Use 对话 | 2024→2025 | — | Anthropic / OpenAI | 多轮 Tool Calling | ✅ 较难 |
| **RE-bench** | 研究工程 | 2025 | — | Frontier model | 开放式科研任务 | ✅ 较难 |
| **SWE-agent** | 软件工程 | 2024 | 附属于 SWE-bench | — | Agent 框架对比 | N/A |

> *AgentBench 分数因版本不同有较大波动，此处为平均参考值。
> 标记 ⚠️ 可 Hack = Berkeley RDI 2026-04 审计确认存在 Reward-Hacking 漏洞。

---

## 各 Benchmark 深度分析

### 1. SWE-bench（软件工程评测基准）

#### 基本信息

| 属性 | 内容 |
|------|------|
| **全称** | Software Engineering Benchmark |
| **发布** | 2023 (SWE-bench) → 2024 (SWE-bench Verified) |
| **主办** | Princeton University |
| **官网** | [swebench.com](https://www.swebench.com) |
| **评估方式** | 模型直接生成 Patch 修复真实 GitHub Issue |

#### 评测机制

```
给定：一个开源 GitHub Repo + 一个真实 Issue 描述
任务：模型输出一个 Diff Patch（代码变更）
评估：Patch 是否能通过该 Repo 的测试套件
```

- **验证机制**：Patch 必须通过对应 Issue 的所有测试用例
- **数据集规模**：Verified 子集 ~500 个 Issue（手动验证过质量）
- **覆盖语言**：Python（主要）、Java、JavaScript、TypeScript 等

#### 演化路线

```
SWE-bench (2023) 
  → SWE-bench Lite (2024, 300 个"简单"样本)
  → SWE-bench Verified (2024, 500 个高质量样本，手动验证)
  → SWE-bench Multilingual (2025, 扩展多语言)
```

#### 关键发现

| 发现 | 说明 |
|------|------|
| **Agent 框架 > 模型能力** | 同一个模型 + 不同 Agent 框架（SWE-agent vs 原生）分数差异可达 30%+ |
| **Context 窗口大小关键** | 能容纳更多文件内容的模型显著优于窗口小的模型 |
| **Patch 格式敏感** | "给出统一 diff" 比 "描述要改什么" 效果更好 |
| **Reward-Hacking 漏洞** | 2026-04 发现 Agent 可绕过测试直接"伪造"跑通过 |

#### 代表参与框架/系统

| 系统 | SOTA 分数 | 特点 |
|------|-----------|------|
| Claude Code / Opus 4.8 | 88.6% | 最高分 |
| SWE-agent | ~50-60% | MIT 开源 Agent 框架 |
| Devin | ~50% | Cognition Labs 商业产品 |
| OpenHands | ~40-45% | 开源自主 Agent |

---

### 2. GAIA（通用助手评测）

#### 基本信息

| 属性 | 内容 |
|------|------|
| **全称** | General AI Assistants |
| **发布** | 2023 |
| **主办** | FAIR (Meta)、Hugging Face、AutoGPT 等 |
| **评估方式** | 多步推理 + 工具调用，输出为简洁答案 |

#### 评测机制

```
给定：一个现实世界问题（需要多步推理）
范例："2020 年获得奥斯卡最佳导演的导演，他执导的第一部电影的上映年份是多少？"
任务：规划步骤 → 调用工具（搜索/代码/文件操作）→ 给出最终答案
评估：答案是否与标准答案完全匹配
```

#### 三个难度级别

| 级别 | 推理步数 | 工具使用 | 示例 |
|------|---------|---------|------|
| **Level 1** | 1-3 步 | 单一工具 | "巴黎的当前时间是什么？" |
| **Level 2** | 3-8 步 | 多工具组合 | "引用论文 A 中使用的数据集，在 Paper B 中的准确率是多少？" |
| **Level 3** | 8-15+ 步 | 复杂工具编排 | 跨多个数据源的推理链 |

#### 关键发现

- **多步推理是主要瓶颈**：模型在 Level 1 表现良好，Level 2-3 大幅下降
- **工具选择质量**：Agent 在"用什么工具"上的决策经常出错（选错搜索词 / 误用计算工具）
- **HAL（Half-thinking Agent Loop）**：Claude Sonnet 4.5 以 74.6% 领先，采用的是"半思考循环"策略
- **Reward-Hacking**：可被扫描 Agent 通过探测答案格式绕过

---

### 3. AgentBench（多维度 Agent 评测）

#### 基本信息

| 属性 | 内容 |
|------|------|
| **全称** | AgentBench: Evaluating LLMs as Agents |
| **发布** | 2023 (ICLR 2024) |
| **主办** | Tsinghua University、Microsoft、UC Berkeley 等 |
| **评估方式** | 8 场景 × 多任务的综合评测 |

#### 八维评测场景

| 场景 | 类型 | 任务示例 |
|------|------|---------|
| **HouseHolding** | 具身交互 | 虚拟家庭环境中的物品操作 |
| **WebShop** | 电商购物 | 根据需求在网页中购买商品 |
| **WebArena** | Web 导航 | 完成复杂 Web 任务 |
| **DB** | 数据库操作 | 用 SQL 查询数据库 |
| **OS** | 操作系统 | 命令行操作 |
| **KG** | 知识图谱 | 图查询与推理 |
| **Tiling** | 环境交互 | 游戏型交互 |
| **AlfWorld** | 文字游戏 | 基于文本的环境交互 |

#### 关键发现

- **AgentBench 综合分 vs 单场景分呈弱相关**：综合能力不等于各场景能力的简单平均
- **分布式推理差距大**：模型在 Web/OS 场景表现远不如推理/知识图谱场景
- **AgentBench 是最早提出"多维 Agent 能力"框架的 Benchmark**

---

### 4. WebArena（Web 导航评测）

| 属性 | 内容 |
|------|------|
| **发布** | 2024 |
| **主办** | University of Washington |
| **评估方式** | Agent 在隔离的 Web 环境中完成开放任务 |

任务类型：在模拟的电子商务、论坛、项目管理等 Web 应用中完成指定操作（如"在论坛中发布新帖子"、"修改购物车中的商品数量"）。

**关键发现**：
- 当前模型在"元素定位"上表现最差（CTR < 50%）
- Accessibility Tree + Bounding Box 是最有效的页面理解方法
- 被 Berkeley 确认为可 Hack

---

### 5. OSWorld（桌面 OS 操控评测）

| 属性 | 内容 |
|------|------|
| **发布** | 2024 |
| **主办** | Microsoft Research |
| **评估方式** | Agent 在 Ubuntu 桌面中完成 GUI 操作 |

任务类型包括：文件操作、应用使用、设置修改、多应用工作流等。

**关键发现**：
- OpenAI CUA 以 76.26% 达到超人类水平（Human 基线 ~72%）
- Computer Use Agent 的"屏幕截图 → 定位 → 点击"循环仍然是主要方法
- 2026-04 被确认为可 Hack

---

### 6. τ-bench（Tool Use 多轮对话评测）

| 属性 | 内容 |
|------|------|
| **发布** | 2024 → τ²-bench (2025) |
| **主办** | Anthropic 等 |
| **评估方式** | 多轮 Tool Calling 对话的语义质量 |

**核心优势**：τ-bench 的 reward function 较为密集——评估的不是最终答案，而是**每一轮的工具调用质量**。

```
用户："帮我订一张明天去北京的机票"
Agent: [调用 search_flights()] ✓  正确调用
Agent: [调用 book_flight(id)] ✓   正确调用
用户："等等，改成后天"
Agent: [调用 modify_booking()] ✓  正确处理变更
评估：每 step 都独立计分，最后聚合
```

**τ²-bench 的改进**：
- 更长的多轮对话（15+ 轮）
- 更复杂的工具依赖关系
- 加入"上下文理解"维度（用户模糊表达 → 模型正确理解意图）

---

### 7. RE-bench（研究工程评测）

| 属性 | 内容 |
|------|------|
| **全称** | Research Engineering Benchmark |
| **发布** | 2025 |
| **主办** | 多机构联合 |
| **评估方式** | 开放式科研任务：文献调研 → 实验设计 → 代码实现 → 结果分析 |

**特点**：
- 任务周期长（数小时级别）
- 评估维度多：不只是"通过与否"，而是结果质量
- 较难 Hack（开放任务，没有标准答案）

---

## Benchmark 选型指南

### 按评估目的选择

| 评估目的 | 推荐 Benchmark | 原因 |
|---------|---------------|------|
| **代码能力** | SWE-bench Verified | 最成熟的代码 Agent 评测 |
| **通用助手能力** | GAIA | 多步推理 + 工具调用 |
| **Web 操作能力** | WebArena | 纯 Web 场景 |
| **桌面操作能力** | OSWorld | GUI 交互 |
| **多轮对话 + 工具** | τ²-bench | 难以 Hack，reward 密集 |
| **科研能力** | RE-bench | 开放性最高 |
| **综合衡量** | AgentBench | 8 维场景全覆盖 |
| **生产上线评估** | 自建 Hold-out Set | ⭐ 最可靠 |

### 抗 Reward-Hacking 评估组合

```
必做：自建 Hold-out Eval Set（生产环境数据）
推荐：τ²-bench (最难以 Hack)
辅助：SWE-bench Verified + GAIA (看 breakdown 不看总分)
参考：AgentBench + RE-bench (多维度交叉验证)
```

---

## Benchmark 的未来趋势

| 趋势 | 描述 | 代表 |
|------|------|------|
| **动态生成** | AI 自动生成评测任务，防止数据泄漏和 Reward-Hacking | Dynabench, LIVE-Bench |
| **人机协同** | 人工评估 + 自动评估混合，降低作弊空间 | Chatbot Arena |
| **领域定制** | 垂直领域的 Agent 评测（医疗、法律、金融）| MedAgentBench |
| **闭环评测** | Agent 的真实部署指标（用户留存、任务完成率）| Production Eval |

---

## 常见陷阱

| 陷阱 | 说明 | 应对 |
|------|------|------|
| **只看 Leaderboard** | Top 分数不代表场景适用 | 看 task-level success rate breakdown |
| **忽略 Reward-Hacking** | 高分可能来自投机取巧 | 结合 trajectory 分析 |
| **单一 Benchmark 崇拜** | 一个分数说明不了全部 | 多 Benchmark 交叉验证 |
| **Benchmark 数据泄漏** | 模型训练集包含测试数据 | 定期更新测试集 |
| **忽略 Cost 维度** | 高分但 Token 消耗巨大 | 结合 Cost-Aware Benchmark |

---

## 关联连接

- [[Eval_Harness]] — Agent 自动化评估流水线，本页是 Eval_Harness 中 Benchmark Landscape 的深度展开
- [[Harness_Engineering]] — Eval Harness 是 Harness 的第 7 个核心元件
- [[Agent能力工程]] — 通过 RL 环境和评测任务构建系统性 Agent 能力
- [[Agent数据产品工程]] — 评测数据生产管线与 Benchmark 设计
- [[后训练研究]] — RLHF/RLVR 评测是后训练的关键环节
- [[Agent_Observability]] — Production 评估与 Eval 的互补关系
- [[Cost_Optimization]] — Cost-Aware Benchmark 的维度参考
- [[promptfoo]] — Eval 标准化工具，可用来自建 Hold-out Set
- [[langfuse]] — 可观测平台，Eval + Tracing 一体化
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — Benchmark Landscape 核心来源
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — Eval Rigor 和 Reward-Hacking 讨论来源
- [[AI产品工程]] — 产品侧评测视角与 Benchmark 选型决策
