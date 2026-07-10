# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概况

这是一个基于 [Karpathy LLM Wiki 理念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 构建的 Obsidian 知识库，主题为 **AI/LLM/Agent 知识体系**。由 Claude Code 通过自定义 Skills 进行日常维护。

## 目录结构

```
.
├── raw/             ← 只读层：原始素材收件箱（绝对禁止修改/删除）
│   ├── 01-articles/  ← 网页剪藏
│   ├── 02-papers/    ← 论文与PDF
│   ├── 03-transcripts/ ← 视频/播客转录
│   └── 09-archive/   ← 已处理文件归档（ingest后自动移入，禁止读取）
├── wiki/            ← 编译输出层（Claude 拥有完全写权限）
│   ├── index.md     ← 全局目录（每次新增页面必须同步更新）
│   ├── log.md       ← 操作日志（Append-only，按 [YYYY-MM-DD] action | 简述 格式）
│   ├── concepts/    ← 概念（框架、方法论，TitleCase命名）
│   ├── entities/    ← 实体（人物、公司、工具，TitleCase命名）
│   ├── sources/     ← 源摘要（raw 文件 1:1 提炼，kebab-case命名）
│   └── syntheses/   ← 综合报告（复杂查询产出的深度分析）
├── assets/          ← 媒体资源层（图片/PDF，引用语法 ![[文件.png]]）
├── Daily/           ← 每日笔记
├── .obsidian/       ← Obsidian插件配置
└── .claude/         ← Claude Skills 配置
```

## 常用命令（Skills）

| 命令 | 功能 | 说明 |
|------|------|------|
| `/ingest <path>` | 摄取原始素材 | 读取 raw/ 文件 → 提炼到 wiki/ → 归档至 09-archive/ |
| `/query <问题>` | 检索知识库 | 查 index.md → 深度阅读 → 双链引用回答 |
| `/lint` | 全局健康检查 | 扫描死链、孤岛页面、索引不一致、知识冲突 |
| `/obsidian-cli` | 操作 Obsidian | 调用 Obsidian 原生 API 检索/打开页面 |
| `/defuddle <url>` | 网页剪藏 | 将 URL 转为 Markdown 存入 raw/ |

其他可用技能参见 skills 列表：`/find-skills`。

## Wiki 页面核心契约

### 1. Frontmatter（YAML）规范

所有 `wiki/` 下的 `.md` 文件必须包含：

```yaml
---
title: "页面标题"
type: concept | entity | source | synthesis
tags: [标签1, 标签2]
sources: [关联的raw文件相对路径]
last_updated: YYYY-MM-DD
---
```

### 2. 强制双向链接

每个 wiki 页面末尾必须有 `## 关联连接` 区域，使用 `[[页面名称]]` 链接到其他概念/实体/来源。不允许孤岛页面。

### 3. 矛盾处理

新旧知识冲突时**不要静默覆盖**。在页面中建立 `## 知识冲突` 区块，保留双方说法并标注对比。

### 4. 操作日志

每次写入操作后必须在 `wiki/log.md` 追加（Append-only）：

```markdown
## [YYYY-MM-DD] ingest | 操作简述
- **变更**: 新增 [[PageName]]; 更新 [[index]]
- **冲突**: 无 (或: 冲突 [[ConflictingPage]], 已标注)
```

支持的操作类型：`ingest`、`query`、`lint`、`sync`、`sec`。

## 命名与语言

- 所有内容使用**简体中文**编写
- 实体/概念命名用 **TitleCase**（如 `Harness_Engineering`）
- 来源用 **kebab-case**（如 `摘要-openai-harness-engineering`）
- `raw/` 文件绝对只读，禁止修改或删除
- `raw/09-archive/` 禁止读取（已处理文件归档）

## Obsidian 插件

| 插件 | 用途 |
|------|------|
| obsidian-git | 自动同步（每 30 分钟）和手动备份 |
| realclaudian | Obsidian 内嵌 Claude 对话 |
| obsidian-excalidraw-plugin | 关系图/架构图绘制 |
| obsidian-style-settings | 主题自定义 |

## Git 惯例

- 自动同步使用 obsidian-git 插件
- 提交类型前缀：`📝 vault sync`、`🔧 修复`、`✨ 新增`
- Python 脚本中的 API Key 必须通过环境变量读取，禁止硬编码

## 架构总览：三层工程模型

```
Prompt Engineering   ← 优化"送进模型的字符串"
Context Engineering  ← 优化"窗口里的信息"（RAG/Memory/Chunking）
Harness Engineering ← 优化"模型外围的执行控制层"（Loop/Retry/Sandbox/Observability）
```

本知识库的 wiki 内容按此三层分类组织，`Harness_Engineering` 是核心枢纽概念，链接多数 pages。
