---
title: "Skills 权限管理"
type: concept
tags: [Skills, 权限, RBAC, 安全, 治理, Agent平台, 平台工程]
sources: []
last_updated: 2026-07-16
---

# Skills 权限管理

## 定义

Skills 权限管理是指 **AI Agent 平台中控制 Skill 创建、注册、发现、使用等全生命周期的授权策略体系**。与传统的 API 权限不同，Skills 权限不仅管"谁能调用什么 API"，还要管"哪个 Agent/用户能用哪个 Skill"、"Skill 在什么上下文中可自动加载"等 Agent 原生场景。

> 核⼼问题：**谁可以创建 Skill？谁可以使用哪个 Skill？Skill 在什么条件下自动触发？**

## 权限模型四层架构

```
┌──────────────────────────────────────────────────────────┐
│                    用户/角色层                             │
│  平台管理员 | 租户管理员 | 普通开发者 | 最终用户 | Agent   │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                    策略评估层                              │
│  RBAC (角色→权限) | ABAC (属性→策略) | 上下文感知评估     │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                    Skill 注册层                            │
│  Skill 元数据 (name/description/tools/所需权限声明)        │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                    执行拦截层                               │
│  Pre-use Hook → 权限检查 → 允许/拒绝 → 审计日志           │
└──────────────────────────────────────────────────────────┘
```

## 核心权限维度

### 1. 谁可以创建/注册 Skill

| 角色 | 创建范围 | 审批流程 | 示例 |
|------|---------|---------|------|
| **平台管理员** | 全局 Skill | 无（或内部审核） | 系统内置 Skill（搜索/计算/文件操作） |
| **租户管理员** | 租户内 Skill | 自动生效 | 企业定制审批流 Skill |
| **普通开发者** | 个人 Skill | 需租户管理员审批 | 开发测试用 Skill |
| **最终用户** | ❌ 不可创建 | — | 只能使用 |

### 2. 谁可以使用哪个 Skill（可见范围）

| 可见范围 | 使用权限规则 | 典型场景 |
|---------|------------|---------|
| **全局可见** | 所有用户、所有 Agent 可用 | 基础工具（网络搜索/数学计算/文件读写） |
| **租户可见** | 同一租户内的用户/Agent 可用 | 企业知识库查询、内部 API 调用 |
| **角色可见** | 特定角色的用户/Agent 可用 | 财务分析 Skill（仅财务角色） |
| **用户可见** | 仅创建者可用 | 个人私有工具链 |
| **Agent 可见** | 仅特定 Agent 实例可用 | 专用 Agent 的独有能力 |

### 3. 自动加载权限（Skill 的核心特性）

Skills 的核心机制是 **Description 匹配自动加载**。权限模型需要额外控制：

| 加载模式 | 说明 | 权限控制点 |
|---------|------|-----------|
| **自动加载** | 匹配到 Description 自动将 SKILL.md 注入 Context | 需检查当前用户/Agent 是否有该 Skill 的 use 权限 |
| **显式调用** | 用户手动 `/skill-name` 调用 | 检查执行权限 |
| **委托加载** | Subagent 需要时从主 Agent 继承权限 | 权限传递校验 |

### 4. Skill 内工具级权限

一个 Skill 可能封装了多个工具调用，需要**细粒度权限**：

```yaml
# Skill 的 Frontmatter 权限声明示例
---
name: enterprise-data-query
description: 查询企业内部数据
permissions:
  required_roles: [data_analyst, admin]
  required_tools:
    - tool: internal_db.query
      access_level: read_only      # 只读
    - tool: internal_api.export
      access_level: require_approval  # 需审批
  data_scope: 
    - department: finance
      level: aggregate_only        # 仅聚合数据
    - department: hr
      level: denied                # 禁止访问
  auto_load: true                  # 允许自动加载
  auto_load_contexts: ["数据查询", "报表", "分析"]
---
```

## 权限评估流程

```
Agent 收到用户请求
  → Skill Description 匹配命中
  → 权限服务获取当前上下文：
      ├── 当前用户/角色
      ├── 当前租户
      ├── 当前 Agent 类型
      └── 操作目标（数据范围/系统）
  → 策略引擎评估：
      ├── 用户是否有该 Skill 的 use 权限？→ 否 → 拒绝 + 记录审计
      ├── Skill 是否允许自动加载？→ 否 → 拒绝
      ├── 本次操作是否在 Skill 声明数据范围内？→ 否 → 拒绝
      └── 所用 Tool 是否在权限内？→ 否 → 拒绝
  → 通过 → 加载 Skill → 执行
  → 执行过程中每次 Tool 调用再次校验
```

## 权限模型设计选项

### RBAC（Role-Based Access Control）

| 角色 | Skill 权限 | 管理范围 |
|------|-----------|---------|
| `platform_admin` | 全部 Skill 全部权限 | 全局配置、租户管理 |
| `tenant_admin` | 租户内 Skill CRUD + 角色分配 | 租户内用户管理 |
| `developer` | 创建个人 Skill + 申请租户级 Skill | 个人 Skill 管理 |
| `analyst` | 使用数据分析类 Skill | 查询类操作 |
| `operator` | 使用业务操作类 Skill | 写入类操作 |
| `viewer` | 仅供查询的 Skill | 只读操作 |

### ABAC（Attribute-Based Access Control）

更灵活但更复杂的模型，基于属性策略：

```python
# 策略示例：工作日才允许执行写入类 Skill
if (resource.type == "write_skill" 
    and subject.role == "operator" 
    and environment.day_of_week in ["Monday","Friday"] 
    and environment.time between "09:00" and "18:00"):
    allow()
```

### ReBAC（Relationship-Based Access Control）

适用于 Agent ↔ Skill ↔ Tool 之间的复杂关系图（参考 Google Zanzibar）：

```
Agent A "拥有" Skill X
Agent A "属于" 租户 T
Skill X "使用" Tool Y
Tool Y "访问" 系统 Z

→ Agent A 能否通过 Skill X 使用 Tool Y 操作系统 Z？
→ 沿着关系图遍历：Agent A → 拥有 → Skill X → 使用 → Tool Y → 访问 → 系统 Z
→ 路径存在 ✅ 允许
```

## 与既有概念的关系

| 概念 | 关系 |
|------|------|
| [[Claude_Code_Skills]] | 本概念的"技能行为层"基础——定义了 Skill 是什么、怎么自动加载 |
| [[MCP]] | Skills 调用的工具通过 MCP 暴露，权限模型需要与 MCP Server 的授权联动 |
| [[多租户SaaS架构]] | Skills 权限是租户隔离在行为层的具体体现 |
| [[Work_Boundary]] | Skills 权限是 Agent "能做什么"的边界控制 |
| [[Harness_Engineering]] | 权限管理是 Harness 安全约束的核心组件 |
| [[Claude_Code_Hooks]] | PreToolUse Hook 是实现权限拦截的技术手段之一 |
| [[Agent_As_Judge]] | 必要时可由另一个 Agent 评审 Skill 调用是否合规 |

## 实现参考

| 方法 | 适用规模 | 复杂度 |
|------|---------|-------|
| **Frontmatter 声明式** | 小团队（<10 人） | ⭐ |
| **RBAC + Middleware** | 中型平台 | ⭐⭐ |
| **ABAC + Policy Engine（OpenFGA / OPA）** | 企业级多租户 | ⭐⭐⭐⭐ |
| **ReBAC（Zanzibar 范式）** | 大型 SaaS | ⭐⭐⭐⭐⭐ |

## 关联连接
- [[Claude_Code_Skills]] — Skills 系统基础架构
- [[MCP]] — Skills 底层工具调用协议
- [[多租户SaaS架构]] — 租户级权限隔离
- [[Work_Boundary]] — Agent 自主权边界
- [[Harness_Engineering]] — 安全约束的工程框架
- [[Claude_Code_Hooks]] — 权限拦截技术手段
- [[Agent_As_Judge]] — Agent 评审机制
- [[Claude_Code_Plugins]] — Plugin 打包 Skills 时的权限传播
