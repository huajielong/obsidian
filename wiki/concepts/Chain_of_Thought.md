---
title: "Chain_of_Thought"
type: concept
tags: [提示词工程, 推理增强, CoT, reasoning]
sources:
  - raw/01-articles/awesome-agentic-ai-zh-stage-02-prompt-engineering.md
  - wiki/sources/摘要-hung-yi-lee-ai-agent-原理.md
last_updated: 2026-08-04
---

# Chain-of-Thought（思维链）

Chain-of-Thought（CoT，思维链/思考链）是一种**引导 LLM 在给出最终答案前显式展示中间推理步骤的提示词技巧**。它通过模拟人类"一步步思考"的过程，显著提升模型在数学、逻辑、推理类任务上的准确率。

## 三种 CoT 变体

### 1. 纯 Prompt（零 CoT）
直接问问题，不提供任何推理引导。模型往往直接跳到最后一步，易出错。

### 2. Zero-shot CoT（标准触发词）
在问题后追加 "Let's think step by step" 或 "请一步步思考"。无需范例，模型自动展开推理链，效果通常优于纯 Prompt。

### 3. Few-shot CoT（带范例）
在提问前展示一个完整的"问题 → 推理步骤 → 答案"范例，引导模型遵循同样的推理格式。适合需要特定推理风格的场景。

## 适用范围与注意事项

- ✅ **适用**：数学计算、逻辑推理、多步骤规划、复杂分析
- ⚠️ **对 reasoning-native 模型的建议**：Claude Opus 4.x、o 系列、Gemini thinking 等内置推理能力的模型，优先使用其 **extended thinking 模式**，不要硬塞 "Let's think step by step"——手动 CoT 可能干扰模型本来的推理路径
- ✅ **对一般 chat model 仍推荐**：对不具内置推理的模型，手写 CoT 仍是有效增强手段

## 典型效果（Gemma 4B 实测）

- 纯 Prompt：常答错数学题
- + "Let's think step by step"：多数情况下正确
- + CoT 范例：几乎都能正确

小模型对 CoT 的依赖性更高，教学价值更明显。

## Reasoning 模型 = 脑内小剧场（Agent 场景视角）

李宏毅《AI Agent 原理》讲义指出：有 **reasoning（思考）** 能力的模型，其所谓思考本质是"演脑内小剧场"——把中间推理步骤展开。当这些模型作为 Agent 时，脑内小剧场可能正好在做 **[[Model_Based_Planning|规划]]**：

- DeepSeek-R1 面对叠积木问题时在"内心"做了约 1500 字搜索，先模拟（把蓝色拿开、放回桌面、再放橙色）找到最优解，才执行第一步——即思考内部模拟了 Tree Search + World Model。
- 因此 reasoning 能力与 Agent 的规划能力有天然关联：**会思考的模型做 Agent 整体更好**。
- 副作用：**[[Over_Thinking|过度思考]]**——想太多、行动太少（"思考的巨人、行动的矮子"），是当前待研究的关键课题。

## 关联连接

- [[Model_Based_Planning]] — 脑内小剧场 = reasoning 模型的内部规划
- [[Over_Thinking]] — reasoning 模型作为 Agent 的过度思考失效模式
- [[Agent_Loop]] — 思考/规划在 Agent 循环中的位置
- [[Prompt_Engineering]] — CoT 是 Prompt Engineering 的核心技术之一
- [[Few_Shot_Prompting]] — CoT 常与 Few-shot 结合使用
- [[Context_Engineering]] — 推理链的上下文组织
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 来源资料
