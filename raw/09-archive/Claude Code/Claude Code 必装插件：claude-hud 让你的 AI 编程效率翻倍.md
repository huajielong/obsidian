---
title: "Claude Code 必装插件：claude-hud 让你的 AI 编程效率翻倍"
source: "feishu/wiki/Claude Code"
node_token: "NahSwXT9uiKolFkjLLBcZMH2nlb"
obj_token: "YPctdblkCoFlRwxpuaycqMFcnNh"
export_date: "2026-07-03"
---

# Claude Code 必装插件：claude-hud 让你的 AI 编程效率翻倍

> 来源：[阿里云开发者社区](https://developer.aliyun.com/article/1728727)作者：JeecgBoot AI专题研究发布日期：2026-04-20标签：AI编程 / Claude Code / 插件 / 监控

---

## 一句话总结

**claude-hud** 是 Claude Code 的状态监控插件，在终端底部实时显示上下文占用、配额消耗、工具活动等关键指标，让 AI 编程从"黑盒"变成"透明箱"。

---

## 效果预览

安装后在终端底部显示两行状态面板：

```Plain Text
[Opus 4.6] │ workspace-ai
Context █████░░░░░ 15% │ Usage ██░░░░░░░░ 13% (resets in 3h 24m)

```

- **第一行**：当前模型版本 + 项目目录名称 + Git 分支状态
- **第二行**：三个颜色编码进度条（Context / Usage / Weekly）

---

## 核心功能

### 1. Context 进度条

- 显示当前对话已用上下文窗口百分比
- 超过 70% 变黄，超过 90% 变红
- **实战经验：超过 50% 时果断执行 /clear**

> 为什么是 50%？

### 2. Usage 配额消耗

- 当前时间窗口内的 API 配额使用率
- 显示距离下次重置的倒计时
- 避免在关键时刻被限速

### 3. Weekly 周配额

- 显示本周整体配额消耗情况
- 从更长维度规划 AI 辅助编程使用策略

### 4. 工具活动追踪（可选）

开启后可实时看到 Claude Code 正在调用哪些工具：

```Plain Text
◐ Edit: src/main.ts | ✓ Read ×3 | ✓ Grep ×2

```

### 5. Agent 与 Todo 状态（可选）

显示子代理（subagent）并行工作状态和耗时：

```Plain Text
⚡ Agent: code-reviewer (12s) | ◐ Agent: test-runner (5s)

```

---

## 三步安装

**第一步：添加插件市场**

```Plain Text
/plugin marketplace add jarrodwatts/claude-hud

```

**第二步：安装插件**

```Plain Text
/plugin install claude-hud

```

**第三步：运行自动配置**

```Plain Text
/claude-hud:setup

```

自动检测运行环境（Node.js / Bun），生成配置并写入 `~/.claude/settings.json`。**零手动配置，开箱即用。**

---

## 进阶配置

插件内置三个预设方案：

| 预设 | 包含内容 | 适用场景 |
|-|-|-|
| **Minimal** | 模型名称 + 上下文进度 | 追求极简的开发者 |
| **Essential** | 核心指标 + Git 状态 + 工具活动 | 大多数日常开发场景 |
| **Full** | 所有模块全开 | 复杂项目调试、多 Agent 并行任务 |

自定义配置文件：`~/.claude/plugins/claude-hud/config.json`

---

## 技术细节

- **刷新频率**：约 300 毫秒刷新一次，对性能几乎无影响
- **运行环境**：Node.js 18+ / Bun
- **支持平台**：macOS、Linux、Windows
- **开源协议**：MIT
- **GitHub 星标**：20,000+
- **项目地址**：https://github.com/jarrodwatts/claude-hud

---

## 为什么值得装？

安装前常遇到的三大痛点：

1. **上下文悄悄爆满** — AI 回答质量骤降才后知后觉
2. **配额意外耗尽** — 大任务执行到一半被限速
3. **黑盒等待焦虑** — 不知道 AI 在读文件还是在写代码

claude-hud 让状态监控**被动式、实时化**，不打断工作流，关键信息始终在眼前。

---

*本文为 JeecgBoot AI 专题研究系列文章。*
