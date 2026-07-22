---
title: "Programmable Skills（可编程 Skill 系统）"
type: concept
tags: [Skills, 可编程, 动态加载, 热更新, 权限管控, 工程化, Claude Code]
sources:
  - wiki/sources/摘要-awesome-agentic-ai-zh-claude-code-ecosystem.md
  - wiki/sources/摘要-adk-agents-with-skills.md
  - wiki/sources/摘要-awesome-agentic-ai-zh-advanced-concepts.md
last_updated: 2026-07-22
---

# Programmable Skills（可编程 Skill 系统）

## 定义

Programmable Skills 是指**将 Skill 从静态 Markdown 行为描述提升为可编程、可动态管理的工程化组件**的系统实践。它涵盖 Skill 的动态加载、热更新、版本管理、权限管控、依赖管理以及运行时生命周期管理，是 [[Claude_Code_Skills]] 从"用户手工编写"向"平台级工程化"演进的关键能力。

> 如果说 [[Claude_Code_Skills]] 定义了 Skill "是什么、怎么写"，Programmable Skills 则定义了 Skill "怎么管、怎么跑、怎么治理"。

---

## 为什么需要 Programmable Skills？

### 静态 Skills 的局限性

| 问题 | 表现 | 后果 |
|------|------|------|
| **缺乏动态性** | 每次修改 SKILL.md 需要手动编辑文件 | 无法响应运行时上下文变化 |
| **无版本管理** | Skill 变更不可追溯、不可回滚 | 团队协作混乱 |
| **无依赖管理** | Skill 间共享代码只能复制粘贴 | 维护成本随 Skill 数量线性增长 |
| **权限粗粒度** | Skill 要么全部加载要么不加载 | 无法精细化管控 Skill 能做什么 |
| **无健康检查** | Skill 出错时静默失败 | 用户感知不到 Skill 是否生效 |

### Programmable Skills 的解决方案

```
静态 Skill           →    Programmable Skill
─────────────────────────────────────────────
手动编辑 SKILL.md    →    声明式配置 + 动态注册
单一文件             →    模块化结构（代码/配置/资源分离）
无版本管理           →    SemVer + 兼容性校验
文件级权限           →    接口级权限声明 + 运行时拦截
无依赖管理           →    显式依赖声明 + 自动解析
无生命周期           →    Load → Init → Ready → Unload
```

---

## 核心能力

### 1. 动态加载与发现

Skill 的动态加载不再是"启动时扫描文件系统"的静态模式，而是支持运行时注册与卸载的灵活机制。

#### 加载模式对比

| 模式 | 时机 | 适用场景 | 示例 |
|------|------|---------|------|
| **静态加载** | Session 启动时扫描 `.claude/skills/` | 稳定的基础 Skill | code-review, pdf |
| **按需加载** | 检测到特定上下文时自动触发 | 场景特定 Skill | CI/CD Skill 仅在检测到 GitHub Actions 时加载 |
| **延迟加载** | 用户显式请求或首次命中时加载 | 低频大 Skill | 部署流水线 Skill, 数据库迁移 Skill |
| **热加载** | 运行时检测到文件变更自动重载 | 开发调试阶段 | 正在编写的 Skill 实时生效 |

#### 动态发现机制

```yaml
# Skill 的注册元数据（在 SKILL.md frontmatter 之外扩展）
skill_registry:
  triggers:
    - pattern: "**/Dockerfile"          # 文件存在时触发
    - command: "deploy:*"               # 命令模式匹配
    - context: "has_docker_compose"     # 上下文条件
  dependencies:
    - skill: "code-review"              # 依赖其他 Skill
    - tool: "docker"                    # 依赖外部工具
  conflicts_with:
    - "legacy-deploy-skill"             # 与旧 Skill 冲突
```

### 2. 热更新机制

热更新允许 Skill 在不中断当前 Session 的情况下被修改和重新加载。

#### 热更新流程

```
开发者修改 SKILL.md / 依赖文件
        ↓
文件系统监测到变更（inotify / Watchdog）
        ↓
版本差异计算（diff from last loaded version）
        ↓
兼容性检查（breaking change detection）
    ┌───┴───┐
    ↓        ↓
  兼容     不兼容
    ↓        ↓
原子加载   提示用户 reload / restart
    ↓
验证新版本功能正常
    ↓
旧版本标记为 stale，保留作为回滚点
```

#### 热更新的安全约束

| 约束 | 说明 | 违反后果 |
|------|------|---------|
| **必须保持 interface 兼容** | Skill 对外暴露的 Hook/Tool 签名不可变 | 其他依赖此 Skill 的组件可能崩溃 |
| **必须通过健康检查** | 新版本必须通过自检才能生效 | 自动回滚到上一版本 |
| **变更必须可追溯** | 每次热更新记录到 Skill 变更日志 | 无法 debug 回归问题 |
| **资源泄漏防护** | 旧版本持有的资源必须释放 | 内存/文件句柄泄漏 |

### 3. 权限管控

Programmable Skills 的权限模型超越了传统的文件级权限，走向**接口级精细化权限**。

#### 四层权限模型

```
Layer 1: Skill 可见性
  ├── Public：任何人都可以发现和使用
  ├── Workspace：仅当前工作区可见
  ├── Role：仅特定角色（admin/maintainer）可见
  └── Private：仅创建者可见

Layer 2: 加载权限
  ├── Auto-load：匹配条件自动加载（默认）
  ├── Prompt：加载前必须得到用户确认
  └── Manual：仅当用户显式请求时才加载

Layer 3: 执行权限
  ├── 文件系统：Skill 能读/写哪些路径
  ├── 网络：Skill 能访问哪些域名/端口
  ├── 工具：Skill 能调用哪些 MCP 工具
  └── 环境变量：Skill 能读取哪些 ENV

Layer 4: 资源配额
  ├── Token 预算：单次执行最大 Token 消耗
  ├── 执行时间：最大执行时长
  ├── 并发限制：最大并行实例数
  └── 存储限制：临时文件最大空间
```

#### 与现有权限系统的整合

[[Skills权限管理]] 提供了 Skills 全生命周期授权体系的基础框架，Programmable Skills 在此之上增加：

| 能力 | 静态 Skill | Programmable Skill |
|------|-----------|-------------------|
| **权限粒度** | Skill 整体 | Skill 内每个 Tool/Hook 可独立授权 |
| **运行时告警** | 越权时静默失败 | 越权时触发告警，提示用户调整 |
| **权限继承** | 无 | Skill B 可继承 Skill A 的部分权限 |
| **临时授权** | 无 | 单次执行提升权限（如：本次允许写 /etc）|
| **审计日志** | 无 | 每次权限检查记录到 audit trail |

### 4. 版本与依赖管理

#### Skill 版本规范

```yaml
version: 1.2.3
api_version: 2                   # Skill 框架 API 版本
compatibility:
  claude_code: ">=1.0.0, <2.0.0" # Claude Code 版本约束
  platform: ["linux", "macos"]   # 支持平台
  mcp_servers:                    # 需要哪些 MCP Server
    - name: "context7"
      version: ">=1.0"
dependencies:
  skills:
    - name: "code-review-base"
      version: "~1.2"
      optional: true             # 可选依赖
  tools:
    - name: "git"
      version: ">=2.30"
```

#### 依赖解析策略

```
Skill A ──depends on──▶ Skill B ──depends on──▶ Skill C (v1.0)
  │                                                 │
  └───────also depends on───────────────────────────┘
                         ↓
                  依赖解析结果：
                  - Skill C 只加载一个版本
                  - 版本兼容检查（无冲突）
                  - 加载顺序：C → B → A
```

### 5. 生命周期管理

Programmable Skill 有明确定义的生命周期状态：

```
          ┌──────────────────────────────┐
          │          Skill Registry       │
          │  (元数据索引，不加载内容)        │
          └──────────┬───────────────────┘
                     │ 触发条件满足
                     ▼
          ┌──────────────────────────────┐
          │      LOADING（加载中）         │
          │  - 文件读取                   │
          │  - 依赖解析与加载              │
          │  - 接口注册                   │
          └──────────┬───────────────────┘
                     │ 加载成功
                     ▼
          ┌──────────────────────────────┐
          │      INITIALIZING（初始化中）   │
          │  - 健康检查                   │
          │  - 资源分配                   │
          │  - 环境校验                   │
          └──────────┬───────────────────┘
                     │ 初始化通过
                     ▼
  ┌──────────────────────────────────────────┐
  │              READY（就绪）                 │
  │  - 等待上下文匹配触发 Skill 执行            │
  │  - 或等待用户手动调用                      │
  └──────────────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │              │
              ▼              ▼
  ┌─────────────────┐  ┌─────────────────┐
  │   UNLOADING     │  │    ERROR        │
  │  - 资源释放      │  │  - 自动回滚     │
  │  - 注销接口      │  │  - 告警通知     │
  │  - 清理临时文件   │  │  - 尝试恢复     │
  └────────┬────────┘  └────────┬────────┘
           │                    │
           ▼                    │
  ┌────────────────┐            │
  │    UNLOADED    │◄───────────┘
  │  (已卸载)       │
  └────────────────┘
```

---

## 工程实现模式

### 模式 A：Skill 即插件（类比 VSCode Extension）

每个 Skill 是一个自包含的"插件包"，包含：

```
skills/<name>/
├── SKILL.md              ← 行为定义（主文件）
├── scripts/              ← 可执行脚本
│   ├── init.sh           ← 初始化脚本
│   ├── validate.sh       ← 健康检查脚本
│   └── cleanup.sh        ← 清理脚本
├── hooks/                ← 生命周期 Hook
│   ├── onLoad.ts         ← 加载时执行
│   ├── onUnload.ts       ← 卸载时执行
│   └── onError.ts        ← 错误处理
├── permissions.yaml      ← 权限声明（Layer 3）
├── package.json          ← 版本/依赖/元数据
└── evals/                ← 自测用例
    └── evals.json
```

### 模式 B：Skill 即微服务（类比 MCP Server）

Skill 作为一个独立服务运行，通过标准协议与主 Session 通信：

```
Claude Code Session
      │
      ├── Local Skill（进程内，SKILL.md 直接加载）
      │
      └── Remote Skill（进程外，通过 MCP 协议通信）
            │
            ├── Skill 服务进程（独立生命周期）
            ├── 可拥有独立的 Tool Registry
            └── 可分布在不同机器上
```

- **优势**：语言无关、进程隔离、独立扩缩容
- **劣势**：通信开销、部署复杂度高
- **适用**：企业级共享 Skill、计算密集型 Skill

### 模式 C：Skill 即流水线（类比 CI/CD Pipeline）

Skill 的执行过程被建模为流水线：

```yaml
pipeline:
  triggers:
    - on: "file:changed"
      pattern: "src/**/*.rs"
  stages:
    - name: "lint"
      run: "cargo clippy"
      on_failure: "cancel"
    - name: "test"
      run: "cargo test"
      on_failure: "report"
    - name: "build"
      run: "cargo build --release"
      on_failure:
        - notify: "#build-alerts"
        - retry: 2
```

---

## 与相邻概念的关系

| 概念 | 关系 | 区别 |
|------|------|------|
| **[[Claude_Code_Skills]]** | 基础层 | Claude_Code_Skills 是"编写规范"，Programmable Skills 是"工程化治理" |
| **[[Skill_Factory]]** | 互补 | Skill_Factory 是"运行时生成新 Skill"，Programmable Skills 是"管理已有的 Skill" |
| **[[Skills权限管理]]** | 子集 | Skills权限管理 是 Programmable Skills 中权限维度的展开 |
| **[[MCP]]** | 基础设施 | MCP 作为独立进程的协议层，为 Remote Skill 模式提供通信基础 |
| **[[Claude_Code_Plugins]]** | 打包层 | Plugin 是 Programmable Skill 的发行包格式 |
| **[[Claude_Code_Hooks]]** | 执行层 | Hooks 在 Skill 执行的关键时机注入拦截逻辑 |
| **[[Claude_Code_Dynamic_Workflows]]** | 编排层 | Dynamic Workflows 可调用多个 Programmable Skills 组成复杂流程 |
| **[[Progressive_Disclosure]]** | 设计模式 | Programmable Skills 的按需加载机制直接实现渐进式披露 |

---

## 前沿方向

| 方向 | 描述 | 探索状态 |
|------|------|---------|
| **Skill Marketplace** | 社区 Skill 的版本化发布/订阅/评分机制 | 早期 |
| **Skill Composition** | 多个 Skill 自动组合成复合 Skill | 概念验证 |
| **AOT Compilation** | Skill 预编译为二进制以减少加载延迟 | 实验阶段 |
| **Dependency Injection** | Skill 间通过接口注入依赖而非硬编码引用 | 设计阶段 |
| **Sandboxed Execution** | Skill 在安全沙箱中运行，限制系统调用 | 已有探索（[[Agent沙箱工程]]）|
| **Skill Telemetry** | Skill 调用统计、性能监控、异常追踪 | 早期 |

---

## 关联连接

- [[Claude_Code_Skills]] — Skill 系统的基础定义和编写规范
- [[Skills权限管理]] — Skill 权限管控的深入展开
- [[Skill_Factory]] — 运行时动态生成新 Skill 的元模式
- [[MCP]] — Skill 的通信协议基础设施（Remote Skill 模式）
- [[Claude_Code_Plugins]] — Skill 的打包与发行格式
- [[Claude_Code_Hooks]] — Skill 执行的关键时机拦截
- [[Claude_Code_Dynamic_Workflows]] — Skill 在复杂编排中的调用
- [[Progressive_Disclosure]] — Skill 按需加载的设计模式
- [[Agent沙箱工程]] — Skill 安全执行的环境基础
- [[Harness_Engineering]] — Programmable Skills 属于 Harness 层的行为治理维度
- [[Claude_Code_Harness]] — 7-Layer Architecture 中 Skill 的管理机制
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — Skills 架构基础来源
- [[摘要-adk-agents-with-skills]] — ADK 的 Skill 模式参考
- [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 进阶概念中关于 Skill 治理的参考
