---
title: "生成式AI Generative AI"
type: concept
tags: [AI基础, 生成式, 内容生成, 核心概念]
sources:
  - "raw/09-archive/AI for everyone 系列教程原声中文版【吴恩达】.md"
  - "raw/09-archive/AI-for-Everyone-吴恩达-p7-35/AI for everyone 系列教程原声中文版【吴恩达】 1.md"
  - "raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md"
last_updated: 2026-08-05
---

# 生成式AI Generative AI

## 定义

生成式AI（Generative AI）是能够生成高质量新内容——尤其是文本、图像和音频——的相对较新的 AI 技术类别。典型代表是 ChatGPT 等大型语言模型（LLM）。据麦肯锡全球研究院预测，到 2033 年 AI 每年创造的 13~22 万亿美元额外价值中，生成式AI 仅占 3~4 万亿美元，**更大比例的价值来自监督学习等成熟技术**。

## 关键信息

### 定位：三分法中的一环

[[Andrew_Ng]] 在 "AI for Everyone" 课程中给出 AI 全景三分法：

| 类别 | 定义 | 现状 |
|------|------|------|
| 人工狭义智能（ANI） | 专做一件事的 AI（智能音箱/自动驾驶/搜索/工厂质检） | 创造当下绝大部分价值 |
| **生成式AI** | 生成文本/图像/音频等新内容 | 快速发展，价值初现 |
| 人工通用智能（AGI） | 完成人类任何智力任务 | 遥不可及，需多次技术突破（可能数十年~数百年） |

### 技术本质

- LLM（如 [[GPT]]）通过**监督学习**在海量文本上训练"预测下一个词"，从而生成连贯文本
- 生成式AI 当前主要用于生成**非结构化数据**（文本/图像/音频），而非结构化数据表
- 与 [[Transformer_Architecture]]、扩展规律（Scaling）密切相关

### 李宏毅课程定义（2025）

[[Hung_yi_Lee]] 在《生成式人工智慧與機器學習導論(2025)》第一讲给出更具操作性的定义：

> **生成式 AI = 让机器学会产生"复杂而有结构的物件"。** "有结构"指物件由**有限可能的基本单位（Token）** 构成，但组合起来有无穷无尽的可能性。

| 物件 | 基本单位（Token） | 说明 |
|------|------------------|------|
| 文字 | 字（中文常用约 4,000 字） | 有限个字 → 无穷文章 |
| 图片 | 像素或压缩后的图片 Token | 16×16 区域一个符号等 |
| 声音 | 采样点或压缩后的声音 Token | 有限取值 → 无穷声音 |
| 蛋白质 | 胺基酸 | 种类有限 → 各式蛋白质（生成式 AI 制药） |

- **不只是生成，而是"根据输入进行生成"**：输入 X → 输出 Y（复杂有结构的物件），才能打造有用应用。
- **核心套路**：每个 Token 的选择是有限的（分类问题/选择题），把生成化约为一连串选择；最基本的生成策略是**文字接龙（[[Auto_Regressive_Generation]]）**，影像生成另见 [[Diffusion_Model]]。
- **万物皆 Token**：黄仁勳 2024 COMPUTEX 名言"万事万物都是 token"——把图片/声音/视频都表示成 Token 再做接龙，即可生成万物（见 [[Jensen_Huang]]）。

### 价值与炒作

- AI 领域存在大量炒作，原因之一是 ANI 与生成式AI 的急速进步被误读为"AGI 近在咫尺"
- 媒体多报道成功案例、少报道失败案例，需对 AI 能力保持现实预期
- 课程强调：即使 AGI 还很遥远，也无须过度焦虑，应聚焦当下可用技术创造价值
- 课程总结（p27）：**[[Generative_Adversarial_Network|GAN]]** 是最具代表性的"从零生成新内容"的生成式技术（合成不存在的名人照片），与 LLM 同属生成式AI 谱系

## 关联连接
- [[Supervised_Learning]] — LLM 的底层训练范式
- [[Artificial_General_Intelligence]] — 与生成式AI 的边界区分
- [[Generative_Adversarial_Network]] — 生成式AI 的另一代表技术
- [[Machine_Learning]] — 生成式AI 所属的机器学习家族
- [[GPT]] — 生成式AI 的典型代表
- [[Transformer_Architecture]] — 底层架构
- [[Neural_Network]] — 实现技术
- [[Andrew_Ng]] — 概念阐释者
- [[摘要-ai-for-everyone-andrew-ng]] — 来源
- [[摘要-hung-yi-lee-生成式AI-原理-第1讲]] — 李宏毅课程定义的来源
- [[Auto_Regressive_Generation]] — 最基本的生成策略（文字接龙）
- [[Diffusion_Model]] — 影像生成的另一生成策略
- [[Jensen_Huang]] — "万事万物都是 token" 出处
- [[BPE_Tokenizer]] — Token 与词汇表机制
