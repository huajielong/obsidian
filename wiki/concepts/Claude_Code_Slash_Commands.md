---
title: "Claude Code 斜杠命令"
type: concept
tags: [Claude, 开发工具, 命令行, 工作流]
sources: [raw/01-articles/Claude Code 完全指南 - 阿里云开发者社区.md]
last_updated: 2026-07-03
---

## 定义

Claude Code 斜杠命令（Slash Commands）是 [[Claude_Code]] 终端的核心交互方式，通过在对话中输入以 `/` 开头的命令来控制 AI 助手的行为、管理上下文、查看状态和配置环境。

## 命令速查

| 命令 | 作用 | 典型场景 |
|---|---|---|
| `/init` | 初始化项目记忆，生成 CLAUDE.md 初稿 | 新项目首次使用 Claude Code |
| `/memory` | 编辑 CLAUDE.md 记忆文件（项目/用户/自动） | 修改项目规则或个人偏好 |
| `/compact` | 压缩对话上下文，保留核心摘要 | 对话过长 token 超限时 |
| `/clear` | 清空所有对话历史，全新开始 | 切换到完全不同的任务时 |
| `/status` | 查看会话状态（目录、模型、记忆等） | 确认当前环境配置 |
| `/cost` | 显示令牌使用量和预估费用 | 掌控 API 使用成本 |
| `/config` | 交互式查看和修改配置 | 设置主题、编辑模式等 |
| `/model` | 切换 AI 模型版本 | 需要更强/更快模型时 |
| `/doctor` | 环境健康检查 | 排查工具调用异常 |
| `/help` | 查看所有可用命令 | 新手入门或忘记命令 |

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
