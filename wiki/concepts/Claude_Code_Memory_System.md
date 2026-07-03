---
title: "Claude Code 记忆系统"
type: concept
tags: [Claude, AI编程, 记忆管理, 工作流]
sources: [raw/01-articles/Claude Code 完全指南 - 阿里云开发者社区.md]
last_updated: 2026-07-03
---

## 定义

Claude Code 记忆系统是 [[Claude_Code]] 的三层持久记忆机制，用于在不同粒度上保存规则、偏好和上下文信息，使 AI 助手在每次会话中都能保持一致的行为模式。

## 三层记忆体系

### 1. Project Memory（项目记忆）
- **文件位置**：`./CLAUDE.md`（项目根目录）
- **作用范围**：当前项目专属
- **典型内容**：技术栈说明、目录结构、代码规范、构建/测试命令、不可修改的目录等
- **使用场景**："这是一个 React + TypeScript 项目，使用 pnpm"，"不要修改 src/legacy/ 目录"

### 2. User Memory（用户记忆）
- **文件位置**：`~/.claude/CLAUDE.md`（用户全局）
- **作用范围**：所有项目通用
- **典型内容**：个人工作习惯、语言偏好、代码风格约定
- **使用场景**："回复一律用中文"，"代码注释保持简洁"，"提交信息用英文 feat: 格式"

### 3. Auto Memory（自动记忆）
- **触发方式**：Claude 在对话中自动判断重要信息并写入
- **作用范围**：跨会话自动生效
- **典型内容**：对话中明确的规则声明（如"我们公司规定所有接口要加错误边界处理"）
- **优势**：省去手动整理的麻烦

## 管理方式

- **查看/编辑**：通过 `/memory` 命令打开编辑
- **初始化**：通过 `/init` 命令自动扫描项目生成 CLAUDE.md 初稿
- **沉淀经验**：完成功能开发后，通过 `/memory` 将项目经验写入记忆文件

## 关键原则

- 项目记忆管"这个项目怎么做"
- 用户记忆管"我这个人怎么工作"
- 自动记忆省去手动整理的麻烦

## 关联连接

- [[Claude_Code]] — 记忆系统所属的工具
- [[Claude_Code_Slash_Commands]] — /memory 和 /init 命令用于管理记忆
- [[Claude_Code_Workflow]] — 记忆沉淀是工作流的最后一步
- [[AGENT_MD]] — Project Memory 即项目根目录的 CLAUDE.md 文件
- [[摘要-claude-code-guide]] — 来源文章
