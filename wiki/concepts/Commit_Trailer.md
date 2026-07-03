---
title: "Commit Trailer"
type: concept
tags: [Git, 版本控制, 元数据, 最佳实践]
sources: [raw/01-articles/万字干货｜AI 时代的 Git 版本管理，你用对了吗？ - 文章 - 开发者社区 - 火山引擎.html]
last_updated: 2026-07-03
---

## 定义

Commit Trailer 是 Git 内置的一种在 commit message 末尾附加结构化元数据的机制。Trailer 是附加在 commit message 末尾（与正文之间有一个空行）的结构化键值对，格式为 `Key: Value`，由 `git` 原生解析，无需额外工具。

## 常见 Trailer 示例

```
Signed-off-by: Alice <alice@example.com>
Co-authored-by: Bob <bob@example.com>
Fixes: #1234
```

## Agent-Aware Trailer 扩展

在 [[Agent_Aware_Commit]] 规范中，为追踪 AI Agent 的决策过程推荐以下自定义 trailer：

| Trailer 字段 | 用途 | 示例值 |
|---|---|---|
| `Agent-Task` | 原始任务描述或任务 ID | `PROJ-234 - Add refresh token support` |
| `Agent-Model` | 使用的 AI 模型 | `gpt-4o`、`gemini-2.5-pro` |
| `Agent-Decision` | 关键设计决策及理由 | `Used 7-day sliding window over fixed expiry` |
| `Agent-Limitation` | 已知局限或后续 TODO | `Redis TTL not yet aligned` |

## 查询与过滤

Git 原生支持对 trailer 的查询：

```bash
# 列出所有包含 Agent-Task trailer 的提交
git log --format='%(trailers:key=Agent-Task,valueonly)'

# 按 trailer 过滤提交历史
git log --grep="^Agent-Task:" --all
```

## 关联连接

- [[Agent_Aware_Commit]] — 利用 Commit Trailer 记录 Agent 决策的规范
- [[Agentic_Coding]] — Commit Trailer 在 AI 编程中的价值
- [[摘要-ai-era-git-management]] — 来源文章
