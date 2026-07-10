---
title: "Few_Shot_Prompting"
type: concept
tags: [提示词工程, few-shot, in-context learning]
sources: [raw/01-articles/awesome-agentic-ai-zh-stage-02-prompt-engineering.md, raw/01-articles/Few-Shot-实验对比.md]
last_updated: 2026-07-10
---

# Few-Shot Prompting（少样本提示）

Few-shot prompting 是一种**在提示词中包含若干"输入 → 期望输出"范例，引导 LLM 理解任务模式并按照范例格式作答**的技术。它是 In-context Learning（上下文学习）最直接的体现。

## 三种变体对比

| 变体 | 范例数量 | 特点 | 适用场景 |
|------|---------|------|---------|
| **Zero-shot（零样本）** | 0 个 | 直接发问，不加范例 | 简单任务、模型已熟悉的任务 |
| **One-shot（单样本）** | 1 个 | 给一个"输入→答案"范例 | 初次引导格式 |
| **Few-shot（少样本）** | 2-5 个 | 给多个范例，展示判断标准和输出格式 | 分类、格式严格的任务 |

## Few-shot 为什么有效

- **格式引导**：LLM 看到范例的输出格式后，倾向于遵循相同格式作答
- **判断标准**：多类别范例展示分类维度，降低歧义
- **上下文校准**：帮助模型理解任务的精确边界

## 实测效果（中文情绪分类）

用 Gemma 4B 对 6 条中文评论进行"正面/负面/中立"三分类：

- **0-shot**：容易将"中立"误判为正面或负面，准确率较低
- **3-shot**：提供三条范例后，准确率明显提升，尤其中立类别的判断改善显著

> 小模型（如 4B 参数量级）对 few-shot 改善幅度比大模型更明显——因为大模型零样本时已有不错准确率，few-shot 的边际增益较小。

## 跨模型对比实验（deepseek-v4-pro vs llama3.2:3b）

### 实验设计

| 项目 | 说明 |
|:----|:-----|
| 任务 | 4 类意图分类（inquiry / complaint / order / spam） |
| 弱模型 | `llama3.2:3b`（本地 Ollama，3B，CPU 推理） |
| 强模型 | `deepseek-v4-pro`（云端 API） |
| 指标 | 0-shot vs 3-shot 准确率 |

### 结果

| 模型 | 0-shot | 3-shot | 变化 |
|:----|:-------|:-------|:----|
| **llama3.2:3b** (3B) | **80%** (8/10) | **90%** (9/10) | **↑ +10%** |
| **deepseek-v4-pro** | ~95% | ~90% | ~0% |

### 关键发现

1. **Few-shot 对小模型更有效** — llama 3B 上 3-shot 带来 +10% 提升，而 deepseek-v4-pro 接近天花板
2. **Few-shot 帮助纠正关键词误导** — "垃圾店" 在 0-shot 中被字面理解为"垃圾"，3-shot 范例让模型学会按意图分类
3. **模型越强，few-shot 边际收益越低** — 当 0-shot 已达到 ~95%，几个范例几乎没有增量价值
4. **格式遵循度不依赖 few-shot** — 两个模型的格式遵循在 0-shot 已是 100%

> 详见 [[摘要-few-shot-experiment]]

## 关联连接

- [[Prompt_Engineering]] — Few-shot 是 Prompt Engineering 的核心技术之一
- [[Chain_of_Thought]] — CoT 常与 Few-shot 结合使用（Few-shot CoT）
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 基础来源资料
- [[摘要-few-shot-experiment]] — 跨模型对比实验来源
- [[DeepSeek]] — 实验中的云端强模型
- [[Llama]] — 实验中的本地弱模型
