---
title: "MLflow"
type: entity
tags: [MLOps, 实验追踪, 模型注册, 模型部署, 开源]
sources:
  - raw/01-articles/算法应用开发工程师-JD.txt
last_updated: 2026-07-16
---

# MLflow

## 概述

**MLflow** 是 Databricks 开源的**机器学习生命周期管理平台**（2018 年开源），致力于解决 ML 项目中的实验跟踪、复现、部署和模型管理的碎片化问题。它提供了一套**轻量级、框架无关**的 API 和 UI，是目前社区最广泛采用的开源 MLOps 工具之一，GitHub ★ 20k+。

## 四大核心组件

### 1. MLflow Tracking — 实验与参数记录

记录每次运行的参数、指标、代码版本和产出物：

```python
import mlflow

# 设置实验
mlflow.set_experiment("lora-fine-tuning")

with mlflow.start_run(run_name="lora-r8-lr2e4"):
    # 记录参数
    mlflow.log_param("model", "Llama-3.2-8B")
    mlflow.log_param("lora_r", 8)
    mlflow.log_param("learning_rate", 2e-4)

    for epoch in range(epochs):
        loss = train_one_epoch()
        # 记录指标
        mlflow.log_metric("loss", loss, step=epoch)

    # 记录模型文件
    mlflow.pytorch.log_model(model, "model")
    # 自动保存 conda 环境
    mlflow.log_artifact("requirements.txt")
```

查看结果：`mlflow ui` → 浏览器打开 `http://localhost:5000`

**核心能力**：
- 自动记录 Git commit、源代码版本、运行环境
- 支持任意框架（PyTorch / TensorFlow / sklearn / XGBoost）
- 支持嵌套运行（parent-child runs）
- REST API 从任何语言记录

### 2. MLflow Models — 模型打包标准

MLflow 定义了一套**统一模型格式**（MLflow Model），将模型权重 + 环境依赖 + 推理代码打包成一个标准化的目录结构：

```
my_model/
├── MLmodel              ← 模型元数据（框架、签名、环境）
├── conda.yaml           ← Conda 环境
├── requirements.txt     ← pip 依赖（自动生成）
├── model.pkl / .pt      ← 序列化模型权重
└── python_env.yaml      ← Python 环境描述
```

```python
# 日志
mlflow.pytorch.log_model(model, "model", registered_model_name="llama-lora")

# 加载（无需微调框架，仅需推理环境）
model = mlflow.pyfunc.load_model("runs:/<run_id>/model")
```

**Flavor（框架适配器）**：MLflow 为每种主流框架定义了 Flavor（`mlflow.pytorch`、`mlflow.sklearn`、`mlflow.transformers` 等），自动处理模型的保存/加载格式。

### 3. MLflow Model Registry — 模型全生命周期管理

注册和版本化管理模型，控制 Stage 晋级：

| Stage | 含义 | 典型条件 |
|-------|------|---------|
| **None** | 刚提交的实验模型 | 训练完毕，未验证 |
| **Staging** | 验证中 | 通过离线评估 |
| **Production** | 生产运行 | 通过 A/B 测试 / 线上评测 |
| **Archived** | 已下线 | 被新版本替代 |

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# 注册模型版本
client.create_registered_model("llama-lora-agent")
client.create_model_version(
    name="llama-lora-agent",
    source="runs:/<run_id>/model",
    run_id="<run_id>",
)

# Stage 晋级
client.transition_model_version_stage(
    name="llama-lora-agent",
    version=3,
    stage="Production"
)
```

### 4. MLflow Deployments — 模型部署（MLflow Serving）

将模型从 Registry 直接部署为 REST API：

```bash
# 启动本地推理服务
mlflow models serve -m "models:/llama-lora-agent/Production" --port 8080

# Docker 部署
mlflow models build-docker -m "models:/llama-lora-agent/Production" -n "llama-serving"
docker run -p 8080:8080 llama-serving

# 请求示例
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"inputs": ["你好，请分析这份报告"]}'
```

## MLflow 生态定位

```
MLflow 完整的 ML 生命周期管理：
┌─────────────────────────────────────────────────────┐
│  MLflow Tracking     ← 开发阶段：实验记录             │
│  MLflow Projects     ← 可复现打包（代码+环境+配置）    │
│  MLflow Models       ← 统一模型格式规范               │
│  MLflow Registry     ← 模型版本/Stage 管理            │
│  MLflow Deployments  ← 生产部署（Serving/Docker/K8s） │
└─────────────────────────────────────────────────────┘
```

## 竞品对比

| 维度 | **MLflow** | **W&B** | **Kubeflow** |
|------|-----------|---------|--------------|
| **定位** | 轻量级 ML 生命周期管理 | 实验追踪 + 生产监控 | K8s 原生 ML 编排平台 |
| **开源程度** | ✅ 完全开源 | ⚠️ SDK 开源，平台 SaaS | ✅ 完全开源 |
| **部署方式** | ☁️ 自托管（简单） | ☁️ 云 SaaS + 自托管 | ☁️ 自托管（需要 K8s） |
| **实验追踪** | ⭐⭐ 基础功能 | ⭐⭐⭐ 最强 | ⭐ 需集成 |
| **超参搜索** | ⭐ 需集成 Optuna/ Hyperopt | ⭐⭐⭐ Sweeps | ⭐ 需集成 Katib |
| **模型注册** | ⭐⭐⭐ Model Registry 最成熟 | ⭐⭐ Artifacts | ⭐⭐ 中等 |
| **部署** | ⭐⭐⭐ Serving + Docker + K8s 直接部署 | ⭐ 依赖外部 | ⭐⭐⭐ K8s 原生 |
| **LLM 追踪** | ⭐ 嵌入式 | ⭐⭐⭐ Prompts + Weave | ⭐ 需集成 |
| **学习成本** | 低（2-3 天上手） | 中（功能多） | 高（K8s 门槛） |

## 与 LLM 微调工作流的集成

```python
# 在 LLM 微调脚本中使用 mlflow + transformers
from transformers import Trainer, TrainingArguments
import mlflow

training_args = TrainingArguments(
    output_dir="./results",
    report_to="mlflow",          # 🔥 Transformers 原生支持
    run_name="lora-llama-v2",
    logging_steps=10,
    save_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)
trainer.train()

# 训练完成后自动保存为 MLflow 格式
mlflow.transformers.log_model(
    transformers_model={"model": model, "tokenizer": tokenizer},
    artifact_path="lora-model",
    registered_model_name="llama-lora-domain-v2",
)
```

## 最佳实践

1. **实验命名规范**：`{model}-{lora_r}-{lr}-{dataset_id}`（如 `llama-lora-r8-2e4-qa-v3`）
2. **Tag 系统**：用 MLflow Tags 标记模型元数据（`wandb.run.id`, `git.sha`, `dataset.version`），方便跨工具检索
3. **嵌套 Runs**：用 Parent/Child Runs 组织实验——Parent=完整训练，Child=每次 Eval
4. **MLflow + W&B 同时使用**：MLflow 负责模型注册与部署，W&B 负责实验可视化和协作

## 相关信息

- **创建者**: Databricks（Matei Zaharia 团队）
- **开源时间**: 2018
- **开源协议**: Apache 2.0
- **当前版本**: v2.19.x（2026）
- **语言**: Python（主） + R / Java / REST API
- **官网**: https://mlflow.org
- **GitHub**: https://github.com/mlflow/mlflow

## 关联连接

- [[Weights_and_Biases]] — MLOps 领域的主要竞品与互补工具（MLflow 偏模型注册与部署，W&B 偏实验追踪）
- [[Ray]] — MLflow 可与 Ray 配合进行分布式训练追踪
- [[Eval_Harness]] — MLflow Registry 的 Stage 晋级与 Eval Harness 评估流程可对接
- [[Agent_Observability]] — MLflow 不直接提供 Agent 可观测性，但可通过自开发集成
- [[AI训练推理系统工程]] — MLflow 可用于管理训练产出的模型权重的版本与部署
- [[摘要-算法应用开发工程师-jd]] — 来源 JD 将 MLflow 列为 MLOps 加分项工具之一
