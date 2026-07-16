---
title: "算法应用开发工程师 JD"
type: source
tags: [JD, Agent研发, RAG, Fine-Tuning, 算法应用]
sources: [raw/01-articles/算法应用开发工程师-JD.txt]
last_updated: 2026-07-16
---

# 算法应用开发工程师 JD

## 来源信息
- **来源文件**: `raw/01-articles/算法应用开发工程师-JD.txt`
- **录入日期**: 2026-07-16
- **职位名称**: 算法应用开发工程师

## 职位概览

这是一份聚焦 **AI 应用层工程落地** 的算法开发工程师 JD。与前几份 DeepSeek 系列 JD（侧重基础设施/研究）不同，本 JD 的核心定位是"将 AI 能力工程化为可交付的业务产品"——它横跨 [[Harness_Engineering]] 的全部三层：

1. **[[Prompt_Engineering]] 层**：Prompt Engineering、Function Calling Schema 设计
2. **[[Context_Engineering]] 层**：RAG 全链路（文档解析→Chunking→Embedding→Hybrid Search）
3. **[[Harness_Engineering]] 层**：Agent Loop 设计、工具调用编排、推理部署、监控评估

### 核心职责四象限

| 职责 | 所属工程层 | 关联概念 |
|------|-----------|---------|
| AI Agent 研发 | Harness Engineering | [[Agent_Loop]], [[Tool_Calling]], [[Agent_Orchestration_Patterns]] |
| RAG 链路优化 | Context Engineering | [[RAG]], [[Chunking]], [[Context_Engineering]] |
| 模型微调与对齐 | Prompt/Model 层 | [[Model_Fine_Tuning]], [[Prompt_Engineering]] |
| 工程落地与运维 | Harness Engineering | [[Agent_Observability]], [[Eval_Harness]], [[Cost_Optimization]] |

### 技术栈全景

| 领域 | 要求技术 | 知识库概念 |
|------|---------|-----------|
| Agent 框架 | LangChain, [[LlamaIndex]], AutoGen | [[LangChain]], [[AutoGen]], [[Agent_Orchestration_Patterns]] |
| 向量数据库 | FAISS, Milvus, Pinecone | [[RAG]] |
| 微调技术 | LoRA, P-Tuning | [[Model_Fine_Tuning]] |
| 深度学习框架 | PyTorch, Hugging Face | - |
| 模型架构 | Transformer | [[Transformer_Architecture]], [[Self_Attention]], [[GPT]] |
| MLOps（加分） | W&B, MLflow, Ray, Docker/K8s | [[Agent_Observability]], [[Eval_Harness]] |

### 与知识库中其他 JD 的对比

与 [[DeepSeek四份JD全景对比]] 中的 DeepSeek 系列 JD 相比，本 JD 的定位差异显著：

| 维度 | 本 JD | DeepSeek 系列 JD |
|------|-------|-----------------|
| 团队层级 | **应用层** — 将 AI 落地到业务产品 | 基础设施层/研究层 — 构建模型与平台本身 |
| 技术重心 | Agent + RAG + Fine-tuning 三项交叉 | 各自纵深（Harness / 服务端 / 预训练数据 / AI 搜索 / Agent Infra） |
| 三层归属 | 横跨 Prompt / Context / Harness 全三层 | 各有侧重的一两个层面 |
| 工程文化 | 产品导向，"交付"是关键词 | 技术深度优先，"平台"和"研究"是关键词 |
| 薪资对标 | 一般在互联网公司中台/业务 AI 团队 | DeepSeek 属于顶尖薪酬区间 |

## 关联连接
- [[Agent_Loop]] — Agent 核心运行机制
- [[Tool_Calling]] — 函数调用与工具编排
- [[RAG]] — 检索增强生成全链路
- [[Chunking]] — 文档分块策略
- [[Context_Engineering]] — RAG 所属的工程层
- [[Harness_Engineering]] — Agent 执行控制层
- [[Model_Fine_Tuning]] — LoRA/P-Tuning 微调
- [[Prompt_Engineering]] — 提示词工程
- [[Transformer_Architecture]] — 模型架构基础
- [[Multi_Agent_System]] — 加分项：多智能体系统
- [[Eval_Harness]] — 模型评估体系
- [[Agent_Observability]] — 可观测性与监控
- [[Cost_Optimization]] — 算力优化与成本控制
- [[Agent_Orchestration_Patterns]] — 多 Agent 编排模式
- [[LangChain]] — Agent 开发框架
- [[AutoGen]] — Multi-agent 框架
- [[Parameter_Efficient_Fine_Tuning]] — 参数高效微调（LoRA/P-Tuning），微调要求的核心概念
- [[Weights_and_Biases]] — MLOps 实验追踪（加分项）
- [[MLflow]] — MLOps 模型生命周期管理（加分项）
- [[Ray]] — 分布式计算与训练编排（加分项）
- [[DeepSeek四份JD全景对比]] — 全景对比参考
