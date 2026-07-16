---
title: "Dify"
type: entity
tags: [LLM平台, 低代码, Agent平台, RAG, Workflow, 开源]
sources: []
last_updated: 2026-07-16
---

# Dify

Dify 是一个开源的 **LLM 应用开发平台**，以可视化 Workflow 编排和低代码理念为核心，让开发者能快速构建 Agent 应用、RAG 知识库、对话机器人和自动化工作流。

- **官网**：https://dify.ai
- **GitHub**：https://github.com/langgenius/dify
- **Star**：★ 70k+

## 核心特性

### 1. 可视化 Agent 编排

Dify 的核心差异化是 **所见即所得的 Agent 构建体验**——通过拖拽式界面完成从 Prompt 设计到工具调用的全过程：

| 组件 | 功能 | 对比 LangChain |
|------|------|---------------|
| **Chatflow** | 对话式 Agent 流程编排 | 类似 LangGraph 但可视化 |
| **Workflow** | 自动化批处理流程（非对话） | 类似 LangChain Chain |
| **Agent 节点** | 定义 Agent 行为、工具、记忆 | 内置 ReAct / Function Calling 模式 |
| **工具节点** | 调用 API/插件/自定义工具 | MCP 兼容 + 内置工具市场 |

### 2. RAG Pipeline 集成

内置从文档导入到检索生成的全链路：

```
文档上传 → 文档解析 → Chunk 策略 → Embedding → Vector DB → 检索策略
```

支持多款 Vector DB（Weaviate / Qdrant / Milvus / Pinecone），并提供 Eval 面板做检索质量评估。

### 3. 模型管理

- 统一模型接入层，支持 OpenAI / Claude / Llama / Qwen / DeepSeek 等 30+ 模型
- 支持模型路由、负载均衡、Failover
- 内置 Token 用量监控与成本统计

### 4. 多租户与权限

| 层级 | 功能 |
|------|------|
| **Workspace** | 工作空间级隔离，每个空间独立数据集/应用/配置 |
| **团队协作** | 成员管理、角色分配（Owner / Admin / Editor / Viewer） |
| **API Key** | 应用级 API Key 管理，支持过期和速率限制 |
| **SSO** | LDAP / OAuth 2.0 企业登录集成 |

### 5. 应用发布

- **WebApp**：直接生成对话式 Web 应用
- **API**：RESTful API 方式集成到现有系统
- **嵌入**：iframe 嵌入第三方网站
- **Clients**：通过 API 对接微信/钉钉/飞书等 IM 平台

## 技术栈

| 组件 | 实现 |
|------|------|
| **后端** | Python (Flask) + PostgreSQL + Redis |
| **前端** | Next.js + TypeScript |
| **Workflow 引擎** | 自研 DAG 图形化编排引擎 |
| **Vector DB** | Weaviate / Qdrant / Milvus / pgvector |
| **文档解析** | Unstructured / PyMuPDF / MarkItDown |
| **模型接入** | 自研 Model Provider 抽象层 |

## 生态定位

Dify 在 LLM 应用开发工具谱系中的位置：

```
                     代码深度 →
                      
  无代码/低代码 ←── Dify ──→ LangChain/LlamaIndex
  (拖拽构建)        │           (编程构建)
                    │
                    ├── 可视化 Workflow 编排
                    ├── 内置 RAG Pipeline
                    └── 多租户团队协作
  
  OpenClaw  ←─── 同级对比 ───→ Dify
  (Skills 插件生态)             (Workflow 可视化)
```

### Dify vs OpenClaw vs LangChain

| 维度 | Dify | OpenClaw | LangChain |
|------|------|---------|-----------|
| **核心理念** | 可视化低代码平台 | Skills 插件生态 | 编程框架 |
| **目标用户** | 产品经理/开发者 | Agent 终端用户 | 工程师/研究者 |
| **Workflow** | ✅ 可视化 DAG | ✅ Session v2.0 | ❌ 纯代码（LangGraph） |
| **Skills/插件** | 内置工具市场 | 1700+ Skills 生态 | 代码级 Tool 定义 |
| **多租户** | ✅ Workspace 级 | ❌ 单用户为主 | ❌ 需自建 |
| **部署方式** | Docker 自部署 / SaaS | CLI + 云端 | 库引用 |
| **开源协议** | Apache 2.0 | MIT | MIT |

## 与本 JD 的关联

本 JD（智能体研发工程师）中 Dify 被列为核心技术栈之一，核心价值在于：

1. **低代码 Agent 构建** — 了解可视化 Workflow 引擎的设计思路，可借鉴到自建 Agent 平台
2. **多租户实现** — Dify 的 Workspace 隔离模型是企业 SaaS 架构的参考模板
3. **RAG Pipeline 整合** — 文档解析→Chunking→检索的完整链路设计
4. **模型统一接入** — Model Provider 抽象层如何实现"一行代码换模型"

## 关联连接
- [[LangChain]] — 同属 LLM 应用框架生态，编程范式 vs 可视化范式
- [[OpenClaw]] — 开源 Agent 平台竞品，Skills 生态 vs Workflow 可视化
- [[Claude_Code_Skills]] — Skills 行为层，与 Dify 的工具节点概念对应
- [[MCP]] — Dify 工具市场的底层协议兼容
- [[RAG]] — Dify 内置的 RAG Pipeline 参考
- [[摘要-算法应用开发工程师-jd]] — AI 应用层 JD，与 Dify 定位重叠
- [[摘要-智能体研发工程师-jd]] — 本 JD，Dify 被列为要求技术栈
