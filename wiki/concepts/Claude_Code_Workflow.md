---
title: "Claude Code 开发工作流"
type: concept
tags: [Claude, AI编程, 方法论, 最佳实践, 工作流]
sources: 
  - raw/01-articles/Claude Code 完全指南 - 阿里云开发者社区.md
  - raw/01-articles/05-claude-code-ecosystem.md
last_updated: 2026-07-10
---

## 定义

Claude Code 开发工作流是一套将 [[Claude_Code]] 的命令、模式、模型和记忆系统串联成流的方法论，核心理念是：**开发者负责方向和判断，Claude 负责执行和细节**。

## 核心公式

> **Plan Mode 想清楚 → Auto-Accept 执行 → /compact 或 /clear 管理上下文 → /memory 沉淀经验**

## 六步工作流

### 第一步：初始化项目认知
```bash
/init
```
自动扫描代码库，生成 `CLAUDE.md` 初稿。然后用 `/memory` 补充人工经验（不可修改目录、提交格式、测试命令等）。

### 第二步：Plan Mode 理解代码
```
Shift+Tab × 2 → 进入 Plan Mode
```
只读模式分析代码结构，不碰任何代码。复杂架构时切换到 Opus 模型。

### 第三步：规划新功能
继续在 Plan Mode 中用自然语言描述需求，Claude 输出实现方案。花时间确认计划，避免返工。

### 第四步：分模块执行
```
Shift+Tab × 1 → 进入 Auto-Accept 模式
```
耗时操作挂后台（`Ctrl+B`），前台继续讨论。每完成一个模块及时 `/clear`。

### 第五步：性能分析与优化
切回 Plan Mode，让 Claude 审视代码的性能和安全隐患，确认后再针对性优化。

### 第六步：记忆沉淀
```bash
/memory
```
把项目经验写进 CLAUDE.md，供后续任务和团队成员复用。

## Skills 增强工作流

在六步工作流之上，使用 [[Claude_Code_Skills]] 可将特定情境的流程自动化。当遇到 Skill description 匹配的情境时，Skill 自动加载到 Context，按预设流程执行——无需每次手动描述步骤。

## Subagent 并行工作流

对于大 Context 任务（如跨文件 Review、全量 Codebase 分析），使用 [[Claude_Code_Subagent]] 将任务 Delegate 给独立 Context 的子 Agent，保护主 Session 不被污染。

## Dynamic Workflows（自动编排）

在 Opus 4.8+ 中，[[Claude_Code_Dynamic_Workflows]] 允许 Claude 自己生成 Workflow 脚本并执行——适用于大型迁移、穷举 Bug 搜索、跨文件批量转换等需要确定控制流的场景。详见 [[Claude_Code_Dynamic_Workflows]]。

## 模式与模型选用原则

| 阶段 | 模式 | 推荐模型 |
|---|---|---|
| 读代码 / 规划 | Plan Mode | Opus |
| 日常编码 | Default | Sonnet |
| 重复性修改 | Auto-Accept | Sonnet / Haiku |
| 快速问答 | Default | Haiku |

## 上下文管理

- **任务切换时**：用 `/clear` 清空历史，避免旧任务干扰新需求
- **对话变长但任务未切换**：用 `/compact "保留XX相关讨论"` 压缩而非清空
- **后台任务**：`Ctrl+B` 挂后台，`Ctrl+T` 查看进度

## 关联连接

- [[Claude_Code]] — 工作流所使用的工具（含三种工作模式：Default/Auto-Accept/Plan）
- [[Claude_Code_Slash_Commands]] — 工作流中使用的命令集
- [[Claude_Code_Memory_System]] — 第一步和第六步涉及的三层记忆体系
- [[Claude_Code_Skills]] — Skills 增强工作流
- [[Claude_Code_Subagent]] — Subagent 并行工作流
- [[Claude_Code_Dynamic_Workflows]] — 自动编排工作流
- [[Claude_Code_Hooks]] — 事件驱动 Hook 流程
- [[AGENT_MD]] — /init 生成和 /memory 编辑的项目记忆文件
- [[From_NoCode_To_Agent_Paradigm]] — Workflow 作为 Agent 编排层替代传统无代码搭建
- [[摘要-claude-code-guide]] — 来源文章
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — Skills/Subagent/DW 的工作流扩展来源
