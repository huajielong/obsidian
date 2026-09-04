---
title: "BPE_Tokenizer"
type: concept
tags: [分词, BPE, tokenizer, 算法, LLM基础]
sources: [raw/01-articles/01-中英文Token差异分析.md, raw/01-articles/06-Tokenizer差异与模型性格分析.md, raw/01-articles/Ollama LLM 实验系列索引.md, raw/01-articles/DeepSeek-API-错误处理实战.md, raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md]
last_updated: 2026-08-05
---

## 定义

BPE（Byte Pair Encoding，字节对编码）是一种子词分词算法，广泛应用于现代 LLM（如 GPT、Llama、Qwen 系列）。它通过统计频率逐步合并最常见的字符/字节对来构建词表。BPE 的核心特点是：**英文单词天然在词表中（约 1 Token/词），而中文需要拆分为 UTF-8 字节序列（约 3~4 Token/字）**。

## 关键信息

### 语言 Token 效率差异

| 语言 | Token/单位 | 原因 |
|:---|:---------:|:-----|
| 英文 | ~1 Token/词 | 常见单词直接存在于 BPE 词表中 |
| 中文 | ~3~4 Token/字 | 需以 UTF-8 字节序列编码，不在基础词表中 |

### 不同模型的 Tokenizer 效率差异

以"你好"为例：

| 模型 | Token 数 | 效率比 |
|:---|:-------:|:-----:|
| qwen3.5:0.8b | **11** | 基准（最高效） |
| llama3.2:3b | **27** | 2.5× 差 |

> Qwen 系列因其中文优化，BPE 词表中包含更多中文词汇，不需要回退到逐字节编码。

### 实用 Token 估算方法

在无法调用模型 Tokenizer 时，可使用字符级粗略估算：

```python
def estimate_tokens(text: str) -> int:
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    ascii_chars = len(text) - chinese_chars
    return chinese_chars // 2 + ascii_chars // 4
```

| 语言 | 字符/Token 比 | 说明 |
|:----|:------------|:-----|
| 中文 | ~2 字符/token | 比理论值 3~4 略保守，便于留余量 |
| 英文 | ~4 字符/token | 常见英文单词约 1 token |

> 该估算适用于 Prompt 长度预检场景。如需精确 Token 计数，使用模型自带的 Tokenizer。

### Llama 词汇表实操观察（课程演示）

李宏毅《生成式人工智慧與機器學習導論(2025)》第一讲对 **Llama-3.2-3B-Instruct** 做了 Tokenizer 实操演示：

- **词汇表规模**：`tokenizer.vocab_size` = **128,000** 个 Token（编号 0~127,999），涵盖多语言文字与各类符号。
- **包罗万象**：0 号是感叹号 `!`；有阿拉伯文/日文/中文（最后一个 Token 是"锦"）；128 个连续空格是一个 Token；爱心、`地球`、`互聯網` 等都是一个 Token。
- **空白即不同 Token**：英文单词 `GOOD` 在句首（无前导空格）与词中（有前导空格）是**不同 Token**（19045 vs 1695）；`HI`/`Hi`/`hi` 三种大小写对应三个不同 Token。
- **特殊符号**：`encode` 默认在开头加一个"句子起始"特殊符号（编号 128,000，即 `<|begin_of_text|>`）；`add_special_tokens=False` 可关闭，否则 encode→decode 会多出该符号。

### 实际影响

1. **上下文窗口虚标**：模型宣称的 128K 上下文，用中文时实际容纳的内容量仅为英文的 **1/3~1/4**
2. **中英文混合 Prompt 成本更高**：同样的语义内容，中文部分消耗更多 Token
3. **不同模型成本差异**：Tokenizer 效率差异可达 2.5×，同样输入不同模型 Token 消耗不同

## 关联连接
- [[摘要-ollama-token-diff]] — 中英文 Token 差异实验数据来源
- [[摘要-ollama-tokenizer-personality]] — Tokenizer 效率差异实验数据来源
- [[摘要-deepseek-api-error-handling]] — 实用 Token 估算方法来源
- [[GPT]] — BPE 是 GPT 系列的基础分词算法
- [[Transformer_Architecture]] — Tokenizer 的输出是 Transformer 的输入
- [[本地_LLM_推理]] — Tokenizer 效率直接影响本地推理的 Token 消耗
- [[Temperature_Parameter]] — 温度参数影响输出 Token 数（高温度下波动可达 28×）
- [[Exponential_Backoff]] — Token 预检与重试策略配合使用
- [[Llama]] — Llama-3.2-3B-Instruct 词汇表实操（128,000 Token）
- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — Tokenizer 实操演示的来源
