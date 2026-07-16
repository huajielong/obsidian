---
title: "摘要-Karpathy-micrograd-神经网络与反向传播"
type: source
tags: [micrograd, backpropagation, neural-networks, autograd, chain-rule, karpathy]
sources: [raw/01-articles/Karpathy_micrograd_neural_networks_backpropagation.md]
last_updated: 2026-07-16
---

## 核心摘要

Andrej Karpathy 的 micrograd 是一个约 100 行的标量自动求导引擎（autograd engine），通过完整实现一个微型神经网络训练系统，直观展示了反向传播（Backpropagation）的核心数学机制。视频从零构建了 Value 类、加减乘除和 tanh 等操作的反向传播实现、拓扑排序保证梯度计算顺序、Neuron/Layer/MLP 神经网络组件，以及完整的训练循环。核心洞见在于：神经网络本质上是数学表达式，反向传播即链式法则沿计算图的递归应用，所有现代深度学习库（PyTorch、JAX）的核心数学机制与此完全相同，区别仅在于张量 vs 标量的效率优化。

## 关联连接

- [[Micrograd]] — Karpathy 构建的标量 autograd 引擎
- [[Andrej_Karpathy]] — 视频讲师与项目作者
- [[Backpropagation]] — 视频讲解的核心算法
- [[Autograd]] — 自动求导技术
- [[Computation_Graph]] — 计算图（DAG）表示
- [[AI训练推理系统工程]] — 训练系统的工程化延伸
- [[预训练研究]] — 预训练技术的底层数学基础
- [[后训练研究]] — RL 算法的梯度计算基础
- [[Agent能力工程]] — RL 训练环境的奖励信号传播
- [[Harness_Engineering]] — 模型执行控制层的底层调用链
- [[Prompt_Engineering]] — 梯度信号与反馈信号的类比
- [[预训练数据工程]] — 数据质量通过梯度直接影响权重
