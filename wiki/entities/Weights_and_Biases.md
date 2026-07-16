---
title: "Weights_and_Biases"
type: entity
tags: [MLOps, 实验追踪, 模型监控, 可视化, W&B]
sources:
  - raw/01-articles/算法应用开发工程师-JD.txt
last_updated: 2026-07-16
---

# Weights & Biases（W&B）

## 概述

**Weights & Biases（简称 W&B 或 wandb）** 是 AI/ML 领域最广泛使用的**实验追踪与模型监控平台**（2017 年创立，总部旧金山）。它提供从实验跟踪、超参数调优、模型注册到生产监控的端到端 MLOps 平台，被 OpenAI、DeepMind、NVIDIA、Meta、Anthropic 等行业领军者采用，GitHub ★ 10k+，社区用户超过 150 万。

## 核心功能

### 1. 实验追踪（Experiment Tracking）— 核心产品

自动记录每次训练的完整上下文：

```python
import wandb

# 初始化一次实验
wandb.init(
    project="llm-fine-tuning",
    config={
        "model": "Llama-3.2-8B",
        "learning_rate": 2e-4,
        "batch_size": 4,
        "lora_r": 8,
        "lora_alpha": 16,
        "dataset": "domain_qa_v3",
    }
)

# 训练循环中自动梯度记录
for epoch in range(10):
    for batch in dataloader:
        loss = train_step(batch)
        # 自动记录 loss / lr / 梯度 / 梯度范数
        wandb.log({"loss": loss, "epoch": epoch})
```

自动捕获的内容：
- **系统指标**：GPU 利用率、显存、温度、网络 I/O
- **训练指标**：loss / accuracy / gradient norm / learning rate
- **代码与 Git**：自动关联当前 Git commit / diff / 依赖环境
- **模型文件**：自动保存 Checkpoint / 权重文件 / ONNX 导出（Artifacts）

### 2. 超参数调优（Sweeps）

分布式超参数搜索，自动调度 GPU：

```python
sweep_config = {
    "method": "bayes",  # grid / random / bayes
    "metric": {"name": "val_loss", "goal": "minimize"},
    "parameters": {
        "learning_rate": {"min": 1e-5, "max": 5e-4},
        "lora_r": {"values": [8, 16, 32]},
        "lora_dropout": {"min": 0.0, "max": 0.2},
    }
}

sweep_id = wandb.sweep(sweep_config, project="lora-sweep")
wandb.agent(sweep_id, train_function, count=20)
```

### 3. 模型注册与 Artifacts

版本化管理数据集、模型、环境：

| 功能 | 说明 | 典型用法 |
|------|------|---------|
| **Artifacts** | 数据/模型版本控制（类似 Git for ML） | `wandb.log_artifact("model.pt", type="model")` |
| **Model Registry** | 模型全生命周期管理 | 从开发→Staging→Production 晋级 |
| **Dataset Versioning** | 数据集版本追踪与血缘关系 | `wandb.use_artifact("dataset:v3")` |

### 4. 生产监控（W&B Prompts / Weave）

| 产品 | 用途 | 监控内容 |
|------|------|---------|
| **W&B Prompts** | LLM Token 级别追踪与调试 | Token 流、延迟、成本、模型调用链 |
| **W&B Weave** | Agent 全链路可观测性（2025 推出） | Agent Loop 每一步、Tool 调用、LLM 响应、总成本 |
| **W&B Models** | 模型推理监控 | Latency / Throughput / Token 消耗 / 错误率 |

### 5. LLM 评估（W&B Evaluate）

大模型特定评估功能：LLM-as-judge、Pairwise 对比、Perturbation Testing。

### 6. Launch — 训练任务编排

将 GPU 训练任务编排到 Kubernetes / Slurm / SageMaker / Lambda Labs：

```yaml
# wandb launch 配置文件
job:
  image: "python:3.11"
  entry_point: "train.py"
  resource: "kubernetes"
  resource_args:
    gpu: 1
    gpu_type: "A100-80GB"
  env:
    WANDB_PROJECT: "llm-fine-tuning"
```

## W&B 生态定位

```
                          开发实验室
                             │
                ┌────────────┴────────────┐
                │       W&B Weave         │ ← Agent 全链路追踪
                │    W&B Prompts          │ ← LLM Token 监控
                │    W&B Experiments      │ ← 训练实验追踪
                │    W&B Sweeps           │ ← 超参数搜索
                │    W&B Model Registry   │ ← 模型版本管理
                │    W&B Artifacts        │ ← 数据/模型版本控制
                └────────────┬────────────┘
                             │
                ┌────────────┴────────────┐
                │   推理引擎                │ ← vLLM / TGI / TensorRT-LLM
                │   训练框架                │ ← PyTorch / Transformers
                │   基础设施                │ ← Docker / K8s / Slurm
                └─────────────────────────┘
```

## 竞品对比

| 维度 | **W&B** | **MLflow** | **Neptune.ai** | **Comet.ml** |
|------|---------|------------|----------------|-------------|
| **定位** | 全栈 MLOps 平台 | 开源 ML 生命周期管理 | AI 元数据平台 | 实验管理平台 |
| **开源** | SDK 开源，平台 SaaS | ✅ 完全开源 | SDK 开源，平台 SaaS | ⚠️ 社区版有限制 |
| **实验追踪** | ⭐⭐⭐ 最强，自动梯度/系统记录 | ⭐⭐ 需手动 log | ⭐⭐⭐ 强 | ⭐⭐ 中等 |
| **LLM 支持** | ⭐⭐⭐ W&B Prompts + Weave | ⭐ LLM 追踪较弱 | ⭐⭐ 有 LLM 模块 | ⭐ 基本 |
| **超参搜索** | ⭐⭐⭐ Sweeps（Bayes/Grid/Random） | ⭐⭐ 需集成 Optuna | ⭐⭐ 中等 | ⭐⭐ 中等 |
| **模型注册** | ⭐⭐⭐ Artifacts + Registry | ⭐⭐⭐ Model Registry | ⭐⭐ 中等 | ⭐⭐ 中等 |
| **生产监控** | ⭐⭐⭐ 强（Weave） | ⭐ 需额外搭建 | ⭐⭐ 中等 | ⭐ 弱 |
| **部署方式** | 云 SaaS + 自托管 | 完全自托管 | 云 SaaS + 自托管 | 云 SaaS 为主 |

## 2026 典型用法

```bash
# 1. 安装
pip install wandb

# 2. 登录（免费注册 https://wandb.ai）
wandb login

# 3. 启用 Weave Agent 追踪
import wandb
wandb.require("core")
wandb.init(project="agent-app")

# 装饰器自动追踪 Agent 函数
@wandb.trace()
def my_agent_step(query: str) -> str:
    ...
```

## 相关信息

- **创立时间**: 2017
- **总部**: 旧金山
- **创始人**: Lukas Biewald, Chris Van Pelt, Shawn Lewis
- **开源协议**: MIT（SDK）/ Proprietary（平台）
- **官网**: https://wandb.ai
- **GitHub**: https://github.com/wandb/wandb

## 关联连接

- [[MLflow]] — W&B 在 MLOps 领域的主要开源竞品，定位互补（SaaS vs 自托管）
- [[Ray]] — W&B Launch 可编排 Ray 训练任务；Ray Train 可直接集成 wandb 回调
- [[Agent_Observability]] — W&B Weave 提供了 Agent 全链路可观测性
- [[Eval_Harness]] — W&B Evaluate 提供了 LLM 评估能力，与 Eval Harness 互补
- [[Cost_Optimization]] — W&B 的 Token/Cost 追踪可直接服务于成本优化分析
- [[摘要-算法应用开发工程师-jd]] — 来源 JD 将 W&B 列为 MLOps 加分项工具之一
