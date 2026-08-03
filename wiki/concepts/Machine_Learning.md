---
title: "机器学习 Machine Learning"
type: concept
tags: [AI基础, 机器学习, 核心概念, 学习范式]
sources:
  - "raw/09-archive/AI for everyone 系列教程原声中文版【吴恩达】 3.md"
  - "raw/09-archive/AI-for-Everyone-吴恩达-p7-35/AI for everyone 系列教程原声中文版【吴恩达】 21.md"
last_updated: 2026-08-03
---

# 机器学习 Machine Learning

## 定义

机器学习（Machine Learning）是让计算机**无需明确编程即可获得学习能力**的研究领域（Arthur Samuel 定义），也是 AI 的核心子集（AI ⊃ 机器学习 ⊃ 神经网络/深度学习）。其价值在于从数据中自动学习规律，而非人工编写规则。[[Andrew_Ng]] 在"AI for Everyone"课程中强调：机器学习输出的是**运行中的 AI 系统**（持续自动预测），与输出决策洞察的数据科学相区别。

## 关键信息

### 三大学习范式

[[Supervised_Learning|监督学习]]、[[Unsupervised_Learning|无监督学习]]、[[Reinforcement_Learning|强化学习]]是机器学习的三大范式：

| 范式 | 学习方式 | 代表技术 | 经济价值 |
|------|---------|---------|---------|
| **监督学习** | 给定标注数据（A→B）学习映射 | 神经网络、逻辑回归 | 目前最高 |
| **无监督学习** | 无标注，让 AI 发现数据中的结构 | 聚类 | 较低，但前景可期 |
| **强化学习** | 靠奖励信号试错优化行为 | 游戏/机器人控制 | 目前低于监督学习 |

### 与相关概念辨析

- **[[Data_Science]]**：机器学习输出运行中的系统；数据科学输出图表/报告/决策建议
- **[[Neural_Network]]/深度学习**：实现机器学习（尤其是监督学习）最高效的技术手段
- **[[Generative_AI]]**：基于机器学习（LLM/GAN）生成新内容的应用方向
- **AI 家族图**：AI ⊃ 机器学习 ⊃ 神经网络/深度学习；数据科学横跨使用 AI 各工具

### 项目落地

机器学习项目遵循[[AI_Project_Workflow|三大步骤工作流]]：收集数据 → 训练模型（A→B 映射，多次迭代）→ 部署模型。企业选择项目时应聚焦"自动化任务而非工作"（见[[AI_Transformation_Playbook]]）。

## 关联连接
- [[Supervised_Learning]] — 机器学习最常用范式（A→B 映射）
- [[Unsupervised_Learning]] — 无标注学习范式
- [[Reinforcement_Learning]] — 奖励信号学习范式
- [[Neural_Network]] — 机器学习的高效实现技术
- [[Data_Science]] — 机器学习 vs 数据科学辨析
- [[Generative_AI]] — 机器学习的生成式应用
- [[AI_Project_Workflow]] — 机器学习项目落地步骤
- [[AI_Transformation_Playbook]] — 企业引入机器学习的路径
- [[Andrew_Ng]] — 概念推广者
- [[摘要-ai-for-everyone-andrew-ng]] — 来源
