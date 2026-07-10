# -*- coding: utf-8 -*-
"""
练习 2（延伸）：Few-Shot —— 弱模型 vs 强模型
对比 qwen3.5:0.8b（本地）和 deepseek-v4-pro 的 few-shot 差异

核心发现预期：
  - qwen3.5: 0-shot 格式偏差大 + 准确率低 → 3-shot 大幅改善
  - deepseek-v4-pro: 0-shot 已有 ~90% → 3-shot 增量有限
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os, json, re
from openai import OpenAI

# ====================================
# 两个客户端
# ====================================
# 本地弱模型（Ollama）
LOCAL_CLIENT = OpenAI(
    api_key="ollama",  # Ollama 不需要真实 key
    base_url="http://localhost:11434/v1",
)
LOCAL_MODEL = "qwen3.5:0.8b"

# 云端强模型（DeepSeek）
# ⚠️ API Key 必须通过环境变量设置，不得硬编码
# 设置方式: export DEEPSEEK_API_KEY="sk-你的key"
_deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
if not _deepseek_key:
    raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")
DEEPSEEK_CLIENT = OpenAI(
    api_key=_deepseek_key,
    base_url="https://api.deepseek.com",
)
DEEPSEEK_MODEL = "deepseek-v4-pro"

# ====================================
# 任务定义（与 V2 完全一致）
# ====================================
TASK_DESC = """
将每条客服留言解析为 JSON 格式，包含三个字段：
- urgency: "high" | "medium" | "low"（紧急程度）
- sentiment: "angry" | "neutral" | "positive"（情绪）
- action: 字符串，建议客服采取的动作（10 字以内）

只输出 JSON 行，不要多余文字。
"""

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
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
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


def run_eval(client, model: str, model_label: str, mode: str):
    """对单个 (client, model, mode) 跑完整评估"""
    print(f"\n{'=' * 60}")
    print(f"[{model_label}] [{mode}] 评估 {len(TEST_SET)} 条")
    print(f"{'=' * 60}")

    correct_urgency = 0
    correct_sentiment = 0
    parse_ok = 0
    details = []

    for text, expected in TEST_SET:
        prompt = build_zero_shot_prompt(text) if mode == "0-shot" else build_three_shot_prompt(text)
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=prompt,
                max_tokens=200,
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

    # 打印明细
    for i, (text, exp, raw, parsed, ok) in enumerate(details, 1):
        if ok:
            u_ok = "✓" if parsed["urgency"] == exp["urgency"] else "✗"
            s_ok = "✓" if parsed["sentiment"] == exp["sentiment"] else "✗"
            print(f"  [{i:2d}] 紧急{u_ok} 情绪{s_ok} | {text[:35]}")
            print(f"       目标: {json.dumps(exp, ensure_ascii=False)}")
            print(f"       预测: {json.dumps(parsed, ensure_ascii=False)}")
        else:
            print(f"  [{i:2d}] ✗ 解析失败 | {text[:35]}")
            print(f"       原始输出: {raw[:120] if raw else '(空)'}")

    n = len(TEST_SET)
    print(f"\n{'─' * 60}")
    print(f"  JSON 格式遵循: {parse_ok}/{n} = {parse_ok/n*100:.0f}%")
    correct_all = 0
    if parse_ok > 0:
        acc_u = correct_urgency / n * 100
        acc_s = correct_sentiment / n * 100
        print(f"  Urgency 准确率: {correct_urgency}/{n} = {acc_u:.0f}%")
        print(f"  Sentiment 准确率: {correct_sentiment}/{n} = {acc_s:.0f}%")
        for _, exp, _, p, ok in details:
            if ok and p["urgency"] == exp["urgency"] and p["sentiment"] == exp["sentiment"]:
                correct_all += 1
        print(f"  完全正确: {correct_all}/{n} = {correct_all/n*100:.0f}%")

    return {
        "mode": mode,
        "model": model_label,
        "parse_ok": parse_ok,
        "correct_urgency": correct_urgency,
        "correct_sentiment": correct_sentiment,
        "correct_all": correct_all,
        "total": n,
    }


def print_summary(results: list):
    """打印两个模型 × 两种模式的对比总结"""
    print(f"\n{'=' * 60}")
    print("对 比 总 结")
    print(f"{'=' * 60}")

    # 按模型分组
    models = set(r["model"] for r in results)
    for m in sorted(models):
        m_results = [r for r in results if r["model"] == m]
        zero = next(r for r in m_results if r["mode"] == "0-shot")
        three = next(r for r in m_results if r["mode"] == "3-shot")

        print(f"\n  [{m}]")
        print(f"  {'':20s} {'0-shot':>10s} {'3-shot':>10s} {'变化':>10s}")
        print(f"  {'─'*50}")
        fmt = f"  {{:20s}} {{:>8d}}/{{:d}} {{:>8d}}/{{:d}} {{:>+9d}}"
        total = zero["total"]
        print(fmt.format("格式遵循", zero["parse_ok"], total, three["parse_ok"], total, three["parse_ok"] - zero["parse_ok"]))
        print(fmt.format("Urgency 正确", zero["correct_urgency"], total, three["correct_urgency"], total, three["correct_urgency"] - zero["correct_urgency"]))
        print(fmt.format("Sentiment 正确", zero["correct_sentiment"], total, three["correct_sentiment"], total, three["correct_sentiment"] - zero["correct_sentiment"]))
        print(fmt.format("完全正确", zero["correct_all"], total, three["correct_all"], total, three["correct_all"] - zero["correct_all"]))

    # 关键结论
    print(f"\n{'─' * 60}")
    print("关 键 结 论")
    print(f"{'─' * 60}")

    for m in sorted(models):
        m_results = [r for r in results if r["model"] == m]
        zero = next(r for r in m_results if r["mode"] == "0-shot")
        three = next(r for r in m_results if r["mode"] == "3-shot")
        gap = three["correct_all"] - zero["correct_all"]
        print(f"\n  [{m}]")
        print(f"    0-shot 完全正确: {zero['correct_all']}/{zero['total']} ({zero['correct_all']/zero['total']*100:.0f}%)")
        print(f"    3-shot 完全正确: {three['correct_all']}/{three['total']} ({three['correct_all']/three['total']*100:.0f}%)")
        if gap > 0:
            print(f"    提升: +{gap} 条 (↑ {gap/zero['total']*100:.0f}%)")
        elif gap == 0:
            print(f"    提升: 无变化 (模型已接近上限)")
        else:
            print(f"    变化: {gap} 条 (3-shot 反而更差)")


# ====================================
# 主流程
# ====================================
if __name__ == "__main__":
    RUN_CONFIGS = [
        # (client, model_name, display_label)
        (LOCAL_CLIENT, LOCAL_MODEL, "qwen3.5:0.8b"),
        (DEEPSEEK_CLIENT, DEEPSEEK_MODEL, "deepseek-v4-pro"),
    ]

    all_results = []

    for client, model, label in RUN_CONFIGS:
        print(f"\n{'#' * 60}")
        print(f"# 模型: {label}")
        print(f"{'#' * 60}")
        for mode in ("0-shot", "3-shot"):
            stats = run_eval(client, model, label, mode)
            all_results.append(stats)

    print_summary(all_results)
