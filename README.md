# Obsidian LLM Wiki

基于 [Karpathy LLM Wiki 理念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 构建的 Obsidian 知识库，由 Claude Code 智能维护。

## 核心结构

| 目录 | 说明 |
|------|------|
| `raw/` | 原始素材收件箱（文章/论文/转录/笔记） |
| `wiki/` | 编译输出层（概念/实体/摘要/分析） |
| `assets/` | 图片与媒体附件 |
| `Daily/` | 每日笔记 |
| `Templates/` | Obsidian 模板 |

## 工作流

- `/ingest` — 读取 `raw/` 文件，提炼到 `wiki/`
- `/query` — 检索知识库，生成带双链引用的回答
- `/lint` — 扫描孤岛页面和死链

## 跨设备同步

已配置 `obsidian-git` 插件自动推送/拉取，每 30 分钟自动同步。

---

> 详细目录结构见 [LLM-Wiki-Vault.md](LLM-Wiki-Vault.md)
