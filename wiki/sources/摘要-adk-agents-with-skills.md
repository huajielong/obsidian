---
title: "开发者指南：使用 Skills 构建 ADK Agent"
type: source
tags: [ADK, Google, Agent, Skills, SkillToolset]
sources: 
  - raw/09-archive/developers-guide-to-building-adk-agents-with-skills.md
  - https://developers.googleblog.com/developers-guide-to-building-adk-agents-with-skills/
last_updated: 2026-07-06
---

# 开发者指南：使用 Skills 构建 ADK Agent

> **原文**: [Developer's Guide to Building ADK Agents with Skills](https://developers.googleblog.com/developers-guide-to-building-adk-agents-with-skills/)
> **作者**: Lavi Nigam（开发者关系工程师）& Shubham Saboo（高级 AI 产品经理）
> **发布日期**: 2026 年 4 月 1 日
> **来源**: Google Developers Blog

---

## 概述

AI Agent 能执行指令，但能不能自己编写指令？

Google Developers Blog 发表了一篇面向开发者的深度指南，介绍了 **Agent Development Kit (ADK) 中的 SkillToolset** 能力。

核心亮点在于**渐进式披露（Progressive Disclosure）** 架构，让 AI Agent 按需加载领域专业知识，最多可将基础上下文消耗降低 **90%**。

通过一种被称为 **Skill 工厂（Skill Factory）** 的设计模式，Agent 甚至可以在运行时动态生成全新的 Skill 定义，实现自我扩展。

---

## AI Agent 的知识膨胀难题

做 AI Agent 开发的人大多遇到过同一个问题——系统提示词（System Prompt）随着业务场景增多而不受控制地膨胀。SEO 规则、代码审查规范、API 接口文档、合规审计流程、数据处理规范，所有领域的知识被一股脑地塞进一个巨大的指令字符串里。

### Token 浪费与成本问题

假设一个 Agent 有 10 项能力，每项能力的完整指令大约需要 1000 个 token，把它们全部拼进系统提示词，每次调用 LLM 就要消耗大约 10000 个 token 的基础上下文。

实际上用户可能只是想让它帮忙写一段营销文案，跟其中 8 项能力完全无关——这 10000 个 token 中有大约 8000 个是白白浪费的。当 Agent 的能力扩展到 20 项甚至更多，浪费的比例更加惊人。

### 响应质量问题

更深层的问题在于响应质量。上下文窗口是有限的资源，塞进太多无关信息会稀释模型对关键指令的关注度。当 Agent 需要在多个能力维度之间切换时，过长的系统提示词会降低它对当前任务相关指令的执行精度。

这个问题在能力维度超过 10 个之后尤为明显，开发者被迫在功能丰富度和响应准确性之间做艰难取舍。

Google 在 ADK 中给出的解决方案是——**渐进式披露（Progressive Disclosure）**。

---

## 渐进式披露：三层知识加载体系

渐进式披露的核心思想是把 Skill 知识分成三个递进的层级，每一层只在被需要时才被激活。该设计借鉴了软件工程中**延迟加载（Lazy Loading）** 的理念，把上下文消耗从一次性全量加载变成按需逐步深入。

| 层级 | 说明 | Token 消耗 | 加载方式 |
|------|------|-----------|---------|
| **L1: 元数据** | Skill 的名称 + 描述（Agent 浏览的"菜单"） | ~100 tokens/技能 | 始终在上下文中 |
| **L2: 指令** | 完整 Skill 主体（SKILL.md） | ~500 tokens，最高 ~5,000 | 通过 `load_skill` 按需加载 |
| **L3: 资源** | 外部参考文件（风格指南、API 规范等） | 可变 | 通过 `load_skill_resource` 按需加载 |

### 三层详解

**L1 元数据层**——每个 Skill 大约消耗 100 个 token。只包含 Skill 的名称和描述，没有任何具体的执行指令。Agent 启动时会加载所有 Skill 的 L1 元数据，相当于拿到一份餐厅菜单。Agent 浏览这份菜单来判断当前用户需求跟哪些 Skill 相关。

**L2 指令层**——每个 Skill 通常不超过 5000 个 token。这是 Skill 的完整指令体，详细描述了执行某项任务所需遵循的每一个步骤。只有当 Agent 通过 L1 判断某个 Skill 确实跟当前任务相关时，才会通过 API 调用显式加载该 Skill 的 L2 内容。

**L3 资源层**——完全按需加载。包括写作风格指南、API 接口规范文档、代码模板等外部参考文件。Agent 在执行过程中根据指令的具体需要才去加载对应的参考文件。

### 数据效果

一个拥有 10 项 Skill 的 Agent：

| 方式 | 每次调用消耗 | 对比 |
|------|-------------|------|
| 传统方式（全部加载） | ~10,000 tokens | 基准 |
| 渐进式披露（仅 L1） | ~1,000 tokens | 降低 ~90% |
| 触发 2 项 Skill 的任务 | ~3,000 tokens（L1+2×L2） | 节省 ~70% |

### ADK 实现

ADK 通过 **`SkillToolset`** 类来实现这套机制。开发者把 Skill 列表传给 `SkillToolset`，它会自动生成三个工具：

| 工具 | 对应层级 | 功能 |
|------|---------|------|
| `list_skills` | L1 | 列出所有可用 Skill（每次对话自动注入） |
| `load_skill` | L2 | 按需加载某个 Skill 的完整指令 |
| `load_skill_resource` | L3 | 按需加载 Skill 关联的参考资源文件 |

Agent 在运行过程中自主决定何时调用哪个工具，开发者不需要手动编写 if-else 逻辑来编排加载流程——**Agent 本身就是决策者**。

---

## 四种 Skill 构建模式

围绕渐进式披露架构，Google 的指南介绍了四种 Skill 构建模式，复杂度依次递增。前三种处理已经存在的 Skill，第四种让 Agent **自己生成新 Skill**。

### 模式 1：内联 Skill（Inline Skill）— 便利贴

最简单的模式。Google 把它比作便利贴——小而直接。开发者直接在 Agent 代码中定义一个 Python 对象，包含名称、描述和指令三个字段，全部用代码字符串写死。

适合小型、稳定、很少变动的规则集，比如检查清单类任务。

```python
seo_skill = models.Skill(
    frontmatter=models.Frontmatter(
        name="seo-checklist",
        description="SEO optimization checklist for blog posts.",
    ),
    instructions=(
        "When optimizing a blog post for SEO, check each item:\n"
        "1. Title: 50-60 chars, primary keyword near the start\n"
        "2. Meta description: 150-160 chars, includes a call-to-action\n"
        "3. Headings: H2/H3 hierarchy, keywords in 2-3 headings\n"
        "..."
    ),
)
```

**工作原理**：`frontmatter` 字段自动成为 L1 元数据，LLM 在每次调用时都能看到这段简短描述。`instructions` 字段成为 L2 内容，只有当 Agent 判断用户请求跟 SEO 优化相关时才会触发加载。

**优点**：简单直接，零配置，适合快速原型开发。几行代码就能给 Agent 加一项新能力。

**局限**：如果 Skill 需要引用外部文档，纯靠代码中的字符串很难承载。且内联 Skill 跟代码耦合在一起，修改 Skill 需要改代码重新部署。

---

### 模式 2：基于文件的 Skill（File-based Skill）— 参考活页夹

把 Skill 从代码中剥离出来，放到独立的目录结构中。Google 把该模式比作**参考活页夹**，按主题分门别类地存放专业知识。

```
skills/blog-writer/
├── SKILL.md           # L2: 指令入口
└── references/
    └── style-guide.md # L3: 按需加载
```

**SKILL.md 示例**：

```markdown
---
name: blog-writer
description: 专业博客内容写作助手，基于风格指南撰写高质量博客文章
---

## 说明

你是一个专业的博客内容写作助手，遵循以下步骤：

1. 读取 `references/style-guide.md` 了解写作风格要求
2. 根据用户提供的主题拟定文章大纲
3. 按照风格指南撰写完整文章
...
```

**加载方式**：

```python
blog_writer_skill = load_skill_from_dir(
    pathlib.Path(__file__).parent / "skills" / "blog-writer"
)
```

**关键优势**：
- **可复用性**——任何遵循 `agentskills.io` 规范的 Agent 都可以加载同一个目录
- **可维护性**——修改 Skill 只需编辑 SKILL.md 文件，不需要改代码重新部署
- **团队协作**——不同成员可以各自维护不同 Skill 的目录，互不干扰
- **版本管理**——Skill 目录可纳入 Git 版本管理

---

### 模式 3：外部导入 Skill（External Skill）— 图书馆借书

代码实现和文件型 Skill 完全一样，唯一区别在于 Skill 目录的来源。文件型 Skill 是开发者自己从零编写的，外部导入 Skill 是从社区仓库中找到并下载的现成 Skill。

就像你需要一本参考书，既可以自己手写一本，也可以直接去图书馆借一本别人已经写好的。

```python
content_researcher_skill = load_skill_from_dir(
    pathlib.Path(__file__).parent / "skills" / "content-research-writer"
)
```

Google 自身也发布了一些官方 ADK 开发 Skill，采用同样的格式，一行命令安装：

```bash
npx skills add google/adk-docs -y -g
```

目前已经有 **40 多个产品**支持 `agentskills.io` 规范，包括 Gemini CLI、Claude Code、Cursor 等。一份 Skill 定义可以在不同厂商的 Agent 平台之间通用。

---

### 模式 4：元 Skill / Skill 工厂（Skill Factory）— 自我扩展

**这是整篇文章最有趣的部分。**

元 Skill（Meta Skill）是一种特殊的 Skill，它的用途不是执行某项具体任务，而是专门用来**生成新的 `SKILL.md` 文件**。配备元 Skill 的 Agent 变成了**自我扩展的系统**——它可以在运行时编写新的 Skill 定义并立即使用，整个过程不需要人工干预。

```python
skill_creator = models.Skill(
    frontmatter=models.Frontmatter(
        name="skill-creator",
        description="Creates new ADK-compatible skill definitions from requirements.",
    ),
    instructions=(
        "When asked to create a new skill, generate a complete SKILL.md file.\n\n"
        "Read `references/skill-spec.md` for the format specification.\n"
        "Read `references/example-skill.md` for a working example.\n\n"
        "Follow these rules:\n"
        "1. Name must be kebab-case, max 64 characters\n"
        "2. Description must be under 1024 characters\n"
        "3. Instructions should be clear, step-by-step\n"
        "..."
    ),
    resources=models.Resources(
        references={
            "skill-spec.md": "# Agent Skills Specification (agentskills.io)...",
            "example-skill.md": "# Example: Code Review Skill...",
        }
    ),
)
```

**关键实现细节**：`resources` 字段内嵌了两份 L3 参考文档——一份是 `agentskills.io` 完整规范（skill-spec.md），另一份是一个可运行的代码审查 Skill 示例（example-skill.md）。当 Agent 被要求创建新 Skill 时，它会通过 `load_skill_resource` 工具读取这两份参考文档，理解规范的格式要求和最佳实践，然后根据用户的具体需求生成一份符合规范的 SKILL.md。

**完整运作流程示例**：

1. 用户对 Agent 说："我需要一个新 Skill，用来审查 Python 代码中的安全漏洞。"
2. Agent 调用 `list_skills` 浏览已有的 Skill 列表，发现没有匹配的安全审查 Skill
3. Agent 激活 `skill-creator` 元 Skill，调用 `load_skill_resource` 读取 `agentskills.io` 规范和示例
4. Agent 根据用户需求生成 Skill 定义，包含合规的 kebab-case 命名、结构化指令、基于严重程度的报告格式
5. 生成的 Skill 遵循 `agentskills.io` 规范，可在 ADK、Gemini CLI、Claude Code、Cursor 等 40+ 产品中使用

> ⚠️ **Google 的务实提醒**：自动生成的 Skill 建议保留人工审核环节。生成的 SKILL.md 应该像代码审查一样认真过一遍再部署上线。

---

## 完整组装：将所有 Skill 连接起来

```python
skill_toolset = SkillToolset(
    skills=[seo_skill, blog_writer_skill, content_researcher_skill, skill_creator]
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="blog_skills_agent",
    description="A blog-writing agent powered by reusable skills.",
    instruction="You are a blog-writing assistant with specialized skills...",
    tools=[skill_toolset],
)
```

Agent 的系统指令非常简洁，只需要告诉它：你是一个博客写作助手，拥有专业 Skill，加载相关 Skill 获取详细指令，用 `load_skill_resource` 访问参考资料，遵循每个 Skill 的步骤指令，并始终解释正在使用哪个 Skill 以及为什么。

### 运行时行为

| 用户需求 | Agent 行为 |
|---------|-----------|
| 审查博客 SEO | 调用 `list_skills` → 识别 `seo-checklist` → 调用 `load_skill` 加载 L2 指令 → 逐条执行检查 |
| 创建新的技术博客引言写作 Skill | 激活 `skill-creator` 元 Skill → 读取规范文档 → 生成新 SKILL.md → 保存供后续复用 |

---

## 设计原则与专业提示

1. **描述即是你的 API 文档**：`description` 字段是 Agent 决策的核心依据。好的描述应该精准地告诉 Agent 什么时候应该激活这个 Skill。模糊的描述（如"一个有用的 Skill"）对 Agent 的判断没有任何帮助。

2. **从内联开始，再升级为文件**：如果 Skill 的指令不超过 10 行，直接内联写就好。过早优化是常见陷阱，只有当 Skill 需要引用外部文档或跨 Agent 复用时才升级到文件型。

3. **像审查代码依赖一样审查生成的 Skill**：元 Skill 的输出直接决定了 Agent 的行为方式和能力边界。上线前必须审核和测试。建议使用 ADK 内置的评估（Evaluation）功能来测试 Skill 的有效性。

4. **生态兼容**：ADK 的 Skill 系统建立在 `agentskills.io` 这个开放标准之上，已被 40+ 产品采用，包括 Gemini CLI、Claude Code、Cursor 等。

---

## 总结

AI Agent 的能力边界，正在从被动执行人类编写的指令，拓展到**主动为自己编写新指令**。

- **渐进式披露架构**解决了知识膨胀的效率问题，让 Agent 既能拥有丰富的能力储备，又不会因为上下文过载而影响响应质量
- **Skill 工厂模式**打开了自我扩展的可能性——Agent 遇到未知场景时不再只能报错说做不到，它可以现场编写一份新 Skill 来补齐能力缺口

目前 Google 的 ADK 已支持 Python 和 Go 语言，Java 版本也在 2026 年 3 月底发布了 1.0 正式版。

---

## 相关资源

- [Google Developers Blog: 原文链接](https://developers.googleblog.com/developers-guide-to-building-adk-agents-with-skills/)
- [ADK Skills 官方文档](https://google.github.io/adk-docs/)
- [Google ADK Samples - Agent Skills Tutorial (GitHub)](https://github.com/google/adk-samples/blob/main/python/agents/README.md)
- [Google Codelabs: Next '26 — 使用 Skills 和 Tools 构建 ADK Agent](https://codelabs.developers.google.com/next26/dev-keynote/building-agents-with-skills?hl=en)
- [Google Cloud Blog: 构建你的第一个 ADK Agent 工作团队](https://cloud.google.com/blog/topics/developers-practitioners/build-your-first-adk-agent-workforce)
- [Damien Martinez: Agent Skills in Google ADK 实践教程](https://damimartinez.github.io/agent-skills-google-adk/)
- [agentskills.io 开放规范](https://agentskills.io)

## 关联连接

- [[ADK]] — Google Agent Development Kit，本摘要的源实体
- [[Skill_Factory]] — 元 Skill / 动态生成新 Skill 的自我扩展模式
- [[Progressive_Disclosure]] — 渐进式披露架构，L1/L2/L3 三层知识按需加载
- [[Claude_Code_Skills]] — Claude Code Skills 生态，与 ADK Skill 对照
- [[MCP]] — Model Context Protocol，LLM 工具调用的互补开放协议
- [[Agent_Orchestration_Patterns]] — Multi-agent 编排模式
