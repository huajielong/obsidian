---
title: "从头构建 micrograd：神经网络与反向传播的直观理解"
type: source
tags: [micrograd, backpropagation, neural-networks, chain-rule, autograd, karpathy]
sources: [raw/01-articles/Karpathy_micrograd_neural_networks_backpropagation.md]
related_video: "https://youtu.be/VMj-3S1tku0"
last_updated: 2026-07-16
---

> [!quote] 核心论断
> "micrograd is what you need to train your networks, and everything else is just efficiency." —— Andrej Karpathy

[[Karpathy]] 的 micrograd 是一个仅约 **100 行** 的标量自动求导引擎（autograd engine），实现了神经网络训练最核心的数学机制：**反向传播（Backpropagation）**。本视频从头构建了这一引擎，证明现代深度学习库（PyTorch、JAX）的核心只需约 150 行代码即可理解。

---

## 视频概览

| 项目 | 内容 |
|------|------|
| **讲师** | Andrej Karpathy（前 Tesla AI 总监、OpenAI 创始成员） |
| **时长** | ~2.5 小时 |
| **仓库** | [micrograd GitHub](https://github.com/karpathy/micrograd) |
| **核心产出** | 一个标量级 autograd 引擎 + 一个极简神经网络库（~150 行） |
| **前置知识** | 基础 Python、高中微积分（导数概念） |

---

## 核心洞察

> [!tip] 洞察 1：神经网络只是数学表达式
> 神经网络本质上就是一个数学表达式——接收输入数据和权重作为参数，输出预测结果。它并不比 `a * b + c` 更神秘，只是规模更大。
>
> 反向传播对数学表达式本身通用，不关心它是否是神经网络。

> [!tip] 洞察 2：反向传播 = 链式法则的递归应用
> 反向传播算法本质上就是沿着计算图**逆向**递归应用微积分中的链式法则：
>
> $$
> \frac{\partial z}{\partial x} = \frac{\partial z}{\partial y} \cdot \frac{\partial y}{\partial x}
> $$
>
> 直观理解：**若汽车速度是自行车的 2 倍，自行车速度是行人的 4 倍，则汽车速度是行人的 8 倍（2 × 4）。**

> [!tip] 洞察 3：加减乘除的局部梯度是封闭的
> | 操作 | 局部梯度 | 反向传播行为 |
> |------|---------|------------|
> | 加法（a + b） | ∂/∂a = 1, ∂/∂b = 1 | 梯度**等分分发**到所有输入 |
> | 乘法（a × b） | ∂/∂a = b, ∂/∂b = a | 梯度 = **对方的值** × 上游梯度 |
> | tanh 激活 | 1 - tanh(x)² | 梯度被 tanh 输出"调制" |
> | 幂运算 xⁿ | n × xⁿ⁻¹ | 标准幂法则 |

> [!warning] 洞察 4：梯度累加（+=）而非赋值（=）
> 当一个变量在计算图中被**多次使用**时，反向传播的梯度必须**累加**而非覆盖。
>
> ```python
> # ❌ 错误：覆盖梯度
> self.grad = local_grad * out.grad
>
> # ✅ 正确：累加梯度
> self.grad += local_grad * out.grad
> ```
>
> 这是反向传播实现中最常见也最隐蔽的 bug——[[Karpathy]] 曾在直播中当众踩坑。

> [!important] 洞察 5：抽象层级是可选的
> 任何函数都可以作为一个"操作节点"——只要你知道其局部梯度。你可以将 tanh 拆解为 exp、加法、除法等原子操作，也可以将其直接实现为一个整体。两者的数学结果完全等价。
>
> **所有 PyTorch 自定义操作（custom autograd Function）正是基于此原理。** 你只需提供 forward 和 backward，PyTorch 就能无缝将其接入庞大的计算图。

> [!tip] 洞察 6：标量 vs 张量——只是效率问题
> micrograd 操作**标量**（单个数字）；PyTorch 操作**张量**（多维数组）。数学完全不变，张量仅是为了利用并行计算加速。
>
> "I don't think it's pedagogically useful to be dealing with tensors from scratch." —— 正因为此，micrograd 从标量开始。

---

## 操作步骤：构建 micrograd

> [!note] 一张图总结
> micrograd 的核心流程：
> ```
> Value 类（封装标量）
>   ├── 前向运算（add / mul / tanh / pow）
>   │     └── 构建计算图（DAG）
>   ├── backward（拓扑排序）
>   │     ├── 设置自身 grad = 1
>   │     └── 拓扑序逆向调用各节点 _backward
>   └── 叶子节点的 .grad 即所求偏导
> ```

### 第一阶段：Value 类（自动求导引擎）

1. **定义 Value 类**
   ```python
   class Value:
       def __init__(self, data, children=(), op=''):
           self.data = data       # 标量值
           self.grad = 0          # 梯度（初始化为 0）
           self._backward = lambda: None  # 反向传播函数
           self._prev = set(children)    # 前驱节点
           self._op = op          # 产生此值的操作名
   ```

2. **实现加法操作**
   - 前向：`out = Value(self.data + other.data, (self, other), '+')`
   - 反向：梯度等分分发——`self.grad += out.grad; other.grad += out.grad`

3. **实现乘法操作**
   - 前向：`out = Value(self.data * other.data, (self, other), '*')`
   - 反向：梯度与对方值互换——`self.grad += other.data * out.grad; other.grad += self.data * out.grad`

4. **实现 tanh 激活函数**
   - 前向：使用 `math.tanh(x)` 计算输出
   - 反向：`self.grad += (1 - t**2) * out.grad`（其中 `t` 是 tanh 输出值）

5. **实现指数运算 `exp()`**
   - 前向：`out = Value(math.exp(self.data), (self,), 'exp')`
   - 反向：`self.grad += out.data * out.grad`（因为 deˣ/dx = eˣ）

> [!warning] 关键 Bug 修复
> **拓扑排序**保证反向传播的正确顺序——必须先处理所有后续节点，再处理前驱节点。
>
> ```python
> def backward(self):
>     topo = []
>     visited = set()
>     def build_topo(v):
>         if v not in visited:
>             visited.add(v)
>             for child in v._prev:
>                 build_topo(child)
>             topo.append(v)
>     build_topo(self)
>     self.grad = 1
>     for v in reversed(topo):
>         v._backward()
> ```

### 第二阶段：便利操作（pow、sub、div）

6. **实现幂运算 `__pow__(self, other)`**
   - 限制 `other` 为 int/float（常数幂）
   - 前向：`out = Value(self.data ** other, (self,), f'**{other}')`
   - 反向：`self.grad += (other * self.data ** (other - 1)) * out.grad`（幂法则）

7. **实现减法 `__sub__` 和除法 `__truediv__`**
   - 减法：`self + (-other)`——复用已有操作
   - 除法：`self * other ** (-1)`——复用幂运算

8. **实现 `__rmul__` 等反转操作**
   - 使 `2 * a` 也能正常工作（Python 特殊方法机制）

### 第三阶段：构建神经网络

9. **实现 Neuron 类**
   ```python
   class Neuron:
       def __init__(self, nin):          # nin: 输入数量
           self.w = [Value(random()) for _ in range(nin)]
           self.b = Value(random())
       def __call__(self, x):
           act = sum(wi*xi for wi, xi in zip(self.w, x)) + self.b
           return act.tanh()             # 经过 tanh 激活
   ```

10. **实现 Layer 类**
    - 包含多个独立 Neuron 的列表
    - 前向传播：逐一计算各神经元的输出

11. **实现 MLP（多层感知机）类**
    - 接收各层尺寸列表（如 `[3, 4, 4, 1]`）
    - 顺序串联各 Layer

### 第四阶段：训练循环

12. **定义损失函数**
    ```python
    # 均方误差（MSE）损失
    loss = sum((yout - ygt)**2 for yout, ygt in zip(y_pred, y_true))
    ```

13. **执行训练循环**
    ```
    for step in range(steps):
        # 1. 前向传播
        y_pred = model(x_data)
        loss = mse_loss(y_pred, y_targets)

        # 2. 清零梯度（关键！）
        for p in model.parameters():
            p.grad = 0

        # 3. 反向传播
        loss.backward()

        # 4. 梯度下降更新参数
        for p in model.parameters():
            p.data -= learning_rate * p.grad
    ```

> [!warning] 最常见 Bug：忘记 Zero Grad
> 梯度会从上一轮累加——若不清零，反向传播的 `+=` 操作会让梯度无限累积，导致训练不稳定。这也是 PyTorch 中每次都需要 `optimizer.zero_grad()` 的原因。

---

## 工程实践关联

本视频内容与以下知识库概念深度相关：

| 概念 | 关联说明 |
|------|---------|
| [[AI训练推理系统工程]] | micrograd 是训练系统的**数学核心原型**；实际训练系统在此基础上添加张量并行、混合精度、分布式训练等工程优化 |
| [[预训练研究]] | 预训练研究中"数据与智能的映射关系"的底层数学机制就是反向传播 + 梯度下降 |
| [[后训练研究]] | RLHF 中的 PPO/GRPO 算法同样基于反向传播计算策略梯度，micrograd 的链式法则是其数学基础 |
| [[Agent能力工程]] | RL 训练环境的奖励信号通过反向传播转化为策略更新 |
| [[Prompt_Engineering]] | 反向传播的"梯度信号"概念在提示工程中演变为"反馈信号"——两者都涉及梯度传播 |
| [[Harness_Engineering]] | 模型执行控制层的底层调用链最终落到 autograd 引擎的 forward/backward |
| [[预训练数据工程]] | 数据处理管线的质量**通过损失函数的梯度**直接影响模型权重更新 |

---

## 与 PyTorch 对比

> [!important] 核心洞见
> micrograd 的 API **刻意模仿** PyTorch：
> - `Value` → `torch.Tensor`
> - `.data` → `.data`
> - `.grad` → `.grad`
> - `.backward()` → `.backward()`
> - `Neuron/Layer/MLP` → `torch.nn.Module` 子类
>
> 区别仅在于 micrograd 操作标量，PyTorch 操作张量。

PyTorch 的 tanh 反向传播源码深度嵌套在 C++ 内核层（CPU kernel vs CUDA kernel），但核心数学与 micrograd 完全相同：

```cpp
// PyTorch CPU tanh backward kernel（简化）
grad_output * (1 - tanh_output^2)
```

自定义 PyTorch 操作只需：
```python
class LegendrePolynomial3(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return ...
    @staticmethod
    def backward(ctx, grad_output):
        x, = ctx.saved_tensors
        return grad_output * ...  # 局部梯度
```

这就是 micrograd 在 100 行内教给你的全部内容。

---

## 扩展阅读

- [micrograd GitHub 仓库](https://github.com/karpathy/micrograd)
- 从 micrograd 到 GPT 的扩展路径：标量 autograd → 张量 autograd → 现代 Transformer 库
- [[Frontier研究]] 中探讨的"超越 Scaling Law"方向，其底层仍然依赖反向传播机制

---

## 关联连接

- [[AI训练推理系统工程]] — 训练系统工程的宏观架构
- [[预训练研究]] — 当前范式下的预训练技术栈
- [[后训练研究]] — RL 算法驱动的后训练体系
- [[Agent能力工程]] — RL 训练环境与策略优化
- [[Harness_Engineering]] — 模型执行控制层
- [[Prompt_Engineering]] — 提示工程与反馈信号
- [[预训练数据工程]] — 数据质量对梯度更新的影响
