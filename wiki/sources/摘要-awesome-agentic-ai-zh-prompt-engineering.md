---
title: "摘要-awesome-agentic-ai-zh-prompt-engineering"
type: source
tags: [提示词工程, 学习路线, prompt engineering, LLM]
sources: [raw/01-articles/awesome-agentic-ai-zh-stage-02-prompt-engineering.md]
last_updated: 2026-07-10
---

## 核心摘要

该资料是 "awesome-agentic-ai-zh" Agentic AI 系统学习路线图的 **Stage 2——Prompt 设计（Prompt Engineering）**，提供从基础提示词到进阶技巧的完整动手教程。核心内容涵盖：结构化 prompt 设计（角色 + 任务 + 格式 + 示例）、Few-shot 提示与零样本对比、Chain-of-Thought（CoT）推理增强、迭代式 prompt 优化方法论，以及三层工程堆栈（Prompt → Context → Harness）的概念框架。每个技能点均配有 Ollama（本机）和 Anthropic（云端）双路径可运行代码练习。

## 关键提炼

- **结构化 Prompt 四要素**：角色设定（System Prompt）+ 任务描述 + 输出格式 + 示例
- **Few-shot 显著提升分类准确率**：尤其对小模型（如 Gemma 4B），zero-shot 常误判 "中立" 类别，3-shot 后改善明显
- **CoT 对推理任务的关键作用**："Let's think step by step" 或带推理步骤的示例能显著提升数学/逻辑题正确率
- **迭代 Refinement 方法论**：从模糊到具体的 5 轮递进——加目标读者 → 加格式约束 → 加示例要求 → 加禁忌词
- **三层工程 stack**：Prompt Engineering（本 stage）→ Context Engineering（Stage 6）→ Harness Engineering（Stage 7）
- **小模型 vs 大模型的教学价值**：小模型（4B）对 prompt 质量敏感，能更清晰展示每种技巧带来的改善幅度

## 关联连接

- [[Prompt_Engineering]] — 该资料的核心主题
- [[Chain_of_Thought]] — CoT 推理增强技术详解
- [[Few_Shot_Prompting]] — Few-shot 提示与零样本对比
- [[Context_Engineering]] — 三层 stack 中的中间层
- [[Harness_Engineering]] — 三层 stack 中的最外层
- [[Ollama]] — 本机练习默认的 LLM 运行环境
- [[Anthropic]] — 云端练习路径的 API 提供商
- [[Andrej_Karpathy]] — 三层 stack 中 Context Engineering 概念的提出者
- [[摘要-awesome-agentic-ai-zh-foundations]] — 本路线图 Stage 0，先修基础
- [[摘要-awesome-agentic-ai-zh-llm-basics]] — 本路线图 Stage 1，LLM 基础
