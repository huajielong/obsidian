---
title: "Claude Code Hooks"
type: concept
tags: [Claude Code, Hooks, 控制层, 安全, 自动化]
sources: [raw/01-articles/05-claude-code-ecosystem.md]
last_updated: 2026-07-10
---

# Claude Code Hooks（事件钩子系统）

## 定义

Hooks 是 Claude Code 的 **L3 控制层**（Control Plane）机制——在 Agent 生命周期事件上挂载自定义脚本，实现**检查、拦截、注入**。如果说 MCP 和 Skills 是"给 Agent 更多能力"，Hooks 就是**反过来**：在 Tool 执行前后、Session 开始/结束等时机用程序强制规则。

## 核心事件（2026 年已扩至约 28 个）

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `PreToolUse` | 工具调用前 | 挡危险指令、权限 Gate |
| `PostToolUse` | 工具调用后 | 自动 Format / Lint / 跑测试 |
| `UserPromptSubmit` | 用户发送 Prompt 时 | 注入 Context、挡掉某些输入 |
| `Stop` / `SubagentStop` | （子）Agent 想停时 | 强制继续或做收尾检查 |
| `SessionStart` / `SessionEnd` | Session 开始/结束 | 加载状态、写 Log |
| `PreCompact` | Context 压缩前 | 保护重要内容 |

## 关键语义

Hook **返回 Exit Code 2 = 阻挡**：Claude 会把 Stderr 当作错误信息读回去。

- `PreToolUse` 返回 2 → 挡下那个工具调用
- `UserPromptSubmit` 返回 2 → 挡下那个 Prompt
- `PostToolUse` 返回 2 → 标记调用失败

这就是"用程序强制规则"的机制——比 CLAUDE.md 的文本描述更强力、不可绕过。

## 配置方式

在 `settings.json` 的 `hooks` 字段中设置某事件发生时跑哪个 Command：

```json
{
  "hooks": {
    "PreToolUse": "node .claude/hooks/pre-tool-check.js",
    "PostToolUse": "bash .claude/hooks/post-lint.sh"
  }
}
```

## 安全注意

- Hook 是在本地机器上运行的 Shell Command
- 不要安装别人的 Hook 而不检查内容
- 不要在 Hook 里运行未经验证的输入

## 在 7-Layer Architecture 中的位置

Hooks 位于 **L3 Control Plane**（"守门员"层），属于 **Harness Engineering** 的范畴——与 L5 Coordination（Subagents）、L7 Interface（CLI/Desktop）并列。

## 关联连接

- [[Claude_Code]] — Hooks 的宿主环境
- [[MCP]] — MCP Tool 执行时 Hook 可以拦截（L2.5 与 L3 协作）
- [[Claude_Code_Skills]] — Skill 执行过程中 Hook 也会触发
- [[Claude_Code_Plugins]] — Plugin 可包含 Hooks 定义
- [[Claude_Code_Harness]] — 7-Layer Architecture，Hooks 位于 L3
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 核心来源
- [[Harness_Engineering]] — Hooks 所属的工程学 Discipline
