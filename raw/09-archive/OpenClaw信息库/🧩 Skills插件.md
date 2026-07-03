---
title: "🧩 Skills插件"
source: "feishu/wiki/OpenClaw信息库"
node_token: "TgDCw3RZniJcEikAHQ0cQsdGnhd"
obj_token: "R3VSdDXfdoOrXixPjBjcxhDynGg"
export_date: "2026-07-03"
---

<title>🧩 Skills插件</title>

# OpenClaw Skills 插件指南

> 更新时间：2026-03-19

---

## 📦 安装方式

### 方式一：ClawHub CLI（推荐）

```Bash
clawhub install <skill-name>

```

### 方式二：openclaw CLI

```Bash
openclaw skills install <skill-name>

```

### 方式三：手动安装

1. 下载Skill包
2. 放入 `~/.openclaw/skills/` 目录
3. 重启OpenClaw

### 方式四：GitHub安装

```Bash
git clone <repo-url> ~/.openclaw/skills/<skill-name>

```

**来源**：[CSDN](https://blog.csdn.net/qq_39329902/article/details/158805774)

---

## 🔧 常用Skills推荐

### 1. weather（天气查询）

- 功能：获取全球天气和预报
- 安装：`clawhub install weather`
- 用途：日常助手

### 2. tavily-search（实时搜索）

- 功能：实时网络搜索
- 安装：`clawhub install tavily-search`
- 用途：获取最新信息

### 3. skill-vetter（安全扫描）

- 功能：安装前安全检查
- 安装：`clawhub install skill-vetter`
- 用途：防病毒/恶意代码

### 4. agent-browser（浏览器自动化）

- 功能：网页操控、填表、截图
- 安装：`clawhub install agent-browser`
- 用途：自动化测试、数据采集

### 5. self-improving-agent（自我进化）

- 功能：记录学习、持续改进
- 安装：`clawhub install self-improving-agent`
- 用途：能力提升

### 6. summarize（信息总结）

- 功能：长文本摘要
- 安装：`clawhub install summarize`
- 用途：阅读助手

### 7. find-skills（技能导购）

- 功能：AI推荐合适技能
- 安装：`clawhub install find-skills`
- 用途：技能发现

**来源**：[CSDN](https://blog.csdn.net/qq_41586848/article/details/159125949)

---

## 📚 学习资源

| 资源 | 链接 |
|-|-|
| ClawHub市场 | https://clawhub.ai |
| 官方文档 | https://docs.openclaw.ai |
| 阿里云教程 | https://developer.aliyun.com |
| GitHub | https://github.com/openclaw/openclaw |

---

## ⚠️ 避坑指南

1. **目录结构** - 确保skill放在正确目录
2. **密钥管理** - 不要硬编码密钥到代码
3. **依赖冲突** - 批量升级前先测试
4. **权限问题** - 注意文件读写权限

**来源**：[阿里云开发者社区](https://developer.aliyun.com/article/1717370)

---

*更多Skills推荐见"神级Skills"分类*
