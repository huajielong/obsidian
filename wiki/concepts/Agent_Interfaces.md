---
title: "Agent Interfaces（智能体接口）"
type: concept
tags: [agent-interfaces, computer-use, browser-use, sandbox, agentic-ai, human-agent-interaction, voice-agents, vla]
sources: [raw/01-articles/08-agent-interfaces.zh-Hans.md]
last_updated: 2026-07-10
---

# Agent Interfaces（智能体接口/Agent 操作界面）

Agent Interfaces 是指 AI Agent 与非 API 世界（桌面应用、网页、操作系统）交互的三种核心接口。它是 Agent 的 **IO 边界（Input/Output Boundary）**，与 Tool Use（API 调用）、MCP（协议标准化）、Harness（运行时控制流）形成互补。

## 三层接口模型

| 层次 | 接口 | 操作对象 | 工作原理 |
|------|------|---------|----------|
| 🖱 **Screen-level** | Computer Use | 任何桌面应用（无 API 限制） | 截图 → 视觉分析 → 坐标映射 → 模拟键鼠 |
| 🌐 **Web-level** | Browser Use | 任何网页 | DOM / Accessibility Tree 导航 + Vision fallback |
| 📦 **Runtime-level** | Code Sandbox | Agent 生成的代码 | microVM/Container 隔离执行 |

## 与相邻概念的区分

| 比较对象 | 管什么 | 本概念管什么 |
|---------|-------|-------------|
| **Tool Use（Stage 3）** | 智能体**调用 API**（函数调用、JSON schema） | 智能体**操作环境**（无 API 的软件/网页/运行代码）|
| **MCP（Stage 5）** | 工具/数据源如何**标准化暴露**给智能体 | 智能体如何**实际与环境交互**（MCP 是协议，Interface 是行为）|
| **Harness Engineering（Stage 7）** | 智能体**运行时控制流**（循环/重试/安全）| 智能体**IO 边界**（运行时内看不到的外部互动）|

**核心区别**：Tool = API 调用，Interface = 操作环境

## 2024-2026 突破时间线

- **2024-10 之前**：智能体只能与有 API 的世界互动
- **2024-10**：Anthropic Computer Use beta → **智能体第一次能操作真实屏幕**
- **2025-2026**：OpenAI（Atlas + Codex desktop）/ Google（Gemini in Chrome）全线入场 → 主流化
- **2026-05**：OSWorld benchmark 达 **76.26%**（超越人类基线 72.36%）
- **2026-04**：OpenAI Agents SDK 内建 7 个 sandbox 提供商 → Sandbox 成为 Agent Framework 标配
- **2026-03**：Comet 注入事件 + 联邦禁令 → Agent 安全成为生产级部署必须关注的问题

---

## Computer Use（计算机操控）

AI 通过视觉理解界面，模拟人类操作（点击/输入/滚动）操控桌面应用。不依赖 API，而是"看着屏幕 → 思考 → 操作"。

### 工作流程
```
智能体收到任务 → 1. 截图 → 2. 视觉模型解析 → 3. 计算坐标 → 4. 模拟键鼠 → 5. 再次截图验证
```

### 2026 四强对比

| 厂商 | 产品 | OSWorld | 特点 |
|------|------|---------|------|
| **Anthropic** | Opus 4.8 / Sonnet 5 Computer Use | 72.7% | GA，跨 macOS/Linux/Windows(Docker) |
| **OpenAI** | Codex desktop + CUA（Computer-Using Agent）| CUA 38.1% / WebArena 58.1% | Background mode 不抢占光标，90+ 插件 |
| **Google** | Gemini in Chrome（Gemini 3）| — | Auto Browse + Chrome Skills，企业 $6/用户/月 |
| **OpenAI Operator** | ❌ 2025-08 停运 | — | 被 Atlas 取代 |

### 平台支持

| OS | Anthropic | OpenAI | Google |
|----|-----------|--------|--------|
| macOS | ✅ GA | ✅ Atlas + Codex GA | Chrome 内 |
| Linux | ✅ Docker | ⚠ 受限 | Chrome 内 |
| Windows | ✅ Docker | 🔜 native preview | Chrome 内 |
| Mobile | — | — | ✅ Android |

### OSWorld Benchmark 解读

| 模型 | OSWorld | 与人类基线差距 |
|------|---------|-------------|
| Human baseline | 72.36% | — |
| Claude Opus 4.6 | 72.7% | 持平 |
| 2026-05 SOTA | **76.26%** | **超越人类** |
| OpenAI CUA | 38.1% | -34% |

> ⚠ OSWorld 在 [UC Berkeley 2026-04 Reward-Hacking 报告](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/) 中证实可被 hack 到 100%

---

## Browser Use（浏览器操控）

AI 通过在浏览器中导航来操控网页。2026 production 主流使用三种模式：

### 三种导航模式

| 模式 | 原理 | 速度 | 可靠性 |
|------|------|------|--------|
| **DOM-aware** | 读取 HTML DOM → CSS selector/XPath 定位 | 快 | 高 |
| **Accessibility Tree** | 读无障碍树（2026 production 主流） | 快 | 稳 |
| **Vision fallback** | 截图 + vision 分析 | 慢 | 中 |

> **Playwright MCP**（★34k, Apache-2.0）— 走 accessibility tree 的浏览器 MCP，Track A 用户可直接挂到 Claude Code 使用

### AI 原生浏览器五强（2026-05）

| 浏览器 | 开发商 | 平台 | Agent Mode | 备注 |
|--------|--------|------|-----------|------|
| **Atlas** | OpenAI | macOS GA, Win 🔜 | ✅ | Plus/Pro/Business 内建 |
| **Comet** | Perplexity | iOS/Android/Win/Mac | ✅ | ⚠ 2026 Brave 发现注入漏洞 + 联邦 Amazon 禁令 |
| **Dia** | Browser Company | macOS | ❌（聚焦性能）| 被 Atlassian 以 $6.1 亿收购 |
| **Gemini in Chrome** | Google | 全平台 + Android | ✅ Auto Browse + Skills | Enterprise Premium $6/用户/月 |
| **Operator** | OpenAI | — | ❌ 2025-08 停运 | CAPTCHA/JS/session 不稳定 |

### 开源框架

- **browser-use**（86k+ stars, MIT）— 5 行 Python 上手，LLM 厂商无关，DOM-first + vision fallback
- **Microsoft OmniParser v2**（Apache 2.0）— 基于视觉的 GUI 解析，延迟改善 60%，含 OmniTool（Windows VM 控制）
- **Playwright + LLM（DIY）**— web 自动化标准 + LLM 包装器

---

## Code Sandbox（代码沙箱）

Agent 生成的代码不能在宿主环境直接运行—— Sandbox 提供安全的隔离执行环境。

### 隔离技术层级

| 技术 | 隔离强度 | 启动速度 | 说明 |
|------|---------|---------|------|
| **Container（Docker）** | 弱（共享内核）| 快 < 1s | 多容器共享主机内核 |
| **microVM ⭐** | **强** | **快 < 100ms** | **智能体沙箱理想选择** |
| **VM** | 最强 | 慢（秒级）| Hypervisor 提供虚拟硬件 |
| **Firecracker** | 强 | 快 | AWS 开源，Rust 编写，Lambda 底层，E2B 使用 |
| **gVisor** | 中强 | 中快 | Google 用户空间内核，拦截系统调用 |

**核心结论：microVM = 兼顾隔离强度与启动速度，大多数智能体沙箱选择 microVM**

### 七种 Sandbox 对比（2026-05）

| Sandbox | 隔离技术 | 冷启时间 | 强项 |
|---------|---------|---------|------|
| **Daytona** | Container | **< 90ms（最快 27ms）** | 最快启动，延迟敏感场景 |
| **E2B** | Firecracker microVM | ~200ms | Python 生态最丰富，最多社区模板 |
| **Modal** | microVM + GPU | ~1s | **唯一 GPU sandbox**（推理/微调）|
| **Vercel Sandbox** | Container | <500ms | Vercel 生态整合 |
| **Cloudflare Workers** | V8 Isolate | <100ms | Edge 全球部署 |
| **Runloop** | — | — | OpenAI SDK 2026-04 内建 |
| **Blaxel** | — | — | OpenAI SDK 2026-04 内建 |

### OpenAI Agents SDK 2026-04 里程碑

**之前**：OpenAI SDK 开发生产级编码 agent 需要自己接沙箱、写 harness
**之后**：SDK 内置 harness 抽象层 + sandbox 抽象层 + Codex filesystem tools
→ **Sandbox 从"可选插件"变为"Agent Framework 标配组件"**

---

## ⚠ 安全性重点

### 真实事故案例

1. **Comet 注入**（Brave Research 2026）：恶意网页隐藏 prompt → agent 读取后执行恶意指令 → 智能体被劫持。**新攻击面**：web 内容 → LLM 上下文（防御方式不同于 SQL 注入）
2. **联邦禁令**（2026-03）：Comet 被禁止访问 Amazon 账户，操作不稳定 + 未经授权商业活动

### 4 个防护模式

| 模式 | 说明 | 何时必须 |
|------|------|---------|
| **审批门** | 高风险操作前弹窗确认 | 所有生产级智能体 |
| **沙箱** | 代码在隔离环境运行 | 任何会运行代码的智能体 |
| **人工介入** | 长时间任务中段检查点 | 任务 > 10 步或 > 5 分钟 |
| **输出过滤器** | 目标限定白名单 | 跨系统操作的智能体 |

---

## Track A 使用方法（CLI Power User）

- **Computer-use MCP** → 在 Claude Code 内接入桌面操作（`.mcp.json` 配置）
- **Codex desktop background mode** → 不抢占光标，多智能体并行后台运行
- **AI 浏览器**：研究用 Comet / ChatGPT 用户用 Atlas / 企业用 Gemini in Chrome

## Track B 构建方法（Agent Builder）

- **browser-use**：5 行 Python 编写 web agent，LLM 厂商无关
- **E2B**：Firecracker microVM 隔离，`Sandbox().run_code(python_code)` 执行
- **OpenAI Agents SDK**：`Agent(..., sandbox=Sandbox(provider="e2b"))` 内建 sandbox
- **GUI 训练数据集**：OSWorld（369 跨 OS 任务）/ WebArena / Mind2Web

## 下一个前沿

- **Voice Agents**：Vapi / Retell / LiveKit Agents / OpenAI Realtime API
- **VLA（Vision-Language-Action）机器人**：RT-2（Google DeepMind）/ OpenVLA（Stanford）/ π0（Physical Intelligence）/ Helix（Figure AI）

## 关联连接

- [[Harness_Engineering]] — Sandbox 是 Harness Safety Layer 元件；Interface 是 Harness 看不到的外部 IO
- [[Agent_Loop]] — Computer Use 操作嵌入在 Agent Loop 内
- [[MCP]] — MCP 是协议，Interface 是行为（互补关系）
- [[Claude_Agent_SDK]] — 内建 Computer Use 的 SDK
- [[Codex]] — OpenAI 编码 agent，内建 CUA + 7 个 sandbox
- [[OpenAI_Agents_SDK]] — 2026-04 内建 sandbox 抽象层
- [[AgentParadigms]] — Agent 五种部署范式，与 Interface 交互方式强相关
- [[摘要-awesome-agentic-ai-zh-agent-interfaces]] — 本概念的源素材摘要

- [[多模态理解研究]] — 内容来源：GUI Agent 属于 Computer Use 层，多模态理解研究为 Agent Interface 提供视觉感知基础
- [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — 前置 Stage 7
