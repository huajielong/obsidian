---
title: "Chain_of_Thought"
type: concept
tags: [提示词工程, 推理增强, CoT, reasoning]
sources:
  - raw/01-articles/awesome-agentic-ai-zh-stage-02-prompt-engineering.md
  - wiki/sources/摘要-hung-yi-lee-ai-agent-原理.md
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
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

### 4. Supervised CoT（把思考流程写进 Prompt）
不只叫模型 think step by step，而是**用人类知识把"怎么想"写进 prompt**（注意：不是机器学习里的 supervised learning，本质仍是 prompt 工程，不微调参数）。例如要求模型："回答前先深入解析题目要求、定出完整解题计划、列出子计划、每步多次验算、考量所有可能解法、思考过程放在 `think`/`/think` 标记中间"。李宏毅演示（GPT-4o 算 123×456）中，模型据此制定计划、分步计算并做了三次验算，甚至学会"发现某招没用就果断略过"。
- **局限**：只适用于较强的模型——弱模型（如 Llama 3）读不懂复杂指令，无法照做多次验算。

### Long CoT vs Short CoT（2025 视角）

- 2022 年经典 CoT 的思考过程较短，如今被称为 **Short CoT**；现役推理模型（o 系列 / DeepSeek-R1 等）产生**很长的思考过程**，被称为 **Long CoT**。
- 长/短没有固定的分界标准；"让思考变长"可以靠更精确的 prompt 指示实现（见 Supervised CoT），也可以靠后训练（[[Imitation_Learning]] / [[Reinforcement_Learning]]）让模型内生长思考能力。
- Long CoT 是 **[[Test_Time_Compute|测试时计算]]** 的体现：在推理阶段投入更多算力换取更好的结果（"深度不够、长度来凑"）。

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

- [[Reasoning]] — CoT 是打造推理模型的方法一（更强的思维链）
- [[Test_Time_Compute]] — Long CoT 是测试时计算的体现
- [[Model_Based_Planning]] — 脑内小剧场 = reasoning 模型的内部规划
- [[Over_Thinking]] — reasoning 模型作为 Agent 的过度思考失效模式
- [[Agent_Loop]] — 思考/规划在 Agent 循环中的位置
- [[Prompt_Engineering]] — CoT 是 Prompt Engineering 的核心技术之一
- [[Few_Shot_Prompting]] — CoT 常与 Few-shot 结合使用
- [[Context_Engineering]] — 推理链的上下文组织
- [[Self_Consistency]] — CoT + 多次采样投票
- [[Process_Verifier]] — 分步验证（step 标记）相关
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 来源资料
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — Long/Short CoT、Supervised CoT 来源
