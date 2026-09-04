---
title: "Imitation_Learning 模仿学习"
type: concept
tags: [模仿学习, imitation, 推理, reasoning, SFT, 后训练, 蒸馏]
sources:
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

# Imitation Learning（模仿学习）

## 定义

Imitation Learning（模仿学习）指**直接教模型"怎么做推理"**：训练数据不只包含"问题 + 答案"，还包含**推理过程（reasoning process）**，让模型模仿老师/范例的推理方式，输出"推理过程 → 正确结果"。它是打造推理模型的**方法三**，属于后训练（Post-training）的一种——可视为监督学习（SFT）或偏好/RL 类学习的统称。

## 核心难点：推理过程从哪来？

通常只有"问题 + 正确答案"，没有推理过程；让人手写代价极高。解决办法：

1. **让 LLM 自己生成**：拿一个语言模型按 CoT 详细解题 → 只把**答对**时的推理过程拿来当训练资料（假设"答案对 ⇒ 推理过程大概率对"）。
2. **无标准答案的问题**：用 verifier（甚至现成的 LLM）判断答案好坏，答案好的就假设推理过程可用。
3. **更严格（树状搜索 + 过程验证器）**：解一步验证一步，只保留验证通过的正确步骤拼成推理过程，保证每一步都较可靠。

## 关键洞察：不要只教"全对的推理"

- 若训练数据每一步推理都是对的，模型**不知道推理过程可能会错**——前面错了也不知道，只会硬凹下去（一步错、步步错）。
- 应教模型**知错能改**，两种代表性做法：
  - **Stream of Search**：在树状结构上做深度优先搜索，把**包含错误路径的推理过程**也放进训练数据（"先走 step1→step2（错）→退回来换 step2'→再错→回到原点重试"）。
  - **Journey Learning**：与只选全对路径的 **Shortcut Learning** 相对，含错误路径的"完整旅程"让模型学会**逆势翻盘**。Math500 实验：两个不同基座模型上 Journey Learning 正确率均高于 Shortcut Learning。
- 可读性优化：在错误步骤与修正之间**插入 verifier 的反馈句子**（"这一步的答案有误，我们换个解法"），或用更强的模型**改写**整个搜索过程、加连接词。
- 副作用：如此训练的模型（如早期 o1）思考会比较**跳跃、前言不对后语**。

## 与 RL 的关系

- 不一定要用监督学习——也可以利用树状结构中的"好步骤/坏步骤、好路径/坏路径"，用 **DPO 或类似 RL 的方法**提高好路径概率、降低坏路径概率。
- DeepSeek-R1 的真实流水线中，模仿学习是承上启下的关键环节（R1-Zero 生成数据 → 人工改写 → 模仿学习 → RL → 再生成数据 → 再模仿学习）。

## 捷径：Knowledge Distillation

已有现成的强推理模型时，不必费劲自造推理数据——直接让老师模型生成推理过程，学生模型学习即可（见 [[Knowledge_Distillation]]；案例：SkyT1、S1、DeepSeek 蒸馏 Qwen/Llama）。

## 关联连接

- [[Reasoning]] — 打造推理模型的方法三
- [[Knowledge_Distillation]] — 模仿学习的捷径（向强推理模型学习）
- [[Reinforcement_Learning]] — 方法四：以结果为导向（对比：模仿学习在意推理过程，RL 只在意结果）
- [[Process_Verifier]] — 生成高质量推理过程数据的工具
- [[Chain_of_Thought]] — 推理过程的形式（CoT）
- [[Model_Fine_Tuning]] — 后训练/微调的上位概念
- [[后训练研究]] — 后训练研究体系（SFT/RL/对齐）
- [[DeepSeek_R1]] — 模仿学习在 R1 流水线中的实际应用
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — 来源
