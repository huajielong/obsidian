# -*- coding: utf-8 -*-
"""
练习 2：Few-Shot 实验 V2
任务：客服留言的「紧急度 + 处理建议」分类
输出格式：JSON 行
比较：0-shot vs 3-shot 的格式遵循度 + 内容准确率
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
# 任务说明
# ====================================
TASK_DESC = """
将每条客服留言解析为 JSON 格式，包含三个字段：
- urgency: "high" | "medium" | "low"（紧急程度）
- sentiment: "angry" | "neutral" | "positive"（情绪）
- action: 字符串，建议客服采取的动作（10 字以内）

只输出 JSON 行，不要多余文字。
"""

# ====================================
# 3-shot 范例（含正确格式示范）
# ====================================
EXAMPLES = [
    (
        "你们发的快递我等了10天还没到，退款！！",
        '{"urgency": "high", "sentiment": "angry", "action": "安抚并催单"}',
    ),
    (
        "请问这个颜色还有货吗？",
        '{"urgency": "low", "sentiment": "neutral", "action": "查询库存"}',
    ),
    (
        "谢谢你们上次的快速处理，很满意",
        '{"urgency": "low", "sentiment": "positive", "action": "转达谢意"}',
    ),
]

# ====================================
# 测试集（10 条 + ground truth）
# ====================================
TEST_SET = [
    ("等了一个小时还没上菜，什么垃圾店，我要退菜！",
     {"urgency": "high", "sentiment": "angry", "action": "道歉退菜"}),
    ("你好，我想问一下这个商品支持7天无理由退货吗？",
     {"urgency": "low", "sentiment": "neutral", "action": "解释退货政策"}),
    ("耳机收到了，音质很好，推荐朋友来买",
     {"urgency": "low", "sentiment": "positive", "action": "感谢好评"}),
    ("你们系统一直报错，付不了款，急死人了！！",
     {"urgency": "high", "sentiment": "angry", "action": "排查技术故障"}),
    ("我的订单显示已签收但我没收到货，怎么回事？",
     {"urgency": "high", "sentiment": "angry", "action": "核实物流"}),
    ("请问你们周末营业吗？",
     {"urgency": "low", "sentiment": "neutral", "action": "告知营业时间"}),
    ("App 闪退，连续试了三次都打不开",
     {"urgency": "high", "sentiment": "angry", "action": "上报技术团队"}),
    ("能不能帮我改一下收货地址，刚才填错了",
     {"urgency": "medium", "sentiment": "neutral", "action": "协助修改地址"}),
    ("你们的售后服务电话是多少？",
     {"urgency": "low", "sentiment": "neutral", "action": "提供联系方式"}),
    ("上次买的充电宝用了两天就坏了，我要投诉",
     {"urgency": "medium", "sentiment": "angry", "action": "登记售后处理"}),
]


def parse_response(raw: str) -> dict | None:
    """尝试从模型输出中解析 JSON"""
    raw = raw.strip()
    # 尝试整体解析
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # 尝试找 {...}
    import re
    m = re.search(r'\{.*?\}', raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return None


def build_zero_shot_prompt(text: str) -> list:
    return [
        {"role": "system", "content": TASK_DESC},
        {"role": "user", "content": text},
    ]


def build_three_shot_prompt(text: str) -> list:
    msgs = [{"role": "system", "content": TASK_DESC}]
    for ex_text, ex_json in EXAMPLES:
        msgs.append({"role": "user", "content": ex_text})
        msgs.append({"role": "assistant", "content": ex_json})
    msgs.append({"role": "user", "content": text})
    return msgs


def run_eval(mode: str):
    print(f"\n{'=' * 60}")
    print(f"[{mode}] 评估 {len(TEST_SET)} 条测试数据")
    print(f"{'=' * 60}")

    correct_urgency = 0
    correct_sentiment = 0
    parse_ok = 0
    details = []

    for text, expected in TEST_SET:
        prompt = build_zero_shot_prompt(text) if mode == "0-shot" else build_three_shot_prompt(text)
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=prompt,
                max_tokens=150,
                temperature=0,
            )
            raw = (resp.choices[0].message.content or "").strip()
        except Exception as e:
            raw = f"[ERROR] {e}"

        parsed = parse_response(raw)
        is_parsed = parsed is not None and all(k in parsed for k in ("urgency", "sentiment", "action"))
        if is_parsed:
            parse_ok += 1
            correct_urgency += 1 if parsed.get("urgency") == expected["urgency"] else 0
            correct_sentiment += 1 if parsed.get("sentiment") == expected["sentiment"] else 0

        details.append((text, expected, raw, parsed, is_parsed))

    # 打印
    for i, (text, exp, raw, parsed, ok) in enumerate(details, 1):
        if ok:
            u_ok = "✓" if parsed["urgency"] == exp["urgency"] else "✗"
            s_ok = "✓" if parsed["sentiment"] == exp["sentiment"] else "✗"
            print(f"  [{i:2d}] 紧急{u_ok} 情绪{s_ok} | {text[:35]}")
            print(f"       目标: {json.dumps(exp, ensure_ascii=False)}")
            print(f"       预测: {json.dumps(parsed, ensure_ascii=False)}")
        else:
            print(f"  [{i:2d}] ✗ 解析失败 | {text[:35]}")
            print(f"       原始输出: {raw[:80]}")

    n = len(TEST_SET)
    print(f"\n{'─' * 60}")
    print(f"  JSON 格式遵循: {parse_ok}/{n} = {parse_ok/n*100:.0f}%")
    if parse_ok > 0:
        acc_u = correct_urgency / n * 100
        acc_s = correct_sentiment / n * 100
        print(f"  Urgency 准确率: {correct_urgency}/{n} = {acc_u:.0f}%")
        print(f"  Sentiment 准确率: {correct_sentiment}/{n} = {acc_s:.0f}%")
        all_ok = sum(1 for _, _, _, p, ok in details
                     if ok and p["urgency"] == exp["urgency"] and p["sentiment"] == exp["sentiment"])
        # 需要重新计算 all_ok
        all_ok = 0
        for _, exp, _, p, ok in details:
            if ok and p["urgency"] == exp["urgency"] and p["sentiment"] == exp["sentiment"]:
                all_ok += 1
        print(f"  完全正确: {all_ok}/{n} = {all_ok/n*100:.0f}%")
    return details


# ====================================
# 主流程
# ====================================
if __name__ == "__main__":
    print("=" * 60)
    print("Few-Shot 实验 V2：客服留言结构化解析")
    print(f"模型: {MODEL}")
    print(f"任务: 从留言中提取 urgency / sentiment / action")
    print(f"测试集: {len(TEST_SET)} 条")
    print(f"3-shot 范例覆盖: anger+neutral+positive 各 1 条")

    d0 = run_eval("0-shot")
    d3 = run_eval("3-shot")

    print(f"\n{'=' * 60}")
    print("对比总结")
    print(f"{'=' * 60}")

    for mode, details in [("0-shot", d0), ("3-shot", d3)]:
        parse_ok = sum(1 for _, _, _, p, ok in details if ok)
        correct_u = sum(1 for _, e, _, p, ok in details if ok and p["urgency"] == e["urgency"])
        correct_s = sum(1 for _, e, _, p, ok in details if ok and p["sentiment"] == e["sentiment"])
        all_ok = sum(1 for _, e, _, p, ok in details if ok and p["urgency"] == e["urgency"] and p["sentiment"] == e["sentiment"])
        print(f"\n  {mode}:")
        print(f"    格式遵循: {parse_ok}/10")
        print(f"    Urgency准确率: {correct_u}/10")
        print(f"    Sentiment准确率: {correct_s}/10")
        print(f"    完全正确: {all_ok}/10")
