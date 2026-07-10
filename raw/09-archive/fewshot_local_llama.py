# -*- coding: utf-8 -*-
"""
Few-Shot 本地实验 —— llama3.2:3b (Ollama)
任务：4 类意图分类 (inquiry/complaint/order/spam)
比较：0-shot vs 3-shot

预期：0-shot 准确率偏低，3-shot 明显提升
（对比 deepseek-v4-pro 的 0-shot ≈ 95%+，几乎没提升空间）
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os, time
from openai import OpenAI

client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
MODEL = "llama3.2:3b"

CATEGORIES = ["inquiry", "complaint", "order", "spam"]
CAT_LABELS = {"inquiry": "咨询", "complaint": "投诉", "order": "下单", "spam": "垃圾"}

TASK_DESC = (
    "你将收到一条用户留言。请将其分类为以下之一，只输出类别名称，不要多余文字：\n"
    "- inquiry：咨询/询问信息\n"
    "- complaint：投诉/抱怨\n"
    "- order：下单/订购\n"
    "- spam：垃圾广告/诈骗"
)

EXAMPLES = [
    ("你好，请问这款手机有蓝色的吗？", "inquiry"),
    ("送来的外卖少了一瓶可乐，退款！", "complaint"),
    ("帮我订两份牛肉面，微辣，送到5号楼", "order"),
]

TEST_SET = [
    ("你好，请问你们家的iPhone 15现在什么价格？",        "inquiry"),
    ("你们发的破快递我等了10天还没到，退款！！",           "complaint"),
    ("恭喜您获得iPhone一部，点击领取 http://xyz.com",      "spam"),
    ("我要订一份宫保鸡丁盖饭，送到3号楼502",               "order"),
    ("请问这个颜色有现货吗？什么时候能发货？",             "inquiry"),
    ("耳机收到了，但是左耳没声音，怎么处理？",             "complaint"),
    ("最后一天清仓！全场1折起，点击购买 http://ad.com",    "spam"),
    ("帮我点一杯拿铁，大杯少糖，办公室302",                "order"),
    ("这个商品拆了包装还能7天无理由退货吗？",              "inquiry"),
    ("等了一个小时还没上菜，什么垃圾店",                    "complaint"),
]


def classify(text: str, mode: str) -> str | None:
    if mode == "0-shot":
        msgs = [
            {"role": "system", "content": TASK_DESC},
            {"role": "user", "content": text},
        ]
    else:
        msgs = [{"role": "system", "content": TASK_DESC}]
        for ex_text, ex_label in EXAMPLES:
            msgs.append({"role": "user", "content": ex_text})
            msgs.append({"role": "assistant", "content": ex_label})
        msgs.append({"role": "user", "content": text})

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=msgs,
            max_tokens=50,
            temperature=0,
        )
        raw = (resp.choices[0].message.content or "").strip().lower()
        for cat in CATEGORIES:
            if cat in raw:
                return cat
        return raw
    except Exception as e:
        return f"[ERROR]"


def run_eval(mode: str):
    print(f"\n{'=' * 60}")
    print(f"[{MODEL}] [{mode}]")
    print(f"{'=' * 60}")
    correct = 0
    details = []
    for idx, (text, expected) in enumerate(TEST_SET, 1):
        predicted = classify(text, mode)
        is_correct = predicted == expected
        if is_correct:
            correct += 1
        details.append((text, expected, predicted, is_correct))
        mark = "✓" if is_correct else "✗"
        exp_cn = CAT_LABELS.get(expected, expected)
        pred_cn = CAT_LABELS.get(predicted, str(predicted)[:12])
        print(f"  {mark} [{idx:2d}] 预期={exp_cn:4s} 预测={pred_cn:12s} | {text[:35]}")
    acc = correct / len(TEST_SET) * 100
    print(f"\n  准确率: {correct}/{len(TEST_SET)} = {acc:.1f}%")
    print(f"  格式遵循: {sum(1 for _,_,p,_ in details if p in CATEGORIES)}/{len(details)}")
    return acc, details


if __name__ == "__main__":
    print(f"\n{'#' * 60}")
    print(f"# Few-Shot 实验: {MODEL} (本地 Ollama)")
    print(f"# 对比: deepseek-v4-pro 是 ~95%+ 0-shot → 3-shot 几乎没提升")
    print(f"# 预期: 本地小模型 0-shot << 3-shot")
    print(f"{'#' * 60}")

    t0 = time.time()
    acc0, d0 = run_eval("0-shot")
    acc3, d3 = run_eval("3-shot")
    elapsed = time.time() - t0

    print(f"\n{'=' * 60}")
    print("对 比 总 结")
    print(f"{'=' * 60}")
    print(f"  {MODEL}")
    print(f"  0-shot: {acc0:.1f}%")
    print(f"  3-shot: {acc3:.1f}%")
    print(f"  变化:   {acc3-acc0:+.1f}%")
    print(f"  耗时:   {elapsed:.0f}s")
