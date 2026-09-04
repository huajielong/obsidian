---
title: "Anthropic"
type: entity
tags: [AI公司, Anthropic, Claude, API, Agent生态]
sources: 
  - raw/01-articles/Claude Code 完全指南 - 阿里云开发者社区.md
  - raw/01-articles/awesome-agentic-ai-zh-stage-01-llm-basics.md
  - raw/01-articles/05-claude-code-ecosystem.md
  - raw/09-archive/The AI-Native SDLC playbook  Claude by Anthropic.md
last_updated: 2026-09-04
---

## 定义

Anthropic 是一家 AI 研究与部署公司，由前 OpenAI 成员创立，专注于构建安全、可解释的 AI 系统。其旗舰产品包括 Claude 系列对话模型、Claude Code 终端 AI 编码助手、Claude Cowork 桌面 AI 应用，以及 Claude Security（hosted 定时安全扫描）、Claude Tag（Slack 值班 Agent）、Claude Design（设计 mock）等企业级 Agent 产品。

## 关键信息

- **创立背景**：由前 OpenAI 成员创立
- **核心产品**：Claude 系列 AI 模型、Claude Code（工程师终端 Agent）、Claude Cowork（非工程师桌面 App）、Claude Security（定时代码扫描）、Claude Tag（IM 值班 Agent）、Claude Design（设计 mock，beta）
- **Context Window**：1M tokens（约 50 万中文字）
- **技术理念**：注重 AI 安全性、可解释性和对齐研究
- **方法论输出**：Applied AI 团队发布《The AI-Native SDLC Playbook》，给出智能体化软件生命周期的六阶段改造路线（见 [[AI_SDLC]]）

### Agent 产品线对比

| 形态 | 目标用户 | 能力 | 
|------|---------|------|
| **Claude Code** | 工程师（Terminal Agent） | 读/改/跑代码，完整 File/Shell/Git/Subprocess 访问 |
| **Claude Cowork** | 非工程师（桌面 App） | 跨文件/应用程序/网页完成一个目标 |
| **Claude API** | 开发者（编程接口） | LLM Call + 自包 Agent Loop |
| **Claude Agent SDK** | 开发者（Python/TS） | 完整 Agent Runtime + Tool Use + 多 Session |
| **Claude Security** | 安全团队（SaaS） | 连 GitHub 仓库的 hosted 定时代码扫描，findings 验证 + 置信度，补丁走 PR gate |
| **Claude Tag** | 值班/事件响应（IM） | 以自身身份入 Slack 频道，即时响应 incident，频道即审计追踪 |

### 模型家族（2026-06）

| 等级 | 模型 | Context | 价格（per 1M tokens） | 特点 |
|:----|:----|:-------:|:--------------------:|:-----|
| **旗舰** | Opus 4.8 | 1M | $5 in / $25 out | 最强复杂推理，目前可用最高层级 |
| **均衡** | Sonnet 5 | 1M | $3 in / $15 out | 速度与品质平衡，生产环境默认 |
| **经济** | Haiku 4.5 | 200k | $1 in / $5 out | 最快最便宜，适合简单任务 |
| **神话级** | Fable 5 ⚠️ | 1M | $10 in / $50 out | Opus 之上，曾暂停（当前状态存疑，见注记） |

> ⚠️ **版本状态沿革**：**Fable 5**（Mythos-class，2026-06-09 上线）与其姊妹版 **Mythos 5** 曾于 2026-06-12 被美国出口管制指令暂停存取。据 2026-09《The AI-Native SDLC Playbook》，**Mythos 5 已在 Anthropic 基础设施中恢复可用**——Claude Security 的 hosted 代码扫描即运行在 Claude Mythos 5 上并按 Mythos 5 费率计费；本页据此**以新来源覆盖**早前「暂停存取、无法使用」的说法。**Fable 5** 的当前状态未在新来源中提及，仍存疑；已确认可用最高层级参考 **Opus 4.8**。
>
> **Sonnet 5**（2026-06-30 上线）是当前 Sonnet 版本：1M context、速度快、价格维持 $3/$15。

### 强项与适用场景

- **Long-form / Coding** — 长文生成、代码审查、论文写作
- **Agent runtime** — Claude Code 驱动，适合 agent 编程
- **Safety alignment** — 行业领先的 AI 安全性
- **教材完整度** — Anthropic Cookbook + Courses 社群公认为最完整的 LLM API 学习资源

## 关联连接

- [[Claude_Code]] — Anthropic 推出的终端 AI 编码助手
- [[Claude_Agent_SDK]] — Anthropic 推出的 Agent Python SDK
- [[Claude_Security]] — Anthropic hosted 定时代码安全扫描
- [[Claude_Tag]] — Anthropic IM 值班/事件响应 Agent
- [[AI_SDLC]] — Anthropic Applied AI 团队发布的 AI-Native SDLC 方法论
- [[摘要-ai-native-sdlc-playbook]] — 该 Playbook 的来源摘要
- [[Agentic_Coding]] — Anthropic 的 Claude Code 所属的 AI 编程范式
- [[MCP]] — Anthropic 提出的 Model Context Protocol 开放标准
- [[Claude_Code_Harness]] — Claude Code 7-Layer Architecture
- [[Multi_Agent_System]] — Anthropic "Building Effective Agents" 的核心观点：90% 场景不该用 Multi-agent
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — 本路线图 Stage 4，引用 Anthropic 的 Building Effective Agents
- [[摘要-claude-code-guide]] — 来源文章
- [[摘要-awesome-agentic-ai-zh-llm-basics]] — LLM 基础补充信息
- [[OpenAI]] — 同为美系商业前沿的竞争对手
- [[Context_Window]] — 1M context 详解
- [[GPT]] — GPT 通用概念
