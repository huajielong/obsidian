---
title: "Micrograd"
type: entity
tags: [autograd, backpropagation, neural-networks, karpathy, 开源项目, 教育工具]
sources: [raw/01-articles/Karpathy_micrograd_neural_networks_backpropagation.md]
last_updated: 2026-07-16
---

## 定义

Micrograd 是 [[Andrej_Karpathy]] 开发的一个极简标量自动求导引擎（autograd engine），仅约 100 行 Python 代码，完整实现了神经网络训练最核心的数学机制——反向传播（Backpropagation）。该项目刻意操作标量而非张量，以最大化教学清晰度，证明现代深度学习库（PyTorch、JAX）的核心数学原理只需约 150 行代码即可理解。

## 关键信息

- **作者**：[[Andrej_Karpathy]]
- **仓库**：[GitHub](https://github.com/karpathy/micrograd)
- **代码规模**：~100 行（autograd 引擎）+ ~50 行（神经网络库）
- **核心实现**：
  - `Value` 类——封装标量值，前向计算时构建计算图（DAG）
  - 操作符重载——`add`、`mul`、`tanh`、`pow`、`exp` 等的前向与反向传播
  - 拓扑排序——保证反向传播按正确顺序遍历计算图
  - 梯度累加——支持计算图中变量被多次使用时的正确梯度计算
- **教学意义**：API 刻意模仿 PyTorch（`.data`、`.grad`、`.backward()`），唯一区别是标量 vs 张量
- **生态定位**：Karpathy "Zero to Hero" 系列的前置教学项目，与其 nanoGPT、makemore、minbpe 等项目构成完整的学习路径

## 关联连接

- [[Andrej_Karpathy]] — 项目作者
- [[摘要-karpathy-micrograd-neural-networks-backpropagation]] — 本项目的深度解读来源
- [[Backpropagation]] — 实现的核心算法
- [[Autograd]] — 自动求导技术
- [[Computation_Graph]] — 计算图数据结构
- [[GPT]] — 同一教学系列的延伸目标
- [[AI训练推理系统工程]] — 从原型到生产训练的工程化路径
