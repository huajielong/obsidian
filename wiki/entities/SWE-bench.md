---
title: "SWE-bench"
type: entity
tags: [eval, benchmark, 软件工程, Agent评测]
sources:
  - wiki/syntheses/Agent_Benchmark_Landscape.md
last_updated: 2026-07-22
---

## 概述

SWE-bench 是评估 LLM/Agent 解决真实软件工程问题能力的标准化评测基准。它使用 GitHub 上的真实 Issue → PR 数据，测试 Agent 能否理解 Issue 描述、定位问题、生成并应用修复补丁。

## 关键参数

| 项目 | 内容 |
|------|------|
| **发布** | 2023 (SWE-bench) → 2024 (SWE-bench Verified) |
| **数据规模** | 2,294 个真实 Issue-PR 对（SWE-bench）→ 500 个高质量样本（Verified）|
| **评测指标** | % resolved（提交的 patch 通过所有测试） |
| **SOTA** | Claude Opus 4.8: 88.6%（SWE-bench Verified） |
| **风险** | ⚠️ 可被 Reward-Hacking（UC Berkeley RDI 2026）|

## 变体

- **SWE-bench Lite**：300 个"简单"样本，快速迭代用
- **SWE-bench Verified**：500 个手动验证的高质量样本，行业标准
- **SWE-bench Multilingual**：2025 年扩展至多语言

## 在 Agent 评测中的定位

SWE-bench 是当前 Agent 评测体系中最成熟的**代码 Agent 能力基准**，与 GAIA（通用任务）、AgentBench（多场景）形成互补。详细分析见 [[Agent_Benchmark_Landscape]]。

## 关联连接

- [[Agent_Benchmark_Landscape]] — 完整 Benchmark 对比分析
- [[Eval_Harness]] — Agent 自动化评估框架
- [[Agentic_Coding]] — Agent 编程范式的理论基础
