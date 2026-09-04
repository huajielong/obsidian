---
title: "Claude Security"
type: entity
tags: [Anthropic, 安全扫描, 代码安全, Agent, Claude]
sources: [raw/09-archive/The AI-Native SDLC playbook  Claude by Anthropic.md]
last_updated: 2026-09-04
---

# Claude Security

## 定义

Anthropic 推出的 **hosted 定时代码安全扫描产品**（Claude Enterprise 组织公测）。连接 GitHub 仓库后，扫描在 Anthropic 自有基础设施上以 **Claude Mythos 5** 运行（按 Mythos 5 费率计费），每个发现**先经验证再报告**并附**置信度评级**；建议补丁在 Claude Code on the Web 上人工 review 后，像任何普通变更一样**走 PR review gate** 合入。

## 关键信息

- **定位**：安全扫描的「点状陈述会过时」问题的 AI-native 答案——代码每周在变、新一代模型能发现上一代漏掉的漏洞，所以**定时跑**、无人在调用路径上，覆盖从上次运行到当下的所有代码。是对既有静态分析与依赖扫描的**补充**（覆盖需要上下文判断的漏洞），确定性检查仍留在 CI。
- **运行机制**：按 repo/service/team 组织成 project → 首次全量扫描建立 baseline → 设周期（活跃服务每周是合理默认，大仓库可限定目录/分支）→ 带置信度 triage。
- **处置分级**：bounded finding → 打开 Claude Code on the Web 的补丁、review 后走 PR gate（**提出修复的 agent 无权批准它**）；跨服务/架构级问题（>1 个补丁）→ 写成 `intent.md` 从 Plan 阶段重新进入 [[AI_SDLC]]。
- **闭环**：修复上线后把该漏洞类别加进持续 evals，从此 agent 的配置就对该漏洞类别免疫；findings 可 CSV/Markdown 导出或 webhook 推送，保持组织既有 tracker 为 system of record。
- **治理**：连哪些仓库、谁持扫描 seat、spend limit 均由组织管理员集中控制；每个 finding 有验证结果 + 置信度、每次 dismissal 必须带理由——**扫描历史 = 审计记录**（发现什么、修了什么、有意接受了什么）。

## 在 AI-Native SDLC 中的位置

Maintain 阶段「Recurring codebase scans」play：前提是 Deploy 阶段已就绪的 PR review gate 与 hooks 审批门，使扫描发现像任何变更一样受治理；依赖 `intent.md` 格式承接跨 PR 的大问题。

## 关联连接

- [[Anthropic]] — 开发商（Claude Security 是其产品线之一）
- [[AI_SDLC]] — 所属的 AI 原生软件生命周期（Maintain 阶段 play）
- [[Claude_Code]] — 补丁 review 与应用的载体
- [[Eval_Harness]] — 修复后把漏洞类别写入持续 evals
- [[System_of_Record]] — findings 导出到组织既有 tracker 保持单一事实来源
- [[摘要-ai-native-sdlc-playbook]] — 来源
