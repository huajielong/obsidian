---
title: "Ray"
type: entity
tags: [分布式计算, 分布式训练, RL训练, 任务编排, GPU集群]
sources:
  - raw/01-articles/算法应用开发工程师-JD.txt
last_updated: 2026-07-16
---

# Ray

## 概述

**Ray** 是 UC Berkeley RISELab 开源的**统一分布式计算框架**（2017 年），定位为 AI/ML 领域的"分布式操作系统"。它提供从**单机多线程到多集群 GPU 训练**的弹性扩展能力，核心创新在于**将分布式系统的复杂性封装到底层运行时**，让开发者以近乎单机代码的体验编写分布式程序。

Ray 已被 OpenAI、Anthropic、DeepMind、Uber、LinkedIn 等采用，GitHub ★ 36k+，ML/AI 分布式计算的头号通用框架。

## 核心理念

```
传统分布式系统：      你必须自己管理节点、通信、容错、调度
Ray 分布式系统：      Ray 管理一切，你只写业务逻辑
                    ↓
@ray.remote          ← 加个装饰器就变成分布式函数
```

## 核心组件

### 1. Ray Core — 分布式计算基础

只需加 `@ray.remote` 装饰器即可将任意 Python 函数/类变为远程任务：

```python
import ray

ray.init()  # 启动 Ray 运行时

# 远程函数
@ray.remote
def train_model(config):
    # 这个函数会自动被调度到集群上的一台机器执行
    return run_training(config)

# 远程类（Actor — 有状态远程对象）
@ray.remote(num_gpus=1)
class InferenceWorker:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def predict(self, input_data):
        return self.model.generate(input_data)

# 并发执行（自动调度）
futures = [train_model.remote(cfg) for cfg in configs]
results = ray.get(futures)  # 阻塞等待所有结果
```

核心抽象：

| 抽象 | 等价单机概念 | 说明 |
|------|-------------|------|
| `@ray.remote` 函数 | 普通函数 | 远程无状态任务 |
| `@ray.remote` class（Actor） | 类实例 | 远程有状态对象（管理 GPU 显存等状态） |
| `ray.get()` | `await future` | 获取远程结果 |
| `ray.put()` | 堆内存 | 将大对象存入共享内存 |
| ObjectRef | 指针 | 分布式引用，跨节点共享 |

### 2. Ray AI Runtime (AIR) — AI 专用库集合

Ray 将核心能力封装为面向 AI 场景的专用库：

```
Ray 生态：
├── Ray Core           ← 分布式运行时基础
├── Ray Train          ← 分布式训练（PyTorch/TF 一键分布化）
├── Ray Tune           ← 超参数调优
├── Ray Serve          ← 模型推理服务
├── Ray Data           ← 分布式数据处理
├── Ray RLlib          ← 强化学习训练框架
└── Ray Cluster        ← 集群管理与自动扩缩容
```

#### Ray Train — 分布式训练

```python
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

def train_func(config):
    # 这个函数在每张 GPU 上执行
    model = create_model()
    for epoch in range(10):
        loss = train_epoch(model)
        report(metrics={"loss": loss})

trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(
        num_workers=8,       # 8 张 GPU
        use_gpu=True,
        resources_per_worker={"GPU": 1}
    ),
)
result = trainer.fit()
```

#### Ray Serve — 模型推理服务

```python
from ray import serve
from starlette.requests import Request

@serve.deployment(
    num_replicas=3,
    ray_actor_options={"num_gpus": 1}
)
class LLMServing:
    def __init__(self):
        from transformers import AutoModelForCausalLM
        self.model = AutoModelForCausalLM.from_pretrained("llama-8b")

    async def __call__(self, request: Request):
        prompt = await request.json()
        output = self.model.generate(**prompt)
        return {"response": output.tolist()}

serve.run(LLMServing.bind())
```

#### Ray RLlib — 强化学习训练

```python
from ray.rllib.algorithms.ppo import PPOConfig

config = (
    PPOConfig()
    .environment("CartPole-v1")
    .training(lr=0.0003, train_batch_size=4000)
    .resources(num_gpus=1, num_gpus_per_worker=0)
)
algo = config.build()
for i in range(100):
    result = algo.train()
    print(f"Iter {i}: reward={result['episode_reward_mean']}")
```

#### Ray Data — 分布式数据处理

```python
import ray

# 读取海量数据（自动分区到集群节点）
ds = ray.data.read_parquet("s3://my-data-bucket/")

# 分布式转换
ds = ds.map_batches(
    lambda batch: [transform(doc) for doc in batch],
    batch_size=1000,
    num_gpus=0,
)

# 流式写入
ds.write_parquet("s3://processed-output/")
```

### 3. Ray Cluster — 弹性集群

Ray 支持从单机到大规模 Kubernetes 集群的无缝扩展：

```yaml
# K8s 上部署 Ray 集群的典型 YAML
apiVersion: ray.io/v1
kind: RayCluster
metadata:
  name: ray-gpu-cluster
spec:
  headGroupSpec:
    serviceType: ClusterIP
    template:
      spec:
        containers:
          - image: rayproject/ray:2.38-gpu
            resources:
              limits: { cpu: 8, memory: "32G" }
  workerGroupSpecs:
    - groupName: gpu-workers
      replicas: 16
      template:
        spec:
          containers:
            - image: rayproject/ray:2.38-gpu
              resources:
                limits: { cpu: 16, memory: "64G", nvidia.com/gpu: 4 }
```

关键特性：
- **自动扩缩容**：基于负载自动增加/减少 Worker 节点
- **动态资源调度**：不同任务可以请求不同资源（CPU/GPU/内存/自定义资源）
- **容错**：Worker 失败自动重启，Object Store 根据引用计数自动回收

## Ray 与主流 MLOps 工具的集成

| 工具 | 集成方式 | 场景 |
|------|---------|------|
| **MLflow** | Ray Tune 内置 MLflow 回调 | 分布式超参搜索时自动记录 |
| **W&B** | PTL + Ray 训练通过 wandb 回调 | 大规模分布式训练实验追踪 |
| **Docker/K8s** | Ray Cluster 管理容器化部署 | 生产级分布式训练集群 |
| **Kubeflow** | Ray Operator + Kubeflow Pipeline | K8s 上端到端 ML 工作流 |

## 竞品对比

| 维度 | **Ray** | **Horovod** | **Slurm** | **Spark** |
|------|---------|-------------|-----------|-----------|
| **定位** | 通用分布式计算 + AI 专用库 | 分布式训练通信框架 | HPC 集群调度器 | 大数据处理引擎 |
| **AI 原生** | ✅ 原生设计 | ✅ 训练专用 | ❌ 通用 HPC | ❌ SQL 设计 |
| **训练支持** | ⭐⭐⭐ Ray Train | ⭐⭐⭐ Horovod | ⭐ 需脚本 | ⭐ 弱 |
| **推理服务** | ⭐⭐⭐ Ray Serve | ❌ 不支持 | ❌ 不支持 | ❌ 不支持 |
| **RL 训练** | ⭐⭐⭐ RLlib | ❌ 不支持 | ❌ 不支持 | ❌ 不支持 |
| **数据处理** | ⭐⭐ Ray Data | ❌ | ❌ | ⭐⭐⭐ Spark |
| **超参调优** | ⭐⭐⭐ Ray Tune | ❌ | ❌ | ⭐ 弱 |
| **K8s 集成** | ⭐⭐⭐ Ray Operator | ⭐ 需手动 | ⭐ 需额外 | ⭐ Spark Operator |
| **学习曲线** | 中（需理解分布式范式） | 低（AllReduce 包裹） | 高（HPC 批处理思想） | 中（SQL/DataFrame） |

## 典型应用场景

| 场景 | 实现路径 | 案例 |
|------|---------|------|
| **大规模 LLM 微调** | Ray Train + PyTorch FSDP + LoRA | 16 卡 A100 分布式 Lora 微调 |
| **分布式超参搜索** | Ray Tune + 自动并行 | 搜索 100 组 LoRA 超参组合 |
| **批量推理** | Ray Serve + 动态 batching | 日处理百万级文本生成请求 |
| **RLHF 训练** | Ray RLlib + Policy/Reward 模型 | 大模型 RLHF 对齐训练 |
| **多 Agent 协作编排** | Ray Core Actor + 自定义调度 | Agent 间异步通信与协调 |

## 相关信息

- **创建方**: UC Berkeley RISELab
- **维护方**: Anyscale Inc.（商业公司，由 Ray 创始人创立）
- **开源协议**: Apache 2.0
- **当前版本**: v2.38.x（2026）
- **语言**: Python + C++ / Java / Go
- **官网**: https://ray.io
- **GitHub**: https://github.com/ray-project/ray
- **文档**: https://docs.ray.io

## 关联连接

- [[Weights_and_Biases]] — Ray Tune 可集成 W&B 进行实验追踪
- [[MLflow]] — Ray + MLflow 组合：Ray 跑分布式训练，MLflow 管理模型版本
- [[AI训练推理系统工程]] — Ray Train 是分布式训练系统的关键实现工具，Ray Serve 是推理服务系统的重要选项
- [[Eval_Harness]] — Ray 可用于分布化 Eval 推理以加速大规模评测
- [[Cost_Optimization]] — Ray 的弹性调度可直接贡献于集群利用率和成本优化
- [[Agent沙箱工程]] — Ray 的容器化部署可与 Agent 沙箱环境集成
- [[摘要-算法应用开发工程师-jd]] — 来源 JD 将 Ray 列为 MLOps 加分项工具之一
