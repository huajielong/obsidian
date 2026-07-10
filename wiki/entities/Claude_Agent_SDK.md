---
title: "Claude Agent SDK"
type: entity
tags: [Claude, SDK, Agent, Anthropic, Python]
sources: [raw/01-articles/05-claude-code-ecosystem.md]
last_updated: 2026-07-10
---

# Claude Agent SDK

## 定义

Claude Agent SDK 是 Anthropic 官方推出的 **Agent Runtime Python SDK**，让开发者用编程方式控制 Agent Loop、Tool Dispatch、Memory 接入。与 [[Claude_Code]] CLI 不同，SDK 适合将 Agent 嵌入自有应用、Cron 调度、公司内部封装等场景。

## 三阶路径

| 阶段 | 方式 | 比喻 |
|------|------|------|
| **第 1 层** | 直接使用 CLI（`claude` 命令） | 现成的车子，点上路 |
| **第 2 层** | CLI + 自定义（CLAUDE.md/Hooks/Skills/Plugins） | 调车子性能 |
| **第 3 层** | SDK（`claude-agent-sdk-python`） | 从引擎开始重造一台 |

> 99% 的学习者天花板停在"调车"就够了。

## 什么时候才需要 SDK

- **嵌进已有的 Web App / 后端** — 用户不开 Terminal 就不能用 CLI
- **Cron / Scheduler 自动触发** — 无人在 Session 里交互
- **公司内部封装** — 加 Auth、Audit Log、限额、自定义 Prompt Template
- **同时跑多 Agent 需 Programmatic 控制 Hand-off** — 比 Task Tool 更细的控制权

## 核心用法（4 行 Python）

```python
from claude_agent_sdk import query

async for msg in query(prompt="用 git status 看当前状态"):
    print(msg)
```

`query()` 会 Yield 多种 Message Type（`AssistantMessage` / `ResultMessage` / `SystemMessage`），想拿到 Agent 真正的回复要用 `isinstance(msg, AssistantMessage)` 再取 `msg.content`。

## vs CLI vs 自定义 对照

| 维度 | CLI | CLI + 自定义 | SDK |
|------|-----|------------|-----|
| 嵌进你的 App | ❌ | ❌ | ✅ |
| Cron/排程跑 | ⚠️ 勉强（`-p` flag） | ⚠️ 同左 | ✅ |
| 换语言/环境 | 绑 Node/Bash | 同左 | Python/TS 随你 |
| Programmatic 控制 | ❌ | ❌ | ✅ |
| 客制 System Prompt | 受限 | 受限 | 完全自由 |
| 学习成本 | 1 天 | 1-2 周 | 1 个月+ |

## 两个主要 SDK 对比

| | Claude Agent SDK Python | OpenAI Agents Python |
|---|---|---|
| 出品 | Anthropic 官方 | OpenAI 官方 |
| 模型 | Claude（Opus / Sonnet / Haiku） | OpenAI 系列 + 其他 |
| 强项 | 与 Claude Code 一致的 Tool/Skill/Hook 抽象 | Handoff / Agents-as-Tools 模式 |
| 适合 | 已在用 Claude Code 想嵌服务的人 | 已 Commit OpenAI 生态的人 |

## 关联连接

- [[Claude_Code]] — SDK 的 CLI 对应物
- [[Claude_Code_Harness]] — SDK 实现的 Harness 架构
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 核心来源
- [[OpenAI_Agents_SDK]] — 同层的 OpenAI 竞品
- [[Anthropic]] — SDK 的开发商
- [[Harness_Engineering]] — SDK 所实现的工程学
