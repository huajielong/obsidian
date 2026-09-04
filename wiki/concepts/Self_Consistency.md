---
title: "Self_Consistency 自洽性/多数投票"
type: concept
tags: [self-consistency, majority-vote, 推理, reasoning, 解码策略, 采样]
sources:
  - wiki/sources/摘要-hung-yi-lee-deepseek-r1-reasoning.md
last_updated: 2026-08-05
---

# Self-Consistency（自洽性 / 多数投票）

## 定义

Self-Consistency（自洽性）是一种**从模型多次采样结果中选出正确答案**的推理时增强方法：让模型对同一个问题生成多个不同的答案，**统计各答案出现的次数，出现最多者（majority vote）即最终答案**。直觉是"正确的答案往往能被模型用不同方式反复得到，而错误答案各不相同、难以重复"。

## 做法要点

- **强制答案落位**：做 majority vote 前，通常在 prompt 中要求模型把最终答案放在 `answer`/`/answer` 标记之间，便于从长篇输出中提取真正的答案。
- **基线地位**：方法简单但**非常强**——如果要投入更多资源换更好结果，建议先做 majority vote 作为 baseline，"你不容易打败 majority vote"。

## 效果

- 让模型产生越多结果再做 majority vote，正确率越高（实验：Llama 3.2 1B / Llama 3.1 8B 采样次数 2^1~2^8 单调提升）。
- 与更强的模型对照：多数投票能让 1B 模型远好于原版，但通常仍不及 8B 模型（超越 8B 需要更复杂的 [[Process_Verifier|过程验证器]] + Beam Search 等工作流）。
- **可与其他方法叠加**：DeepSeek-R1-Zero 用 RL 训练后，再对每题采样 16 个答案做 majority vote，可与 o1 的 majority vote 相当——证明"RL 训练 + 推理时投票"可以组合使用。

## 与其他选出正确答案的方法对比

| 方法 | 做法 | 优劣 |
|------|------|------|
| **Majority Vote / Self-Consistency** | 出现次数最多的答案 | 简单、强、基线之选 |
| **Confidence** | 用模型产生该答案的机率当置信度 | 可用于 CoT-decoding |
| **Verifier + Best-of-N** | 训练验证器给答案打分，选最高 | 需要额外验证器/训练数据 |
| **Process Verifier + Beam Search** | 边解边验证中间步骤 | 可避免"第一步错、白算很久" |

## 关联连接

- [[Reasoning]] — 大规模采样 + 投票是打造推理模型的方法二
- [[Test_Time_Compute]] — 多数投票是在测试阶段投入更多算力
- [[Chain_of_Thought]] — 采样时让模型展开思考链
- [[Process_Verifier]] — 比多数投票更复杂的"逐步验证 + Beam Search"方法
- [[DeepSeek_R1]] — R1-Zero 用 majority vote 增强推理时表现
- [[摘要-hung-yi-lee-deepseek-r1-reasoning]] — 来源
