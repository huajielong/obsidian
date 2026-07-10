---
title: "Claude Code 斜杠命令"
type: concept
tags: [Claude, 开发工具, 命令行, 工作流]
sources: 
  - raw/01-articles/Claude Code 完全指南 - 阿里云开发者社区.md
  - raw/01-articles/05-claude-code-ecosystem.md
last_updated: 2026-07-10
---

## 定义

Claude Code 斜杠命令（Slash Commands）是 [[Claude_Code]] 终端的核心交互方式，通过在对话中输入以 `/` 开头的命令来控制 AI 助手的行为、管理上下文、查看状态和配置环境。

## 必备命令速查

| 命令 | 用途 | 何时用 |
|------|------|--------|
| `/help` | 列出所有可用命令 | 不知道有什么指令时 |
| `/clear` | 清空对话历史（保留 System Context） | Session 太长、想重启逻辑 |
| `/compact` | 自动摘要对话、释放 Context Window | Context 接近用满 |
| `/plan` | 进入 Plan Mode（Read-only、先规划才动手） | 大改动前先让 Claude 列计划 |
| `/model` | 切换模型（Sonnet / Haiku / Opus） | 改成更便宜模型省 Token |
| `/agents` | 列/管理 Subagent | 看哪些 Subagent 可用、Debug |
| `/plugin install <name>@<marketplace>` | 安装 Plugin | 加新功能 |
| `/permissions` | 看/改当前 Session 权限 | 太多 Permission Prompt 想精简 |
| `/resume` | 恢复前次 Session | 接续昨天工作 |
| `/bg` | 把当前 Session 背景化（移到 Agent View） | 想同时跑多任务 |
| `/init` | 初始化项目记忆，生成 CLAUDE.md 初稿 | 新项目首次使用 |
| `/memory` | 编辑 CLAUDE.md 记忆文件 | 修改项目规则或个人偏好 |
| `/status` | 查看会话状态（目录、模型、记忆等） | 确认当前环境配置 |
| `/cost` | 显示令牌使用量和预估费用 | 掌控 API 使用成本 |
| `/config` | 交互式查看和修改配置 | 设置主题、编辑模式等 |
| `/doctor` | 环境健康检查 | 排查工具调用异常 |
| `/rewind` | 回退或总结（Esc × 2） | 回滚 AI 操作 |

## 快捷键参考

| 快捷键 | 作用 |
|---|---|
| `Ctrl+B` | 将任务挂到后台运行 |
| `Ctrl+T` | 显示/隐藏任务列表面板 |
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+G` | 打开计划文件编辑 |
| `Shift+Tab` | 循环切换三种工作模式 |
| `ESC×2` (`/rewind`) | 回退或总结（回滚 AI 操作） |
| `Alt+V` | 粘贴图像（Windows） |
| `\+Enter` | 输入框内换行 |

## 关联连接

- [[Claude_Code]] — 斜杠命令所属的工具
- [[Claude_Code_Memory_System]] — /memory 命令管理的三层记忆系统
- [[Claude_Code_Workflow]] — 命令在完整工作流中的运用
- [[AGENT_MD]] — /init 生成的项目记忆文件
- [[摘要-claude-code-guide]] — 来源文章
