---
title: "MCP (Model Context Protocol)"
type: concept
tags: [MCP, 协议, 工具调用, Claude Code, 标准化, 外部集成]
sources: [raw/01-articles/05-claude-code-ecosystem.md]
last_updated: 2026-07-10
---

# MCP — Model Context Protocol（模型上下文协议）

## 定义

MCP 是一个**开放协议**，标准化了 LLM 与外部工具/数据源之间的通信接口。在 MCP 之前，每个 LLM 厂商需要各自定义 Tool 规格，每个工具供应商需要为每个 LLM 分别适配。MCP 将这一层**标准化**——写一次 MCP Server，任何支持 MCP 的 Host（Claude / Codex / Cursor 等）都能使用。

## 三个核心抽象

| 抽象 | 本质 | 范例 |
|------|------|------|
| **Tools** | LLM 可以调用的 Function | `read_file(path)` / `query_db(sql)` / `send_slack(channel, msg)` |
| **Resources** | LLM 可以读取的数据源 | `file:///path/file.md` / `postgres://db/users` |
| **Prompts** | Server 预定义的 Prompt 样板 | 一份"Review Code"的 Prompt Template |

> 多数 MCP Server 主要使用 **Tools** 抽象，Resources 和 Prompts 使用较少。

## MCP vs 相关概念

| 组件 | 本质 | 触发方式 |
|------|------|---------|
| **Tool Use**（Stage 3） | 你 In-process 写的 Function 给 LLM 调用 | 代码内显式调用 |
| **MCP** | 标准化 Server/Client 协议，跨 Host 跨 LLM | Server 启动后可随时调用 |
| **Skill**（5.3） | 行为层——教 Claude "遇到 X 用哪个 MCP Tool" | Description 匹配自动加载 |
| **Plugin**（5.4） | 把 MCP + Skill + 其他打包散布 | `/plugin install` |

> 核心区分：MCP = **能力**（让 LLM 能做什么），Skill = **行为**（什么时候用什么能力）。

## 在 7-Layer Architecture 中的位置

MCP 位于 **L2.5 Tool Provider**——介于 L2 Tool Use（LLM 调用 Function 的协议）和 L4 Memory/Context 之间。它严格来说是 **Context Engineering**（Feed Context Source）+ **Tool Design**（协议规范）的跨层组件。

## 2026 年生态现状

- **官方 Registry**（registry.modelcontextprotocol.io）——发现/发布 MCP Server 的中央目录
- **FastMCP**（[jlowin/fastmcp](https://github.com/jlowin/fastmcp)，★25k）——用 `@mcp.tool` 几行写出 Server
- **官方 Servers**（[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)）——20+ 官方 MCP Server（filesystem/git/github/sqlite/time/fetch/memory/sequential-thinking），★85k+
- **社区目录**：[wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)（150+ 社区 Server）+ [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- **GitHub MCP Server**：[github/github-mcp-server](https://github.com/github/github-mcp-server) —— GitHub 官方维护的 Production 级范例

## 安全注意事项

MCP Server 返回的内容是**不可信输入**，可能引发 **Tool Poisoning** 或 **Confused-Deputy Problem**。不要将未检查的第三方 Server 接入有高权限的 Agent。

## 跨 CLI Vendor 支持（2026-05 Snapshot）

| 平台 | MCP 支持 |
|------|---------|
| Claude Code | ✅ 原生完整支持 |
| OpenAI Codex | ✅ 已支持 MCP |
| Gemini CLI | ✅ 需手动安装 MCP Server |
| Cursor | ✅ 已支持 MCP |

## 关联连接

- [[Claude_Code]] — MCP 的宿主 Host
- [[Claude_Code_Skills]] — 行为层，与 MCP 形成"能力+行为"互补
- [[Claude_Code_Hooks]] — 控制层，可在 MCP Tool 执行前后拦截
- [[Claude_Code_Plugins]] — 打包层，MCP Config 可被 Plugin 封装
- [[Claude_Code_Harness]] — 7-Layer Architecture，MCP 位于 L2.5
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 核心来源
- [[Context_Engineering]] — MCP 属于 Context Engineering 的范畴
- [[OpenAI_Compatible_API]] — 同为 AI 行业的标准化接口规范
