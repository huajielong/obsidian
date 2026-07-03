---
title: "GSD Core安装到Claude Code"
source: "feishu/wiki/Claude Code"
node_token: "MZFmw5ikyitoyZk5b1lc0enXn3e"
obj_token: "CVyWdgzdjo64pHxvVuacE6Aunuy"
export_date: "2026-07-03"
---

# GSD Core安装到Claude Code

## 📦 安装 GSD Core 到 Claude Code



### **前置条件**：node.js 版本需要

```Plain Text
# 在 CentOS 上执行
☐ node --version           # 必须 >= 22.13.0
☐ npm --version            # 必须 >= 10.9.8
```

官网：https://nodejs.org/zh-cn/download

建议node.js使用版本：v22.23.1

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YWFkMGI0ODAwYzYyNTA1YjEwMTc2MDI0NDkwNmViN2NfN2UyMzE1N2ZiYTZjYWYxMmUzMzNmZDBlNjZjZWRkOTFfSUQ6NzY1NDg3NjQ1OTE2NjQ2OTMzMl8xNzgzMDcwMDY5OjE3ODMwNzM2NjlfVjM)

### **方法 1：NPX 一行命令（推荐）**



```Bash
npx @opengsd/gsd-core@latest
```



然后：

1. 选择 runtime → 选 **Claude Code**
2. 选择 scope → 选 **global**（全局）或 **local**（项目级）
3. 等待安装完成

### **方法 2：手动从源码安装（开发者向）**



如果你想从 GitHub 最新代码安装：



```Bash
git clone https://github.com/open-gsd/gsd-core
cd gsd-core
npm install
node scripts/build-hooks.js
node bin/install.js --claude --global
```



完成后**重启 Claude Code**，hooks 才会生效。



---



## ✅ **验证安装成功**



在 Claude Code 的任何对话里，输入：



```Plain Text
/gsd-help
```



你应该会看到所有可用的 GSD 命令列表。



或者直接开始：



```Plain Text
/gsd-new-project
```

<callout emoji="🥇">
 已有代码库？先运行 /gsd-map-codebase 让 GSD 了解你的代码
</callout>

系统会提示你：

1. 输入项目理念
2. 进行自适应问卷（GSD 会问问题理解需求）
3. 生成 `ROADMAP.md` 和 `.planning/` 目录

---



## 🚀 **快速开始流程**



### **第 1 步：初始化项目**



在任何 Claude Code 对话里：



```Plain Text
/gsd-new-project
```



**GSD 会问你：**

- 你要做什么项目？（例如："一个 AI 笔记应用"）
- 用什么技术栈？
- 主要功能是什么？
- 有什么约束？

然后 GSD 会：

1. 自动启动 4 个并行 researcher agent → 研究技术栈、特性、架构、陷阱
2. 生成 `ROADMAP.md`（分解成多个 phase）
3. 生成 `REQUIREMENTS.md`（v1/v2/out-of-scope）
4. 创建 `.planning/` 目录

### **第 2 步：讨论第一个 phase**



```Plain Text
/gsd-discuss-phase 1
```



GSD 会问你关于实现的具体决策：

- UI 是怎样的？
- API 如何设计？
- 数据库结构？
- 错误处理？

生成 `01-CONTEXT.md`（记录所有决策）



### **第 3 步：规划第一个 phase**



```Plain Text
/gsd-plan-phase 1
```



GSD 会：

1. 研究生态（npm 包、最佳实践）
2. 拆分成原子 plan（2-3 个 task 每个）
3. 生成 `01-01-PLAN.md`、`01-02-PLAN.md` 等
4. Plan Checker 验证质量（最多 3 次迭代）

### **第 4 步：执行**



```Plain Text
/gsd-execute-phase 1
```



GSD 会：

1. 分析 plan 依赖 → 分组成 Wave
2. **并行启动多个 executor**（各自 fresh 200K context）
3. 每个 executor 写代码 + 原子 commit
4. 生成 `01-01-SUMMARY.md` 等
5. Verifier 检查是否达到目标

### **第 5 步：验证**



```Plain Text
/gsd-verify-work 1
```



GSD 会：

1. 问你每个功能是否工作
2. 有问题？自动诊断 + 生成 fix plan
3. 生成 `01-UAT.md`

### **第 6 步：交付**



```Plain Text
/gsd-ship 1
```



GSD 会：

1. 推送分支
2. 生成 PR（自动写 body）
3. 更新 `STATE.md`

然后进下一个 phase...



---



## 🎯 **常用命令速查**



```Bash
# 项目级
/gsd-new-project               # 初始化新项目
/gsd-progress --next           # 自动检测下一步（不用记命令）
/gsd-progress --do "xxx"       # 自然语言路由（例如"我要修复 bug"）

# Phase 工作流（完整）
/gsd-discuss-phase 1           # 讨论决策
/gsd-plan-phase 1              # 规划
/gsd-execute-phase 1           # 执行
/gsd-verify-work 1             # 验证
/gsd-ship 1                    # 交付 PR

# 快速模式（跳过验证）
/gsd-quick "add dark mode"     # 快速任务（<1 小时）
/gsd-quick --full              # 包含 plan checker + verifier

# 自动化
/gsd-autonomous                # 自动 discuss→plan→execute 全部剩余 phase
/gsd-autonomous --from 2       # 从 phase 2 开始

# 工具
/gsd-stats                     # 项目统计
/gsd-debug "bug description"   # 系统化调试
/gsd-capture "idea"            # 快速笔记
/gsd-health                    # 检查项目健康度
```



---



## 📂 **安装后的文件结构**



```Plain Text
~/.claude/                          # Claude Code 全局目录
├── gsd-core/
│   ├── bin/gsd-tools.cjs          # CLI 工具
│   ├── workflows/                 # 工作流定义
│   ├── references/                # 共享知识文档
│   └── templates/                 # 模板
├── agents/gsd-*.md                # 33 个专门化 agent
├── commands/gsd/*.md              # 60+ 个 GSD 命令
├── hooks/                         # 运行时 hooks（context 监控等）
└── settings.json                  # Hook 注册

你的项目目录
└── .planning/                     # GSD 会在这里创建
    ├── PROJECT.md
    ├── REQUIREMENTS.md
    ├── ROADMAP.md
    ├── STATE.md
    ├── config.json
    ├── research/
    ├── phases/
    │   ├── 01-phase-name/
    │   │   ├── 01-CONTEXT.md
    │   │   ├── 01-RESEARCH.md
    │   │   ├── 01-01-PLAN.md
    │   │   ├── 01-01-SUMMARY.md
    │   │   └── 01-VERIFICATION.md
    │   └── 02-phase-name/
    └── debug/
```



---



## ⚙️ **安装选项**



### **Global 安装（推荐）**

```Bash
npx @opengsd/gsd-core@latest --claude --global
```

- 好处：一次安装，所有项目都能用
- 坏处：会修改 `~/.claude/` 目录

### **Local 安装（项目级）**

```Bash
npx @opengsd/gsd-core@latest --claude --local
```

- 好处：只影响当前项目，`.claude/` 在项目根目录
- 坏处：每个项目要装一次

### **更新 GSD**

```Bash
/gsd-update
```

会自动检查新版本 + 备份本地修改



### **卸载 GSD**

```Bash
npx @opengsd/gsd-core@latest --claude --uninstall
```



---



## 🔧 **安装后配置（可选）**



进任何项目后：



```Plain Text
/gsd-settings
```



可以配置：

- `model_profile`：选 `quality`（Opus）/ `balanced`（Sonnet）/ `budget`（Haiku）
- `workflow.plan_check`：是否启用 Plan Checker
- `workflow.verifier`：是否启用自动验证
- `git.branching_strategy`：git 分支策略
- 等等...

---



## 💡 **第一个项目推荐流程**



```Bash
# 1. 安装
npx @opengsd/gsd-core@latest

# 2. 在 Claude Code 里
/gsd-new-project
# 输入你的项目想法，回车

# 3. 等 GSD 生成规划（几分钟）

# 4. 开始第一个 phase
/gsd-discuss-phase 1

# 5. 用 /gsd-progress --next 自动找下一步
# （这样就不用记命令了）

# 6. 完成所有 phase 后
/gsd-autonomous --from 1
# 自动处理剩余 phases
```



---



## ⚠️ **注意事项**



1. **Node.js 版本**：需要 Node 22+

   ```Bash
   node --version  # 检查，如果 <22，升级
   ```
2. **Git 初始化**：项目要先 `git init` 或在 git 仓库里

   ```Bash
   cd your-project
   git init
   ```
3. **重启 Claude Code**：安装后一定要重启，hooks 才会加载
4. **`.planning/` 建议提交到 Git**：这样团队协作时信息不丢失

   ```Bash
   # 但也可以加到 .gitignore
   echo ".planning/" >> .gitignore
   ```

---



**现在就可以试了！** 🚀



在 Claude Code 里输入 `/gsd-new-project`，开始你的第一个项目吧。
