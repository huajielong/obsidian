---
title: "Claude Code Subagent"
type: concept
tags: [Claude Code, Subagent, Multi-Agent, 并行, 编排]
sources: [raw/01-articles/05-claude-code-ecosystem.md]
last_updated: 2026-07-10
---

# Claude Code Subagent（原生 Multi-Agent 机制）

## 定义

Subagent 是 Claude Code 内建的 **Multi-Agent 层（L5 Coordination）**——让主 Claude Session Spawn 出拥有独立 Context 的子 Agent，跑特定任务、回报结果。与 [[Multi_Agent_System]] 中的 Framework 路线不同，Subagent 路线只需写 Markdown 文件即可。

## Claude Code 的三种 Multi-Agent 机制

| 机制 | 状态 | 何时用 | 派遣方式 |
|------|------|--------|---------|
| **Subagent** | 稳定版 | Delegate 大 Context 任务，结果回主 Session | 写 `.claude/agents/<name>.md` → Description 自动 Delegate |
| **Agent Team** | 正式文档但需 Opt-in | 多 Worker 互相沟通、辩论、多角度探索 | `settings.json` 加 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` → 自然语言派遣 |
| **Background Agent** | Research Preview | 多个独立任务各自后台跑，统一监控 | Shell 派遣 `claude --bg "..."` 或 Session 内 `/bg` |

## Subagent vs Skill — 5 个关键差别

| 维度 | Subagent（子 Agent） | Skill（技能） |
|------|---------------------|--------------|
| **执行环境** | 新的独立 Context Window（底层新 Subprocess） | 主 Session 内、同 Context |
| **工具权限** | 自己的 `tools:` 清单（可限制只读） | 主 Session 的工具（默认全开） |
| **返回结果** | 一个 Final Message 摘要回主 Session | 没有返回，是行为改变（规则/Persona） |
| **适合做** | 长任务/并行跑/要 Context 隔离 | 知识注入/规则/改 Claude 行为 |
| **范例** | `code-reviewer` / `Explore` / `Plan` | `pdf` / `docx` / `skill-creator` |

**快速判断**：需要**新 Context Window**？要 → Subagent；不要 → Skill。

## 内置 Subagent

| Subagent | 用途 |
|----------|------|
| `general-purpose` | 通用，可 Web Search，适合 Fallback |
| `code-reviewer` | Review Staged Diff，安全审查 |
| `Explore` | Read-only 搜索，探索陌生 Codebase |
| `Plan` | 输出 Step-by-step 计划 |
| `frontend-developer` | React / 响应式 / A11y 领域知识 |

> 在终端跑 `/agents` 可列出所有可用 Subagent（内置 + Plugin + 自定义）。

## 自定义 Subagent 写法

`.claude/agents/<name>.md`：

```markdown
---
name: code-reviewer
description: Review staged git changes. Use when user asks "review my changes".
tools:
  - Read
  - Grep
  - Bash
model: claude-haiku-4-5
---

You are a senior code reviewer. When invoked:
1. Run `git diff --cached` to get staged changes
2. Check for: hard-coded secrets, SQL injection, missing error handling
3. Output: PASS / list of specific issues with file:line references
```

### Frontmatter 关键字段

| 字段 | 作用 | 注意 |
|------|------|------|
| `description` | 路由 Key，决定何时被自动派遣 | 写具体触发条件，`PROACTIVELY` 是强信号词 |
| `tools:` | 工具白名单 | 空 = 继承主 Session 全部工具 |
| `model:` | 模型指定 | 不写 = 跟主 Session 同 Model（烧大钱），省成本写 `sonnet` 或 `haiku` |

## 五条老手 Gotcha

1. **Description 写精准即可**——过长占 Context Budget；建议"触发条件+适用场景"
2. **`tools:` 写空 = 继承主 Session 全部工具**——想限制就要明写
3. **不写 `model:` = 跟主 Session 同 Model**——省成本务必指定
4. **Subagent 无跨 Call 记忆**——每次派遣全新 Context，Prompt 必须 Self-contained
5. **Subagent 也吃 Hook**——PreToolUse/PostToolUse 在 Subagent 内也会触发

## 适用判断

**用 Subagent 的时机**：任务 ≥ 5 分钟 + 可以用一个 Brief 写死（不需要来回对话）+ 结果一次回来够用。

**Subagent 的优缺点**：
- ✅ Context 隔离、Tool Allowlist、Model Override、Parallel Spawn、专业化 Prompt
- ❌ Spawn Overhead、无 Cross-Call Memory、只回一个 Message、Token Cost N×、Debug 多一层

## Subagent vs Framework 路线对比

| 维度 | Framework 路线（Stage 4） | Claude Subagent 路线 |
|------|------------------------|---------------------|
| 启动方式 | `pip install crewai` + Python Code | 写 `.claude/agents/<name>.md` |
| Runtime | 你自己的 Python Process | Claude Code 内建 Task Tool |
| Context Isolation | Framework 自己管 | 天生各 Subagent 独立 Window |
| Provider Lock-in | 中等（多 Framework 支持 Multi-LLM） | 强（绑 Claude Code） |
| 学习曲线 | 高（Framework 抽象 + Async） | 低（写 Markdown）|

## 关联连接

- [[Claude_Code]] — Subagent 的宿主环境
- [[Multi_Agent_System]] — Multi-Agent 核心概念框架，Subagent 是两条路线之一
- [[Agent_Orchestration_Patterns]] — 编排模式，与 Subagent 互补
- [[Claude_Code_Skills]] — Subagent vs Skill 的决策对比
- [[Claude_Code_Dynamic_Workflows]] — 建立在 Subagent 之上的更高层编排
- [[Claude_Code_Harness]] — 7-Layer Architecture，Subagent 位于 L5 Coordination
- [[Claude_Code_Hooks]] — Subagent 也受 Hook 影响
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 核心来源
