---
title: "Agent 五种部署范式"
type: concept
tags: [AI代理, Agent范式, 部署模式, 开发工具链, Agent运行环境]
sources: [https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/resources/agent-paradigms.zh-Hans.md]
last_updated: 2026-07-14
---

# Agent 五种部署范式

> **一句话**：Cursor 是 agent、Claude Code 是 agent、Telegram 上陪你聊天的 Hermes 也是 agent、家里 Jetson 板子跑的 OpenClaw 也是 agent——但用起来完全不同感受，因为它们属于**不同的部署范式**。真正的分水岭不在 LLM 是哪家，而在 **agent 跑在哪、你用什么界面跟它互动、需不需要联网**。

## 核心框架

这五种范式可进一步归为两大类：

| 类别 | 包含的 Type | 核心特征 |
|------|------------|---------|
| **Co-located Agent**（共位代理） | Type 1–3 | agent 跟你一起在 laptop 上、你走它停 |
| **Deployed Autonomous Agent**（部署型自主代理） | Type 4–5 | agent **不在你 laptop 前**、跑在外面 24×7 服务你 |

理解这五种范式的差异，不只是"换工具"——而是**换思考方式**。同一个 use case 从 Type 2 搬到 Type 4，需要重新理解人与 agent 的互动边界、成本结构和可靠性模型。

---

## 一图总览

| Type | 代表项目 | Agent 跑在哪 | 交互界面 | LLM 来源 | 离线可用? | 月成本（粗估）|
|------|---------|-------------|---------|---------|----------|--------------|
| **1. IDE-coupled** | [[Cursor]] / [[Cline]] / Windsurf | IDE 内部 | IDE 侧边栏 | 多 provider | ❌ | $0–20 |
| **2. Terminal pair-programmer** | [[Claude_Code]] / [[Codex]] / Gemini CLI | 终端 | terminal REPL | 绑定特定厂商 | ❌ | $20 订阅或 API 用量 |
| **3. BYO-LLM CLI** | [[Aider]] / OpenCode / [[Goose_AI]] | 终端 | terminal REPL | 自帶 API Key | ❌ | API 用量 |
| **4. Cloud-deployed** | [[Hermes Agent]] | VPS / 云端 | [[Telegram]] / [[Slack]] / 任一 chat app | 200+ provider 路由 | ❌ | ~$5 server + API |
| **5. Edge-deployed** | [[OpenClaw]] / ClawBox | Jetson 板子 / Raspberry Pi | local chat / SSH | 本机 [[Ollama]]（[[Qwen]] / [[Llama]] / Mistral）| ✅ | 硬件 €549、之后 ≈ $0 |

---

## Type 1: IDE-coupled（IDE 集成式）

**运行位置**：IDE 侧边栏（Sidebar）

**核心逻辑**：写代码时你的**眼睛要看代码**，不能频繁切换到 terminal 对话。IDE-coupled agent 把 LLM 放在视线旁边，保留完整的视觉上下文（editor + inline diff + file tree）。

**典型工作流**：选一段 code → 按快捷键（如 `Cmd+K`）→ LLM 就地改写 → 查看 inline diff → accept/reject。

**代表项目**：[[Cursor]]、Windsurf、[[Cline]]、Continue、Zed

**适合场景**：
- Edit 多、Explore 少的迭代式编码
- Side-by-side coding + visual diff 需要
- 快速代码重构 inline 完成

**不适合场景**：
- 需要 agent 自主执行多步骤长任务（sidebar 不太自由）
- Non-coding 任务

---

## Type 2: Terminal pair-programmer（终端结对编程式）

**运行位置**：你的终端（Terminal）

**核心逻辑**：把整个 terminal 变成 agent 的 workspace——agent 拥有 file system / shell / git 完整访问权，可以自主完成多步骤复杂任务。比 Type 1 更 autonomous。

**典型工作流**：在 terminal 启动 agent → 输入自然语言指令（如"重构整个 auth module"）→ agent 自己读档、改档、跑测试、报告结果 → 你看 streaming output。

**代表项目**：[[Claude_Code]]（Anthropic）、[[Codex]]（OpenAI）、Gemini CLI（Google）

**关键特性**：
- 订阅制为主（如 Claude Code $20/月整月可用，不按 token 计费）
- 绑定特定 LLM 家族
- 比 Type 1 更高的自主度

**适合场景**：
- Agentic task（长 refactor、paper writing）
- 任何超出 1–2 步的复杂工作
- 需要完整 file system / shell / git 访问

**不适合场景**：
- 跨多家 LLM 比较成本
- 非 coding/writing 场景
- 离线环境

---

## Type 3: BYO-LLM CLI（自帶模型 CLI 式）

**运行位置**：你的终端（Terminal）

**核心逻辑**：与 Type 2 相同的 terminal REPL 模式，但 LLM 来源由用户自带——任何 OpenAI-compatible endpoint 都可接入。属于 **multi-provider** 同一思维模型。

**与 Type 2 的本质区别**：Type 2 绑定特定供应商，Type 3 的用户自带 API Key，可以在不同模型间自由切换。

**典型工作流**：设定 provider 和 model（如 `--model deepseek/deepseek-reasoner`）→ 设环境变量 `OPENROUTER_API_KEY` → 运行 agent，git-aware，自动写 commit message。

**代表项目**：[[Aider]]、OpenCode、[[Goose_AI]]、[[Hermes Agent]]（CLI 模式）

**关键特性**：
- Cost-sensitive，可灵活选择性价比模型
- 多 provider 横向比较
- 支持自架 LLM（[[Ollama]] / vLLM）

**适合场景**：
- 实验多家 LLM 对比效果和成本
- 省钱（用小模型做简单任务）
- 本机 LLM 推理
- 不想被单一供应商绑定

**不适合场景**：
- 怕 setup 复杂（需要管理 API Key、provider config）

---

## Type 4: Cloud-deployed（云端部署式）

**运行位置**：VPS / Modal 等云端服务（24×7）

**核心逻辑**：当 agent 是 **"个人助理"** 而不是 pair programmer 时，它不该绑在你的 laptop 上。Type 4 把 agent 变成 24×7 在线服务，通过 chat app 交互。

**典型工作流**：你在地铁上用手机打 Telegram → 对 agent 发指令（如"整理今天 arXiv 新 paper"）→ agent 自主调用多模型完成 → 传回结果。全程无需碰 laptop。

**代表项目**：[[Hermes Agent]]（Nous Research，★ 213k+）

**5 大核心特性**：

1. **Multi-platform chat interface**：Telegram / Discord / Slack / WhatsApp / Signal 均可作为入口
2. **Multi-LLM routing（200+ models）**：OpenRouter + NVIDIA NIM + 智谱 GLM + Kimi + 小米 MiMo + MiniMax + HF + OpenAI + Anthropic + Google——**同一 conversation 内可跨 LLM**
3. **24/7 在线**：不依赖你 laptop，cloud VPS host，任何时刻可用
4. **Built-in cron**："每天 9am 抓 X 给我 Y"这类 routine 直接内建
5. **自我学习技能**（实验中）：agent 与你互动久了，自动归纳可复用的 skill，跨 session 累积演化

**适合场景**：
- 跨平台通知与任务分发
- 24/7 routine（每天抓 paper / 看股票 / 提醒）
- 中国区 LLM 支持（GLM / Kimi）——国际服务中断时可用作接力
- 多 LLM cost optimization
- 非 laptop-bound 工作流

**不适合场景**：
- 纯写代码（Type 2 更自然）
- 不想 self-host VPS
- 对 production reliability 要求高（需要专业运维）

---

## Type 5: Edge-deployed（边缘部署式）

**运行位置**：Jetson 板子 / Raspberry Pi 等边缘硬件

**核心逻辑**：当数据**绝对不能离开本机**时（医疗 / 法律 / 军工 / 隐私敏感），cloud 方案不是选项。Type 5 把 agent 完全放在 on-device 运行，用一次硬件投资换取 0 cloud cost + 0 data exposure。

**典型工作流**：法律事务所买一台 ClawBox（NVIDIA Jetson Orin Nano + 预装 OpenClaw + Ollama + Qwen 3.5 7B）→ 放在内网 → SSH 进去工作 → 所有资料只在盒子里，零 telemetry、零 API call、完全可审计。

**代表项目**：[[OpenClaw]]（社群）/ ClawBox（€549 预装套件，67 TOPS）

**5 大核心特性**：

1. **Hardware-specific**：NVIDIA Jetson（Orin Nano 8 GB / Thor 128 GB）或 Raspberry Pi，GPU 加速边缘推理
2. **本机 LLM only**：[[Ollama]] backend，运行 [[Qwen]] / [[Llama]] / Mistral / Gemma 等 open-weight 模型，**没有任何 cloud API call**
3. **零云端依赖 / 完全可审计**：localhost-bound、network-isolated
4. **Edge-optimized memory**：semantic search memory file < 10 MB，跨 session 记忆
5. **Physical AI bridge**：可控制物理设备（robot / sensor / smart home），跨 physical + digital 环境

**适合场景**：
- 隐私敏感数据处理（医疗 / 法律 / 军工）
- Offline-first 环境
- 家用 AI box（smart home）
- Physical AI（robot）
- 长期持有、不想付 API recurring cost

**不适合场景**：
- 不熟悉 Linux / NVIDIA 环境
- 需要前沿大模型（GPT-5 / Claude Opus）
- 不想一次性投入硬件成本

---

## 额外维度：Subagent（子代理）

上述 5 个 type 描述的是 **agent 跑在哪里**。**Subagent** 是另一个正交维度：**一个 agent 在执行任务时，spawn 出另一个 agent 跑子任务**。

主要有两条实现路径：

| 路径 | 启动方式 | 代表项目 |
|------|---------|---------|
| **Framework-based** | `pip install langgraph/crewai/autogen` + Python orchestration code | [[LangGraph]] / [[CrewAI]] / [[AutoGen]] / Swarm |
| **Claude Code 原生** | 写 `.claude/agents/<name>.md`，主 session 用 Task tool invoke | [[Claude_Code_Subagent]] / [[Claude_Agent_SDK]] |

**核心差异在 runtime ownership**：
- Framework path：你用 Python 写 orchestrator 调度，每个 sub-agent 都是程序中的对象
- Claude path：Claude Code 自动建立新的子 agent，主 agent 只拿结果、不管内部过程（context 自动隔离）

**选择建议**：需要跨 LLM provider 混用，或要把 multi-agent 嵌入应用程序 → framework path。已 commit Claude Code 生态 → subagent path（少很多 boilerplate）。

延伸阅读：[[Claude_Code_Workflow]]、[[Multi_Agent_System]]、[[Agent_Orchestration_Patterns]]

---

## 跨范式组合（Power User 模式）

真实用户常常**同时用 2–3 个 type**，各做擅长的事：

| 组合 | 说明 |
|------|------|
| **Type 2 + Type 4** | Type 2 处理日常 coding（terminal 界面最自然）；Type 4 处理 routine + 跨平台任务（laptop 没开时也工作） |
| **Type 2 + Type 5** | Type 2 写代码；Type 5 处理隐私敏感文档 |
| **Type 1 + Type 2** | Type 1 做快速 inline 编辑；Type 2 做大规模重构和研究 |
| **Type 4 + Type 5** | Type 4 做常规 24/7 助理；Type 5 做数据不出门的隐私任务 |

---

## 决策指南

### 第一步：选大类
- 你的资料**不能上 cloud**？→ **Type 5**（Edge-deployed）
- 你需要 agent **24/7 在线服务你**？→ **Type 4**（Cloud-deployed）
- 你只是本地开发需要辅助？→ 继续第二步

### 第二步：选本地范式
- 你主要在 IDE 里写代码，**眼睛离不开 editor**？→ **Type 1**（IDE-coupled）
- 你习惯 terminal 工作流，需要 agent **自主完成多步骤**？→ **Type 2**（Terminal pair-programmer）
- 你**想自由选择 LLM**、在乎成本、或要用本地模型？→ **Type 3**（BYO-LLM CLI）

---

## 关联概念

### 上游理论框架
- [[Harness_Engineering]] — 五种范式本质上是 Harness Engineering 在不同部署环境下的特化
- [[Agent_Interfaces]] — 不同范式对应的交互界面（Terminal / IDE / Chat / SSH / Physical）
- [[Agent_Loop]] — 所有范式共享的 Agent Loop 核心机制，差异在 Loop 的"boundary"在哪

### 同层概念
- [[Claude_Code_Subagent]] — Subagent 机制详解（Claude Code 原生路径）
- [[Multi_Agent_System]] — 多 agent 协作的编排模式
- [[Agent_Orchestration_Patterns]] — 从简单 chain 到复杂 graph 的编排演进
- [[Autonomy_Gradient]] — 不同类型对应不同的自主性梯度
- [[Context_Engineering]] — 不同范式下上下文管理的差异（local vs cloud context window）
- [[Cost_Aware_Budget_Gates]] — Type 3/4 场景下特别重要的成本控制机制

### 代表工具
- [[Cursor]] — Type 1 代表，IDE agent 比较基准
- [[Claude_Code]] — Type 2 代表，Anthropic 终端 AI 编码助手
- [[Aider]] — Type 3 代表，git-native AI pair programmer
- [[Cline]] — Type 1 代表，VS Code autonomous in-IDE agent
- [[OpenClaw]] — Type 5 代表，边缘 AI Agent 平台

### 延伸阅读
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — Claude Code 生态系全景（Type 2 深化）
- [[摘要-awesome-agentic-ai-zh-agent-frameworks]] — Multi-agent 框架全览（Subagent 维度深化）
- [[Developer_Agentic_Workflow]] — 开发者 agentic 工作流的分层实践
