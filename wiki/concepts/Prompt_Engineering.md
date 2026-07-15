---
title: "Prompt_Engineering"
type: concept
tags: [AI, prompt, 提示词工程, few-shot, CoT]
sources: [raw/01-articles/awesome-agentic-ai-zh-stage-02-prompt-engineering.md, raw/01-articles/System-Prompt-实验对比.md]
last_updated: 2026-07-10
---

# Prompt Engineering

Prompt Engineering（提示词工程）是**设计和优化输入提示词以引导 AI 模型产生期望输出的实践**。它是 AI 应用开发中最基础的操作层技术，涵盖了从简单的指令格式调整到复杂的思维链（Chain-of-Thought）提示、少样本（Few-shot）示例设计等系统性方法。

## 核心维度

- **指令清晰性** — 明确的任务描述、角色设定和输出格式规范
- **上下文管理** — 在有限的上下文窗口中高效组织信息优先级
- **示例设计** — 通过 Few-shot 示例引导模型理解任务模式
- **推理增强** — 使用 Chain-of-Thought、Tree-of-Thought 等技术提升复杂推理能力
- **迭代优化** — 基于输出反馈持续调整提示词结构

## 结构化 Prompt 四要素

高质量的 prompt 通常包含四个结构化要素（按重要性排序）：

| 要素 | 说明 | 示例 |
|------|------|------|
| **角色设定（Role）** | 通过 System Prompt 定义 AI 的身份和行为准则 | "你是严谨的合约律师。回答要精准、引用法条编号。" |
| **任务描述（Task）** | 清晰说明需要完成的任务 | "请帮我解释什么是租赁合约。" |
| **格式规范（Format）** | 指定输出格式、长度约束 | "100 字以内、用一个段落。" |
| **示例（Examples）** | 零样本/单样本/少样本范例 | 3 条"输入→输出"的分类范例 |

## 核心技巧

### 1. Few-shot Prompting
通过在 prompt 中包含 2-5 个"输入→期望输出"范例，引导 LLM 理解任务模式。实测（Gemma 4B 中文情绪三分类）：
- **0-shot**：中立类别易误判为正面或负面
- **3-shot**：准确率明显提升，分类边界更精准
- 小模型对 few-shot 的改善幅度比大模型更显著

> 详见 [[Few_Shot_Prompting]]

### 2. Chain-of-Thought（CoT）
引导 LLM 在给出最终答案前显式展示中间推理步骤。三种变体：
- **纯 Prompt**：直接问，模型易跳步出错
- **Zero-shot CoT**：追加 "Let's think step by step"
- **Few-shot CoT**：展示完整"问题→推理→答案"范例

> 对 reasoning-native 模型（Claude Opus 4.x、o 系列、Gemini thinking），优先使用内置 extended thinking，而非手动 CoT。详见 [[Chain_of_Thought]]

### 3. System Prompt 控制力实验

固定 User Message（"请帮我解释什么是租赁合约"），仅改变 System Prompt 为三种人格，deepseek-v4-pro 的输出对比：

| 维度 | 冷酷技术专家 | 热情营销写手 | 三行格式机器人 |
|:----|:-----------|:-----------|:------------|
| 语气 | 冰冷客观 | 热情洋溢 | 简洁中性 |
| 格式 | 分点段落+法条引用 | 短句+emoji+hashtag | 精确三行结构 |
| 知识深度 | **最高**（引用民法典） | **最低**（被风格挤占） | 中等（被格式压缩） |
| 可靠度 | 高（可溯源法条） | 低（夸张比喻为主） | 中（结构清晰但浅） |

> **关键发现**：System Prompt 不只控制"怎么说"，它也实质性地改变"说什么"——风格越强，内容深度往往越浅。

**工程启示：**
1. **System Prompt 是最强控制手段** — 同样模型+同样 User Message，输出可以像三个不同的人写的一样
2. **格式约束比语气约束更稳定** — "三行格式"被严格执行，没有因为话题需要就被打破
3. **风格与深度存在取舍** — 如果答案的正确性至关重要，避免用强风格 System Prompt
4. **根据目标受众选择 System Prompt** — 面向法务 vs 面向年轻用户，需要不同的语气和信息密度

> 详见 [[摘要-system-prompt-experiment]]

### 4. 迭代 Refinement
从模糊到具体的渐进式优化过程：

| 版本 | 改进点 |
|------|--------|
| v1 模糊 | 简单描述任务 |
| v2 加目标读者 | 指定读者群体（如"给写过 Python 的工程师看"） |
| v3 加格式 | 增加字数/段落约束 |
| v4 加示例要求 | 要求在结尾举具体例子 |
| v5 加禁忌 | 排除空泛词（如"賦能""驅动""智能"） |

> 小模型（4B）对 prompt 质量极度敏感，5 轮 refine 的差距比大模型更明显——教学上更有价值。

## 三层工程堆栈中的位置

Prompt Engineering 是 LLM-powered system **三层工程堆栈中的最底层**（优化输入给模型的字符串）。其上层为：

- **[[Context_Engineering]]（上下文工程）** — 优化模型可访问的信息范围（RAG / Memory / Tool defs）
- **[[Harness_Engineering]]（驾驭工程）** — 优化模型运行的系统与环境（Agent loop / Retry / Sandbox）

> 三层的区分不在于调用次数，而在于工程对象不同。

## 局限与进阶

Prompt Engineering 虽然上手门槛低、见效快，但存在天然局限：
- 单次提示词的优化无法系统性沉淀为可复用的方法论
- 面对复杂任务时，纯提示词技巧往往不足以保证输出的稳定性和准确性
- 缺乏闭环反馈机制，难以持续迭代改进

[[AI_Mastery_Compass]] 正是在此基础上构建的系统化升级——将零散的提示词技巧整合为目标锚定、角色设定、结构化提示、交互协作、迭代优化和技能整合的六步闭环方法论。

## 关联连接

- [[专业领域数据工程]] — 专业领域评测数据层：通过领域专家判断力构建评测体系与高质量数据，将人类专业知识注入模型；覆盖小语种/医学/法律等学科
- [[Agent数据产品工程]] — 评测数据桥梁层：通过评测体系设计与数据生产管线构建，连接产品体验与模型能力；聚焦办公/生活/搜索等通用场景
- [[AI_Mastery_Compass]] — 罗盘是对 Prompt Engineering 的系统化升级
- [[Agentic_Coding]] — AI Agent 编程中的提示词工程实践
- [[Harness_Engineering]] — 为 AI 设计约束机制的系统工程中包含提示词规范设计
- [[Context_Engineering]] — 三层堆栈中间层，工程上下文信息的组装
- [[Chain_of_Thought]] — CoT 推理增强技术
- [[Few_Shot_Prompting]] — Few-shot 少样本提示技术
- [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 结构化提示词基础来源
- [[摘要-system-prompt-experiment]] — System Prompt 控制力实验来源
- [[DeepSeek]] — 实验使用的模型
