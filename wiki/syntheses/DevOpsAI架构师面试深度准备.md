---
title: "DevOps AI 架构师面试深度准备"
type: synthesis
tags: [面试, 架构设计, DevOps, AI, HarnessEngineering, 伪代码, 工具选型]
sources:
  - wiki/sources/摘要-devops-ai-architect-xiamen.md
  - wiki/syntheses/DevOpsAI架构师JD全景对标分析.md
last_updated: 2026-07-22
---

# DevOps AI 架构师面试深度准备

> 基于 [[摘要-devops-ai-architect-xiamen]] 的 JD 要求，使用 [[Harness_Engineering]] 框架给出**伪代码级架构实现 + 工具选型对比 + 关键权衡分析**。适用于面试中的 System Design 和架构面环节。

---

## 一、DevOps Agent：AI 驱动 CICD 无人值守

### 1.1 伪代码级实现

```python
# CI Agent Orchestrator - 核心编排逻辑
# 基于 Harness Engineering 8 核心元件框架

class CIAgentOrchestrator:
    """CI Agent 编排器：接收 PR 事件，驱动 Agent Loop 完成审查-测试-发布"""

    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.context_manager = ContextManager()
        self.safety_layer = SafetyLayer()
        self.agent_loop = AgentLoop()
        self.observability = ObservabilityClient()

    async def handle_pr_event(self, pr_event: PREvent):
        """PR 事件入口 - 触发完整 CI Agent 管道"""
        trace_id = self.observability.start_trace("ci_pipeline", {
            "repo": pr_event.repo,
            "pr": pr_event.pr_number,
            "author": pr_event.author,
            "branch": pr_event.branch
        })

        try:
            # Step 1: 收集上下文
            context = await self.context_manager.collect({
                "diff": await self.tool_registry.call("git", "diff", pr_event.diff_url),
                "project_config": await self._load_project_config(pr_event.repo),
                "history": await self._load_build_history(pr_event.repo, limit=3),
                "lint_rules": await self._load_lint_rules(pr_event.repo),
                "changed_files": await self._classify_changed_files(pr_event.diff)
            })

            # Step 2: Agent Loop - Plan 阶段
            plan = await self.agent_loop.plan(
                objective=f"审查 PR #{pr_event.pr_number}，确保代码质量和构建通过",
                context=context,
                available_tools=self.tool_registry.list_tools(),
                model="sonnet"  # 计划阶段用中端模型
            )
            # plan 输出: [
            #   {"step": "lint_check", "files": ["src/*.py"], "tool": "pylint"},
            #   {"step": "unit_test", "files": ["tests/*.py"], "tool": "pytest"},
            #   {"step": "build", "target": "docker_image", "tool": "docker_build"},
            #   {"step": "code_review", "focus_areas": ["security", "performance"]}
            # ]

            # Step 3: 安全门禁 - 审查 plan 的合法性
            plan = await self.safety_layer.validate_plan(plan)
            # 安全检查项:
            # - 不执行写操作（除非授权）
            # - 不访问敏感文件
            # - 不超出资源配额

            # Step 4: 执行 - 使用推理三明治模式
            # 昂贵模型（Opus）做规划，便宜模型（Haiku）做执行
            results = []
            for step in plan.steps:
                if step.requires_deep_reasoning:  # 复杂代码审查
                    step_result = await self.agent_loop.execute(
                        step, context=context, model="opus",
                        trace_id=f"{trace_id}_step_{step.name}"
                    )
                else:  # lint / test / build
                    step_result = await self.agent_loop.execute(
                        step, context=context, model="haiku",
                        trace_id=f"{trace_id}_step_{step.name}"
                    )
                results.append(step_result)

                # 熔断：如果关键步骤失败，提前终止
                if step.critical and not step_result.passed:
                    await self._trigger_circuit_breaker(trace_id, step, step_result)
                    break

            # Step 5: Verify & Critique
            verification = await self.agent_loop.verify(
                results=results,
                criteria=[
                    "是否所有 lint 规则通过",
                    "是否所有测试通过（含新增测试覆盖率 > 80%）",
                    "是否构建产物可复现",
                    "是否有安全漏洞（依赖扫描 + 代码审计）"
                ],
                model="sonnet"
            )

            # Step 6: 生成报告与自动修复
            if verification.passed:
                await self._post_pass_comment(pr_event, verification.summary)
            else:
                # 自动修复简单问题
                auto_fixable = [r for r in results if r.can_auto_fix]
                for fix_issue in auto_fixable:
                    fix = await self.agent_loop.repair(
                        issue=fix_issue,
                        context=context,
                        model="sonnet",
                        max_retries=3
                    )
                    if fix.success:
                        await self._apply_fix(fix)
                        await self.observability.log_fix(trace_id, fix)

                # 复杂问题发评论让人工处理
                need_human = [r for r in results if not r.can_auto_fix]
                await self._post_fail_comment(pr_event, need_human, verification.details)

            # 更新 CI 状态
            await self._update_ci_status(pr_event, verification.status)

            # 记录可观测性数据
            await self.observability.end_trace(trace_id, {
                "status": verification.status,
                "total_steps": len(plan.steps),
                "passed": sum(1 for r in results if r.passed),
                "failed": sum(1 for r in results if not r.passed),
                "auto_fixed": sum(1 for r in results if r.auto_fixed),
                "total_tokens": self.agent_loop.token_usage,
                "total_cost": self.agent_loop.cost,
                "latency_ms": self.agent_loop.latency_ms
            })

        except Exception as e:
            await self.observability.log_error(trace_id, e)
            await self._safe_fallback(pr_event, e)
            raise

    async def _classify_changed_files(self, diff: str) -> Dict:
        """将变更文件按类型分类，辅助 Agent 决策"""
        changes = {"source": [], "test": [], "config": [], "docs": [], "infra": []}
        for file_path in diff.get_changed_files():
            if file_path.startswith("tests/") or file_path.startswith("test_"):
                changes["test"].append(file_path)
            elif file_path.endswith((".yml", ".yaml", ".json", ".toml")):
                changes["config"].append(file_path)
            elif file_path.endswith((".md", ".rst", ".txt")):
                changes["docs"].append(file_path)
            elif file_path.startswith(("Dockerfile", ".github", "k8s")):
                changes["infra"].append(file_path)
            else:
                changes["source"].append(file_path)
        return changes

    async def _safe_fallback(self, pr_event: PREvent, error: Exception):
        """优雅降级：Agent 宕机时回退到传统 CI 流程"""
        self.observability.log("CI Agent unavailable, falling back to traditional CI")
        # 触发传统 CI 流程（Jenkins/GitHub Actions）
        await self.tool_registry.call("ci_trigger", "fallback", {
            "repo": pr_event.repo,
            "pr": pr_event.pr_number,
            "fallback_reason": str(error)
        })
```

### 1.2 工具选型对比

| 对比维度 | Claude Code Skills | Dify Workflow | LangGraph | 自建 Agent |
|---------|-------------------|---------------|-----------|-----------|
| **上手速度** | ⭐⭐⭐⭐⭐ 即装即用 | ⭐⭐⭐⭐ 可视化编排 | ⭐⭐ 需代码开发 | ⭐ 全自建 |
| **CI/CD 集成** | ⭐⭐⭐⭐⭐ 原生 Shell/Git | ⭐⭐⭐ API 对接 | ⭐⭐⭐ API 对接 | ⭐⭐⭐⭐⭐ 完全可控 |
| **编排灵活性** | ⭐⭐⭐ Skill 组合 | ⭐⭐⭐ 固定 Workflow | ⭐⭐⭐⭐⭐ 图式编排 | ⭐⭐⭐⭐⭐ 无限 |
| **可观测性** | ⭐⭐⭐ 内置 Log | ⭐⭐⭐ Log + Trace | ⭐⭐⭐⭐⭐ LangSmith | ⭐ 需自建 |
| **安全沙箱** | ⭐⭐⭐⭐ 内置 | ⭐⭐⭐ 平台管控 | ⭐⭐ 需自建 | ⭐⭐⭐⭐⭐ 完全可控 |
| **生产可靠性** | ⭐⭐⭐⭐ 经过验证 | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐ LangGraph Platform | ⭐ 取决于实现 |
| **适合场景** | 快速落地 CI Agent | 非技术人员编排流程 | 复杂的多 Agent 编排 | 深度定制需求 |

**选型建议**：对"领域全球第一企业"的效能团队，推荐**分阶段策略**：
- **Phase 1 (MVP)**：Claude Code Skills 快速验证 CI Agent 效果，积累最佳实践
- **Phase 2 (扩展)**：用 LangGraph 构建生产级多 Agent 编排，替换原型
- **Phase 3 (平台化)**：将成功的 Agent 模式沉淀为内部 Agent Framework

### 1.3 关键架构权衡

| 权衡 | 选项 A | 选项 B | 推荐 |
|------|--------|--------|------|
| **Agent 状态管理** | 有状态（记忆上下文） vs 无状态（每次独立） | 混合：Session 内有状态，跨 Session 无状态 |
| **模型选择策略** | 固定模型 vs 动态路由 | 动态路由（简单→Haiku，复杂→Sonnet，关键→Opus） |
| **错误处理** | 快速失败 vs 自动重试 | 自动重试 3 次 + 失败归因 + 人工升级 |
| **部署方式** | 单体 Agent vs 微服务 Agent | 微服务：每个 CI 阶段独立 Agent（lint/test/build/review） |
| **并行粒度** | 串行执行 vs 全并行 | Plan 串行，Execute 并行（DAG 依赖图） |

---

## 二、通用排障：智能归因与自动修复

### 2.1 伪代码级实现

```python
# Intelligent Troubleshooting Agent - 核心排障逻辑

class TroubleshootingAgent:
    """智能排障 Agent：告警触发 → 上下文聚合 → 归因分析 → 修复执行 → 知识沉淀"""

    def __init__(self):
        self.tools = DiagnosticToolkit()
        self.knowledge_base = RAGKnowledgeBase()
        self.safety = SafetyClassifier()
        self.tracer = ObservabilityTracer("troubleshooting")

    async def handle_alert(self, alert: Alert):
        """排障主流程"""
        trace_id = self.tracer.start("troubleshoot", alert.to_dict())

        try:
            # === Phase 1: 确认异常 ===
            confirmed = await self._confirm_incident(alert)
            if not confirmed:
                self.tracer.log(trace_id, "alert_false_positive", alert.id)
                return  # 误报，直接退出

            # === Phase 2: 上下文聚合 ===
            context = await self._aggregate_context(alert)
            # context = {
            #   "logs": [{"time": "...", "level": "ERROR", "msg": "..."}, ...],
            #   "metrics": {"p99_latency": 2500, "error_rate": 5.2, ...},
            #   "events": [{"type": "deploy", "time": "15min_ago", ...}],
            #   "topology": {"service": "payment", "deps": ["auth", "db", "redis"]},
            #   "recent_changes": [{"file": "payment_service.go", "lines": "45-60"}]
            # }

            # === Phase 3: 归因分析 ===
            # 方法：多 Agent 投票共识 + 证据链验证
            root_causes = await self._root_cause_analysis(context)

            # root_causes 输出示例:
            # [
            #   {
            #     "rank": 1, "confidence": 0.87,
            #     "cause": "payment_service.go 第 52 行空指针: db.Query() 未判 nil",
            #     "evidence": [
            #       "log_123: 'panic: runtime error: invalid memory address'",
            #       "event_045: 'commit 3a1b2c - fix payment gateway timeout' (15min ago)",
            #       "metric_spike: error_rate 0.2→5.2 at 14:30 (deploy time)"
            #     ],
            #     "suggested_action": "rollback_commit_3a1b2c",
            #     "action_level": "medium"  # 需要人工确认
            #   },
            #   {
            #     "rank": 2, "confidence": 0.45,
            #     "cause": "数据库连接池耗尽: max_connections=100, 活跃=98",
            #     "evidence": [...],
            #     "suggested_action": "increase_max_connections_to_200",
            #     "action_level": "low"  # 可自动执行
            #   }
            # ]

            # === Phase 4: 知识检索 ===
            # 在知识库中匹配相似历史排障案例
            similar_cases = await self.knowledge_base.search(
                query=root_causes[0].cause,
                top_k=3
            )
            if similar_cases:
                # 补充历史方案到修复建议
                for case in similar_cases:
                    root_causes[0].suggested_action += f"\n历史案例 #{case.id}: {case.resolution}"

            # === Phase 5: 修复执行 ===
            for rc in root_causes:
                if rc.confidence < 0.3:
                    continue  # 置信度太低，跳过

                safe_level = self.safety.classify(rc.suggested_action, context)
                # safe_level: "auto" | "notify" | "approve" | "manual_only"

                if safe_level == "auto":
                    await self._execute_fix(rc, trace_id)
                    self.tracer.log(trace_id, "auto_fix_executed", {
                        "cause": rc.cause, "action": rc.suggested_action
                    })

                elif safe_level == "notify":
                    await self._notify_oncall(rc)
                    await self._execute_fix(rc, trace_id)  # 自动执行但通知

                elif safe_level == "approve":
                    approval = await self._request_approval(rc)
                    if approval.granted:
                        await self._execute_fix(rc, trace_id)
                    else:
                        self.tracer.log(trace_id, "fix_rejected", {
                            "cause": rc.cause, "reason": approval.reason
                        })

                else:  # manual_only
                    await self._escalate_to_human(rc)

            # === Phase 6: 验证确认 ===
            verification = await self._verify_fix(context, timeout_minutes=5)
            if not verification.success:
                # 修复无效或恶化，自动回滚
                await self._rollback_fix(root_causes[0], trace_id)
                await self._escalate_to_human(
                    root_causes[0],
                    reason="fix_unsuccessful",
                    verification=verification
                )

            # === Phase 7: 知识沉淀 ===
            await self.knowledge_base.store(
                incident={
                    "alert": alert.to_dict(),
                    "context_summary": self._summarize_context(context),
                    "root_cause": root_causes[0].cause,
                    "evidence": root_causes[0].evidence,
                    "fix_applied": root_causes[0].suggested_action if verification.success else None,
                    "verification": verification.to_dict(),
                    "timestamp": datetime.utcnow()
                }
            )

            # 完成排障记录
            self.tracer.end(trace_id, {
                "status": "resolved" if verification.success else "escalated",
                "root_causes_found": len(root_causes),
                "auto_fix": verification.success and safe_level in ("auto", "notify"),
                "ttr_minutes": self.tracer.elapsed_minutes(trace_id)
            })

        except Exception as e:
            self.tracer.error(trace_id, e)
            await self._escalate_to_human(
                alert=alert,
                reason=f"Troubleshooting agent error: {str(e)}"
            )

    async def _root_cause_analysis(self, context: dict) -> list:
        """多 Agent 投票的归因分析"""
        analyzers = [
            LogAnalyzer(),
            MetricAnalyzer(),
            EventTimelineAnalyzer(),
            DependencyGraphAnalyzer()
        ]
        # 每个 analyzer 是一个独立 Agent，各自分析后投票
        candidates = []
        for analyzer in analyzers:
            result = await analyzer.analyze(context)
            candidates.extend(result)

        # 投票排序：按置信度降序，合并相似原因
        merged = self._merge_similar_causes(candidates)
        merged.sort(key=lambda x: x.confidence, reverse=True)
        return merged[:3]  # 返回 Top-3

    async def _verify_fix(self, original_context: dict, timeout_minutes: int) -> VerificationResult:
        """修复后验证 - 确认指标回归基线"""
        start = time.time()
        while time.time() - start < timeout_minutes * 60:
            current_metrics = await self._fetch_current_metrics(original_context)
            if self._is_back_to_baseline(current_metrics, original_context["metrics"]):
                return VerificationResult(success=True, metrics=current_metrics)
            if self._is_worsening(current_metrics, original_context["metrics"]):
                return VerificationResult(success=False, reason="metrics_worsening")
            await asyncio.sleep(30)  # 每 30s 检查一次
        return VerificationResult(success=False, reason="timeout")
```

### 2.2 归因分析方法论对比

| 方法 | 原理 | 适用场景 | 复杂度 | 准确率 | 速度 |
|------|------|---------|--------|--------|------|
| **时序关联** | 指标突变 + 事件时间线对齐 | 发布/配置变更导致的问题 | 低 | 中 | 快 |
| **日志模式匹配** | Error 日志聚类 → 已知模式匹配 | 已知异常（OOM/空指针/慢查询） | 中 | 高 | 快 |
| **依赖图追溯** | 沿服务拓扑逐层检查上游 | 分布式链路故障 | 高 | 高 | 慢 |
| **多 Agent 投票** | 多个独立 Analyzer 投票合并 | 复杂未知问题 | 高 | 最高 | 最慢 |
| **ML 异常检测** | 时序模型预测基线偏差 | 性能退化/容量问题 | 极高 | 中高 | 中 |

### 2.3 Harness Safety Layer 分级实现

```python
class SafetyClassifier:
    """排障 Agent 的操作安全分级 - 对应 Autonomy_Gradient"""

    ACTION_LEVELS = {
        "auto": ["restart_service", "clear_cache", "retry_job", "rescale_replicas"],
        "notify": ["rollback_deploy", "adjust_config", "scale_up", "switch_traffic"],
        "approve": ["database_failover", "modify_iam", "change_network_rule"],
        "manual_only": ["data_restore", "permission_change", "cross_region_operation"]
    }

    def classify(self, action: str, context: dict) -> str:
        """根据操作类型和当前上下文判断安全等级"""
        # 1. 操作类型匹配
        for level, actions in self.ACTION_LEVELS.items():
            if any(a in action for a in actions):
                base_level = level
                break
        else:
            base_level = "approve"  # 未知操作默认需要审批

        # 2. 上下文风险调整
        risk_score = self._compute_risk_score(context)
        # risk_score: 0-1, 越大越危险

        if risk_score > 0.8 and base_level in ("auto", "notify"):
            return "approve"  # 高风险环境下提高安全等级
        if risk_score < 0.2 and base_level == "approve":
            return "notify"   # 低风险环境降低安全等级

        return base_level

    def _compute_risk_score(self, context: dict) -> float:
        """计算风险评分"""
        score = 0.0
        # 影响范围
        if context.get("affected_users", 0) > 10000:
            score += 0.4
        elif context.get("affected_users", 0) > 1000:
            score += 0.2
        # 是否在生产环境
        if context.get("environment") == "production":
            score += 0.3
        # 是否关键链路
        if context.get("is_critical_path"):
            score += 0.2
        # 是否是业务高峰期
        if context.get("is_peak_hours"):
            score += 0.1
        return min(score, 1.0)
```

---

## 三、企业级 LLM Gateway：完整架构设计

### 3.1 伪代码级实现

```python
# LLM Gateway - 生产级实现的核心模块

class LLMGateway:
    """企业级 LLM Gateway：多模型路由 / 限流鉴权 / 成本追踪 / 优雅降级"""

    def __init__(self, config: GatewayConfig):
        self.router = ModelRouter(config.models)
        self.auth = AuthManager(config.auth_providers)
        self.rate_limiter = RateLimiter(config.rate_limits)
        self.cost_tracker = CostTracker(config.budgets)
        self.cache_manager = CacheManager(config.cache)
        self.fallback_chain = FallbackChain(config.fallback_config)
        self.observability = ObservabilityClient()

    async def route_request(self, request: GatewayRequest) -> GatewayResponse:
        """处理 LLM 请求的完整路由链路"""
        trace_id = self.observability.start_trace("llm_gateway", {
            "client": request.client_id,
            "model_preference": request.model,
            "input_tokens": len(request.messages[-1].content)
        })

        start_time = time.time()

        try:
            # Step 1: 鉴权
            auth_result = await self.auth.authenticate(request.api_key, request.client_id)
            if not auth_result.authorized:
                self.observability.log(trace_id, "auth_failed", {
                    "client": request.client_id, "reason": auth_result.reason
                })
                return GatewayResponse(
                    status=401,
                    error=f"Unauthorized: {auth_result.reason}"
                )

            # Step 2: 限流检查
            remaining = await self.rate_limiter.check(
                key=request.client_id,
                cost=request.estimated_cost
            )
            if remaining <= 0:
                reset_time = await self.rate_limiter.reset_time(request.client_id)
                return GatewayResponse(
                    status=429,
                    error=f"Rate limit exceeded. Resets at {reset_time}",
                    headers={"X-RateLimit-Reset": str(reset_time)}
                )

            # Step 3: 缓存检查
            cache_key = self._build_cache_key(request)
            if request.use_cache:
                cached = await self.cache_manager.get(cache_key)
                if cached:
                    self.observability.log(trace_id, "cache_hit", {
                        "cache_key": cache_key, "saved_tokens": cached.total_tokens
                    })
                    return GatewayResponse(
                        status=200,
                        body=cached.response,
                        cached=True,
                        latency_ms=2  # 缓存几乎零延迟
                    )

            # Step 4: 模型路由选择
            selected_model = await self.router.select(
                request=request,
                auth_context=auth_result,
                # 路由考虑因素：请求复杂度、成本预算、延迟要求、可用性
            )
            # selected_model = {
            #   "provider": "anthropic",
            #   "model": "claude-sonnet-4-20260514",
            #   "reason": "code_review_task",
            #   "estimated_cost": 0.05
            # }

            # Step 5: 成本预算检查
            budget_check = await self.cost_tracker.check_budget(
                client=request.client_id,
                estimated_cost=selected_model.estimated_cost
            )
            if not budget_check.allowed:
                # 预算超限，尝试降级到更便宜的模型
                downgraded = await self.router.downgrade(
                    selected_model,
                    max_cost=budget_check.remaining_budget
                )
                if downgraded:
                    selected_model = downgraded
                    self.observability.log(trace_id, "budget_downgrade", {
                        "original": selected_model.model,
                        "downgraded_to": downgraded.model
                    })
                else:
                    return GatewayResponse(
                        status=402,
                        error=f"Budget exceeded. Monthly limit: {budget_check.monthly_limit}"
                    )

            # Step 6: 调用 LLM Provider（带 Fallback Chain）
            response = await self.fallback_chain.execute(
                provider=selected_model.provider,
                model=selected_model.model,
                messages=request.messages,
                tools=request.tools,
                max_retries=3,
                timeout_seconds=60
            )

            # 如果 fallback chain 全部失败
            if response is None:
                self.observability.log(trace_id, "all_providers_failed", {
                    "attempted_providers": self.fallback_chain.attempted
                })
                return GatewayResponse(
                    status=503,
                    error="All LLM providers unavailable. Please retry later."
                )

            # Step 7: 缓存响应（如果适用）
            if request.use_cache and response.should_cache:
                await self.cache_manager.set(
                    cache_key, response,
                    ttl=request.cache_ttl or 300  # 默认 5 分钟
                )

            # Step 8: 记录成本
            actual_cost = response.usage.total_tokens * selected_model.price_per_token
            await self.cost_tracker.record(
                client=request.client_id,
                model=selected_model.model,
                tokens=response.usage.total_tokens,
                cost=actual_cost,
                trace_id=trace_id
            )

            # Step 9: 可观测性记录
            latency_ms = (time.time() - start_time) * 1000
            self.observability.end_trace(trace_id, {
                "status": 200,
                "model": selected_model.model,
                "provider": selected_model.provider,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens,
                "cost": actual_cost,
                "latency_ms": latency_ms,
                "cache_hit": False,
                "fallback_used": len(self.fallback_chain.attempted) > 1
            })

            # Step 10: 返回
            return GatewayResponse(
                status=200,
                body=response.content,
                model=selected_model.model,
                usage=response.usage,
                latency_ms=latency_ms
            )

        except Exception as e:
            self.observability.error(trace_id, e)
            return GatewayResponse(
                status=500,
                error=f"Gateway internal error: {str(e)}"
            )

    def _build_cache_key(self, request: GatewayRequest) -> str:
        """构建缓存键 - 考虑 semantic similarity"""
        # 方案 1: Exact Match（最快，但有局限性）
        return f"llm:{request.client_id}:{hash(str(request.messages))}"

        # 方案 2: Semantic Cache（更高效，需要 Embedding）
        # embedding = await self.embedder.encode(str(request.messages))
        # return f"semantic:{self._quantize(embedding)}"


class ModelRouter:
    """智能模型路由 - Cost_Optimization 核心"""

    def __init__(self, models_config: list):
        self.models = models_config
        # models_config = [
        #   {"name": "claude-opus", "price": 0.15, "capabilities": ["reasoning", "code"], "weight": 0.2},
        #   {"name": "claude-sonnet", "price": 0.03, "capabilities": ["code", "general"], "weight": 0.5},
        #   {"name": "claude-haiku", "price": 0.002, "capabilities": ["general"], "weight": 0.3},
        # ]

    async def select(self, request, auth_context) -> Model:
        """基于多层因素选择最优模型"""

        # 1. 显式指定：如果请求指定了模型且权限允许
        if request.model and auth_context.allowed_models.get(request.model):
            return self._get_model(request.model)

        # 2. 场景识别：根据请求内容推断复杂度
        complexity = self._estimate_complexity(request)

        # 3. 成本优先：结合用户预算等级
        budget_tier = auth_context.budget_tier  # "low" | "medium" | "unlimited"

        # 4. 最终选择
        if budget_tier == "low":
            return self._cheapest_model()
        elif complexity == "simple" and budget_tier != "unlimited":
            return self._get_model("claude-haiku")
        elif complexity == "complex":
            return self._get_model("claude-sonnet")
        elif complexity == "critical":
            return self._get_model("claude-opus")
        else:
            return self._weighted_random()

    def _estimate_complexity(self, request) -> str:
        """估计请求复杂度"""
        total_text = sum(len(m.content) for m in request.messages)
        has_tools = len(request.tools or []) > 0

        if total_text > 8000 or has_tools:
            return "complex"
        elif any(kw in str(request.messages) for kw in ["reason", "analyze", "review", "debug"]):
            return "complex"
        elif total_text > 2000:
            return "medium"
        else:
            return "simple"


class FallbackChain:
    """优雅降级链 - Graceful_Degradation 实现"""

    def __init__(self, config: dict):
        self.providers = config["providers"]  # 有序列表，先尝试的在前
        # [
        #   {"name": "anthropic", "models": ["opus", "sonnet"], "timeout": 60},
        #   {"name": "openai", "models": ["gpt-4o"], "timeout": 45},
        #   {"name": "openrouter", "models": ["qwen-max"], "timeout": 60},
        #   {"name": "local", "models": ["llama-3"], "timeout": 120},
        # ]
        self.attempted = []

    async def execute(self, provider, model, messages, tools, max_retries, timeout_seconds):
        """执行 LLM 调用，带 fallback 链"""

        # 先尝试首选 provider
        last_error = None
        for attempt in range(max_retries):
            try:
                response = await self._call_provider(
                    provider, model, messages, tools, timeout_seconds
                )
                return response
            except Exception as e:
                last_error = e
                self.attempted.append(f"{provider}/{model} (attempt {attempt+1}): {str(e)}")
                await asyncio.sleep(2 ** attempt)  # Exponential Backoff

        # 首选 provider 全部失败，尝试 fallback
        self.attempted.append(f"Primary failed after {max_retries} retries")

        for fallback in self.providers[1:]:  # 跳过第一个（已尝试）
            if fallback["name"] == provider:
                continue
            try:
                # 使用降级模型
                fallback_model = fallback["models"][-1]  # 用最便宜的模型
                response = await self._call_provider(
                    fallback["name"], fallback_model,
                    messages, tools,
                    fallback.get("timeout", timeout_seconds)
                )
                return response
            except Exception as e:
                self.attempted.append(f"Fallback {fallback['name']}: {str(e)}")
                continue

        return None
```

### 3.2 自建 Gateway vs 开源方案对比

| 对比维度 | 自建 Gateway | LiteLLM | OpenRouter | Kong AI Gateway |
|---------|-------------|---------|-----------|----------------|
| **部署复杂度** | ⭐ 高（全自建） | ⭐⭐⭐⭐ （一行代码集成） | ⭐⭐⭐⭐⭐（SaaS 零部署） | ⭐⭐⭐（已有 Kong 则快） |
| **模型覆盖** | ⭐ 取决于实现 | ⭐⭐⭐⭐⭐（100+ 模型） | ⭐⭐⭐⭐⭐（200+ 模型） | ⭐⭐⭐（插件生态） |
| **定制灵活性** | ⭐⭐⭐⭐⭐ 完全可控 | ⭐⭐⭐ 配置化（有限） | ⭐⭐ 受限于平台 | ⭐⭐⭐ Lua 插件 |
| **成本控制** | ⭐⭐⭐⭐⭐ 精细预算门控 | ⭐⭐⭐⭐ 内置费用追踪 | ⭐⭐⭐ 按量计费无预算 | ⭐⭐ 需要自建 |
| **性能/延迟** | ⭐⭐⭐⭐⭐ 零额外开销 | ⭐⭐⭐⭐ 代理层 5-10ms | ⭐⭐⭐ 网络额外 20-50ms | ⭐⭐⭐ 代理层 10-30ms |
| **数据隐私** | ⭐⭐⭐⭐⭐ 数据不出网 | ⭐⭐⭐⭐ 可自建 | ⭐⭐ 数据经过平台 | ⭐⭐⭐⭐ 可自建 |
| **企业级特性** | ⭐ 需要自建 | ⭐⭐⭐ 基础功能 | ⭐⭐⭐ 限流+鉴权 | ⭐⭐⭐⭐⭐ 全栈 |
| **适合团队规模** | 大型团队（20+ 人） | 中小型团队 | 个人/小团队 | 已有 Kong 的企业 |

**选型建议**：
- **起步阶段**：LiteLLM（快速上线，成本追踪内置）
- **成长阶段**：自建 Gateway（完全控制权，对接内部 IAM/计费系统）
- **企业已有 API 网关**：Kong + AI Gateway 插件
- **全球第一企业级别**：自建 + Rust/Go 实现核心路由层，保证极致性能和安全性

### 3.3 Cost Optimization 真实数据参考

基于当前（2026 年 7 月）的市场定价：

| 模型 | 输入价格 (/1M tokens) | 输出价格 (/1M tokens) | 适用场景 |
|------|---------------------|---------------------|---------|
| Claude Opus 4 | $15 | $75 | 复杂推理、架构设计、代码审查 |
| Claude Sonnet 4 | $3 | $15 | 代码生成、文档编写、通用任务 |
| Claude Haiku 3.5 | $0.25 | $1.25 | 简单问答、摘要、分类、lint 修复 |
| GPT-4o | $2.50 | $10 | 通用场景 |
| GPT-4o-mini | $0.15 | $0.60 | 简单任务 |
| Qwen-Max | $0.80 | $2.40 | 中文优化，性价比高 |
| DeepSeek-V3 | $0.27 | $1.10 | 高性价比长上下文 |

**成本优化案例**（基于知识库 [[Cost_Optimization]]）：

```
一个典型的 CI Agent 流程：
  传统方案：全程使用 Opus（审查 + 测试 + 构建）
    → 每次构建约 $0.50-1.00
    → 每日 200 次构建 = $100-200/天 = $3000-6000/月

  优化方案（动态路由 + Caching + 推理三明治）：
    阶段 1: 代码变更分类 → Haiku（$0.002）
    阶段 2: lint/test/build → Haiku 自动化（$0.01）
    阶段 3: 复杂逻辑审查 → Sonnet（$0.05）
    阶段 4: 关键安全审查 → Opus（$0.15）
    Prompt Caching 省 50-90% 重复 prefix
    → 每次构建约 $0.08-0.20（含缓存）
    → 每日 200 次构建 = $16-40/天 = $480-1200/月

  节省比例：约 70-85%
```

---

## 四、企业级 LLM 应用基础设施：完整架构蓝图

### 4.1 分层架构总览

```python
# 企业级 LLM 应用基础设施 - 架构蓝图

"""
┌────────────────────────────────────────────────────────────────────┐
│                        应用层 (Application Layer)                    │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│ │DevOps    │ │Code      │ │Chatbot   │ │RAG 应用  │ │内部工具  │  │
│ │Agent     │ │Review    │ │          │ │          │ │          │  │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
├────────────────────────────────────────────────────────────────────┤
│                    Agent Framework Layer                            │
│ ┌──────────────────────────────────────────────────────────────┐   │
│ │ Agent Orchestrator  ─  Agent Loop 管理 / 状态机 / 重试 / 熔断 │   │
│ │ Tool Registry ────  工具注册 / 发现 / MCP 协议桥接              │   │
│ │ Context Manager ──  Memory / RAG / Session 管理                │   │
│ │ Skill System ─────  Skills 加载 / 热更新 / 权限 / 生命周期     │   │
│ └──────────────────────────────────────────────────────────────┘   │
├────────────────────────────────────────────────────────────────────┤
│                      LLM Gateway Layer                              │
│ ┌──────────────────────────────────────────────────────────────┐   │
│ │  Router  │  Auth  │  Rate Limit  │  Cache  │  Cost Track     │   │
│ │  ┌──────┐│ ┌────┐│ ┌──────────┐ │ ┌─────┐ │ ┌────────────┐  │   │
│ │  │Model ││ │JWT/││ │Sliding   │ │ │Exact│ │ │Token Count │  │   │
│ │  │Route ││ │API ││ │Window    │ │ │Cache│ │ │Budget Alert│  │   │
│ │  │Cascade││ │Key ││ │Token     │ │ │Sem. │ │ │Cost Split  │  │   │
│ │  │      ││ │    ││ │Bucket    │ │ │Cache│ │ │            │  │   │
│ │  └──────┘│ └────┘│ └──────────┘ │ └─────┘ │ └────────────┘  │   │
│ └──────────────────────────────────────────────────────────────┘   │
├────────────────────────────────────────────────────────────────────┤
│                      LLM Provider Layer                             │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │Anthropic │ │OpenAI    │ │Qwen      │ │DeepSeek  │ │私有部署   │ │
│ │(Claude)  │ │(GPT)     │ │          │ │          │ │(vLLM)    │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├────────────────────────────────────────────────────────────────────┤
│                    Observability & Platform Layer                    │
│ ┌──────────────────────────────────────────────────────────────┐   │
│ │ Tracing (Langfuse)  │  Metrics (Prometheus)  │  Logs (ELK)   │   │
│ │ 评估 Pipeline       │  Cost Dashboard       │  Alerting     │   │
│ └──────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
"""

# 各层的核心职责

class AgentFrameworkLayer:
    """
    Agent Framework Layer - 让开发者能高效构建可靠 Agent
    
    核心能力:
    1. Agent Loop 管理 - 状态机 / 重试 / 熔断 / 断点续传
    2. Tool Registry - 工具注册 / Schema 校验 / MCP 桥接
    3. Context Manager - 多轮对话 / 记忆管理 / RAG 集成
    4. Skill System - 技能热加载 / 权限 / 版本管理
    5. 安全沙箱 - 执行隔离 / 资源限制 / 审计
    
    知识库对应: Agent_Loop, MCP, Claude_Code_Skills, Agent沙箱工程
    """

class GatewayLayer:
    """
    LLM Gateway Layer - 企业级 LLM 接入基础设施
    
    核心能力:
    1. 多模型路由 - 按能力/成本/延迟/可用性智能分流
    2. 鉴权与审计 - API Key / JWT / RBAC / 全审计日志
    3. 限流与治理 - 租户级/全局级限流, 优先级队列
    4. 缓存加速 - Exact Match + Semantic Cache
    5. 成本管控 - Token 计量/预算告警/费用分摊
    6. 优雅降级 - 多 Provider Fallback / 降级策略
    
    知识库对应: LLM_Gateway模式, Cost_Optimization, Graceful_Degradation
    """
```

### 4.2 关键设计决策与权衡

| 决策点 | 方案 A | 方案 B | 推荐理由 |
|--------|--------|--------|---------|
| **Agent Framework 选型** | 自建 Framework | 基于 LangChain/LangGraph | 大型企业推荐**自建 + 开源核心**——LangGraph 作为编排引擎，自建 Tool Registry 和 Context Manager |
| **Gateway 架构** | 集中式（所有流量经过单一 Gateway） | 去中心式（每个 Agent 直接调用模型） | **集中式**——企业必须有统一的鉴限、审计、成本管控。Gateway 是 Central Policy Enforcement Point |
| **模型部署** | 全云端 | 混合（云端+私有部署） | **混合**——敏感数据走私有 vLLM（如代码库内部 Agent），非敏感走云端。Gateway 透明路由 |
| **缓存策略** | 只做 Exact Match Cache | Exact + Semantic Cache | **分级缓存**——L1 Exact Cache（LRU, TTL 60s）, L2 Semantic Cache（Embedding 相似度, TTL 300s） |
| **费用分摊** | 按 API Key 平摊 | 按 Token + 模型精细计量 | **精细计量**——Redis INCR 实时记录, 每日出报表, 团队级 budget alert |
| **可观测性方案** | 自建 Prometheus + Grafana | Langfuse 托管 | **混合**——Langfuse 做 LLM Trace, Prometheus 做系统指标, 评估 Pipeline 用 promptfoo |

---

## 五、面试应答策略

### 5.1 不同的面试环节，不同的回答粒度

| 面试环节 | 回答深度 | 重点展示 | 时间控制 |
|---------|---------|---------|---------|
| **简历面** | 简述项目结果 | STAR 法则、量化指标 | 3-5 min/题 |
| **技术深度面** | 展开架构决策 | Harness Engineering 框架、伪代码 | 10-15 min/题 |
| **System Design** | 架构蓝图 + 权衡分析 | 分层架构、关键权衡、故障场景 | 30-45 min |
| **交叉面（非 AI）** | 讲清楚你做了什么 | 业务视角、ROI、协作 | 5-8 min/题 |
| **HR 面** | 一句话总结亮点 | 匹配度、成长性、文化 | 2-3 min/题 |

### 5.2 回答时的三层工程模型话术

在任何技术面中，用这个话术结构组织回答，展示系统思维：

```
第一步：Prompt Engineering 层面 → "首先，我们需要给 Agent 设计高质量的指令..."
第二步：Context Engineering 层面 → "其次，我们需要把相关的上下文信息（日志/指标/代码）有效组织到窗口里..."
第三步：Harness Engineering 层面 → "最重要的是，我们需要设计 Agent 外部的执行控制系统——包括工具调用、安全边界、错误恢复、可观测性和成本管理..."
```

### 5.3 核心话术模板

**Q: "你做过的最复杂的系统设计是什么？"**

> "我负责设计的是一个 AI 驱动的 CI/CD Agent 系统。从 [[Harness_Engineering]] 的角度来看：
>
> **Prompt Engineering 层面**：我们为不同的 CI 阶段设计了结构化的 Agent Prompt——代码审查 Agent 的 Prompt 强调安全性和性能；构建 Agent 的 Prompt 关注错误诊断和修复方案。每条 Prompt 都经过 A/B 测试验证。
>
> **Context Engineering 层面**：我们构建了一个 Context Aggregator，把 PR diff、构建日志、历史失败模式、团队编码规范等信息组装成 Agent 可理解的上下文。使用了 RAG 来检索历史构建的失败原因。
>
> **Harness Engineering 层面**：这是最核心的部分。我们实现了 Agent Loop（Plan→Act→Verify→Repair→Commit 的完整闭环）、Safety Layer（写操作必须人工审批、自动修复有熔断机制）、Tool Registry（统一管理 Git/Jenkins/K8s 等工具的调用权限），以及 Cost Optimization（动态模型路由：简单 lint 用 Haiku、代码审查用 Sonnet、安全审查用 Opus，加上 Prompt Caching 省了约 70% 的成本）。
>
> 这套系统上线后，构建失败修复时间中位数从 45 分钟降到了 8 分钟，人工介入率从 100% 降到了 30%。"

---

## 六、关联页面

- [[摘要-devops-ai-architect-xiamen]] — 本 JD
- [[DevOpsAI架构师JD全景对标分析]] — JD 全景对标报告
- [[Harness_Engineering]] — 三层工程模型理论基础
- [[AI驱动的CICD]] — DevOps Agent 概念页
- [[智能排障系统]] — 智能排障概念页
- [[LLM_Gateway模式]] — LLM Gateway 概念页
- [[Cost_Optimization]] — 成本优化核心策略
- [[Graceful_Degradation]] — 优雅降级设计模式
- [[Agent_Loop]] — Agent 循环机制
- [[Agent_Observability]] — 可观测性
- [[Vue在效能平台中的应用]] — 前端技术栈
- [[Redis在效能平台中的应用]] — 中间件技术栈
