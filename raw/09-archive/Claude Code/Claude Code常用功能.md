---
title: "Claude Code常用功能"
source: "feishu/wiki/Claude Code"
node_token: "I3LawCa7zi77hkkvX68cw6T3nWg"
obj_token: "IN29dgGFaodJBVx506yc0czAnag"
export_date: "2026-07-03"
---

# Claude Code常用功能

## 一、安装与配置

### 安装方式

- **官网命令安装**：复制官网命令到终端执行，自动下载安装。
- **IDE Agent 协助安装**：让 IDE 中的 Agent 帮你安装，它会处理依赖和网络问题。
- **包管理器安装**：

  - **macOS/Linux**：`brew install claude-code`
  - **Windows**：`winget install Anthropic.ClaudeCode`

### 模型配置

- **官方订阅**：直接登录 Claude 账号使用。
- **第三方模型**：通过配置`ANTHROPIC_BASE_URL`和`ANTHROPIC_AUTH_TOKEN`环境变量，使用 DeepSeek、GLM 等模型。
- **CC Switch**：可视化工具，方便管理多个模型配置。

### 启动与初始化

- 命令：`claude`。
- 首次启动会进行主题选择、安全提示确认、目录信任设置等初始化操作。

## 二、基础交互操作

### 权限模式切换（Shift+Tab）

- **计划模式（Plan Mode）**：只生成计划不执行操作，适合复杂任务前期规划。
- **默认模式（Default Mode）**：敏感操作（如执行命令、删除文件）会询问确认，一般操作直接执行，平衡安全与效率。
- **自动编辑模式（Accept Edits Mode）**：自动执行文件编辑操作，Shell 命令仍需确认，日常开发常用。

### 输入方式

- **文本交互**：直接输入自然语言指令。
- **@文件**：精准传递上下文，如`@src/main.js`，让 AI 解释或修改该文件。
- **图片输入**：拖拽图片或 Ctrl+V 粘贴，利用多模态能力处理视觉信息。

    windows:  截图发送：截图 → 在 claude-code 里 **Ctrl+V，**

     **依赖：**[**https://github.com/citizenll/clipboard-image-watcher/releases**](https://github.com/citizenll/clipboard-image-watcher/releases)

### 常用斜杠命令

- **/model**：切换不同模型（如 Haiku、Sonnet、Opus）。
- **/BTW**：插入不相关问题，不影响当前任务上下文。
- **/simplify**：代码优化，派生子 Agent 从质量、效率、复用性角度审查并优化代码。
- **/help**：查看所有可用命令。

## 三、文件管理与版本控制

### 回滚操作

- 命令：`/rewind`或双击 ESC。
- 可选择回滚对话、文件修改或两者同时回滚，但只能回滚 AI 编辑的文件，终端命令产生的影响无法回滚。

### Git 版本控制

- AI 可通过自然语言操作 Git，如提交代码、创建分支等。
- 建议养成使用 Git 的习惯，作为最终安全保障。

### 上下文管理

- **/compact**：压缩上下文，保留关键信息，节省 Token。
- **/clear**：彻底清空当前对话上下文。
- **/resume**：恢复之前的对话会话。
- **claude -c**：启动时自动恢复最近一次对话。

## 四、个性化设置

### CLAUDE.md 文件

- **全局级**：`~/.claude/CLAUDE.md`，所有项目生效，存放个人偏好（如 “始终用中文回答”）。
- **项目级**：项目根目录`CLAUDE.md`，团队共享，描述项目架构、技术栈、开发规范等。
- **目录级**：子目录下的`CLAUDE.md`，针对特定模块设置规则。
- **生成方式**：`/init`命令，AI 分析项目后自动生成初始`CLAUDE.md`。

### 自动记忆（Auto Memory）

- 命令：`/memory`开启，AI 后台自动记录用户习惯、项目信息、反馈等。
- 记忆内容存储在`~/.claude/projects/<project>/memory/`目录下，以 Markdown 文件形式持久化。

### 自定义文档

- 可创建品牌视觉规范、语言风格指南等文档，在`CLAUDE.md`中指定 AI 在特定场景参考这些文档，实现更精细个性化。

## 五、高级拓展功能

### 技能（Skills）

- **概念**：给 AI 的专业说明书和操作手册，分为知识型、流程型、工具型、混合型。
- **安装**：

  - 手动复制到`~/.claude/skills/`或项目`.claude/skills/`目录。
  - 通过插件市场安装，如`/plugin install superpowers-skills@anthropics-claude-code`。
- **使用**：AI 可自动调用或手动触发，如`/frontend-design`优化 UI。

### 子 Agent（Subagents）

- **概念**：独立上下文的专用 AI 助手，可并行处理任务，只返回结果摘要，不污染主对话上下文。
- **创建方式**：

  - **自动派生**：复杂任务时 AI 自动派生子 Agent 并行处理。
  - **手动创建**：`/agents`命令进入交互界面创建，定义名称、描述、工具权限等。
- **应用场景**：代码审查、调研分析、测试运行等，提高处理复杂任务效率。

### 外部连接（MCP 与 CLI）

- **MCP（Model Context Protocol）**：连接外部服务的协议，如飞书 MCP 让 AI 操作文档、多维表格等。
- **CLI 工具**：厂商提供的命令行工具，AI 可精准调用，如飞书 CLI、OpenCLI 等，扩展 AI 操作外部服务能力。

### 钩子（Hooks）与插件（Plugins）

- **Hooks**：特定事件触发自定义脚本，如每次文件编辑后自动格式化代码。
- **Plugins**：打包整合 Skills、子 Agent、Hooks 等功能的扩展包，通过`/plugin`命令管理。

## 六、避免频繁按 Yes 的方法

### 启动时指定权限模式

- **完全跳过确认（谨慎使用）**：`claude --dangerously-skip-permissions`，所有操作自动执行，适合隔离沙箱环境。
- **自动接受文件编辑**：`claude --permission-mode acceptEdits`，文件修改自动通过，Shell 命令仍需确认，日常开发推荐。
- **智能自动模式**：`claude --permission-mode auto`，AI 分类器自动判断操作安全性，拦截高危操作，减少弹窗同时保证安全。

### 配置文件永久设置

- 修改`~/.claude/settings.json`，添加：
- {  
  "permissions": {  
    "defaultMode": "acceptEdits"  
  }  
}
- 以后启动默认使用`acceptEdits`模式。

### 精细化权限规则

- 在`settings.json`中配置`allow`、`deny`、`ask`规则，如：
- {  
  "permissions": {  
    "allow": ["Bash(npm install)", "Bash(npm run test)"],  
    "deny": ["Bash(rm -rf \*)", "Bash(sudo \*)"],  
    "ask": ["Bash(git push)"]  
  }  
}
- 实现更细粒度权限控制。

掌握以上内容，可从安装配置到高级拓展全面使用 Claude Code，提升开发效率。
