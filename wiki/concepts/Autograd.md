---
title: "Autograd"
type: concept
tags: [自动求导, 反向传播, 链式法则, 计算图, 深度学习框架]
sources: [raw/01-articles/Karpathy_micrograd_neural_networks_backpropagation.md]
last_updated: 2026-07-16
---

## 定义

Autograd（Automatic Differentiation，自动求导）是一种自动计算数学表达式中所有参数梯度的技术。其核心机制是：在前向传播过程中构建计算图记录所有操作依赖关系，随后通过反向传播（[[Backpropagation]]）沿计算图逆向递归应用链式法则，高效计算每个中间变量和参数对最终输出的偏导数。

## 关键信息

### 工作原理

```
前向传播 → 构建计算图（DAG）
                  ↓
反向传播 → 拓扑排序 → 逆向遍历 → 链式法则递归应用
                  ↓
每个叶子节点 .grad = 所求偏导
```

### 实现层级

1. **标量 Autograd**（如 [[Micrograd]]）
   - 操作单个数字
   - 教学目的，代码约 100 行
   - API 模仿 PyTorch：`Value.data`、`.grad`、`.backward()`

2. **张量 Autograd**（如 PyTorch、JAX）
   - 操作多维数组
   - 数学逻辑完全不变
   - 利用张量并行计算加速

### 关键设计模式

- **局部梯度封闭性**：每个基础操作（add、mul、tanh、exp）的局部梯度是已知且封闭的
- **操作节点抽象**：任何函数只要提供 forward 和 backward 即可接入计算图（对应 PyTorch `torch.autograd.Function`）
- **梯度累加**：变量被多次使用时梯度必须累加（`+=`）而非覆盖（`=`）
- **拓扑排序**：保证子节点梯度先于父节点计算，防止梯度传播顺序错误

### 生态对比

| 框架 | 底层技术 | 特点 |
|------|---------|------|
| [[Micrograd]] | 标量 autograd | 教学目的，~100 行代码 |
| PyTorch | 张量 autograd | 动态计算图，学术界标准 |
| JAX | XLA 编译 + 函数变换 | 函数式纯计算，JIT 编译优化 |
| TensorFlow | 静态计算图 → eager mode | 生产部署成熟 |

## 关联连接

- [[摘要-karpathy-micrograd-neural-networks-backpropagation]] — 从零构建 autograd 引擎的深度解读
- [[Micrograd]] — 最简化的标量 autograd 实现
- [[Backpropagation]] — autograd 依赖的核心算法
- [[Computation_Graph]] — 计算图数据结构
- [[AI训练推理系统工程]] — 生产环境训练系统中 autograd 的工程化角色
