---
title: "AIDE"
type: entity
tags: [agent, ML工程, data science, 开源, 框架]
sources:
  - wiki/sources/摘要-hung-yi-lee-ai-agent-原理.md
last_updated: 2026-08-04
---

## 定义

AIDE 是面向机器学习/数据科学任务的 Agent 框架，目标是打造一个"**机器学习工程师 Agent**"（Machine Learning Engineer Agent）——用 Multi-Agent 框架解决数据科学竞赛类任务，让 AI 像工程师一样迭代地训练模型。

## 关键信息

- **定位**：从技术报告标题即可看出其野心——ML engineer agent，用 multi-agent framework 解 data science competition。
- **运作方式**：目标（如"过 strong baseline"）→ 读训练数据 → 写程序训练模型 → 得到正确率 → 根据正确率重写程序 → 再得到新正确率，循环优化。
- **教学用途**：李宏毅课程作业二用它演示"用 AI 训练 AI 模型"。

## 关联连接

- [[Agent_Loop]] — 迭代训练循环是 Agent Loop 的典型应用
- [[Multi_Agent_System]] — AIDE 采用 multi-agent 框架
- [[Model_Based_Planning]] — 迭代重写程序蕴含规划与反馈
- [[摘要-hung-yi-lee-ai-agent-原理]] — 本实体的来源
