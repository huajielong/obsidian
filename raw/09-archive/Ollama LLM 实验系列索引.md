---
tags: [ollama, llm, experiment, index]
created: 2026-07-09
---

# Ollama LLM 实验系列索引

## 实验环境

| 项目 | 内容 |
|:---|:---|
| 本地模型 | llama3.2:3b (3B/2GB)、qwen3.5:0.8b (0.8B/1GB) |
| 云端模型 | DeepSeek V4 Flash、Doubao Seed Character |
| 推理设备 | CPU only (Intel, ~6.1GB 可用内存) |
| Ollama 版本 | 0.31.1 |
| 调用方式 | 原生 API `/api/chat` + OpenAI 兼容 API |
| 关键参数 | `keep_alive: "10m"`、`temperature=0.0`（除温度实验外） |

---

## 实验一览

| # | 实验 | 核心发现 | 链接 |
|:-:|:---|:---------|:----:|
| 1 | **中英文 Token 差异** | 中文每个字 ≈ 3~4 Token（BPE 字节编码），英文每个词 ≈ 1 Token；同样语义中文多耗 3~4 倍 Token | [[01-中英文Token差异分析]] |
| 2 | **温度参数扫描** | 温度范围 0.0~2.0；0.0 确定性，0.1 即开始变化，0.3+ 完全多样，1.5 开始语言混入 | [[02-温度参数扫描与取值范围]] |
| 3 | **温度=0 确定性验证** | 20/20 次输出完全一致 | [[03-温度为零确定性验证]] |
| 4 | **温度=0.7 的 Token 波动** | 同一 Prompt 输出 Token 极差 333（28 倍）；100/100 条回复全部不同 | [[04-温度零点七的Token波动分析]] |
| 5 | **跨平台成本对比** | 豆包 0.45s/次最快，DeepSeek 回复最长（144 tokens），本地模型 ¥0 | [[05-跨平台成本对比本地vs云端]] |
| 6 | **Tokenizer 差异与模型性格** | qwen3.5 分词效率高 2.5×（11 vs 27 tokens）；Fine-tuning 决定话痨程度 | [[06-Tokenizer差异与模型性格分析]] |
| 7 | **多模型回答风格对比** | 同一观点判断 Prompt，llama3.2 简洁要点式（475字），qwen3.5 长篇学术风（1,404字，3×）；云端 API 待补充 | [[07-多模型回答风格对比]] |

---

## 综合结论

### 中英文 Token 差异

| 语言 | 平均 Token/字符 | 含义 |
|:---|:-------------:|:---|
| 中文 | ~3.5 | 一个中文字 ≈ 3~4 Token（BPE 字节编码） |
| 英文 | ~1.0 | 一个英文词 ≈ 1 Token（词表匹配） |

> **不同模型 Tokenizer 差异巨大**：同样 "你好"，llama3.2 用 27 Tokens，qwen3.5 只用 11（2.5× 效率差）

### 温度参数的选择指南

| 温度 | 确定性 | 多样性 | 推荐用途 |
|:--:|:-----:|:-----:|---------|
| 0.0 | **100%** | 无 | 事实问答、代码生成、结构化输出 |
| 0.1~0.3 | 高 | 低 | 翻译、摘要、少量变体 |
| 0.5~0.7 | 低 | 中高 | 创意写作、对话、头脑风暴 |
| 0.8~1.0 | 很低 | 高 | 诗歌、故事、创意探索 |
| >1.0 | 不可控 | 极高 | 极少使用，可能产生无意义内容 |

**取值范围**：API 层（Ollama/OpenAI）限 `0.0~2.0`，超出会截断。理论无上限，但 >2.0 时输出基本乱码。

### 成本选择指南

| 场景 | 推荐方案 | 理由 |
|:---|:--------|:----|
| 开发调试、快速原型 | **豆包 / DeepSeek** | 45s~265s 跑完 100 次，几分钱 |
| 隐私敏感、离线、批量 | **Ollama 本地** | ¥0 直接成本，需硬件 |
| 高频短请求（如客服） | **豆包** | 0.45s/次，0.6 分/百次 |
| 需要长文本生成 | **DeepSeek** | 输出质量高、上下文窗口大 |
| 生产环境确定性输出 | **任何模型 + temperature=0** | 保证一致性 |

### 实践建议

1. **生产环境使用 `temperature=0`**：保证输出一致性和格式稳定
2. **需要多样性时用 `temperature=0.7`**：配合 `top_p=0.9` 效果更佳
3. **永远不要假设 `temperature>0` 的输出长度**：同一 Prompt 的 Token 数波动可达 28 倍
4. **中文 Prompt 更消耗 Token**：注意模型的上下文窗口上限
5. **温度 > 0 时指令遵循能力下降**：长度约束在高温度下基本失效
6. **模型间 Tokenizer 效率差异可达 2.5×**：同样输入，不同模型的 Token 消耗不同
7. **Fine-tuning 决定模型"性格"**：0.8B 模型可以比 3B 模型回复长 15 倍

---

## 核心 API 函数（通用）

```python
def call_ollama(prompt, temperature=0.0, retries=3):
    """带重试的 Ollama API 调用"""
    payload = {
        "model": "llama3.2:3b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": temperature},
        "keep_alive": "10m",
    }
    data = json.dumps(payload).encode("utf-8")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                "http://localhost:11434/api/chat",
                data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(5)
            else:
                raise
```

返回 JSON 包含 `prompt_eval_count`（输入 Token）、`eval_count`（输出 Token）、`message.content`（回复文本）。

---

*实验日期：2026-07-09*
*模型：llama3.2:3b / qwen3.5:0.8b / DeepSeek V4 Flash / Doubao Seed Character*
