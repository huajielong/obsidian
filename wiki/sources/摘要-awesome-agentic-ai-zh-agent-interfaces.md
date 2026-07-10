---
title: "摘要-awesome-agentic-ai-zh-agent-interfaces"
type: source
tags: [agent-interfaces, computer-use, browser-use, code-sandbox, agentic-ai, voice-agents, vla]
sources: [raw/01-articles/08-agent-interfaces.zh-Hans.md]
last_updated: 2026-07-10
---

# 摘要：Agent Interfaces（智能体接口）— awesome-agentic-ai-zh Stage 8

> 来源：https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/stages/08-agent-interfaces.zh-Hans.md
> 原始素材已归档至：[[摘要-awesome-agentic-ai-zh-agent-interfaces]]（原始素材在 raw/09-archive/）

本 Stage 是 awesome-agentic-ai-zh 学习路线的 **Track A + Track B 共用 hub**（与 Stage 5 并列核心枢纽），覆盖三大主题：**Computer Use（计算机操控）→ Browser Use（浏览器操控）→ Code Sandbox（代码沙箱）**。

## 核心定位

**Agent Interfaces = Agent 操作 API 以外的真实世界**（IO boundary）。Stage 0-7 教你"如何构建智能体本身"，Stage 8 教你"构建好后，如何操作真实环境"。

### 与之前阶段的区别

| 比较对象 | 该阶段管什么 | 本阶段管什么 |
|---------|-------------|-------------|
| **Stage 3 Tool Use** | 智能体**调用 API**（函数调用、JSON schema） | 智能体**操作环境**（无 API 的软件/网页/运行代码） |
| **Stage 5 MCP** | 工具/数据源如何**标准化暴露**给智能体 | 智能体如何**实际与环境交互**（MCP 是协议，Interface 是行为）|
| **Stage 7 Harness** | 智能体**运行时控制流**（循环/重试/安全）| 智能体**IO 边界**（运行时内看不到的外部互动）|

**核心区别**：Tool = API 调用，Interface = 操作环境

## 2024-2026 突破时间线

- **2024-10 之前**：智能体只能与有 API 的世界互动
- **2024-10**：Anthropic Computer Use beta → **第一次能操作真实屏幕**
- **2025-2026**：OpenAI（Atlas + Codex desktop）/ Google（Gemini in Chrome）全线入场
- **2026-05**：OSWorld benchmark 达 **76.26%**（超越人类基线 72.36%）

## Computer Use — 四强对比

| 厂商 | 产品 | OSWorld | 特点 |
|------|------|---------|------|
| **Anthropic** | Opus 4.8 / Sonnet 5 CU | 72.7% | GA，跨 macOS/Linux/Windows(Docker) |
| **OpenAI** | Codex desktop + CUA | 38.1% / WebArena 58.1% | Background mode 不抢占光标，90+ 插件 |
| **Google** | Gemini in Chrome (Gemini 3) | — | Auto Browse + Chrome Skills，企业 $6/用户/月 |
| **Operator** | ❌ 2025-08 停运 | — | 被 Atlas 取代 |

**OSWorld 关键数据**：Human baseline 72.36%，2026-05 SOTA 76.26% 已超越人类，但 UC Berkeley 2026-04 证实 OSWorld 可被 reward-hack 到 100%。

### 平台支持

| OS | Anthropic | OpenAI | Google |
|----|-----------|--------|--------|
| macOS | ✅ GA | ✅ Atlas + Codex GA | Chrome 内 |
| Linux | ✅ Docker | ⚠ 受限 | Chrome 内 |
| Windows | ✅ Docker | 🔜 native preview | Chrome 内 |
| Mobile | — | — | ✅ Android |

## Browser Use — 三种导航模式

| 模式 | 原理 | 速度 | 可靠性 |
|------|------|------|--------|
| **DOM-aware** | 读取 HTML DOM → CSS selector 定位 | 快 | 高 |
| **Accessibility Tree** | 读无障碍树（2026 production 主流）| 快 | 稳 |
| **Vision fallback** | 截图 + vision 分析 | 慢 | 中 |

> **Playwright MCP**（★34k, Apache-2.0）— Track A 直接挂 Claude Code 可用的浏览器 MCP，走 accessibility tree

### 闭源 AI 浏览器五强（2026-05）

Atlas（OpenAI）/ Comet（Perplexity）/ Dia（Browser Company）/ Gemini in Chrome（Google）/ Operator（❌ 停运）

## Code Sandbox — 隔离技术术语小词典

| 术语 | 隔离强度 | 启动速度 | 典型用途 |
|------|---------|---------|---------|
| **Container**（Docker）| 弱（共享内核）| 快 < 1s | 低风险任务 |
| **VM** | 最强 | 慢（秒级）| 企业级 |
| **microVM** ⭐ | **强** | **快 < 100ms** | **智能体沙箱理想选择** |
| **Firecracker** | 强 | 快 | AWS Lambda 底层，E2B 使用 |
| **gVisor** | 中强 | 中快 | Google 用户空间内核 |

### 7 个沙箱对比

详细对比见原文，关键选择：
- **延迟敏感** → Daytona（< 90ms）
- **Python 智能体** → E2B（Firecracker microVM，模板最丰富）
- **GPU 需求** → Modal（唯一 GPU 沙箱）
- **Web 技术栈** → Vercel Sandbox
- **Edge 部署** → Cloudflare Workers（< 100ms）

### OpenAI Agents SDK 2026-04 里程碑

内建 harness 抽象层 + 7 个沙箱提供商（Blaxel/Cloudflare/Daytona/E2B/Modal/Runloop/Vercel）+ Codex filesystem tools。**这是 sandbox 从"可选插件"变为"Agent Framework 标配组件"的标志性事件。**

## Track A 如何使用

- **Computer-use MCP** → 在 Claude Code 内接入桌面操作
- **Codex desktop background mode** → 不抢占光标，多智能体并行
- **AI 浏览器选择**：研究用 Comet / ChatGPT 用户用 Atlas / 企业用 Gemini in Chrome

## Track B 如何构建

- **browser-use**：5 行 Python 编写 web agent（86k+ stars, MIT, LLM 厂商无关）
- **E2B**：Firecracker microVM 隔离执行 Python 代码
- **OpenAI Agents SDK**：内建 sandbox 抽象的 production harness
- **GUI 训练数据**：OSWorld（369 跨 OS 任务）/ WebArena / Mind2Web

## ⚠ 2026 安全性重点

### 真实案例

1. **Comet 注入**（Brave Research 2026）：网页隐藏恶意 prompt → LLM 解析后执行 → 智能体被劫持。**新攻击面**：web 内容 → LLM 上下文（不同于传统 SQL 注入的路径）
2. **联邦禁令**（2026-03）：Comet 被禁止访问 Amazon 账户，操作不稳定 + 未经授权商业活动

### 4 个防护模式

| 模式 | 说明 | 何时必须 |
|------|------|---------|
| **审批门** | 高风险操作前弹窗确认 | 所有生产级智能体 |
| **沙箱** | 代码在隔离环境运行 | 任何会运行代码的智能体 |
| **人工介入** | 长时间任务中段检查点 | 任务 > 10 步或 > 5 分钟 |
| **输出过滤器** | 目标限定白名单 | 跨系统操作的智能体 |

## 下一个前沿（Stage 9 待规划）

- **Voice Agents**：Vapi / Retell / LiveKit Agents / OpenAI Realtime API
- **VLA（Vision-Language-Action）机器人**：RT-2（Google）、OpenVLA（Stanford）、π0（Physical Intelligence）、Helix（Figure AI）

## 关联连接

- [[Agent_Interfaces]] — 三层智能体接口概念
- [[Harness_Engineering]] — Sandbox 是 Harness 的 Safety Layer 元件
- [[Agent_Loop]] — Agent Loop 运行循环
- [[MCP]] — MCP 协议（与 Interface 互补：MCP=协议, Interface=行为）
- [[Claude_Agent_SDK]] — 内建 Computer Use 的 SDK
- [[Codex]] — OpenAI 编码 agent，内建 CUA + 7 个 sandbox
- [[OpenAI_Agents_SDK]] — 2026-04 内建 sandbox 生态
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — 前置 Stage 7（Harness 8 元件）
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 前置 Stage 7.5
- [[摘要-awesome-agentic-ai-zh-tool-use]] — Stage 3（Tool Use 与 Interface 的区分）
