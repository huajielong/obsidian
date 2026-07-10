# -*- coding: utf-8 -*-
"""
练习 2：Few-Shot 实验
任务：短信/留言意图分类（4 类）
比较：0-shot vs 3-shot 的准确率 + 格式遵循度
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os, json
from openai import OpenAI

# ⚠️ API Key 必须通过环境变量设置，不得硬编码
# 设置方式: export DEEPSEEK_API_KEY="sk-你的key"
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-pro"
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)

# ====================================
# 分类体系
# ====================================
CATEGORIES = ["inquiry", "complaint", "order", "spam"]
CAT_LABELS = {
    "inquiry": "咨询", "complaint": "投诉", "order": "下单", "spam": "垃圾"
}

# ====================================
# 3-shot 范例
# ====================================
EXAMPLES = [
    ("你好，请问这款手机有蓝色的吗？", "inquiry"),
    ("送来的外卖少了一瓶可乐，退款！", "complaint"),
    ("帮我订两份牛肉面，微辣，送到5号楼", "order"),
]
# 注意：spam 类别不出现在范例中——看模型能否零样本泛化

# ====================================
# 测试集（10 条，含 ground truth）
# ====================================
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

# 测试集各类别分布
distro = {}
for _, lbl in TEST_SET:
    distro[lbl] = distro.get(lbl, 0) + 1


def build_zero_shot_prompt(text: str) -> list:
    return [
        {"role": "system", "content":
            f"你将收到一条用户留言。请将其分类为以下之一，只输出类别名称：\n"
            f"- inquiry：咨询/询问信息\n"
            f"- complaint：投诉/抱怨\n"
            f"- order：下单/订购\n"
            f"- spam：垃圾广告/诈骗\n"},
        {"role": "user", "content": text},
    ]


def build_three_shot_prompt(text: str) -> list:
    msgs = [
        {"role": "system", "content":
            f"你将收到一条用户留言。请将其分类为以下之一，只输出类别名称：\n"
            f"- inquiry：咨询/询问信息\n"
            f"- complaint：投诉/抱怨\n"
            f"- order：下单/订购\n"
            f"- spam：垃圾广告/诈骗\n"},
    ]
    # 插入 3 个范例
    for ex_text, ex_label in EXAMPLES:
        msgs.append({"role": "user", "content": ex_text})
        msgs.append({"role": "assistant", "content": ex_label})
    # 真正的 query
    msgs.append({"role": "user", "content": text})
    return msgs


def classify(text: str, mode: str) -> str | None:
    """调用 API 返回预测的类别，或 None"""
    prompt = build_zero_shot_prompt(text) if mode == "0-shot" else build_three_shot_prompt(text)
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            max_tokens=100,
            temperature=0,
        )
        raw = (resp.choices[0].message.content or "").strip().lower()
        # 从响应中提取类别
        for cat in CATEGORIES:
            if cat in raw:
                return cat
        # 没匹配到 → 记录原始输出
        return raw
    except Exception as e:
        return f"[ERROR] {e}"


def run_eval(mode: str):
    print(f"\n{'=' * 60}")
    print(f"[{mode}] 评估 {len(TEST_SET)} 条测试数据")
    print(f"{'=' * 60}")

    correct = 0
    details = []

    for text, expected in TEST_SET:
        predicted = classify(text, mode)
        is_correct = predicted == expected
        if is_correct:
            correct += 1
        details.append((text, expected, predicted, is_correct))

    # 打印详细结果
    print(f"\n{'─' * 60}")
    for i, (text, exp, pred, ok) in enumerate(details, 1):
        mark = "✓" if ok else "✗"
        print(f"  {mark} [{i:2d}] 预期={CAT_LABELS.get(exp,exp):4s} | "
              f"预测={CAT_LABELS.get(pred,str(pred)):12s} | {text[:30]}")

    # 统计
    acc = correct / len(TEST_SET) * 100
    print(f"\n{'─' * 60}")
    print(f"  正确: {correct}/{len(TEST_SET)}  →  准确率: {acc:.1f}%")

    # 按类别分析
    print(f"\n  各类别准确率:")
    for cat in CATEGORIES:
        total = sum(1 for _, e in TEST_SET if e == cat)
        ok = sum(1 for t, e, p, _ in details if e == cat and p == e)
        if total > 0:
            print(f"    {CAT_LABELS[cat]:8s} ({cat:12s}): {ok}/{total} = {ok/total*100:.0f}%")

    # 格式遵循度
    format_errors = sum(1 for _, _, p, _ in details if p not in CATEGORIES)
    total = len(details)
    format_ok = total - format_errors
    print(f"\n  格式遵循: {format_ok}/{total} = {format_ok/total*100:.1f}%")
    if format_errors > 0:
        bad_outputs = [(t, p) for t, _, p, _ in details if p not in CATEGORIES]
        print(f"  格式异常输出:")
        for t, p in bad_outputs:
            print(f"    → 输入: {t[:40]}")
            print(f"      输出: {p}")

    return acc, details


# ====================================
# 主流程
# ====================================
if __name__ == "__main__":
    print("=" * 60)
    print("Few-Shot 实验：意图分类")
    print(f"模型: {MODEL}")
    print(f"类别: {', '.join(f'{k}({v})' for k,v in CAT_LABELS.items())}")
    print(f"测试集: {len(TEST_SET)} 条")
    print(f"分布: { {CAT_LABELS[k]: v for k,v in sorted(distro.items())} }")
    print(f"3-shot 范例覆盖: {', '.join(CAT_LABELS[e] for _, e in EXAMPLES)}")
    print(f"  (注: spam 未出现在范例中，检验泛化能力)")

    acc0, details0 = run_eval("0-shot")
    acc3, details3 = run_eval("3-shot")

    # 对比总结
    print(f"\n{'=' * 60}")
    print("对比总结")
    print(f"{'=' * 60}")
    print(f"  0-shot 准确率: {acc0:.1f}%")
    print(f"  3-shot 准确率: {acc3:.1f}%")
    diff = acc3 - acc0
    arrow = "↑" if diff > 0 else ("↓" if diff < 0 else "→")
    print(f"  差异:         {arrow} {abs(diff):.1f}%")

    # 逐条对比
    print(f"\n  逐条差异:")
    for i, ((t0, _, d0, _), (t3, _, d3, _)) in enumerate(zip(details0, details3)):
        if d0 != d3:
            print(f"    [{i+1:2d}] {t0[:40]}")
            print(f"         0-shot: {d0}   3-shot: {d3}")
