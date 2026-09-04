---
title: "System_Prompt"
type: concept
tags: [系统提示词, System Prompt, LLM基础, Prompt]
sources: [raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md]
last_updated: 2026-08-05
---

## 定义

**系统提示词（System Prompt）** 是开发者/平台在每次对话中**预先设定、自动附加**在用户输入之前的提示内容，用于给模型注入**基础信息与行为约束**（如当前日期、模型身份、回答风格、安全规则）。与用户输入的 **User Prompt** 相对，System Prompt 通常由系统侧控制、用户不可见，且在冲突时优先级更高。

## 关键信息

### 为什么需要它

- 语言模型是"关在暗无天日小房间里只会接龙的人"，看不到外部世界 → 问"今天是几月几号"只能瞎猜。
- 平台把**每次对话都会用到的信息**（今天几月几号、模型叫什么名字）预先塞在对话最前面，模型接龙时就有机会接出正确答案。
- 这正体现了 [[Context_Engineering]] 的核心：人类确保输入 Prompt 的信息足够。

### 实际观察（Llama 实操）

- 用 `apply_chat_template` 时，模板自动塞入一段 system 内容，例如"我的知识到 2023 年 12 月、今天是 2025 年 9 月 12 日"。
- **身份幻觉**：不设置 System Prompt 时，Llama 会自称 GPT-3.5（训练数据里常见）；在 System Prompt 写"你的名字是 Llama"即可纠正。
- 回答风格也能控制（实操中让模型"都用中文回答、开头说哈哈哈"，模型照做）。

### 与 User Prompt 的区分

| 类型 | 谁提供 | 特征 |
|------|--------|------|
| **System Prompt** | 开发者/平台 | 每次对话自动加上、用户通常不可见、最高优先级 |
| **User Prompt** | 用户 | 用户直接输入的请求 |

> 平台背后到底加了什么 Prompt 通常不公开（ChatGPT 即如此），这正是 System Prompt 的"黑箱"一面。

## 关联连接

- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — 本概念的来源
- [[Chat_Template]] — System Prompt 通常作为模板中的第一个 system 角色段
- [[Context_Engineering]] — System Prompt 是注入基础信息、保障接龙正确的手段
- [[Prompt_Engineering]] — System Prompt 属于提示工程的输入优化层
- [[AI_Hallucination]] — 注入事实性 System Prompt 可减少部分幻觉
- [[摘要-system-prompt-experiment]] — 知识库中 System Prompt 控制力实验（三种人格输出对比）
- [[Auto_Regressive_Generation]] — System Prompt 只是改变输入，模型仍在做接龙
