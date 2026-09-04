---
title: "Chat_Template"
type: concept
tags: [聊天模板, Chat Template, LLM基础, Prompt, 多轮对话]
sources: [raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md]
last_updated: 2026-08-05
---

## 定义

**聊天模板（Chat Template）** 是平台/模型在用户输入前后**偷偷追加**的结构化包装，把"用户提问 + AI 回答"的对话角色格式（如 `使用者問：…？AI回答：`）拼接到 Prompt 上，让只会做文字接龙的模型顺着"AI回答："接下去，从而**回答**用户问题而非继续接出其他内容。

## 关键信息

### 为什么需要它

- 纯文字接龙不保证接出"答案"："台湾最高的山是哪座？"后面也可以接"谁告诉我呀"或"出个考题"。
- 加上 `AI回答：` 后，接龙唯一合理的走向就是回答问题。

### 结构示例

```
（可选 System Prompt / 基础信息）
<|start_header_id|>system<|end_header_id|> 你的名字是 Llama …<|eot_id|>
<|start_header_id|>user<|end_header_id|> 你是誰？<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>   ← 模型从这里开始接龙
```

- 用 `<|start_header_id|>/<|end_header_id|>`（Llama 官方模板）标注每一段话的说话人（role）。
- 模型实际看到的输入 = **System Prompt / 基础信息 + Chat Template 包装的对话历史 + 最新用户输入**。

### 关键要点

| 要点 | 说明 |
|------|------|
| **各模型模板不同且常不公开** | ChatGPT 的模板未知；Llama 的官方模板可在实操中打印查看 |
| **必须用官方模板** | 自己发明的模板效果差（模型接出"使用者说"却收不了尾）；官方模板经过测试、效果最佳 |
| **不要手写，用函数** | `tokenizer.apply_chat_template(messages)` 自动加模板 + 编码（输出直接是 Token ID） |
| **多轮对话靠它拼接历史** | 每轮把完整历史 messages（user/assistant/system）全部传给模板，模型才能理解上下文 |
| **可强制预设回答** | 把模型"没说过的话"塞进 assistant 角色，模型只能顺着接龙（可用来强制回答开头） |

### 与 System Prompt 的关系

System Prompt 通常作为 Chat Template 中的第一个 system 角色段，或叠加在模板之前的 Prompt 前缀里，二者共同构成模型实际看到的完整输入。

## 关联连接

- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — 本概念的来源
- [[System_Prompt]] — 模板中最高优先级的 system 角色段
- [[Auto_Regressive_Generation]] — 模板包装后模型仍只是做文字接龙
- [[AI_Hallucination]] — 模板不完善时模型会自行接出不该有的内容
- [[Llama]] — 官方模板的实操示例（apply_chat_template）
- [[Prompt_Engineering]] — 模板与提示工程的上位概念
