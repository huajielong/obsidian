---
title: "监督学习 Supervised Learning"
type: concept
tags: [机器学习, AI基础, A-B映射, 核心概念]
sources:
  - "raw/09-archive/AI for everyone 系列教程原声中文版【吴恩达】.md"
  - "raw/09-archive/AI-for-Everyone-吴恩达-p7-35/AI for everyone 系列教程原声中文版【吴恩达】 1.md"
  - "raw/09-archive/AI-for-Everyone-吴恩达-p7-35/AI for everyone 系列教程原声中文版【吴恩达】 2.md"
  - "raw/09-archive/AI-for-Everyone-吴恩达-p7-35/AI for everyone 系列教程原声中文版【吴恩达】 21.md"
last_updated: 2026-08-03
---

# 监督学习 Supervised Learning

## 定义

监督学习（Supervised Learning）是机器学习中最常用、创造最多实际价值的一类方法，其核心是学习 **A→B（输入→输出）的映射**。给定标注好的数据（输入 A 与期望输出 B 的配对），模型学习从 A 预测 B 的规律，之后便可对未见过的输入自动给出输出。

[[Andrew_Ng]] 在 "AI for Everyone" 课程中将其概括为：几乎所有能用**一秒钟思考**完成的任务，都可以用监督学习自动化（如判断车辆位置、看手机是否有划痕、识别垃圾邮件）。

## 关键信息

### 典型应用

| 应用 | 输入 A | 输出 B |
|------|--------|--------|
| 垃圾邮件过滤 | 电子邮件 | 是否垃圾（0/1） |
| 语音识别 | 音频片段 | 文本转录 |
| 机器翻译 | 英语 | 其他语言 |
| 在线广告 | 广告信息+用户信息 | 是否会点击 |
| 自动驾驶 | 图像+雷达传感器 | 其他车辆位置 |
| 制造业质检 | 产品照片 | 是否有划痕/缺陷 |
| 房价预测 | 房屋属性 | 房屋价值 |

### 与 LLM 的关系

**大型语言模型（LLM）本质上是监督学习**：在海量互联网文本上训练模型"预测下一个词"。如句子"我最喜欢的饮料是荔枝泡泡茶"会被拆解为多个 A→B 数据点（给定前缀→预测下一个词），数据规模达数百亿甚至 1000 亿+ 词时，即得到 ChatGPT 等大模型。

### 扩展规律（Scaling Law 的前身直觉）

- **传统 AI 算法**：性能随数据量增长而提升，但到达某个点后进入平台期不再改善
- **神经网络 + 深度学习**：性能随数据量**持续提升**——模型越大、数据越多，性能越好
- 这一"规模扩展"现象是近期生成式AI（尤其 LLM）突破的关键驱动力

### 与相关概念辨析

- **[[Generative_AI]]**：主要生成非结构化数据（文本/图像/音频）；监督学习对结构化与非结构化数据都能处理
- **[[Data_Science]]**：监督学习输出**运行中的系统**（持续预测），数据科学输出**决策洞察**（图表/报告）
- **[[Neural_Network]]**：实现监督学习最高效的技术手段
- **[[Machine_Learning]]**：监督学习是机器学习三大范式（监督/无监督/强化）中最常用、经济价值最大的一支
- **[[Unsupervised_Learning]]**：无需标注输出 B，让 AI 在数据中发现结构（聚类）——数据需求远小于监督学习
- **[[Reinforcement_Learning]]**：靠奖励信号而非标注数据学习；目前经济价值仍低于监督学习

## 关联连接
- [[Machine_Learning]] — 监督学习是机器学习的核心范式
- [[Generative_AI]] — 生成式AI 的底层训练范式
- [[Neural_Network]] — 实现监督学习的主流技术
- [[Data_Science]] — 机器学习 vs 数据科学辨析
- [[Unsupervised_Learning]] — 无标注学习范式对比
- [[Reinforcement_Learning]] — 奖励信号学习范式对比
- [[Artificial_General_Intelligence]] — 监督学习属于 ANI 范畴
- [[GPT]] — 基于监督学习训练的 LLM 代表
- [[Transformer_Architecture]] — LLM 底层架构
- [[Model_Fine_Tuning]] — 监督学习的迁移应用
- [[AI_Project_Workflow]] — 监督学习项目的落地步骤
- [[AI_Transformation_Playbook]] — 企业应用监督学习的落地路径
- [[Andrew_Ng]] — 概念推广者
- [[摘要-ai-for-everyone-andrew-ng]] — 来源
