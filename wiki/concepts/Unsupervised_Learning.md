---
title: "无监督学习 Unsupervised Learning"
type: concept
tags: [机器学习, 学习范式, 聚类, AI基础]
sources:
  - "raw/09-archive/AI-for-Everyone-吴恩达-p7-35/AI for everyone 系列教程原声中文版【吴恩达】 21.md"
last_updated: 2026-08-03
---

# 无监督学习 Unsupervised Learning

## 定义

无监督学习（Unsupervised Learning）是机器学习的一种范式：给定**没有标注输出 B 的数据**，让算法自动在数据中发现有意义的结构。与[[Supervised_Learning|监督学习]]必须提供"输入 A + 期望输出 B"不同，无监督学习不告诉 AI 想要什么，而是让它自行探索。

## 关键信息

### 最著名例子：聚类（Clustering）

- **薯片顾客案例**：给定每位顾客购买薯片包数 + 平均支付价格，聚类算法自动发现两个市场细分——大学生（买便宜薯片但量大）vs 上班族（买少量贵薯片）
- **用途**：市场细分、发现相似客户群、数据探索

### 其他例子

- **Google Cat 项目**（Andrew Ng 团队）：在大量 YouTube 视频上运行无监督学习，AI **自发发现了"猫"的概念**（无需事先告知）——尽管视频中有猫是网络刻板印象，但这是无监督学习的标志性成果

### 与监督学习的对比

- 监督学习需要大量标注数据（教孩子认识咖啡杯可能要指出上万个示例）；无监督学习对数据标注需求小得多
- 因此研究者寄望无监督学习让 AI 以更像人类/生物的方式从**更少标注数据**中学习（实现需重大突破，尚不可知）
- 现实价值：无监督学习今天主要用于改进网络搜索质量等特定场景，**经济价值仍远小于监督学习**

## 关联连接
- [[Supervised_Learning]] — 监督学习对比（A→B 标注 vs 无标注）
- [[Machine_Learning]] — 无监督学习是机器学习三大范式之一
- [[Reinforcement_Learning]] — 另一非监督范式对比
- [[Neural_Network]] — 常作为无监督学习的底层工具
- [[Andrew_Ng]] — Google Cat 项目负责人
- [[摘要-ai-for-everyone-andrew-ng]] — 来源
