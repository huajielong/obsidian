---
title: "生成对抗网络 GAN"
type: concept
tags: [生成式AI, 深度学习, GAN, 图像生成]
sources:
  - "raw/09-archive/AI-for-Everyone-吴恩达-p7-35/AI for everyone 系列教程原声中文版【吴恩达】 21.md"
last_updated: 2026-08-03
---

# 生成对抗网络 GAN

## 定义

生成对抗网络（Generative Adversarial Network，GAN）是 [[Andrew_Ng]] 的学生 **Ian Goodfellow** 创造的一种深度学习技术，**极其擅长从零合成新的图像内容**。其核心思想是让两个网络相互对抗：生成器（Generator）试图生成逼真假图，判别器（Discriminator）试图区分真伪，两者在对抗中共同进化。

## 关键信息

### 课程示例：NVIDIA 合成名人

- 从名人图像数据库学习"名人长什么样"，生成**大量现实中从未存在过的人物照片**
- 这些合成图片可以假乱真，是 GAN 能力的标志性展示

### 应用领域

- **娱乐产业**：计算机图形学、电脑游戏、媒体内容
- **从零生成新内容**：图像合成、风格迁移、数据增强

### 在生成式AI谱系中的位置

GAN 与 LLM 同属[[Generative_AI|生成式AI]]：两者都能"生成新内容"，但 GAN 侧重图像、LLM 侧重文本。GAN 是"从零生成"思想的早期代表，为后续扩散模型等生成式技术铺路。

### 风险与伦理

GAN 合成的"以假乱真"图像也是深度伪造（Deepfake）的技术基础之一，需警惕被用于虚假信息与诬陷（见 AI 恶意使用话题）。

## 关联连接
- [[Generative_AI]] — GAN 是生成式AI 的代表技术
- [[Neural_Network]] — GAN 的底层架构
- [[Machine_Learning]] — GAN 属于机器学习技术
- [[Andrew_Ng]] — Ian Goodfellow 是其学生
- [[摘要-ai-for-everyone-andrew-ng]] — 来源
