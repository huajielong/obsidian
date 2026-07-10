---
title: "Claude Code Harness"
type: concept
tags: [Claude Code, Harness, 架构, 7层架构, 工程设计]
sources: [raw/01-articles/05-claude-code-ecosystem.md]
last_updated: 2026-07-10
---

# Claude Code Harness — 7-Layer Architecture

## 定义

Claude Code Harness 是 Claude Code 作为 **Reference Harness Implementation** 的完整架构视图。它将 Claude Code 生态的 7 个 Primitive（MCP / Skills / Plugins / Subagents / Hooks / Slash Commands / CLI）映射到 **7 个架构层**，并关联到 **3 个 Engineering Discipline**。

## 7-Layer Architecture Map

| Layer | 名称 | Claude 的版本 | Engineering Discipline |
|-------|------|--------------|----------------------|
| **L7** | **Interface** | claude-code CLI / Desktop | Harness Engineering |
| **L6** | **Workflow** | Skills + Slash Commands + Plugins | Prompt Engineering |
| **L5** | **Coordination** | Subagents + Agent Team + Background | Harness Engineering |
| **L4** | **Memory/Context** | History / /compact / Memory hooks | Context Engineering |
| **L3** | **Control Plane** | Hooks（PreToolUse/PostToolUse 等） | Harness Engineering |
| **L2.5** | **Tool Provider** | MCP Servers | Context Engineering + Tool Design |
| **L2** | **Tool Use** | Anthropic Tool Use（`input_schema`） | Tool Design |
| **L1** | **Foundation** | Anthropic API（System Prompt 直达） | Prompt Engineering |

## 每层一句话

- **L7 Interface** — 用户和 Agent 交谈的入口
- **L6 Workflow** — 固定可复用的流程模板
- **L5 Coordination** — 多 Agent 分工合作
- **L4 Memory/Context** — 跨对话/跨 Session 记忆
- **L3 Control Plane** — Tool 执行前/后拦截、验证、阻挡（"守门员"层）
- **L2.5 Tool Provider** — 把外部 API 包成 Tool 给 L2 用
- **L2 Tool Use** — LLM 调用外部 Function 的协议
- **L1 Foundation** — LLM 本体

## 3 个 Engineering Discipline

| Discipline | 负责的 Layer | 一句话 |
|-----------|-------------|--------|
| **Prompt Engineering** | L1 + L6 | "送进 LLM 的字符串怎么设计" |
| **Context Engineering** | L4 + L2.5 | "Context Window 装什么信息" |
| **Harness Engineering** | L3 + L5 + L7 | "LLM 外面的'运行外壳'" |

> 这三个 Discipline 是**不同层的技能**——学会其中一个，不会自动会另一个。

## 跨 CLI Vendor 对比

只有 Claude Code 有**完整 7-Layer Stack**：

| 层 | Claude Code | OpenAI Codex | Gemini CLI |
|---|:-----------:|:------------:|:----------:|
| L5 Coordination（Multi-Agent）| ✅ Subagents | ❌ Single-agent | ❌ |
| L3 Control Plane（Hooks）| ✅ Hooks | ❌ | ❌ |
| L2.5 Tool Provider（MCP）| ✅ | ✅（已支持 MCP）| ✅（需手动装）|
| L6 Workflow（Skills）| ✅ SKILL.md | AGENTS.md（仅 Context）| GEMINI.md（仅 Context）|

## Source 解剖：6 个 Runtime-Internal Harness 元件

在 `claude-agent-sdk-python` 源码中可找到前 6 个 Runtime-Internal 元件：

1. **Agent Loop** — 发出 LLM Call + 收 Response 的循环
2. **Tool Registry / Dispatch** — Tool_use → Route 到对应 Tool 实现
3. **Context Manager** — Tool Result 写回 Message History + Context 控制/Auto-compact
4. **Safety Layer** — Tool 执行前的 Permission Gate / Sandboxing
5. **Retry / Recovery** — Tool Fail 时的 Exception vs LLM 自反思处理
6. **Telemetry** — Metrics / Logging / Token Counting

> 第 7 个 Eval 是外挂，第 8 个 Cost/Latency 是 Cross-cutting，不在 Source 主 Loop 内。

## 关联连接

- [[Claude_Code]] — Harness 的宿主环境
- [[MCP]] — L2.5 Tool Provider
- [[Claude_Code_Skills]] — L6 Workflow 的 Skill 部分
- [[Claude_Code_Subagent]] — L5 Coordination
- [[Claude_Code_Hooks]] — L3 Control Plane
- [[Claude_Code_Plugins]] — L6 Workflow 的 Plugin 部分
- [[Claude_Code_Dynamic_Workflows]] — L6 Workflow 的进阶形式
- [[Claude_Code_Slash_Commands]] — L7 Interface
- [[Harness_Engineering]] — L3+L5+L7 所属的 Engineering Discipline
- [[Context_Engineering]] — L4+L2.5 所属的 Engineering Discipline
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 核心来源
