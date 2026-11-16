---
title: "Claude Code 与 Codex 浏览器操作方式对比"
type: synthesis
tags: [browser-automation, claude-code, codex, playwright, mcp, computer-use, agent-interfaces]
sources: []
last_updated: 2026-11-11
---

# Claude Code 与 Codex 浏览器操作方式对比

> 本文由 2026-11-11 会话调研沉淀（WebSearch + 官方文档 + 知识库既有页面），无 raw 源文件。核心框架对应 [[Agent_Interfaces]] 三层模型中的 **Browser Use** 层。

## 核心结论

两家都不是"只有一种方式"，而是分布在同一条**控制深度谱系**上：只读抓取 → 页面协议控制 → 真实会话接管 → 视觉坐标控制 → 云端隔离浏览器。

- **CLI 本体**通常只原生提供只读抓取层；其余能力靠 **MCP / Shell 脚本 / 浏览器扩展**接入。
- **官方 App**（Claude Code Desktop、Codex App）正在把"真实浏览器接管"和"Computer Use"做成内置能力。
- 选型的核心不是"哪家强"，而是**任务需要多深的控制、是否需要登录态、是否要进 CI**。

## 一、五种控制深度

| 层级 | 控制方式 | 是否写代码 | 登录态 | 典型代表 |
|---|---|---|---|---|
| L0 只读抓取 | HTTP 请求 → Markdown | 否 | ❌ | WebFetch / curl |
| L1 页面协议控制 | DOM / Accessibility Tree | 是（或 MCP 代劳） | 需自行处理 | Playwright / Puppeteer |
| L2 真实会话接管 | 扩展或 CDP attach 到已登录 Chrome | 否 | ✅ | Claude in Chrome / Codex Chrome 扩展 |
| L3 视觉坐标控制 | 截图 → 视觉模型 → 模拟键鼠 | 否 | ✅ | Computer Use |
| L4 云端隔离浏览器 | 远程 CDP / 云沙箱 | 是 | 难 | Browserbase、Cloudflare Browser Rendering |

## 二、Claude Code 的六种方式

### 1. 内置只读层：WebFetch / WebSearch（L0）

- **优点**：零配置、零成本、最快
- **缺点**：只读单页，不执行交互、不带登录态、拿不到 console/network
- **适用**：读文档、查资料，不属于真正的"浏览器操作"

### 2. 官方 Chrome 扩展：`claude --chrome`（L2）⭐

- 会话内也可用 `/chrome` 唤起
- 能力：读页面、点击、输入、导航、填表、多 Tab、截图、录制 GIF，并可读取 **console 日志、网络请求、DOM 状态**
- 使用**真实登录态与 Profile**（Gmail、Notion、内部系统均可操作）
- **限制**：需 Pro/Max/Team/Enterprise 直连 Anthropic（Bedrock/Vertex/Foundry 不可用）；必须交互式登录；WSL 不支持；Chrome/Edge；扩展 v1.0.36+
- **适用**：构建-测试-验证闭环、需要登录态的真实站点调试

### 3. Desktop App 内置 Browser Pane（L1+L2，2026-07 起）

- 沙箱化浏览器面板，**干净 Profile**（无登录、无历史），安全分类器审查外部站点操作
- 与扩展分工明确：**测试自己的应用用 Browser pane；需要"以用户身份"操作才用扩展**
- **注意**：这是 **Desktop App** 能力，不是 CLI TUI 的内置功能

### 4. MCP 浏览器服务器（L1/L2）

```bash
# Playwright MCP（微软，Apache-2.0，走 Accessibility Tree）
claude mcp add playwright -- npx @playwright/mcp@latest

# Chrome DevTools MCP（Google，Puppeteer + CDP）
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

| | Playwright MCP | Chrome DevTools MCP |
|---|---|---|
| 强项 | 通用驱动、跨浏览器（Firefox/WebKit）、可复现 | 性能 Trace、Lighthouse、console/network 调试 |
| Token | 较省 | 更贵（工具多、快照大） |
| 定位 | "把页面跑起来" | "把问题查清楚" |

- **共同缺点**：MCP 工具 schema 每轮重发（26 个工具约 3,600 tokens），页面快照堆积在上下文且不会清理
- **经验法则**：**一个项目只装一个浏览器 MCP**；两个都装工具重叠严重、纯浪费上下文

### 5. Shell + Playwright CLI / 自写脚本（L1）⭐ 2026 主流推荐

```bash
npx playwright open https://example.com
```

- 快照落盘为 YAML，只把**路径**返回模型，需要时再读
- 实测 **~27K tokens/任务 vs MCP ~114K**（约 4 倍；2026-07 Checkly 复测差距缩小到 ~45–48K vs ~48–50K，成本优势仍在）
- 微软官方 README 已引导 coding agent 用 **Playwright CLI + Skills** 替代 MCP
- **优点**：可版本化、可进 CI、可复用、headless 默认、便宜
- **缺点**：探索性交互弱、需自己写断言

### 6. 云浏览器 / 远程 CDP（L4）

- Browserbase、Cloudflare Browser Rendering、E2B、Browserless
- 通过 `--cdp-endpoint` 接 Playwright MCP 或 CLI
- **优点**：隔离、可横向扩展、无本地依赖；**缺点**：延迟、成本、登录态难处理

## 三、Codex 的六种方式

### 1. Codex App 内置浏览器：`@Browser`（L1+L2）⭐

- 与 Codex 共享同一渲染视图，可点击、输入、检查、截图、执行只读 JS
- **明确不支持**：登录页、Cookie、浏览器扩展、已有标签页
- 适合本地 dev server、前端/游戏开发迭代，支持页面元素视觉批注

### 2. Codex App Computer Use：`@Computer`（L3）

- macOS + Windows，可操作任意桌面应用
- **平台差异大**：macOS 支持后台、按应用授权；**Windows 会抢占鼠标键盘前台运行**
- 适合 GUI-only 场景（桌面应用、系统设置、只能在界面复现的 Bug）
- 官方建议：本地 Web 应用优先用内置浏览器，不要上 Computer Use

### 3. Codex Chrome 扩展（L2）

- 官方明确指路：需要登录态/已有标签页 → 用 Chrome 扩展，而非 `@Browser`

### 4. Codex CLI + MCP（L1/L2）

```toml
# ~/.codex/config.toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest", "--isolated"]
startup_timeout_sec = 60
default_tools_approval_mode = "writes"
```

- 配置在 App / CLI / IDE 扩展之间共享，`codex mcp add` 或 `/mcp` 管理
- 社区方案：openchrome-mcp、WebBrain MCP（桥接真实登录会话）、realbrowser

### 5. Codex CLI + Shell 脚本（L1）

- Codex 有完整 shell 权限，可跑 Playwright CLI、Puppeteer 脚本
- 与 Claude Code 第 5 种等价，**token 最省**

### 6. 云浏览器（L4）

- 同上，通过 CDP endpoint 接入

## 四、横向对比

| 方式                         | Token 成本 | 速度    | 可靠性     | 登录态           | 调试能力                        | 安全隔离    | 适合场景                |
| -------------------------- | -------- | ----- | ------- | ------------- | --------------------------- | ------- | ------------------- |
| WebFetch / Search          | 极低       | 极快    | 中（静态页好） | ❌             | 无                           | 好       | 读文档、查资料             |
| Chrome 扩展（两家）              | 中        | 快     | 高       | ✅ 真实会话        | **最强**（console/network/DOM） | ⚠ 有注入风险 | 登录态站点、构建后验证         |
| App 内置浏览器（两家）              | 中        | 快     | 高       | ❌             | 强                           | ✅ 沙箱    | 本地前端开发、视觉验证         |
| Computer Use               | 高（截图）    | 慢     | 中       | ✅             | 弱（只有像素）                     | ⚠       | 桌面 App、GUI-only 任务  |
| Playwright MCP             | 高        | 中     | 高（确定性）  | 需配置           | 中                           | ✅       | 探索性浏览器任务、无 Shell 环境 |
| **Playwright CLI + Shell** | **最低**   | 快     | 高       | 需配置           | 中                           | ✅       | **E2E 测试、CI、长流程**   |
| Chrome DevTools MCP        | 最高       | 中     | 高       | ✅（CDP attach） | **最强**                      | ✅       | 性能分析、网络/console 排障  |
| 云浏览器                       | 中（另计费）   | 慢（网络） | 高       | 难             | 中                           | ✅ 最强    | 大规模爬取、多租户隔离         |

## 五、选型决策树

```
需要登录态 / 操作真实账号？
├─ 是 → Chrome 扩展（Claude in Chrome / Codex Chrome 扩展）
└─ 否 → 要操作桌面 App 吗？
        ├─ 是 → Computer Use（Codex @Computer / Claude 侧 computer-use MCP）
        └─ 否 → 是在做 E2E / 长流程 / CI 吗？
                ├─ 是 → Playwright CLI + Shell 脚本（最省 token）
                └─ 否 → 要调试性能/网络吗？
                        ├─ 是 → Chrome DevTools MCP
                        └─ 否 → Playwright MCP（探索性）或 App 内置浏览器
```

**两家定位差异**：

- **Claude Code**：官方把"真实浏览器接管"（Chrome 扩展）做得最完整；CLI 侧靠 MCP + Shell 补齐，生态最开放
- **Codex**：官方把"内置浏览器 + Computer Use"做进 App；CLI 侧完全依赖 MCP，**App 体验强于 CLI**

## 六、坑与最佳实践

1. **别同时装 Playwright MCP 和 Chrome DevTools MCP**——工具重叠、schema 每轮重复计费（16 工具服务器约 3,141 tokens/轮）
2. **Codex 下 MCP 建议加 `--isolated`**，避免 "browser profile already in use"
3. **Codex `startup_timeout_sec` 默认 10 秒不够**，首次 npx 下载会超时，改 30–60
4. **Windows 上 npx 可能 "program not found"**，需 `cmd /c` 包裹或绝对路径
5. **长会话可能泄漏 Playwright MCP 孤儿进程**（Codex issue #17832），需定期清理
6. **安全**：网页内容是不可信输入，prompt injection 是真实攻击面（Comet 2026 事故）；生产环境必须有审批门 + 域名白名单，参见 [[Agent_Interfaces]] 的"4 个防护模式"
7. **MCP 工具不是越多越好**：用 `enabled_tools` 白名单裁剪，可省大半 schema 开销
8. **浏览器扩展/token 数据随版本变化**：本文 token 数据来自第三方评测，选型前应以当前版本实测为准

## 来源

- [Use Claude Code with Chrome — Claude Code Docs](https://code.claude.com/docs/en/chrome)
- [开始在 Chrome 中使用 Claude — Anthropic Help Center](https://support.claude.com/zh-CN/articles/12012173)
- [Claude Code on desktop gets a built-in browser — heise](https://www.heise.de/en/news/Claude-Code-on-desktop-gets-a-built-in-browser-11362155.html)
- [Anthropic highlights Claude Code's in-app browser — 9to5Mac](https://9to5mac.com/2026/07/10/anthropic-highlights-claude-codes-in-app-browser-on-the-desktop/)
- [Codex App: In-app browser — OpenAI Docs](https://developers.openai.com/codex/app/browser.md)
- [Codex App: Computer Use — OpenAI Docs](https://developers.openai.com/codex/app/computer-use.md)
- [Codex for (almost) everything — OpenAI](https://openai.com/index/codex-for-almost-everything/)
- [The Best MCP Servers to Control a Browser From Your Coding Agent (2026) — browser-use](https://browser-use.com/posts/best-mcp-servers-to-control-a-browser)
- [Playwright, Chrome DevTools, and Claude in Chrome — Steve Kinney](https://stevekinney.com/courses/self-testing-ai-agents/runtime-tools-compared)
- [Playwright CLI: The Token-Efficient Alternative to Playwright MCP — TestCollab](https://testcollab.com/blog/playwright-cli)
- [Connect Codex to Playwright — Codex Insider](https://codexinsider.com/guides/connect-codex-to-playwright/)
- [The 10 Best MCP Servers for OpenAI Codex in 2026 — Bright Data](https://brightdata.com/blog/ai/best-mcp-servers-for-codex)

## 关联连接

- [[Agent_Interfaces]] — 三层接口模型（Computer Use / Browser Use / Code Sandbox）的总框架
- [[Harness_Engineering]] — 浏览器操作属于 Agent 的 IO 边界，处于 Harness 运行时控制之外
- [[Claude_Code]] — Claude Code 侧方式 1–6 的宿主
- [[Codex]] — Codex 侧方式 1–6 的宿主
- [[MCP]] — L1/L2 浏览器 MCP 的标准接入协议
- [[Claude_Code_Harness]] — L2.5 Tool Provider 层的浏览器 MCP 映射
- [[Agent_Loop]] — 浏览器操作嵌入 Agent 循环的观察-行动环节
- [[摘要-awesome-agentic-ai-zh-agent-interfaces]] — 三层接口模型的源素材摘要
- [[Agent_Benchmark_Landscape]] — WebArena / OSWorld 等浏览器与桌面 Agent 评测基准
