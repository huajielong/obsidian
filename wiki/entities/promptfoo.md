---
title: "promptfoo"
type: entity
tags: [工具, LLM, Evals, 测试]
sources: []
last_updated: 2026-07-10
---

## 定义

promptfoo 是一个**开源的 LLM 评估标准化工具**，通过 YAML 配置文件定义测试用例，支持跨模型对比、CI 自动化整合，帮助团队在开发期和 CI 阶段系统性地评估 LLM 输出质量。★ 22k+。

## 关键信息

- **定位**: Eval 标准化工具
- **核心理念**: 用代码定义和管理评估，像管理软件测试一样管理 LLM 输出质量
- **核心功能**: YAML config、跨模型比较、CI 整合
- **适用场景**: 单元评估（单次 LLM call 的输出质量）、回归测试
- **与 [[langfuse]] 的区别**: prompfoo 侧重 Eval 标准化和 CI 整合，langfuse 侧重 Eval + Observability 一体化

## 关联连接

- [[Eval_Harness]] — Eval 工具生态的核心成员
- [[langfuse]] — 互补的 Eval + Observability 工具
- [[Agent_As_Judge]] — LLM-as-Judge 评估方式与 prompfoo 可配合使用
- [[Hamel_Husain]] — "Evals are everything" 理念的实践工具
