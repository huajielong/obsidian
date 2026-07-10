---
date: 2026-07-10
tags:
  - deepseek
  - api
  - python
  - error-handling
  - retry
title: DeepSeek API 错误处理实战：认证失败、上下文溢出与指数退避重试
---

# DeepSeek API 错误处理实战

## 环境配置

- **模型**: `deepseek-v4-pro`
- **Base URL**: `https://api.deepseek.com`
- **Python SDK**: `openai` (OpenAI 兼容接口)
- **关键发现**: DeepSeek API 完全兼容 OpenAI SDK，但错误处理行为**与 OpenAI 有重要差异**

---

## 情景 1：API Key 错误

### 触发方式

使用无效的 API Key 发起请求：

```python
from openai import OpenAI

client = OpenAI(api_key="sk-fake-key-12345", base_url="https://api.deepseek.com")

try:
    resp = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[{"role": "user", "content": "你好"}],
    )
except Exception as e:
    print(type(e).__name__)       # AuthenticationError
    print(e.status_code)          # 401
    print(e.body)                 # {'message': '...', 'type': 'authentication_error', ...}
    print(e.code)                 # invalid_request_error
```

### 实验结果

```
AuthenticationError | HTTP 401
Body: {'message': 'Authentication Fails, Your api key: ****2345 is invalid',
       'type': 'authentication_error',
       'code': 'invalid_request_error'}
```

### 结论

| 属性 | 值 | 说明 |
|------|-----|------|
| 异常类型 | `openai.AuthenticationError` | 继承自 `openai.APIStatusError` |
| HTTP 状态码 | `401` | 可通过 `e.status_code` 获取 |
| 错误码 | `invalid_request_error` | 可通过 `e.code` 获取 |
| 是否可重试 | **否** | 属于 `FatalError`，应直接报错 |

错误分类决策：认证错误属于**不可恢复错误**，不应放入重试循环。

---

## 情景 2：Prompt 超长（Context Window）

### 触发方式

分别测试不同长度输入：

```python
# 测试 1：超长文本（300 万字符）
huge = "hello " * 500_000
resp = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": huge}],
    max_tokens=100,
)
# 完成原因: "length", 返回内容: 空字符串
```

### 实验结果

| Prompt 长度 | API 行为 | `finish_reason` | 内容 |
|-------------|----------|-----------------|------|
| 短（正常） | 正常返回 | `stop` | 完整回答 |
| 中（~10 万字符） | 返回部分 | `length` | 有截断的内容 |
| 大（300 万字符） | **静默处理** | `length` | **空字符串** |

### 关键发现

> **DeepSeek 不会抛出 `context_length_exceeded` 错误。** 当输入超出上下文窗口时，它选择**静默截断**并返回空内容，而不是像 OpenAI 那样抛异常拒绝请求。

这意味着：

1. 不能依赖 API 来告诉你输入太长
2. 需要在客户端做 prompt 长度预检
3. 需要对空响应做兜底处理

### 建议的预检实现

```python
def estimate_tokens(text: str) -> int:
    """粗略估算 token 数（中文 ~1.5 字符/token，英文 ~4 字符/token）"""
    import re
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    ascii_chars   = len(text) - chinese_chars
    return chinese_chars // 2 + ascii_chars // 4

def validate_prompt(messages: list, max_context: int = 128_000) -> bool:
    total = sum(estimate_tokens(m["content"]) for m in messages if "content" in m)
    if total > max_context:
        raise ValueError(
            f"Prompt 过长 ({total} tokens)，超出模型上下文窗口 ({max_context})"
        )
    return True
```

---

## 情景 3：Exponential Backoff Retry Wrapper

### 完整实现

```python
import time
import random
from typing import Optional, Callable


class RetryableError(Exception):
    """需要重试的可恢复错误"""
    pass


class FatalError(Exception):
    """不可恢复的错误，不需要重试"""
    pass


def classify_error(e: Exception) -> type[Exception]:
    """
    判断错误类型：可重试 vs 不可重试。

    可重试：网络超时 / 连接错误 / 429 限流 / 5xx
    不可重试：401 认证错误 / 400 参数错误 / 413 超长
    """
    status = getattr(e, "status_code", None) or getattr(e, "code", None)
    name = type(e).__name__

    if "APIConnectionError" in name:
        return RetryableError
    if "APITimeoutError" in name:
        return RetryableError
    if "RateLimitError" in name:
        return RetryableError
    if status == 429:
        return RetryableError
    if status in (502, 503, 504):
        return RetryableError
    if status in (400, 401, 403, 413):
        return FatalError

    return RetryableError  # 默认保守：可重试


def retry_with_exponential_backoff(
    func: Callable,
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
):
    """
    Exponential Backoff Retry Wrapper

    参数:
        func: 要重试的零参数函数
        max_retries: 最大重试次数
        base_delay: 初始等待秒数
        max_delay: 最大等待秒数
        jitter: 是否加随机抖动（防止惊群效应）
    """
    attempt = 0

    while attempt <= max_retries:
        try:
            result = func()
            if attempt > 0:
                print(f"[OK] 第 {attempt} 次重试成功!")
            return result

        except Exception as e:
            if classify_error(e) == FatalError:
                raise  # 不可恢复，直接抛出

            attempt += 1
            if attempt > max_retries:
                raise  # 重试用完，抛出最后一次异常

            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            if jitter:
                delay *= 0.5 + random.random() * 0.5  # ±50% 随机抖动

            print(
                f"[RETRY] 第 {attempt}/{max_retries} 次，"
                f"等待 {delay:.1f}s... (原因: {type(e).__name__})"
            )
            time.sleep(delay)
```

### 运行结果演示

模拟的前 2 次网络超时，第 3 次成功：

```
[RETRY] 第 1/5 次，等待 0.3s... (ReadTimeout)
[RETRY] 第 2/5 次，等待 0.8s... (ReadTimeout)
[OK] 第 2 次重试成功! → "3的平方是9。"
```

### 退避策略详解

| 重试次数 | 基础延迟 | 带抖动（±50%） |
|----------|----------|---------------|
| 1 | 0.5s | 0.25s ~ 0.75s |
| 2 | 1.0s | 0.50s ~ 1.50s |
| 3 | 2.0s | 1.00s ~ 3.00s |
| 4 | 4.0s | 2.00s ~ 6.00s |
| 5 | 8.0s | 4.00s ~ 12.00s |

抖动（jitter）的作用：当多个客户端同时失败并重试时，防止它们在同一时刻集中重试造成"惊群效应"。

### 错误分类决策树

```
API 调用异常
├── APIConnectionError / APITimeoutError / ReadTimeout
│   └── 可重试（网络问题通常是临时性的）
├── HTTP 429 Too Many Requests
│   └── 可重试（限流，等配额恢复）
├── HTTP 5xx (502/503/504)
│   └── 可重试（服务端临时故障）
├── HTTP 401 Authentication Error
│   └── 不可重试（API Key 错了，重试多少次都一样）
├── HTTP 400 Bad Request
│   └── 不可重试（请求参数错了，改代码才能解决）
├── HTTP 413 Payload Too Large
│   └── 不可重试（输入太大了，需要截断再重试）
└── 其他未知错误
    └── 保守策略：暂时按可重试处理
```

---

## 完整练习脚本

脚本文件：`error_handling_practice.py`

```python
# -*- coding: utf-8 -*-
"""
DeepSeek API 错误处理练习
情景1: API Key 错误 -> 认证异常捕获
情景2: Prompt 超长 -> Context Window 溢出
情景3: 网络断开 -> Exponential Backoff Retry Wrapper
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os
import time
import random
from openai import OpenAI
from typing import Optional

# 配置
os.environ["DEEPSEEK_API_KEY"] = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-pro"

client_ok = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url=BASE_URL)
client_bad = OpenAI(api_key="sk-fake-key-12345", base_url=BASE_URL)


def scenario_wrong_api_key():
    print("\n[情景 1] 使用错误的 API Key 调用")
    try:
        resp = client_bad.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "你好"}],
            max_tokens=100,
        )
    except Exception as e:
        print(f"[ERROR] 类型: {type(e).__name__}")
        print(f"       Status: {getattr(e, 'status_code', 'N/A')}")
        print(f"       Body: {getattr(e, 'body', 'N/A')}")
        print(f"       Code: {getattr(e, 'code', 'N/A')}")


def scenario_context_window_overflow():
    print("\n[情景 2] 超长 Prompt")
    huge = "hello " * 500_000
    print(f"   生成长度: {len(huge)} 字符")
    try:
        resp = client_ok.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": huge}],
            max_tokens=100, timeout=30,
        )
        print(f"   finish_reason: {resp.choices[0].finish_reason}")
        print(f"   内容长度: {len(resp.choices[0].message.content or '')}")
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")


class RetryableError(Exception): pass
class FatalError(Exception): pass


def classify_error(e):
    status = getattr(e, "status_code", None) or getattr(e, "code", None)
    name = type(e).__name__
    if "APIConnectionError" in name or "APITimeoutError" in name or "RateLimitError" in name:
        return RetryableError
    if status == 429 or status in (502, 503, 504):
        return RetryableError
    if status in (400, 401, 403, 413):
        return FatalError
    return RetryableError


def retry_with_exponential_backoff(func, max_retries=5, base_delay=1.0,
                                   max_delay=60.0, jitter=True):
    attempt = 0
    while attempt <= max_retries:
        try:
            result = func()
            if attempt > 0:
                print(f"  [OK] 第 {attempt} 次重试成功!")
            return result
        except Exception as e:
            if classify_error(e) == FatalError:
                raise
            attempt += 1
            if attempt > max_retries:
                raise
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            if jitter:
                delay *= 0.5 + random.random() * 0.5
            print(f"  [RETRY] 第 {attempt}/{max_retries} 次，等待 {delay:.1f}s... "
                  f"(原因: {type(e).__name__})")
            time.sleep(delay)


def simulate_flaky_call():
    if not hasattr(simulate_flaky_call, "call_count"):
        simulate_flaky_call.call_count = 0
    simulate_flaky_call.call_count += 1
    n = simulate_flaky_call.call_count
    if n <= 2:
        import httpx
        raise httpx.ReadTimeout(f"模拟网络超时 (第 {n} 次)")
    return client_ok.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"用一句话回答：{n} 的平方是多少？"}],
        max_tokens=200,
    )


def scenario_network_retry():
    print("\n[情景 3] 网络断开 -> Exponential Backoff Retry")
    simulate_flaky_call.call_count = 0
    try:
        resp = retry_with_exponential_backoff(
            simulate_flaky_call, max_retries=5, base_delay=0.5, max_delay=10)
        print(f"  [OK] 最终响应: {resp.choices[0].message.content}")
    except Exception as e:
        print(f"  [FAIL] {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("DeepSeek API 错误处理练习")
    scenario_wrong_api_key()
    scenario_context_window_overflow()
    scenario_network_retry()
```

---

## 总结

| 错误类型 | DeepSeek 行为 | 处理策略 |
|----------|--------------|---------|
| 无效 API Key | 抛出 `AuthenticationError` (401) | 捕获后提示用户检查 key，不重试 |
| 输入超长 | **不抛异常**，返回空内容 | 客户端预检 token 数；对空响应兜底 |
| 网络超时 | 抛出 `ReadTimeout`/`APITimeoutError` | 指数退避重试（最多 3~5 次） |
| 限流 (429) | 抛出 `RateLimitError` | 指数退避重试 |
| 服务端 5xx | 抛出 `APIStatusError` | 指数退避重试 |

> **教训**: 永远不要假设 API 会帮你发现所有问题。客户端要做好预检、分类重试和兜底。
