---
title: "智能体研发工程师 JD"
type: source
tags: [JD, Agent研发, Agent平台, Skills, MCP, 多租户SaaS]
sources: [raw/01-articles/智能体研发工程师-JD.txt]
last_updated: 2026-07-16
---

# 智能体研发工程师 JD

## 来源信息
- **来源文件**: `raw/01-articles/智能体研发工程师-JD.txt`
- **录入日期**: 2026-07-16
- **职位名称**: 智能体研发工程师

## 职位概览

这是一份聚焦 **企业级 AI Agent 平台架构** 的研发工程师 JD。与 [[摘要-算法应用开发工程师-jd]]（侧重应用层算法落地）不同，本 JD 的核心定位是**从零到一搭建高可用的 AI Agent 平台基础设施**——它更接近 [[Harness_Engineering]] 的**平台工程**维度：

1. **平台架构** — 企业级高可用 Agent 平台的顶层设计（API Gateway、多租户、微服务）
2. **能力框架** — Skills 权限管理、Memory 插件体系、多用户多 Agent 架构
3. **外部集成** — 企业与第三方系统（钉钉、飞书等）的工具链接入
4. **技术栈** —横跨 LLM 框架生态（[[LangChain]]/Dify/[[AutoGen]]/[[OpenClaw]]）、Agent 技术组件（Skills/CLI/RAG/[[MCP]]）

### 与同类 JD 的核心差异

| 维度 | 本 JD | 算法应用开发工程师 JD |
|------|-------|-------------------|
| 定位层级 | **平台层** — 构建 Agent 基础设施/中间件 | **应用层** — 将 AI 能力落地到业务产品 |
| 核心能力 | 微服务架构 / API Gateway / 多租户 SaaS | Agent 应用 / RAG 链路 / 模型微调 |
| 技术聚焦 | Skills | CLI | MCP | 权限管理 | Prompt / Context / Harness 三层工程 |
| 交付目标 | **Agent 平台本身**（内部开发者平台） | **AI 产品功能**（面向最终用户） |
| 工程文化 | 平台工程/中间件/DevOps 基因浓厚 | 算法应用/产品交付基因浓厚 |

这与 [[DeepSeek四份JD全景对比]] 中的 [[摘要-deepseek-service-engineer-jd]]（服务端工程）在架构层面有部分交叉，但本 JD 更强调 **Agent 框架的架构设计与编排能力**，而非纯后端服务。

## 核心职责解析

### 1. 企业级高可用 AI Agent 平台架构设计

- **高可用设计**：多数据中心部署、故障转移、负载均衡
- **Agent 平台**：不仅要跑模型推理，还要管理 Agent 的生命周期、状态持久化、事件驱动
- 关联概念：[[Harness_Engineering]]、[[Agent_Loop]]、[[Graceful_Degradation]]

### 2. Skills 权限管理、Memory 插件、多用户多 Agent 架构

- **Skills 权限管理**：精细化的函数级权限控制，什么 Skill 对什么用户/角色可见可用 → 关联 [[Claude_Code_Skills]]、[[MCP]]
- **Memory 插件**：可插拔的 Agent 记忆后端（对话历史、用户画像、长期知识）→ 关联 [[Memory_Agent]]、[[Claude_Code_Memory_System]]
- **多用户多 Agent 架构**：SaaS 多租户场景下的隔离与共享策略 → Agent 实例级隔离 vs 用户级隔离

### 3. Agent 能力框架

- 定义 Agent 能做什么、不能做什么的标准化接口层
- 推动各业务场景的 Agent 落地：按业务线/场景抽象共性的 Agent 能力
- 关联概念：[[Agent_Orchestration_Patterns]]、[[Multi_Agent_System]]、[[Hierarchical_Task_Decomposition]]

### 4. 外部工具链集成

- 钉钉、飞书等 IM 平台 → 关联 [[Telegram]]、[[Slack]]（Agent 的聊天界面接口）
- 企业内部系统（ERP/CRM/OA 等）
- 需要统一的外部工具接入层 → [[Agent_Interfaces]]、[[MCP]]

## 技术栈全景

| 领域 | 技术栈 | 知识库关联 |
|------|--------|-----------|
| LLM 应用框架 | LangChain, Dify, AutoGen, OpenClaw | [[LangChain]], [[AutoGen]], [[OpenClaw]] |
| Agent 技术组件 | Skills, CLI, RAG, MCP | [[Claude_Code_Skills]], [[Agent_Interfaces]], [[RAG]], [[MCP]] |
| 微服务/API 网关 | API Gateway, 微服务架构 | —（架构经验型，无可直接映射的概念） |
| 多租户 SaaS | 多租户隔离、多用户架构 | —（需结合 Cloud SaaS 通用知识） |
| 外部集成 | 钉钉、飞书 API | [[Telegram]], [[Slack]]（类比参考） |
| Memory 系统 | Memory 插件 | [[Memory_Agent]], [[Claude_Code_Memory_System]] |
| 中间件 | 中间件架构 | — |

## 职位的三层工程模型归属

按照本知识库的三层工程框架 [[Harness_Engineering]]：

| 工程层 | 归属度 | 对应职责 |
|--------|--------|---------|
| **Harness Engineering** | ⭐⭐⭐ | Agent 平台架构、权限管理、多 Agent 编排、外部工具链 |
| **Context Engineering** | ⭐⭐ | Memory 系统设计、RAG 能力集成 |
| **Prompt Engineering** | ⭐ | 框架层以下，较少涉及直接 Prompt 优化 |

## 对标建议

这份 JD 在知识库中最对应的角色是**Agent 平台架构师/基础设施工程师**——需要的不仅是 AI 知识，更是扎实的分布式系统功底。对于准备此职位的候选人，建议：

1. **夯实微服务/中间件基础**：API Gateway 设计模式、多租户隔离策略、高可用架构
2. **深入 Agent 框架源码**：LangChain、AutoGen、OpenClaw 的架构设计
3. **理解 MCP 协议**：作为 Agent 工具调用的标准化协议，是本 JD 技术栈中的关键差异化点
4. **聚焦 Skills 生态**：Skills 的权限、热加载、版本管理是 Agent 平台的核心产品功能

## 关联连接
- [[Harness_Engineering]] — Agent 平台归属的顶层工程层
- [[Agent_Loop]] — Agent 核心运行机制
- [[Memory_Agent]] — Memory 插件系统设计参考
- [[Claude_Code_Skills]] — Skills 系统架构
- [[Claude_Code_Memory_System]] — 三层持久记忆机制
- [[MCP]] — Model Context Protocol，工具调用标准化协议
- [[RAG]] — 检索增强生成
- [[Agent_Interfaces]] — 外部工具链接入
- [[Agent_Orchestration_Patterns]] — 多 Agent 编排模式
- [[Multi_Agent_System]] — 多智能体系统架构
- [[Hierarchical_Task_Decomposition]] — 层级任务分解
- [[LangChain]] — LLM 应用框架生态核心
- [[AutoGen]] — Microsoft Multi-agent 框架
- [[OpenClaw]] — 开源 Skills 插件生态平台
- [[Graceful_Degradation]] — 高可用中的优雅降级
- [[Slack]] — 外部工具链（聊天接口）参考
- [[Telegram]] — 外部工具链（聊天接口）参考
- [[摘要-算法应用开发工程师-jd]] — 同类职位的应用层对比
- [[摘要-deepseek-service-engineer-jd]] — 服务端架构的交叉对比
- [[DeepSeek四份JD全景对比]] — DeepSeek 系列 JD 全景对比
