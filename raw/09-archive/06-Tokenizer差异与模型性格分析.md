---
tags: [ollama, llm, experiment, tokenizer, token, qwen, finetuning]
created: 2026-07-09
---

# 实验六：Tokenizer 差异与模型性格分析

> [[Ollama LLM 实验系列索引]] | 模型：llama3.2:3b vs qwen3.5:0.8b

## 实验方法

同机 Ollama 运行两个本地模型，对同一 Prompt（"你好"）各请求 100 次（`temperature=0.0`），观察分词和生成行为的差异。

## 实验结果

| 指标 | llama3.2:3b | qwen3.5:0.8b | 差异倍数 |
|:---|:---:|:---:|:---:|
| 模型参数量 | 3B | 0.8B | 小 3.75× |
| 输入 Token（"你好"） | 27 | **11** | Tokenizer 高效 2.5× |
| 输出 Token | 18 | **278** | 回复长 15× |
| 生成速度 | 7.8 tok/s | **19.0 tok/s** | 快 2.4× |
| 总耗时/次 | **2.3s** | 14.6s | 慢 6× |

## 分析

### 1. Tokenizer 效率差异

qwen3.5 对中文的分词效率远高于 llama3.2：`"你好"` 仅 11 Tokens（vs 27）。说明 qwen 的 BPE 词表中包含了更多中文词汇，不需要回退到逐字节编码。同样的中文句子，qwen3.5 消耗的 Token 数约为 llama3.2 的 **40%**。

### 2. 回复风格差异（Fine-tuning 影响）

```
"你好"
→ llama3.2: "你好！有什么可以帮助你的吗？"（18 tokens，惜字如金）
→ qwen3.5: "你好！我是 Qwen3.5，一个基于多模态大模型架构的超大规模语言模型。我支持多种任务类型，包括文本生成、逻辑推理、信息检索…你有任何具体需求吗？😊"（278 tokens，热情话痨）
```

qwen3.5 的 fine-tuning 让它对简单问候也回以 **完整自我介绍**（158 字）甚至带 emoji，而 llama 保持简洁。这说明 **模型的"性格"由 fine-tuning 决定，而非参数规模**——0.8B 的 qwen 回得比 3B 的 llama 长 15 倍。

### 3. "小模型更快"是误解

qwen3.5:0.8b 纯生成速度确实更快（19 vs 7.8 tok/s），但因为输出量大了 15×，总耗时反而慢 6 倍。

> **模型大小影响的是"每秒生成多少个字"，不决定"总共生成多少字"**。最终的响应时间 = 输出量 ÷ 生成速度。

## 附：实验代码

```python
# 本地模型对比 — test_ollama.py
import sys, time, statistics, json, urllib.request

PROMPT = "你好"
N = 100

def call(model):
    p = {"model": model, "messages": [{"role":"user","content":PROMPT}],
         "stream": False, "options": {"temperature": 0.0}, "keep_alive": "10m"}
    req = urllib.request.Request("http://localhost:11434/api/chat",
        data=json.dumps(p).encode(), headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())

def run(model):
    lat, it, ot = [], [], []
    for i in range(N):
        t0 = time.time()
        r = call(model)
        d = time.time() - t0
        lat.append(d); it.append(r["prompt_eval_count"])
        ot.append(r["eval_count"])
        if (i+1)%10 == 0:
            print(f"  [{i+1:3d}/{N}] in={it[-1]} out={ot[-1]} {d:.2f}s")
    return lat, it, ot

models = ["llama3.2:3b", "qwen3.5:0.8b"]
results = []
for m in models:
    print(f"\n测试 {m}...")
    results.append(run(m))

print(f"\n\n{'='*60}")
print(f"模型对比 (Prompt=\"{PROMPT}\" x{N}次)")
print(f"{'模型':<20} {'总耗时':>7} {'均延迟':>7} {'输入T':>6} {'输出T':>6} {'tok/s':>6}")
for i, r in enumerate(results):
    l = r[0]
    avg_lat = statistics.mean(l)
    avg_out = statistics.mean(r[2])
    print(f"{models[i]:<20} {sum(l):>7.1f}s {avg_lat:>6.3f}s "
          f"{statistics.mean(r[1]):>5.0f} {avg_out:>5.0f} {avg_out/avg_lat:>5.1f}")
```
