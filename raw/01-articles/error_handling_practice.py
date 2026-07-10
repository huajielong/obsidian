# -*- coding: utf-8 -*-
"""
DeepSeek API 错误处理练习
情景1: API Key 错误 -> 认证异常捕获
情景2: Prompt 超长 -> Context Window 溢出
情景3: 网络断开 -> Exponential Backoff Retry Wrapper
"""

import sys
import io

# 强制 stdout 使用 utf-8，避免 Windows GBK 乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os
import time
import random
from openai import OpenAI
from typing import Optional

# ============================================================
# 配置
# ============================================================
os.environ["DEEPSEEK_API_KEY"] = "sk-92517a9c52f84be3a4d4ee7e87bdb5cc"
REAL_KEY = "sk-92517a9c52f84be3a4d4ee7e87bdb5cc"
WRONG_KEY = "sk-fake-key-12345"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-pro"  # 修正为正确的模型名

client_ok = OpenAI(api_key=REAL_KEY, base_url=BASE_URL)
client_bad = OpenAI(api_key=WRONG_KEY, base_url=BASE_URL)


# ============================================================
# 情景 1：API Key 错误 -> 看怎么 raise
# ============================================================
def scenario_wrong_api_key():
    print("\n" + "=" * 60)
    print("[情景 1] 使用错误的 API Key 调用")
    print("=" * 60)

    try:
        resp = client_bad.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "你好"}],
            max_tokens=100,
        )
        print("[OK] 居然成功了？", resp)
    except Exception as e:
        print(f"[ERROR] 捕获到异常:")
        print(f"         类型: {type(e).__name__}")
        print(f"         信息: {e}")

        # 解剖异常对象
        if hasattr(e, "status_code"):
            print(f"         HTTP Status: {e.status_code}")
        if hasattr(e, "body"):
            print(f"         Body: {e.body}")
        if hasattr(e, "code"):
            print(f"         Code: {e.code}")


# ============================================================
# 情景 2：Prompt 超长 -> Context Window 溢出
# ============================================================
def scenario_context_window_overflow():
    print("\n" + "=" * 60)
    print("[情景 2] 超长 Prompt 触发 Context Window 溢出")
    print("=" * 60)

    # 制造一个超长文本
    print("   正在生成超长文本...")
    LONG_TEXT = "hello " * 500_000
    print(f"   生成长度: {len(LONG_TEXT)} 字符")

    try:
        resp = client_ok.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一个助手"},
                {"role": "user", "content": LONG_TEXT},
            ],
            max_tokens=100,
            timeout=30,
        )
        content = resp.choices[0].message.content
        print(f"[OK] 返回了内容 (长度={len(content) if content else 0}): {content[:100] if content else '(空)'}")
    except Exception as e:
        print(f"[ERROR] 捕获到异常:")
        print(f"         类型: {type(e).__name__}")
        print(f"         信息: {e}")

        if hasattr(e, "status_code"):
            print(f"         HTTP Status: {e.status_code}")
        if hasattr(e, "code"):
            print(f"         Code: {e.code}")
        if hasattr(e, "type"):
            print(f"         Type: {e.type}")


# ============================================================
# 情景 3：Exponential Backoff Retry Wrapper
# ============================================================

class RetryableError(Exception):
    """需要重试的可恢复错误"""
    pass


class FatalError(Exception):
    """不可恢复的错误，不需要重试"""
    pass


def classify_error(e: Exception) -> type[Exception]:
    """
    判断错误类型：可重试 vs 不可重试。
    - 网络超时 / 连接错误 / 429 限流 / 5xx -> 可重试
    - 401 认证错误 / 400 参数错误 / 413 超长 -> 不可重试
    """
    status = getattr(e, "status_code", None) or getattr(e, "code", None)

    # OpenAI SDK 特定异常类型
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
    func,
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
) -> Optional[str]:
    """
    Exponential Backoff Retry Wrapper

    参数:
        func: 要重试的零参数函数
        max_retries: 最大重试次数
        base_delay: 初始等待秒数
        max_delay: 最大等待秒数
        jitter: 是否加随机抖动
    返回:
        API 响应，或抛出异常
    """
    attempt = 0

    while attempt <= max_retries:
        try:
            result = func()
            if attempt > 0:
                print(f"  [OK] 第 {attempt} 次重试成功!")
            return result

        except Exception as e:
            error_class = classify_error(e)

            if error_class == FatalError:
                print(f"  [STOP] 不可恢复错误，放弃重试: {type(e).__name__}: {e}")
                raise

            attempt += 1
            if attempt > max_retries:
                print(f"  [FAIL] 已达最大重试次数 ({max_retries})，放弃")
                raise

            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            if jitter:
                delay = delay * (0.5 + random.random() * 0.5)

            print(f"  [RETRY] 第 {attempt}/{max_retries} 次，等待 {delay:.1f}s... "
                  f"(原因: {type(e).__name__})")
            time.sleep(delay)

    return None


# ============================================================
# 模拟网络闪断
# ============================================================
def make_flaky_api_call():
    """模拟一个间歇性网络故障（前 2 次失败，第 3 次成功）"""
    if not hasattr(make_flaky_api_call, "call_count"):
        make_flaky_api_call.call_count = 0
    make_flaky_api_call.call_count += 1

    n = make_flaky_api_call.call_count

    if n <= 2:
        import httpx
        raise httpx.ReadTimeout(f"模拟网络超时 (第 {n} 次调用)")

    return client_ok.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"用一句话回答：{n} 的平方是多少？"}],
        max_tokens=200,
    )


def scenario_network_retry():
    print("\n" + "=" * 60)
    print("[情景 3] 网络断开 -> Exponential Backoff Retry")
    print("=" * 60)

    make_flaky_api_call.call_count = 0

    try:
        resp = retry_with_exponential_backoff(
            make_flaky_api_call,
            max_retries=5,
            base_delay=0.5,
            max_delay=10,
            jitter=True,
        )
        print(f"  [OK] 最终响应: {resp.choices[0].message.content}")

    except Exception as e:
        print(f"  [FAIL] 最终失败: {type(e).__name__}: {e}")


# ============================================================
# 真实 API 调用（走 retry wrapper）
# ============================================================
def demo_real_api_call_with_retry():
    print("\n" + "=" * 60)
    print("[附加] 真实 API 调用 + Retry Wrapper")
    print("=" * 60)

    def real_api_call():
        return client_ok.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "用一句中文回答：1+1=？"}],
            max_tokens=200,
            timeout=30,
        )

    try:
        resp = retry_with_exponential_backoff(
            real_api_call,
            max_retries=3,
            base_delay=1.0,
            max_delay=10,
        )
        content = resp.choices[0].message.content
        print(f"  [OK] 真实调用成功: {content}")
    except Exception as e:
        print(f"  [FAIL] 真实调用失败: {type(e).__name__}: {e}")


# ============================================================
# 主入口
# ============================================================
if __name__ == "__main__":
    print("[开始] DeepSeek API 错误处理练习")
    print(f"模型: {MODEL}, Base URL: {BASE_URL}")

    # 情景 1
    scenario_wrong_api_key()

    # 情景 2
    scenario_context_window_overflow()

    # 情景 3
    scenario_network_retry()

    # 附加
    demo_real_api_call_with_retry()

    print("\n" + "=" * 60)
    print("[结束] 练习结束")
