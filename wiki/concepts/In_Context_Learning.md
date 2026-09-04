---
title: "In_Context_Learning"
type: concept
tags: [in-context learning, 上下文学习, few-shot, LLM基础, context engineering]
sources: [raw/09-archive/【生成式人工智慧與機器學習導論2025】第 2 講：上下文工程 (Context Engineering) — AI Agent 背後的關鍵技術.md]
last_updated: 2026-08-05
---

## 定义

In-Context Learning（情境学习 / 上下文学习）指：**在给语言模型的输入（context）中直接放入范例（示例输入-输出对），模型的输出随之改变**——它"学着"范例的规律来回答新问题。它由 GPT-3 那篇论文正式命名。

> **关键：这里的"Learning"必须加引号。** 它**不是**传统机器学习意义上的学习——**模型的参数完全没有改变**。代表模型行为的函数 f 不变，只是因为输入 x（context）变了，输出才跟着变。把范例从 context 中拿掉，模型立刻回到原状。

## 为什么是 Context Engineering 的核心

In-Context Learning 是 [[Context_Engineering]] 的基石：在"改不了 f（闭源模型），只能改输入 x"的前提下，**给范例是影响模型能力最直接、最不需要训练的手段**。它对应 [[Few_Shot_Prompting]]（少样本提示）背后的机制。

## 经典案例

### 1. GPT-3 的翻译范例

早期模型很弱，直接说"把英文翻成法文"它不一定懂；但给它几个"这个字变这个字"的范例后，再问"cheese 的翻译是什么"，它答对的几率就高得多。这是 GPT-3 论文中 In-Context Learning 的原始演示。

### 2. Gemini 1.5 的卡拉蒙语（Kalamang）神迹

- 卡拉蒙语是世上只有**数千人**使用、网络上几乎找不到资料的语言，模型照理完全不会。
- 把**卡拉蒙语的教科书、文法和字典**放进 context 后，模型突然就会翻译了——仿佛"读"了教科书。
- Gemini 1.5 技术报告用它炫耀**超长 context**：其他模型只能放半本教科书（评分不足 1 分/满分 6），Gemini 1.5 能放整本教科书 → 翻译评分 4~5.5 分（人类学习者也只略好一点）。
- **后续分析**：真正让模型获得翻译能力的，是教科书里的**例句**（句子-翻译对照），文法说明几乎没帮助——模型是"照着例句的样子接龙"，而非真正理解了语法。
- **再次强调**：没有改变任何参数。把教科书拿掉，模型就恢复成不会卡拉蒙语的状态。

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[Few_Shot_Prompting]] | In-Context Learning 是 few-shot 背后的机制；few-shot 是它的工程叫法 |
| [[Context_Engineering]] | "给对范例"是组装 context 的核心手段之一（范例是 User Prompt 的重要成分） |
| [[Chain_of_Thought]] | CoT 是给"思考过程"范例的特殊 In-Context Learning |
| [[RAG]] | 检索到的资料也是"范例/事实"的一种，同样只改 context 不改参数 |
| [[Model_Fine_Tuning]] | **对照组**：微调才真正改变参数；ICL 与微调是"改输入 vs 改模型"两条路 |

## 关联连接

- [[Few_Shot_Prompting]] — ICL 的工程实现形式
- [[Context_Engineering]] — ICL 是"改输入"路径的核心技术
- [[Chain_of_Thought]] — 给"推理范例"的 ICL 特例
- [[RAG]] — 把外部知识放进 context 的机制
- [[Model_Fine_Tuning]] — 真正改变参数的学习（与 ICL 对照）
- [[Hung_yi_Lee]] — 本概念的教学来源（《生成式AI导论2025》第二讲）
- [[摘要-hung-yi-lee-上下文工程-第2讲]] — 来源摘要
