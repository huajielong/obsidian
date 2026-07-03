---
title: "claude官方人员教工具"
source: "feishu/wiki/Claude Code"
node_token: "B0Hbwh1BdiXkVQk2qbEceYMXnCh"
obj_token: "HhtMd48S9oq8PWxX37tcsPyHnag"
export_date: "2026-07-03"
---

# claude官方人员教工具

1.Terminal-setup是什么意思？没明白



2. /allowed-tools     如何配置？



3./install-github-app



4.用嘴说。  
  
5。具体使用  

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OWU3ZThlYjQwNWNlY2E2OWQyMWJlZTVjNGU4Y2Y0NWZfMmU2YzExZTFiZjYzZjY2ZmRkMDk3OGQwZDliN2U3ZWRfSUQ6NzYzMzQ1MDM5OTY2NzYzNzQyOF8xNzgzMDcwMDU2OjE3ODMwNzM2NTZfVjM)

**示例提示词：**

> `@RoutingController.py` 是如何使用的？
> 
> 我该如何新建一个 `@app/services/ValidationTemplateFactory`？
> 
> `recoverFromException` 函数为什么需要这么多参数？请查看 Git 历史来回答。
> 
> 我们为什么要通过在 `@src/login.ts` API 中添加 if/else 逻辑来修复 #18363 号问题？
> 
> 我们是在哪个版本中发布了新的 `@api/ext/PreHooks.php` API？
> 
> 查看 #9383 号 PR，然后仔细验证哪些应用版本受到了影响。
> 
> 我上周发布了哪些内容？



<callout emoji="💡">
Tip #1:
use codebase Q&A as a way to dip your feet into Claude Code
</callout>



<callout emoji="💡">
Tip #2:
practice prompting, and start to understand what Claude Code "gets" immediately vs. what needs more specific instructions
</callout>







**Steer Claude to use tools your way**

译文：按你的方式引导 Claude 使用工具

 **示例指令（Example prompts）**

1.  **原文**：Propose a few fixes for issue #8732, then implement the one I pick

    **译文**：为 #8732 号问题提供几种修复方案，然后实现我选中的那一个



2.  **原文**：Identify edge cases that are not covered in @app/tests/signupTest.ts, then update the tests to cover these. think hard

    **译文**：找出 \`@app/tests/signupTest.ts\` 中未覆盖的边界情况，然后更新测试用例来覆盖这些场景。请认真思考



3.  **原文**：commit, push, pr

    **译文**：提交（commit）、推送（push）、创建 PR（pr）

    *注：这是开发中常用的 Git 流程简写，直接保留术语即可理解*



4.  **原文**：Use 3 parallel agents to brainstorm ideas for how to clean up @services/aggregator/feed_service.cpp

    **译文**：使用 3 个并行代理，为如何重构/清理 \`@services/aggregator/feed_service.cpp\` 集思广益



---



### 一、向 Claude 介绍你的 Bash 工具

**原文**：Tell Claude about your bash tools

译文：向 Claude 介绍你的 Bash 工具



> **原文**：Use the barley CLI to check for error logs in the last training run. Use -h to check how to use it.
> 
> 译文：使用 `barley` CLI 工具，检查上一次训练运行的错误日志。可以用 `-h` 参数查看工具的使用方法。





### 二、向 Claude 介绍你的 MCP 工具

**原文**：Tell Claude about your MCP tools

译文：向 Claude 介绍你的 MCP 工具



```Bash
$ claude mcp add barley_server -- node myserver
```



> **原文**：Use the barley MCP server to check for error logs in the last training run
> 
> 译文：使用 `barley` MCP 服务器，检查上一次训练运行的错误日志

---

### 一、原文信息提取（无篡改）

```Plain Text
Common workflows

Explore › plan › confirm › code › commit
> Figure out the root cause for issue #983, then propose a few fixes. Let me choose an approach before you code. ultrathink

Write tests › commit › code › iterate › commit
> Write tests for @utils/markdown.ts to make sure links render properly (note the tests won’t pass yet, since links aren’t yet implemented). Then commit. Then update the code to make the tests pass.

Write code › screenshot result › iterate
> Implement [mock.png]. Then screenshot it with Puppeteer and iterate till it looks like the mock.
```



---



### 二、中文翻译版本

```Plain Text
常见工作流

探索 › 规划 › 确认 › 编码 › 提交
> 找出 #983 号问题的根本原因，然后提出几种修复方案。在编码前让我选择实现方式。ultrathink

编写测试 › 提交 › 编码 › 迭代 › 提交
> 为 @utils/markdown.ts 编写测试，确保链接能正确渲染（注意：此时链接尚未实现，测试会暂时不通过）。然后提交。再更新代码，让测试通过。

编写代码 › 截图结果 › 迭代
> 实现 [mock.png] 对应的功能。用 Puppeteer 截图，反复迭代直到效果和原型图一致。
```



---

### 一、原文信息提取（无篡改）

```Plain Text
Give Claude more context

Auto-add common bash commands, files, and style conventions to every session:
• /<enterprise root>/CLAUDE.md      Shared across all projects
• ~/.claude/CLAUDE.md               Shared across all projects
• project-root/
  • CLAUDE.md                       Checked in
  • CLAUDE.local.md                 Not checked in

(Shortcut: type #)
```



---



### 二、中文翻译版本

```Plain Text
给 Claude 更多上下文

自动将常用的 Bash 命令、文件和代码风格规范添加到每个会话中：
• /<企业根目录>/CLAUDE.md           所有项目共享
• ~/.claude/CLAUDE.md              所有项目共享
• 项目根目录/
  • CLAUDE.md                      已纳入版本控制（提交到仓库）
  • CLAUDE.local.md                未纳入版本控制（不提交到仓库）

（快捷方式：输入 #）
```



---

### 一、原文信息提取（无篡改）

```Plain Text
Share with your team

|                | Enterprise policy (shared)                             | Global (just me)             | Project (shared)         | Project (just me)          |
|----------------|--------------------------------------------------------|------------------------------|--------------------------|----------------------------|
| Memory         | /Library/Application Support/ClaudeCode/CLAUDE.md      | ~/.claude/CLAUDE.md          | CLAUDE.md                | CLAUDE.local.md            |
| Slash commands | -                                                      | ~/.claude/commands/          | .claude/commands/         | -                          |
| Permissions    | /Library/Application Support/ClaudeCode/policies.json  | ~/.claude/settings.json      | .claude/settings.json    | .claude/settings.local.json|
| MCP servers    | -                                                      | claude mcp                   | .mpc.json                | claude mcp                 |
```



---



### 二、中文翻译版本

```Plain Text
与你的团队共享

|                | 企业级策略（团队共享）                              | 全局配置（仅自己使用）       | 项目级配置（团队共享）    | 项目级配置（仅自己使用）     |
|----------------|---------------------------------------------------|--------------------------|-----------------------|---------------------------|
| 记忆/上下文配置 | /Library/Application Support/ClaudeCode/CLAUDE.md | ~/.claude/CLAUDE.md      | CLAUDE.md             | CLAUDE.local.md           |
| 斜杠命令       | -                                                 | ~/.claude/commands/      | .claude/commands/     | -                         |
| 权限设置       | /Library/Application Support/ClaudeCode/policies.json | ~/.claude/settings.json | .claude/settings.json | .claude/settings.local.json |
| MCP 服务器     | -                                                 | claude mcp               | .mpc.json             | claude mcp                |
```



---



### 补充说明

- **Memory**：指 Claude 会话中自动加载的项目/团队上下文文件，包含代码规范、项目约定等信息。
- **Slash commands**：以 `/` 开头的快捷指令，可快速调用预设的开发流程（如 `lint`、`fix-github-issue`）。
- **Permissions**：Claude 执行命令、访问文件的权限控制配置，可限制高危操作。
- **MCP servers**：Claude 的工具集成服务器配置，用于接入团队内部的 CLI、API 等工具。
- 表格中的路径均为 Claude Code 的标准配置文件位置，不同层级的配置会按「企业级 > 全局 > 项目级共享 > 项目级本地」的优先级生效。



---



**Puppeteer 是 Google Chrome 团队开源的 Node.js 库，用于用代码控制浏览器（Chrome/Chromium/Firefox），实现浏览器自动化**。





### 一、核心定位

- 它是**浏览器自动化工具**：通过**Chrome DevTools Protocol（CDP）或WebDriver BiDi**直接控制浏览器，默认**无头（headless）模式**运行（无界面，适合服务器），也可开启“有头”模式调试。
- 类比：给浏览器装了个**可编程遥控器**，代码可模拟人手动操作（打开页、点击、填表、截图等）。

### 二、能做什么（常见用途）

- ✅ **网页爬虫**：抓取动态渲染页面（SPA、JS加载内容），解决普通爬虫抓不到JS渲染内容的问题。
- ✅ **自动化测试**：UI 自动化、表单提交、键盘输入、Chrome 扩展测试。
- ✅ **生成截图/PDF**：批量网页截图、导出 PDF（如报告生成）。
- ✅ **性能分析**：捕获页面性能跟踪数据，诊断加载/渲染性能问题。
- ✅ **SSR 预渲染**：爬取 SPA 并生成静态 HTML，用于 SEO 或首屏加速。

### 三、关键特点

1. **Google 官方维护**：Chrome 团队开发，更新快，适配最新浏览器特性。
2. **默认无头模式**：资源占用低，适合 CI/CD、服务器定时任务。
3. **纯 Node.js/JavaScript**：API 友好，前端/Node 开发者上手快。
4. **自动管理浏览器**：安装时自动下载匹配的 Chromium，无需手动装浏览器。
5. **两版可用**：

   - `puppeteer`：自带浏览器，开箱即用。
   - `puppeteer-core`：不含浏览器，可连现有浏览器（如本地 Chrome）。

### 四、简单代码示例（打开网页+截图）

```JavaScript
const puppeteer = require('puppeteer');

(async () => {
  // 启动浏览器（默认无头，设 headless: false 可见浏览器）
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage(); // 新建标签页
  
  await page.goto('https://example.com'); // 打开网址
  await page.screenshot({ path: 'example.png' }); // 截图保存
  
  await browser.close(); // 关闭浏览器
})();
```



### 五、与 Selenium/Playwright 区别

- **Puppeteer**：Google 官方，仅 JS，专注 Chrome/Firefox，轻量、性能好。
- **Selenium**：跨语言（Java/Python/JS 等）、跨浏览器，适合大型分布式测试（如 Selenium Grid）。
- **Playwright**：微软开源，跨浏览器、支持多语言，API 类似 Puppeteer，功能更全（如自动等待、网络拦截）。

要不要我给你一份 Puppeteer 快速安装与环境搭建步骤？



---

### 一、原文信息提取（无篡改）

```Plain Text
Interlude:
Keybindings

Key combos for common tasks:

1 Shift+tab to auto-accept edits
2 # to create a memory
3 ! to enter bash mode
4 @ to add a file/folder to context
5 Esc to cancel
6 Double-esc to jump back in history, --resume to resume
7 ctrl+r for verbose output
8 /vibe
```



---



### 二、中文翻译版本

```Plain Text
插曲：快捷键绑定

常用任务的快捷键组合：

1 Shift+Tab：自动接受修改
2 #：创建记忆（上下文片段）
3 !：进入 Bash 模式
4 @：将文件/文件夹添加到上下文
5 Esc：取消当前操作
6 双击 Esc：跳转到历史对话；--resume：恢复对话
7 Ctrl+R：切换详细日志输出（Verbose output）
8 /vibe：调用 vibe 模式
```



---

补充说明：

- `create a memory`：指通过 `#` 快捷唤起 CLAUDE.md 这类上下文文件，将项目规范、约定等信息快速提供给 Claude，类似“记忆片段”。
- `bash mode`：在 Claude Code 中直接执行终端命令的模式，通过 `!` 快捷进入。
- `verbose output`：开启/关闭详细日志，方便排查工具执行细节。
- `/vibe`：Claude Code 的一种快捷指令，通常用于开启更自由、低约束的生成模式。

需要我帮你整理一份这些快捷键的**使用场景说明和使用建议**吗？



---

### 一、原文信息提取（无篡改）

```Plain Text
Claude Code SDK

Use the SDK as a unix utility: pipe in, pipe out

$ git status |
  claude -p "what are my changes?" \
  --output-format=json |
  jq '.result'

"Your changes are:..."

右侧图示结构：
Your agentic application
↓
Claude Code SDK
↓
Anthropic, Bedrock, or Vertex API
↓
Claude models
```



---



### 二、中文翻译与说明

```Plain Text
Claude Code SDK

将 SDK 作为 Unix 工具使用：支持管道输入、管道输出

$ git status |
  claude -p "帮我分析一下当前的代码变更？" \
  --output-format=json |
  jq '.result'

输出示例："你的变更内容是：..."

右侧图示说明：
你的智能应用
↓
Claude Code SDK
↓
Anthropic / Bedrock / Vertex API
↓
Claude 模型
```



---



### 补充说明

1. **核心用法**：Claude Code SDK 可以像标准 Unix 工具一样，通过管道（`|`）接收前序命令的输出，处理后再通过管道传给后续命令，实现命令行链式调用。

   - 示例中，`git status` 的结果通过管道传给 `claude`，Claude 分析后以 JSON 格式输出，再通过 `jq` 工具提取结果字段。
2. **调用链路**：SDK 作为中间层，支持对接 Anthropic 官方 API、AWS Bedrock、Google Vertex 等不同平台的 Claude 模型，让你的应用能以统一方式调用 Claude 的能力。

需要我帮你解释一下这个管道命令的完整执行流程吗？



这里为你整理了这 4 种并行运行 Claude 实例的方式，做了详细的优缺点对比和适用场景分析：



---



### 📊 四种并行方式对比表

| 方式 | 核心原理 | 优点 | 缺点 | 适用场景 |
|-|-|-|-|-|
| **多终端标签页 + 多副本** | 克隆多个独立的项目目录，每个目录运行一个 Claude 会话 | 上手零成本、完全隔离，互不干扰；本地调试方便 | 占用双倍磁盘空间；需要手动同步代码变更；多任务切换繁琐 | 本地多分支开发、互不相关的独立任务 |
| **Git Worktrees** | 单仓库管理多个工作区，共享 `.git` 目录 | 仅需一份仓库副本，节省空间；分支切换灵活，代码变更自动同步 | 对 Git 操作有一定门槛；部分 IDE/工具对 Worktrees 支持不佳 | 同一项目的多分支并行开发（如 bug 修复 + 功能开发） |
| **SSH + Tmux** | 远程服务器上通过 Tmux 创建持久会话，后台运行 Claude | 不占用本地资源；会话可脱离终端后台运行；可利用服务器算力 | 需要配置 SSH 环境；依赖 Tmux 命令；网络不稳定时会话易断 | 长时间、高负载任务（如大规模重构、批量代码分析） |
| **GitHub Actions** | 利用 CI/CD 流水线的并行任务能力，批量执行 Claude | 完全自动化，无需手动管理；支持大规模并行；可与工作流深度集成 | 受 CI 资源和时长限制；配置复杂，依赖流水线脚本 | 批量任务（如全量代码审查、多语言文档生成、测试用例批量生成） |



---



### 💡 快速选型建议

- **本地快速并行开发**：优先用「多终端标签页 + 多副本」，零配置直接上手。
- **同一项目多分支并行**：优先用 `git worktrees`，节省空间且代码同步更方便。
- **长时间高负载任务**：优先用 `SSH + Tmux`，解放本地电脑，后台稳定运行。
- **批量自动化任务**：优先用 GitHub Actions，一次配置，可反复复用。

---



如果你告诉我你当前的主要使用场景，我可以帮你挑一个最合适的方案，并附上对应的快速上手命令/配置模板。
