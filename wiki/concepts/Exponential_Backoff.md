---
title: "Exponential_Backoff"
type: concept
tags: [重试, 错误处理, 可靠性, 系统设计]
sources: [raw/01-articles/DeepSeek-API-错误处理实战.md]
last_updated: 2026-07-10
---

## 定义

指数退避（Exponential Backoff）是一种**在网络请求失败时逐次增加重试等待时间的重试策略**。每次重试的等待时间按指数增长（如 1s → 2s → 4s → 8s），有效减轻重试对下游服务的压力，是分布式系统中提升可靠性的标准模式。

## 关键信息

### 退避策略详解

| 重试次数 | 基础延迟 | 带抖动（±50%） |
|:--------|:--------|:-------------|
| 1 | 0.5s | 0.25s ~ 0.75s |
| 2 | 1.0s | 0.50s ~ 1.50s |
| 3 | 2.0s | 1.00s ~ 3.00s |
| 4 | 4.0s | 2.00s ~ 6.00s |
| 5 | 8.0s | 4.00s ~ 12.00s |

### 抖动的意义

抖动（Jitter）为每次等待时间添加随机偏移（通常 ±50%），防止多个客户端同时失败并同时重试时造成的"惊群效应"（Thundering Herd Problem）。

### 核心参数

| 参数 | 说明 | 推荐值 |
|:----|:-----|:------|
| `max_retries` | 最大重试次数 | 3~5 |
| `base_delay` | 初始等待时间 | 0.5~1.0s |
| `max_delay` | 最长等待时间上限 | 30~60s |
| `jitter` | 是否启用随机抖动 | True（生产环境必开） |

### 错误分类决策树

```
API 调用异常
├── 可重试（网络问题通常是临时性的）
│   ├── APIConnectionError / APITimeoutError / ReadTimeout
│   ├── HTTP 429 Too Many Requests（限流）
│   └── HTTP 5xx (502/503/504)（服务端临时故障）
├── 不可重试（改代码或配置才能解决）
│   ├── HTTP 401 Authentication Error
│   ├── HTTP 400 Bad Request
│   └── HTTP 413 Payload Too Large
└── 其他未知错误 → 保守策略：按可重试处理
```

## 关联连接

- [[Agent_Loop]] — Agent Loop 中的瞬态错误处理包含指数退避重试
- [[DeepSeek]] — API 错误处理中实现了指数退避策略
- [[Harness_Engineering]] — 重试机制是 Harness Engineering 的核心反馈循环之一
- [[摘要-deepseek-api-error-handling]] — 指数退避的完整 Python 实现来源
