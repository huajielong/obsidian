---
title: "Aider"
type: entity
tags: [工具, CLI, 结对编程, Git, 开源]
sources: [https://github.com/Aider-AI/aider, https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/branches/for-developer.zh-Hans.md]
last_updated: 2026-07-10
---

# Aider

> ★ 44k+ · Apache-2.0 · [GitHub](https://github.com/Aider-AI/aider)

**git-aware 的 CLI pair-programmer**。直接编辑你 repo 中的文件，commit 都自动写好。被称为 **"git-native AI 编辑流程"的开源模板**。模型不限。

## 核心特性

- **Git-native**: 每次编辑自动生成 commit，保持干净 git 历史
- **模型无关**: 支持多种 LLM 后端（Claude、GPT、本地模型等）
- **/undo**: 可退掉最后一次 AI commit，安全回滚
- **自然语言驱动**: 以自然语言请求描述代码变更

## 典型工作流

```bash
# 进入 repo 后
aider --model anthropic/claude-sonnet-5

# 自然语言请求
> 帮我把 utils.py 的 parse_date 加上时区参数，默认 UTC

# Aider 会自动编辑 + commit。若不满意：
> /undo # 退掉最后一次 AI commit
```

## 在开发者工作流中的角色

- 适合 **每日 AI 结对**：最像"跟 AI pair"的体验
- 适合 **测试生成**：从 function signature + docstring 生成 pytest case
- **Tier 1** 工具：适合想拥有干净 git 流程的开发者

## 关联链接

- [[Cursor]] — 编辑器集成 AI 工具（Tier 0）
- [[Claude_Code]] — Anthropic 官方 agentic coding 助理（同为 CLI agent）
- [[Cline]] — VS Code autonomous in-IDE agent
- [[Developer_Agentic_Workflow]] — 开发者工作流场景分类
- [[Agentic_Coding]] — AI 自主编程范式
