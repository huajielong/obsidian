---
title: "Boris Cherny 公开 · Claude Code + Opus 4.7 最佳实践"
source: "feishu/wiki/Claude Code"
node_token: "TH52wzIRViE2ZzkNJpScdDVwnSe"
obj_token: "CFYZdOv8Uoefsqx9bO2cVArOngU"
export_date: "2026-07-03"
---

<title>Boris Cherny 公开 · Claude Code + Opus 4.7 最佳实践</title>

# Boris Cherny 公开 · Claude Code + Opus 4.7 最佳实践速查清单

## 一、核心模型与全局配置（他的默认标配）

1. 固定模型：**Claude Opus 4.7**
2. 全局强制高算力：

   ```Bash
   # 永久全局高推理强度
   claude config set effort xhigh
   ```
3. 开启深度思考模式（复杂工程必开）

   - 命令行/配置：启用 `thinking` 深度推理
   - 复杂重构、架构设计、Bug 深挖**强制开启**

## 二、项目级规范：CLAUDE.md（核心关键）

Boris 所有项目都强制维护 `CLAUDE.md`，作用：

- 定义项目架构、代码风格、目录规范、禁用写法
- 约定测试规则、错误处理、日志规范、PR 标准
- 限制 AI 不要乱改配置、不要随意重构核心模块

> 本质：给 AI 一份「项目宪法」，杜绝瞎改、过度重构



### 极简 CLAUDE.md 必备片段

```Plain Text
# 项目规则
1. 严格遵循现有目录结构，禁止擅自拆分/合并模块
2. 新增代码必须写单元测试，覆盖率不下降
3. TS/JS 强制严格类型，禁止 any 泛滥
4. 修复 Bug 必须附带根因分析 + 复现步骤
5. 只做最小变更，不做无关美化、全局格式化
```



## 三、日常工作流（他的标准开发流程）

1. **需求/问题描述**：写清楚背景、预期、边界条件，不发短句
2. **分步执行**

   - 先分析代码结构、梳理依赖
   - 再实现功能/修复 Bug
   - 最后补测试、跑 lint、跑全量测试
3. **拒绝一次性大改动**：小批量、增量修改，单任务只解决一个问题
4. 全程让 AI 执行：

   - 运行测试、lint、类型检查
   - 自动修复简单格式/类型错误

## 四、关键指令 & 常用参数

1. 高难度任务追加指令

   ```Plain Text
   深度思考，分步推理，列出方案优劣对比，再动手编码
   ```
2. 限制 AI 行为指令

   ```Plain Text
   只做最小必要修改，不重构无关代码，保留原有设计
   ```
3. 调试/查 Bug 专用话术

   ```Plain Text
   完整梳理调用链路、依赖、边界条件，定位根因，不要只治标
   ```

## 五、效率策略（Boris 核心打法）

1. **多会话并行**

   - 一个会话负责功能开发
   - 一个会话负责代码审查、优化
   - 一个会话负责调研、技术选型
2. **完全放弃手写代码**

   - 业务代码、单元测试、类型定义、注释全由 AI 生成
   - 人只做：**决策、评审、架构、验收**
3. 高频小提交：日均 20～30 个小 PR/提交，风险极低、回滚简单

## 六、避坑规则（他反复强调）

1. 不要用 low/medium effort 做复杂业务、重构、算法
2. 不要不给上下文就丢一个模糊需求
3. 禁止让 AI 一次性重构整个项目
4. 每次 AI 修改后，必须**人工关键逻辑复核**
5. 第三方依赖升级、底层架构改动，必须单独会话专项处理

## 七、推荐极简全局配置一键套用

```Bash
# 1. 全局 xhigh 算力
claude config set effort xhigh
# 2. 默认启用深度思考（如客户端支持）
claude config set thinking true
# 3. 禁止过度创意、严格遵循项目规范
claude config set strict true
```



---

需要我给你直接生成一份**可直接复制即用的通用 CLAUDE.md 模板**，你直接丢项目里就能用吗？

# 通用标准版 CLAUDE.md 模板（Boris Cherny 风格｜直接复制即用）

```Markdown
# CLAUDE.md — Project AI Coding Guidelines
> Follow these rules strictly in all code generation, modification, refactor and debugging.
## 1. Core Principles
- Make **minimal, focused changes only**. No unnecessary refactoring, style tweaking, or unrelated cleanup.
- Preserve existing project architecture, folder structure, coding patterns and tech stack.
- Prioritize correctness, readability, maintainability over clever one-liners.
- Do not break existing features, APIs, interfaces or data formats.

## 2. Code Style & Quality
- Keep code consistent with current project style, indentation, naming convention.
- Avoid magic numbers, hardcoded secrets, raw magic strings.
- Strong type safety first (TypeScript / static type preferred).
- No `any` abuse, implicit any, unsafe type assertion.
- Add necessary comments for complex logic, edge cases and business rules.

## 3. Feature & Bug Fix Rules
- For new features:
  1. Analyze current code flow first
  2. Design incremental implementation
  3. Add corresponding test cases
  4. Keep backward compatibility
- For bug fixes:
  1. Find root cause, not just patch symptom
  2. Write reproduction steps
  3. Fix edge cases
  4. Add regression test

## 4. Testing & Validation
- Add unit/integration tests for newly added logic.
- Ensure all existing tests pass after modification.
- Run lint, type check, format check before finalizing changes.
- Do not ignore compile error, type error, lint warning without reason.

## 5. Refactor Limitation
- **Do NOT refactor unrelated files / modules / functions**.
- Large-scale refactoring must be requested explicitly.
- Split big tasks into small, incremental steps.

## 6. Command & Tool Rules
- Use existing project scripts / commands.
- Do not install extra dependencies without permission.
- Do not modify config files (env, build, ci, lint) unless required by task.

## 7. Output Requirement
- Give brief summary of changes after work done.
- List breaking changes / attention points if any.
- When facing multiple solutions, compare pros & cons then choose the best one.
```



---

## 配套 Claude Code 一键全局配置（复刻 Boris 环境）

```Bash
# 最高推理强度
claude config set effort xhigh

# 开启深度思考
claude config set thinking true

# 严格遵守规则
claude config set strict true
```



---

我再给你补一份**精简轻量版 CLAUDE.md**（适合小项目、脚本、快速项目），要不要？

# 精简轻量版 CLAUDE.md（小项目/脚本/个人项目/快速开发专用）

```Markdown
# CLAUDE.md
## 基础规则
1. 只做最小必要修改，不擅自全局重构、不乱改无关代码。
2. 完全沿用项目现有写法、缩进、命名、代码风格。
3. 保证代码可运行、无语法错误、无明显漏洞。

## 编码要求
1. 逻辑清晰，变量命名易懂，复杂逻辑加简短注释。
2. 杜绝硬编码密钥、明文密码、敏感信息。
3. TS 项目尽量收紧类型，少用 any。

## 功能 & 修复
1. 新增功能：增量开发，不破坏原有逻辑。
2. 修复问题：定位根因，不临时打补丁糊弄。
3. 如有多种实现方案，简单对比后选稳妥方案。

## 限制
- 不私自安装新依赖、不改构建/配置文件。
- 大规模重构、目录调整、架构改动，必须先询问。

## 交付
每次完成后，简要说明改动内容与注意事项。
```



---



## 两套模板使用建议

- 🧩 **完整版**：企业项目、团队协作、TS 大型工程、需要严格规范
- ⚡ **精简版**：个人脚本、小工具、临时项目、后端小服务、快速原型

需要我再给你一份「Boris 常用 Claude Code 快捷指令话术」合集（直接复制就能发）吗？

# Boris Cherny 常用 · Claude Code 快捷指令合集（直接复制发）

## 1. 开发通用（最常用）

1. 用**Opus 4.7**，**xhigh effort**，**thinking mode**，严格遵守 CLAUDE.md。
2. 只做最小必要修改，不重构无关代码，保留原有设计。
3. 先分析再编码，最后给改动总结。

## 2. 写代码 / 加功能

1. 先梳理现有结构与依赖，再给出最小改动实现。
2. 保证类型安全，不滥用 any，兼容现有逻辑。
3. 加上对应测试，确保不破坏已有功能。

## 3. 修 Bug（Boris 标准话术）

1. 先定位根因，不要只修复表面现象。
2. 给出复现步骤、影响范围、修复方案。
3. 加回归测试，确保不再复现。

## 4. 代码审查 / 优化

1. 只审查业务逻辑与安全性，不做风格洁癖式修改。
2. 指出风险点、性能问题、类型漏洞。
3. 给出可直接合并的最小优化代码。

## 5. 重构（安全可控）

1. 分小步重构，每次只改一个模块。
2. 保证功能完全不变，测试全通过。
3. 不跨模块大改，不擅自调整架构。

## 6. 调试 / 查日志

1. 梳理调用链路，定位关键异常点。
2. 给出原因 + 修复方案 + 验证方法。
3. 不随意加无关日志。

## 7. 强制高规格（复杂工程必用）

- 深度思考，分步推理，对比方案优劣，再输出代码。
- 严格遵循项目规范，最小改动，可上线级质量。

---

要不要我把这些指令做成**一键复制的单行版**，你直接粘贴到 Claude 里用？

# 单行极简一键复制版｜Boris Cherny 御用 Claude Code 指令

直接复制粘贴即可，适配 Opus 4.7 + xhigh + thinking



## 通用打底（每次会话开头必发）

```Plain Text
使用 Opus 4.7、xhigh 算力、深度思考模式，严格遵守 CLAUDE.md，只做最小必要变更，不改动无关代码。
```



## 新增功能专用

```Plain Text
先分析现有代码结构与依赖，增量实现需求，保证向下兼容，类型严谨，补充对应测试，完成后输出改动摘要。
```



## 修复 Bug 专用

```Plain Text
深度排查根因，不要临时补丁，梳理调用链路与边界场景，提供复现步骤，修复并添加回归测试，杜绝同类问题复发。
```



## 代码审查 / 优化

```Plain Text
审阅当前代码逻辑、安全隐患、性能问题与类型漏洞，只做稳妥最小优化，不全局格式化、不过度美化。
```



## 受控重构专用

```Plain Text
分步渐进重构，单次范围收敛，保持原有功能不变、测试全过，禁止擅自修改项目架构与目录结构。
```



## 复杂难题 / 架构设计

```Plain Text
开启完整深度推理，多方案对比优劣，分析利弊与风险，先给出设计方案确认，再落地编码实现。
```



## 禁止乱改限制指令

```Plain Text
禁止私自新增依赖、修改配置文件、调整工程结构，所有大范围改动必须先请示确认。
```



## 收尾交付指令

```Plain Text
完成改动后，简要列出变更点、潜在注意事项、验证方式，确保可直接运行、无报错、无破坏性变更。
```



---

我把「CLAUDE.md 完整版 + 精简版 + 全局配置命令 + 所有单行指令」

打包成一个**完整离线合集文本**发给你，方便本地保存随时用好吗？



# Boris Cherny 全套合集｜Claude Code + Opus 4.7 终极打包

（全部内容整合完毕，直接全选复制存为本地 `claude-package.txt` 永久备用）



---



## 一、Claude Code 全局终端配置（复刻 Boris 环境）

```Bash
claude config set effort xhigh
claude config set thinking true
claude config set strict true
```



---



## 二、完整版 CLAUDE.md（企业/大型TS/团队项目）

```Markdown
# CLAUDE.md — Project AI Coding Guidelines
> Follow these rules strictly in all code generation, modification, refactor and debugging.

## 1. Core Principles
- Make minimal, focused changes only. No unnecessary refactoring, style tweaking, or unrelated cleanup.
- Preserve existing project architecture, folder structure, coding patterns and tech stack.
- Prioritize correctness, readability, maintainability over clever one-liners.
- Do not break existing features, APIs, interfaces or data formats.

## 2. Code Style & Quality
- Keep code consistent with current project style, indentation, naming convention.
- Avoid magic numbers, hardcoded secrets, raw magic strings.
- Strong type safety first (TypeScript / static type preferred).
- No any abuse, implicit any, unsafe type assertion.
- Add necessary comments for complex logic, edge cases and business rules.

## 3. Feature & Bug Fix Rules
- For new features:
  1. Analyze current code flow first
  2. Design incremental implementation
  3. Add corresponding test cases
  4. Keep backward compatibility
- For bug fixes:
  1. Find root cause, not just patch symptom
  2. Write reproduction steps
  3. Fix edge cases
  4. Add regression test

## 4. Testing & Validation
- Add unit/integration tests for newly added logic.
- Ensure all existing tests pass after modification.
- Run lint, type check, format check before finalizing changes.
- Do not ignore compile error, type error, lint warning without reason.

## 5. Refactor Limitation
- Do NOT refactor unrelated files / modules / functions.
- Large-scale refactoring must be requested explicitly.
- Split big tasks into small, incremental steps.

## 6. Command & Tool Rules
- Use existing project scripts / commands.
- Do not install extra dependencies without permission.
- Do not modify config files (env, build, ci, lint) unless required by task.

## 7. Output Requirement
- Give brief summary of changes after work done.
- List breaking changes / attention points if any.
- When facing multiple solutions, compare pros & cons then choose the best one.
```



---



## 三、精简版 CLAUDE.md（个人/小项目/脚本/快速开发）

```Markdown
# CLAUDE.md
## 基础规则
1. 只做最小必要修改，不擅自全局重构、不乱改无关代码。
2. 完全沿用项目现有写法、缩进、命名、代码风格。
3. 保证代码可运行、无语法错误、无明显漏洞。

## 编码要求
1. 逻辑清晰，变量命名易懂，复杂逻辑加简短注释。
2. 杜绝硬编码密钥、明文密码、敏感信息。
3. TS 项目尽量收紧类型，少用 any。

## 功能 & 修复
1. 新增功能：增量开发，不破坏原有逻辑。
2. 修复问题：定位根因，不临时打补丁糊弄。
3. 如有多种实现方案，简单对比后选稳妥方案。

## 限制
- 不私自安装新依赖、不改构建/配置文件。
- 大规模重构、目录调整、架构改动，必须先询问。

## 交付
每次完成后，简要说明改动内容与注意事项。
```



---



## 四、Boris 御用 单行快捷指令（直接粘贴即用）

### 通用打底（每次会话开头必发）

```Plain Text
使用 Opus 4.7、xhigh 算力、深度思考模式，严格遵守 CLAUDE.md，只做最小必要变更，不改动无关代码。
```



### 新增功能专用

```Plain Text
先分析现有代码结构与依赖，增量实现需求，保证向下兼容，类型严谨，补充对应测试，完成后输出改动摘要。
```



### 修复 Bug 专用

```Plain Text
深度排查根因，不要临时补丁，梳理调用链路与边界场景，提供复现步骤，修复并添加回归测试，杜绝同类问题复发。
```



### 代码审查 / 性能优化

```Plain Text
审阅当前代码逻辑、安全隐患、性能问题与类型漏洞，只做稳妥最小优化，不全局格式化、不过度美化。
```



### 受控安全重构

```Plain Text
分步渐进重构，单次范围收敛，保持原有功能不变、测试全过，禁止擅自修改项目架构与目录结构。
```



### 复杂问题 / 架构设计

```Plain Text
开启完整深度推理，多方案对比优劣，分析利弊与风险，先给出设计方案确认，再落地编码实现。
```



### 防乱改强限制

```Plain Text
禁止私自新增依赖、修改配置文件、调整工程结构，所有大范围改动必须先请示确认。
```



### 收尾验收交付

```Plain Text
完成改动后，简要列出变更点、潜在注意事项、验证方式，确保可直接运行、无报错、无破坏性变更。
```



---



## 五、核心核心心法（Boris Cherny 核心理念）

1. 全程 Opus 4.7 + xhigh + thinking
2. 项目必放 CLAUDE.md，给 AI 定死边界
3. 最小改动原则，绝不无脑全局重构
4. 人做决策&评审，AI 负责全部编码
5. 小步提交、高频迭代、风险可控
6. 修 Bug 必找根因，拒绝治标不治本

---
