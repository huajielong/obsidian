![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_e6f110eb98a04ce68aea6e0033869a59.png?x-oss-process=image/resize,w_1400/format,webp)

## 1\. Claude 常用命令

- 查看版本：
```bash
claude --version
```

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_5a447b1ceabb43fdb0632ba1712827a2.png)

- 启动交互界面（当前目录）：
```bash
claude
```
- 指定目录启动：
```bash
claude /path/to/project
```
- 升级到最新版本
```bash
claude update
```

## 2\. Claude Code 界面说明

- 左下：模式指示器  
	Default / Accept Edits / Plan Mode，Shift+Tab 切换模式

> 1、Default（默认模式） — 每次编辑文件或执行命令都需要你确认  
> 2、Auto-Accept（自动接受模式） — 文件修改自动执行，无需逐一确认（但 shell 命令仍需确认）  
> 3、Plan（计划模式） — 只读模式，Claude 只分析和规划，不做任何修改，等你审核计划后再执行 Skill-gallery、

- Claude Code 底部状态栏显示的不同状态

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_96ae7a725c27449d94ed8efb2414d524.png)

1、默认模式  
![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_ac4739e04fcc42349fc20eafbbd4cfe4.png)

2、自动接受模式  
![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_a909cf2abcfa4c1cb0eec12576abf7d0.png)

3、计划模式  
![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_3d669b495efa4f6594496ccdf47a7a5c.png)

- 对话中：工具调用  
	Claude 读文件、写文件、执行命令的详情嵌入在对话流中
- 中间：对话输入框  
	自然语言输入需求，支持Markdown，可拖拽文件/图片
- 底部：快捷键提示  
	Ctrl+C 中断· Ctrl+B 后台· ESC 返回/取消
- 输入? ，显示一些快捷键  
	![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_92712a3e2b60435ea57969b1536bdd94.png)

## 3\. Claude 常用指令速查

- Claude Code 指令 / 快捷键参考

| 指令 / 快捷键 | 作用 | 典型场景 |
| --- | --- | --- |
| `/compact` | 压缩对话上下文，保留核心摘要 | 对话过长 token 超限时 |
| `/clear` | 清空所有对话历史，全新开始 | 切换到完全不同的任务时 |
| `claude -c` | 启动时恢复上一次对话 | 次日继续昨天未完成的工作 |
| `Ctrl+B` | 将当前任务挂到后台运行 | 让 AI 后台编译，前台讨论下一步 |
| `ESC×2` (`/rewind`) | 回退或总结（回滚 AI 操作） | AI 改错了代码，快速撤销 |
| `↓ / /tasks` | 管理后台任务（查看/停止） | 检查后台编译/测试是否完成 |
| `Ctrl+T` | 显示/隐藏任务列表面板 | 查看 Claude 创建的任务进度 |
| `Alt+V` | 粘贴图像（Windows） | 截图粘贴给 Claude 分析 UI/报错 |
| `/memory` | 打开并编辑 CLAUDE.md | 修改项目规则或个人偏好 |
| `/init` | 自动生成 CLAUDE.md 初稿 | 新项目首次接入 Claude Code |
| `/hooks` | 配置工具钩子（自动化触发） | 写文件后自动 prettier 格式化 |
| `\+Enter` | 输入框内换行（不发送消息） | 输入多行代码或多段需求描述时 |
| `Shift+Tab` | 循环切换三种工作模式 | 从 Plan Mode 切到 Accept Edits 执行 |

- claude code 读取图片信息处理机制

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_34969bd3bed8432caacd009e2536fd64.png)

## 4\. Claude Code 的命令行输入

- Claude Code 是 Anthropic 推出的终端 AI 编码助手，在交互界面中通过 斜杠命令（Slash Commands）来控制 AI 助手的行为和上下文，合理使用斜杠命令，配合自然语言输入更加顺利完成开发操作。

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_1a7b33394f3b4eb99cfaa057f380407a.png)

Calude Code 执行初始化命令

- 在使用Claude Code的时候，一般都会首先添加工作目录。这里一般通过一个斜杠： `/` 来表示输入指令。这里输入如下指令选定工作目录
```bash
/add-dir <你的工作目录>
```
- 在创建工作目录后，使用初始化工具对该目录下的项目进行初始化分析，生成一份 `CLAUDE.md` 文档。这个文档的作用是建立上下文，让Claude Code理解当前项目的目标和结构、设置代码风格和一些规则、设置Claude Code的角色。可以在进行初始化之后通过自然语言输入让其修改该初始化说明文档，进而实现所需的设定

在一个已完成的项目下，通过 `/init` 完成项目分析的初始化

## 4.1 /init – 初始化项目记忆指南

- 定义与语法： /init 无参数。运行此命令会扫描当前项目代码库，在项目根目录生成一个 `CLAUDE.md` 文件，作为该项目的知识指南。 `CLAUDE.md` 通常包含项目结构摘要、主要模块说明、依赖列表等内容。
- 使用场景： 建议首次在新项目中使用 Claude Code时立即执行 /init。这样Claude会自动了解项目的大概结构和背景，相当于给Claude这个AI同事一本项目手册。/init 生成的 CLAUDE.md 可由Claude根据代码自动提取要点，你也可以在Claude的帮助下完善它——比如询问 “请列出项目架构的关键部分写入 CLAUDE.md” 等。完成后，将 CLAUDE.md 保存（甚至提交进仓库共享给团队）。之后每次在该项目目录启动Claude Code，它都会首先读取 CLAUDE.md，拥有持久的项目信息。
	```bash
	/init
	```
	![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_5860c7ee53bb4e0b9d3ce3c18a396a8c.png)

## 4.2 /help – 查看命令列表

```bash
/help
```

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_0654b4db864e4b9f9167c11ae7af5d08.png)

## 4.3 /clear – 清除对话历史

```bash
/clear
```
- 定义与语法： /clear 无参数。用于清除当前会话的对话历史，使 Claude 忘记之前的所有对话内容。执行后，相当于开启一个新会话，但不会退出 Claude Code 界面。
- 使用场景： 当对话持续很久、上下文累积过多时，可以使用 /clear 来重置上下文窗口，保持思路清晰。例如在完成一个独立任务后，开始新任务前执行 /clear，Claude 将从空上下文开始理解你的下一指令。这在任务切换时非常有用，可以避免旧话题干扰新需求。此外，当Claude的回答出现偏离正轨或上下文混乱时，/clear 可以一键“重启”对话。

## 4.4 /compact – 压缩对话内容

```bash
/compact
```
- 定义与语法： `/compact [instructions]` 可选附加“指令”参数。此命令会将当前对话历史总结压缩，并以该摘要作为新对话的开场上下文。可选的 instructions 参数允许你指定压缩时的侧重点，例如 /compact "保留尚未解决的问题" 会让 Claude 在总结时侧重未解决问题部分。
- 使用场景： 当会话长度接近模型上下文长度上限时，/compact 是延续长对话的救星。Claude 会将已有对话自动总结为更短的内容，从而释放大量上下文令牌供后续交流使用。这类似于有个 AI 秘书在会议途中帮你记录会议纪要，确保你们不会因为对话太长而“忘记”前情。不过，与 /clear 不同，/compact 保留了上下文的精华——在新会话中Claude仍可以参考之前对话的摘要继续讨论。

## 4.5 /memory – 编辑会话记忆文件

```bash
/memory
```
- 定义与语法： /memory 无参数。用于直接打开并编辑当前项目的持久记忆文件 CLAUDE.md（或用户级别的全局记忆文件），方便查看和修改 Claude 的“长期记忆”。你也可以通过这个命令向 CLAUDE.md 添加或移除内容。
- 使用场景： CLAUDE.md 是 Claude Code 用于初始化上下文的指南文件，通常包含项目简介、架构要点、代码惯例等。通过 /memory 命令，你可以随时更新该文件的内容：比如在初始化项目后发现 CLAUDE.md 漏掉了一些关键业务术语解释，可以输入 /memory 打开文件，在其中添加术语解释列表并保存。保存退出后，可以 /clear 然后开始新会话，Claude 将自动参照更新后的 CLAUDE.md 来回答问题，减少对术语的误解。
- 一般选择当前项目记忆

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_bbd144acf26d46139d43b1a04da1b88a.png)  
  
![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_5ed76e71fbe945c3b4fa50984e5a5872.png)

> 简单理解就是：  
> Project memory = 这个项目的专属规则/偏好  
> User memory = 你个人的全局习惯/偏好，跨项目通用  
> Auto-memory = 让 Claude 自己决定什么值得记，自动写入，不用你手动管

举几个典型场景：

1. **Project memory（项目记忆）** `./CLAUDE.md`

> 适合写跟这个项目强绑定的内容

- "这是一个 React + TypeScript 项目，使用 pnpm"
- "不要修改 `src/legacy/` 目录下的任何文件"
- "测试命令是 `pnpm test` ，构建是 `pnpm build` "
- "API 接口统一放在 `src/api/` ，不要分散"
1. **User memory（用户记忆）** `~/.claude/CLAUDE.md`

> 适合写跟你个人习惯相关、所有项目通用的内容

- "回复一律用中文"
- "代码注释保持简洁，不要废话"
- "提交信息用英文，格式 `feat: xxx` "
- "不要主动帮我重构我没提到的代码"
1. **Auto-memory（自动记忆）**

> Claude 自己判断什么重要，自动写入，比如你在对话中说了：

- "我们公司规定所有接口要加错误边界处理"——Claude 自动记下来
- "这个项目不用写单元测试"——自动记下来，下次不再建议你写测试

---

总结就是： **项目记忆管"这个项目怎么做"，用户记忆管"我这个人怎么工作"，自动记忆省去你手动整理的麻烦** 。

## 4.6 /status – 会话状态检查

```bash
/status
```

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_cc1c5bdd0b9c43e9a26f5b8b2c4d503b.png)

- 定义与语法： /status 无参数。显示当前 Claude Code 会话和系统状态，包括工作目录、登录账户、所用模型、加载的项目记忆等。这是一条只读命令，不会更改任何设置。
- 使用场景： 当你需要确认当前环境时（例如切换目录后不确定Claude是否跟随了新项目，或刚切换模型后想验证当前模型名），/status 可以立刻给出答案。它也是排查问题的起点：如果Claude行为异常，先看一下 /status 是否仍指向正确的路径和模型，是否有正确加载 CLAUDE.md 等。

## 4.7 /cost – 令牌与费用统计

```bash
/cost
```

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_aca9bc0ba3c945f28b570323c52162fd.png)

- 定义与语法： /cost 无参数。用于显示当前会话的令牌使用量统计，包括提示和回答分别用了多少 token，以及预估的 API 消耗费用。这对掌控 Claude Code 的使用成本非常有帮助。
- 使用场景： 如果你使用按量计费的API密钥或免费额度，随时关注对话的 token 消耗情况是个好习惯。执行 /cost 可以让你了解目前这场对话累计用了多少 token，并据此估算花费。在长时间编程会话或密集代码生成功能中，偶尔检查 /cost 有助于及时止损：发现token飙升可以选择提问更具体、压缩上下文等节约开销。另外，当你打算结束当天工作时，可以用 /cost 获取会话用量总结，核对是否在预算之内。

## 4.8 /config – 查看或修改配置

```bash
/config
```

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_fbe597b55ca24470a283e09d69db484e.png)

- 定义与语法： /config 可交互式查看和修改 Claude Code 配置参数。执行命令会显示配置菜单，你可以根据提示修改设置，例如启用/禁用自动压缩、设置主题、切换编辑模式等。部分配置也支持通过子命令直接设置，比如 /config set autocompact off 等。
- 使用场景： Claude Code 提供许多可定制选项，通过 /config 你可以根据个人习惯进行调整。例如：Autocompact（自动压缩）默认开启以防止上下文溢出，通常建议保持开启；待办事项（to-do）功能可以让Claude Code在长任务中列步骤，你可在配置中启用/停用；verbose输出用于调试，可通过 /config 打开，当需要看Claude内部推理步骤时很有用（对应快捷键 Ctrl+R 切换verbose模式）；还有主题配色、通知方式（如终端铃声提醒Claude完成思考）、编辑模式等。总之，/config 是你的个性化Claude控制面板。

## 4.9 /model – 切换AI模型版本

```bash
/model
```
- 定义与语法： /model \[model\_name\]。不带参数时通常会显示当前使用的模型，并提示可选模型列表；指定参数则可切换Claude所用的AI模型。Claude Code 常用的模型代号包括 Sonnet（较快、上下文较短）和 Opus（较慢但能力更强、上下文长度更大）等，或具体版本如 claude-4-100k 等。
- 使用场景： 根据任务需要选择合适的模型，能在速度和质量间取得平衡。默认情况下Claude Code启动用的是较快的模型。当你需要更深入的分析、更大的上下文或更高准确度时，可以通过 /model opus 切换到能力更强的模型。例如复杂架构设计讨论、批量代码重构等场景，Opus模型（类似GPT-4之于GPT-3.5的角色）会表现更佳。而在简单问答或需要快速响应的场景下，继续使用Sonnet模型更高效。/model 让你动态调整AI助手的大脑，以匹配任务要求。

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_662e1ae046bb4f079d0416a711403874.png)

**模型选项**

| 选项 | 含义 |
| --- | --- |
| `1. Default` | 当前默认模型是 `qwen3-max-2026-01-23` |
| `2. Sonnet (1M context)` | 均衡型，性价比高，适合日常编码 |
| `3. Opus (1M context)` | 最强模型，适合复杂架构/难题，但最慢最贵 |
| `4. Haiku` | 最快最便宜，适合简单问答/快速任务 |

**价格** `$3/$15 per Mtok` = 输入 $3 / 输出 $15（每百万 token）

**底部两个设置**

| 项目 | 含义 |
| --- | --- |
| `◐ Medium effort` | 思考力度，← → 可调节，分 low / medium / high，越高越慢越费 token |
| `/fast` | 快速模式，仅 Opus 可用，关闭深度思考，速度更快 |

---

**一般怎么选：**

- 日常写代码 → **Sonnet**
- 复杂重构/架构设计 → **Opus** （配合 Plan Mode 效果最好）
- 简单问题/快速查询 → **Haiku**

## 4.10 /doctor – 环境健康检查

```bash
/doctor
```
- 定义与语法： /doctor 无参数。执行后Claude Code会检查当前安装环境的健康状态，验证所需依赖和权限是否正确配置，并报告潜在问题。
- 使用场景： 当Claude Code行为异常（比如无法读取文件、工具调用总是失败等），/doctor 是排查问题的第一步。它会自动检查：Anthropic API连通性、已登录账户有效性、必需的依赖（git、GitHub CLI、ripgrep等）是否安装、Claude Code所需的文件权限是否授予等等。检查完后会输出一份报告，指出哪些项目通过，哪些存在问题。例如 “✘ 未检测到 GitHub CLI，请安装以使用 PR 功能” 或 “当前Anthropic API凭据无效” 等。有了这些信息，你可以据此修复环境，然后重试之前的操作。

![image.png](https://ucc.alicdn.com/pic/developer-ecology/bjq2ogst3ulqs_c627d0c167cd4be6b461859e50e0658d.png)

## 5\. Claude Code 进阶实战指南

## 5.1 核心理念

Claude Code 的真正价值不在于某个单一功能，而在于将命令、模型、记忆、模式 **串联成流** 。开发者负责方向和判断，Claude 负责执行和细节。

---

## 5.2 一套完整的开发工作流

以"接手新项目并开发新功能"为例，展示如何从头到尾组合使用各项能力。

### 第一步：初始化项目认知

进入项目目录后，第一件事不是写代码，而是让 Claude 先"读懂"项目。

```bash
/init
```

自动扫描代码库，生成 `CLAUDE.md` 初稿，包含技术栈、目录结构、常用命令等基础信息。生成后用 `/memory` 打开，补充人工经验：

```bash
- 不要修改 src/legacy/ 目录
- 提交信息格式：feat: / fix: / chore:
- 测试命令：pnpm test
```

这份记忆会在之后每次对话自动加载，省去反复交代背景的成本。

---

### 第二步：理解代码结构（Plan Mode）

熟悉陌生代码库，Plan Mode 是最安全的方式——只读不改，专注理解。

```bash
Shift+Tab × 2  →  进入 Plan Mode
```

然后自然语言提问：

```bash
分析 src/auth/ 模块的整体架构，梳理用户登录的完整调用链
```

Claude 会遍历相关文件、整理逻辑、输出结构图和说明，全程不碰任何代码。遇到复杂架构时，切换到 Opus 模型，思考更深：

```bash
/model  →  选择 Opus
```

---

### 第三步：规划新功能（Plan Mode + Opus）

理解现有代码后，继续在 Plan Mode 里规划新功能，不要急着切换到执行模式。

```bash
我需要给登录模块加上 OAuth 支持，请分析现有代码结构，
制定一个改动最小、风险最低的实现方案
```

Claude 输出计划后，用 `Ctrl+G` 直接打开计划文件编辑，删掉不需要的步骤、补充业务约束，比对话描述修改精准得多。

> 💡 这一步不要省。花 10 分钟确认计划，能避免后面返工 1 小时。

---

### 第四步：分模块执行（Auto-Accept + 后台任务）

计划确认后，切换到 Auto-Accept 模式开始执行：

```bash
Shift+Tab × 1  →  进入 Auto-Accept 模式
```

对于耗时操作（跑测试、编译），挂到后台：

```bash
Ctrl+B  →  后台执行
Ctrl+T  →  查看任务进度
```

前台继续和 Claude 讨论下一个模块，互不干扰。

**每完成一个独立模块，及时 `/clear` ，避免上下文污染下一个任务：**

```bash
/clear
```

对话变长但还没到切换模块的时机，用 `/compact` 压缩而非清空：

```bash
/compact "保留 OAuth 登录相关的讨论和决策"
```

---

### 第五步：性能分析与优化

功能开发完成后，切回 Plan Mode，让 Claude 做一轮审视：

```bash
Shift+Tab × 2  →  Plan Mode
分析刚才新增的代码，找出潜在的性能问题和安全隐患，不要修改，只给报告
```

确认问题后，再切换到执行模式针对性优化。这样比"边写边优化"更清晰，也不容易引入新问题。

---

### 第六步：收尾与记忆沉淀

开发完成后，用 `/memory` 把这次积累的项目经验写进 CLAUDE.md：

```bash
- OAuth 相关逻辑统一在 src/auth/oauth/ 下
- 新增第三方登录时参考 GoogleOAuthProvider 的实现模式
```

下一个功能开发、或者团队其他人接手时，这些经验直接生效。

---

## 5.3 模式与模型的选用原则

| 阶段 | 模式 | 模型 |
| --- | --- | --- |
| 读代码 / 规划 | Plan Mode | Opus |
| 日常编码 | Default | Sonnet |
| 重复性修改 | Auto-Accept | Sonnet / Haiku |
| 快速问答 | Default | Haiku |

---

## 5.4 一句话总结

> **Plan Mode 想清楚 → Auto-Accept 执行 → /compact 或 /clear 管理上下文 → /memory 沉淀经验**

把这条主线跑顺，Claude Code 才算真正用起来了。