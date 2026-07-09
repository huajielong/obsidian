---
tags: [ollama, llm, experiment, token, chinese]
created: 2026-07-09
---

# 实验一：中英文 Token 差异

> [[Ollama LLM 实验系列索引]] | 模型：llama3.2:3b

## 实验方法

对 3 组语义相同的中英文句子，计算 Prompt 的 Token 数和字符数，观察 Token 化差异。

## 实验结果

| 语言 | 内容 | Token 数 | 字符数 | Token/字符 |
|:---|:---|:-------:|:-----:|:----------:|
| 中文 | 用一句话介绍你自己。 | 32 | 10 | 3.20 |
| English | Introduce yourself in one sentence. | 32 | 35 | 0.91 |
| 中文 | 背诵一首唐诗的五言绝句。 | 38 | 12 | 3.17 |
| English | Recite a five-character Tang poem. | 33 | 34 | 0.97 |
| 中文 | 太阳从东方升起。 | 33 | 8 | 4.13 |
| English | The sun rises in the east. | 32 | 26 | 1.23 |

## 结论

> **核心规律**：中文每个字 ≈ **3~4 Token**，英文每个词 ≈ **1 Token**。

Llama 3.2（基于 BPE 分词）对中文的处理方式：每个汉字通常被拆分为 2~4 个 Token，因为中文不在 BPE 词表中，需要以 UTF-8 字节序列编码。而英文单词天然在词表中，一个常见单词 = 1 Token。

**实际影响**：
- 中英文混合 Prompt 时，同样的语义内容，中文部分 Token 消耗更多
- 模型的 `context_window`（如 4K/8K/128K）对不同语言的实际承载能力不同——中文能容纳的字符数远少于英文
- 如果模型宣称 128K 上下文，用中文时实际能容纳的内容量约是英文的 **1/3~1/4**

## 附：实验代码

```python
# 中英文 Token 对比 — 取自 ollama_experiment_v3.py
pairs = [
    ("中文", "用一句话介绍你自己。"),
    ("English", "Introduce yourself in one sentence."),
    ("中文", "背诵一首唐诗的五言绝句。"),
    ("English", "Recite a five-character Tang poem."),
    ("中文", "太阳从东方升起。"),
    ("English", "The sun rises in the east."),
    ("中文", "请用50字以内解释什么是人工智能。"),
    ("English", "Explain what AI is in under 50 words."),
]
for lang, text in pairs:
    r = call_ollama(text, temperature=0.0)
    print(f"{lang:<8} {text[:37]:<40} "
          f"Prompt Token={r['prompt_eval_count']:>3}  字符数={len(text)}")
```

> `call_ollama` 实现见 [[Ollama LLM 实验系列索引#核心 API 函数（通用）]]
