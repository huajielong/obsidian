---
title: "DSPy"
type: concept
tags: [DSPy, programming not prompting, 自动优化, compiler, RAG]
sources: [raw/01-articles/06-memory-rag.zh-Hans.md]
last_updated: 2026-07-10
---

# DSPy — Programming, Not Prompting

DSPy（Declarative Self-improving Python）是由 Stanford NLP Group 于 2024 年提出的框架，核心理念是 **"Programming, not Prompting"**（编程而非编写提示词）。它消除了手动编写 prompt 的过程——开发者只需定义"签名"（Signature，输入/输出类型）和编写程序（Module，chain 结构），DSPy 会用 LLM 编译器自动搜索出最佳的 prompt、few-shot 示例和 retriever 设置。

> 心智模型：DSPy = 用 Python 表达你想让 LLM 做什么，编译器帮你搞定 prompt 怎么写。

## 核心概念

| 概念 | 说明 |
|------|------|
| **Signature（签名）** | 定义模块的输入/输出类型，如 `question: str → answer: str` |
| **Module（模块）** | 基本计算单元，如 `ChainOfThought`, `ReAct`, `Retrieve` |
| **Compiler（编译器）** | 自动优化 prompt、few-shot 示例和 retriever 配置 |
| **Teleprompter** | 编译器中的优化器（如 `BootstrapFewShot`, `COPRO`, `MIPRO`）|

## 何时使用

- RAG prompt 已积累 6 个月，维护困难，想自动优化
- 同一程序需要切换不同的 LLM Provider（DSPy 会自动重新编译）
- Agent 系统有多个步骤，你想跟踪 Metrics 和 Traces

## 何时不使用

- 你只有一个 prompt，不需要优化
- 你是 LLM 新手，还没摸过 Prompting

## DSPy 与 RAG

DSPy 与本阶段讨论的 RAG 技巧 **并不冲突**——你可以将 GraphRAG / Hybrid Search / Reranking 都当作 DSPy 的模块来组装，然后进行编译。它是一个更高层级的 RAG 构建类型系统。

```python
# DSPy 示例：定义 RAG 签名和模块
class GenerateAnswer(dspy.Signature):
    """回答基于上下文信息的问题"""
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.OutputField()

class RAG(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.ChainOfThought(GenerateAnswer)
    
    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```

## Path 3 范式

DSPy 代表 LLM 工程的三条路径之 **Path 3**：

| 路径 | 做法 | 代表 |
|------|------|------|
| **Path 1** | 手动编写 prompt | 传统 Prompt Engineering |
| **Path 2** | 将 Reflection 训练进模型权重 | o1 / R1 / Opus 4.8 |
| **Path 3** | 程序自动搜索最佳 prompt | **DSPy** |

> 在 [[Multi_Agent_System|Stage 7 Multi-agent]] 的进阶场景中尤其好用——Agent 系统有多个步骤时，DSPy 可跟踪 metrics 和 traces 并自动优化。

## 代表作

- [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) ★ 34.4k MIT — Stanford NLP Group 官方，积极维护中

## 关联连接

- [[RAG]] — DSPy 可直接编译 RAG Pipeline，与所有 RAG 技巧兼容
- [[Context_Engineering]] — DSPy 是自动优化 Context Engineering 中 Prompt + Retriever 配置的工具
- [[Reflexion]] — Path 1（基于 prompt）的 reflection，与 Path 3 DSPy 互补
- [[Agent_Loop]] — DSPy 可优化 Agent Loop 中每一步的 prompt 设计
- [[摘要-awesome-agentic-ai-zh-memory-rag]] — 本概念的来源资料
