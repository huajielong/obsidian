# -*- coding: utf-8 -*-
"""
练习 1b：System Prompt 实验
User Prompt: "请帮我解释什么是租赁合约。"
同样的三个 system prompt → 观察解释内容 + 格式 + 语气变化
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os
from openai import OpenAI

# ⚠️ API Key 必须通过环境变量设置，不得硬编码
# 设置方式: export DEEPSEEK_API_KEY="sk-你的key"
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-pro"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)

USER_MSG = "请帮我解释什么是租赁合约。"

SYSTEMS = [
    {
        "name": "1. 冷酷技术专家",
        "system": "你是一个冷酷、理性的技术专家。只用事实说话，不用礼貌用语，不寒暄，不废话。直接给出最精确的技术回答。",
    },
    {
        "name": "2. 热情营销写手",
        "system": "你是一个充满激情的营销文案专家。语气热情洋溢，善用感叹号和emoji，每段结尾可以加上相关tag。目的是吸引读者注意。",
    },
    {
        "name": "3. 三行格式机器人",
        "system": "你是一个严格遵循格式的 AI。每条回答必须精确输出三行：\n第一行：一句话总结\n第二行：详细解释\n第三行：一个类比或例子\n不要输出除此以外的任何内容。",
    },
]

print("=" * 60)
print("练习 1b：System Prompt 实验 (租赁合约)")
print(f"模型: {MODEL}")
print(f"User Message: \"{USER_MSG}\"")
print("=" * 60)

for s in SYSTEMS:
    print(f"\n{'─' * 60}")
    print(f"[System] {s['name']}")
    print(f"{'─' * 60}")

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": s["system"]},
                {"role": "user", "content": USER_MSG},
            ],
            max_tokens=600,
            temperature=0.7,
        )
        content = resp.choices[0].message.content
        print(f"[回复] ({len(content)} 字符)")
        print(content)
        print()
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
