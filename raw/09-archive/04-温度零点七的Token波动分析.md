---
tags: [ollama, llm, experiment, token, temperature, fluctuation]
created: 2026-07-09
---

# 实验四：温度 = 0.7 的 Token 波动

> [[Ollama LLM 实验系列索引]] | 模型：llama3.2:3b

## 实验方法

同一 Prompt（"背诵一首唐诗的五言绝句。"），`temperature=0.7`，重复请求 100 次，统计输出 Token 数的分布。

## 实验结果

```
成功: 100/100  失败: 0   ← 所有请求均正常返回
去重: 100/100 条不同回复  ← 每次输出都不一样！

输出 Token 统计:
  最小 = 12
  最大 = 345
  平均 = 84.7
  标准差 = 68.2
  极差 = 333   ← 同一 Prompt 输出长度差 28 倍！
```

### 各次输出长度分布

| 次数 | 输出 Token | 次数 | 输出 Token |
|:---:|:---------:|:---:|:---------:|
| 1 | 138 | 11 | — |
| 2 | 258 | 12 | — |
| 3 | 52 | 13 | — |
| 4 | — | 14 | — |
| 5 | 56 | 15 | 55 |
| 6 | — | 16 | — |
| 7 | — | 17 | — |
| 8 | — | 18 | — |
| 9 | — | 19 | — |
| 10 | 129 | 20 | 85 |

## 分析

`temperature=0.7` 下的 Token 波动极为显著：

1. **长度差异巨大**：最短 12 Token（约 8 个中文字），最长 345 Token（约 240 个中文字），相差 **28 倍**！
2. **内容完全不可预测**：模型有时生成"五言绝句"格式，有时生成大段解释性文本，有时混入英文词甚至 emoji（🌸）
3. **"指令遵循"不稳定**：Prompt 要求"背诵一首唐诗"，但高温度下模型经常自创伪唐诗
4. **100% 不同的输出**：100 次请求，100 种完全不同的回复，无一重复

> ⚠️ **生产环境警示**：如果你依赖 LLM 生成固定格式的输出（如 JSON、代码、特定长度的摘要），`temperature=0` 是必须的。`temperature>0` 的输出长度波动可达 **28 倍**，且格式完全不可预测。

## 附：实验代码

```python
# 温度=0.7 跑 100 次 — 取自 ollama_experiment_v3.py
prompt = "背诵一首唐诗的五言绝句。"
results_b = []
errors = 0

for i in range(100):
    try:
        r = call_ollama(prompt, temperature=0.7)
        results_b.append(r)
        if i < 5 or (i + 1) % 10 == 0:
            print(f"  [{i+1:3d}/100] in={r['prompt_eval_count']:3d}  "
                  f"out={r['eval_count']:3d}  | {r['message']['content'][:55]}")
    except Exception as e:
        errors += 1
        time.sleep(10)

out_tokens = [r["eval_count"] for r in results_b]
texts = [r["message"]["content"] for r in results_b]
unique = len(set(texts))

print(f"成功: {len(results_b)}/100  失败: {errors}")
print(f"去重: {unique}/{len(results_b)} 条不同回复")
print(f"输出 Token: min={min(out_tokens)}  max={max(out_tokens)}  "
      f"avg={sum(out_tokens)/len(out_tokens):.1f}")
if len(out_tokens) > 1:
    print(f"标准差: {__import__('statistics').stdev(out_tokens):.1f}")
```

> `call_ollama` 实现见 [[Ollama LLM 实验系列索引#核心 API 函数（通用）]]
