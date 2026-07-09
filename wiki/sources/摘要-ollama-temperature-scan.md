---
title: "摘要-ollama-temperature-scan"
type: source
tags: [来源, ollama, temperature, 温度参数]
sources: [raw/01-articles/02-温度参数扫描与取值范围.md]
last_updated: 2026-07-09
---

## 核心摘要

实验二：对同一 Prompt 从 temperature=0.0 到 1.5 扫描 8 档温度，每档重复 5 次。发现温度=0 时输出完全确定（5/5 相同）；仅 0.1 即开始出现多样性（2/5）；0.3+ 完全多样；1.5 时英文单词开始混入中文语境。温度越高，模型对输出长度的控制力越弱。

## 关联连接
- [[Ollama]] — 实验平台
- [[Llama]] — 实验模型
- [[Temperature_Parameter]] — 温度参数的核心实验数据
