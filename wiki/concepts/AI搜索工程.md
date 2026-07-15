---
title: "AI搜索工程"
type: concept
tags: [AI搜索, 信息检索, LLM, 搜索引擎, RAG, 多模态检索, Context_Engineering, Harness_Engineering]
sources:
  - wiki/sources/摘要-deepseek-ai-search-jd.md
last_updated: 2026-07-15
---

# AI 搜索工程

## 定义

AI 搜索工程（AI-native Search Engineering）是融合大语言模型与传统信息检索技术的系统工程体系。其核心目标不是"给搜索引擎加一个 AI 对话层"，而是从根本上重构搜索引擎的架构——让每一次搜索提问都被 LLM 深度理解，在全球范围内找到准确、及时、权威的信息，并以 LLM 可直接消费的形式输出。

> 搜索是 AGI 感知世界的原生感官。AI 搜索工程的目标是让搜索成为 LLM 理解世界的重要基础设施。

## 与三层工程模型的关系

AI 搜索工程横跨三层工程模型，但以 **Context Engineering** 为主战场：

| 工程层 | AI 搜索中的对应 | 说明 |
|-------|---------------|------|
| **Context Engineering** | 检索结果的组装与管理 | 搜索是"Select"子问题在搜索引擎尺度的独立成体系——从有限文档库放大到互联网级 |
| **Harness Engineering** | 搜索 Pipeline 的调度与调优 | 召回→排序→过滤的管道本质上是一个大规模 Harness |
| **Prompt Engineering** | Query 改写与搜索提示优化 | Query 理解、意图分类、多轮对话的搜索上下文构建 |

> 核心区别：RAG 中检索是 LLM 的"上下文补充"，AI 搜索中检索是**独立且与 LLM 对等的系统组件**。

## 与传统搜索的根本差异

```
传统搜索                    AI 原生搜索
┌─────────────────┐       ┌─────────────────┐
│ Query: 关键词匹配  │       │ Query: LLM 语义理解 │
│ 索引: 倒排索引为主 │       │ 索引: 倒排 + 向量    │
│ 排序: LTR/点击信号 │       │ 排序: 语义 + 权威性  │
│ 输出: 蓝色链接列表 │       │ 输出: 结构化答案     │
│ 重查: 用户自己点   │       │ 重查: LLM 再次检索   │
│ 模态: 文本为主     │   →   │ 模态: 全模态平等     │
└─────────────────┘       └─────────────────┘
    ↓                        ↓
静态规则驱动               LLM 动态理解驱动
```

## 搜索 Pipeline

```
Query
  │
  ├──→ Query Understanding
  │       ├── Intent Classification（意图分类）
  │       ├── Query Rewriting（改写/补全/纠错）
  │       ├── Multi-Query Expansion（多查询扩展）
  │       └── Lang Detection（语言检测）
  │
  ├──→ Recall（召回层）
  │       ├── Sparse Retrieval（BM25 / 倒排索引）
  │       ├── Dense Retrieval（向量检索 - 稠密/hybrid）
  │       ├── Multi-Vector Retrieval（ColBERT 等多向量）
  │       └── Multi-Modal Retrieval（图文/视频检索）
  │
  ├──→ Ranking（排序层）
  │       ├── First-stage Ranker（轻量级粗排）
  │       ├── Second-stage Ranker（LTR 精排）
  │       ├── LLM Reranker（LLM 重排）
  │       └── Diversity Promotion（多样性保证）
  │
  ├──→ Index Filtering（索引筛选）
  │       ├── Quality Gating（质量门控）
  │       ├── Freshness Control（时效控制）
  │       ├── Authority Scoring（权威性评分）
  │       └── Dedup（去重）
  │
  ├──→ Quality Evaluation（质量评估）
  │       ├── Automated Evaluation（自动评估）
  │       ├── Badcase Analysis（Badcase 分析）
  │       └── User Feedback Loop（用户反馈闭环）
  │
  └──→ Output（输出）
          ├── LLM-friendly Format（结构化输出）
          ├── Multi-Modal Presentation（多模态呈现）
          └── Agent Integration（Agent 检索工具）
```

## 核心技术维度

### 1. Query 理解

| 技术 | 说明 |
|------|------|
| **LLM-based Intent Classification** | 用 LLM 代替传统分类器做意图识别，支持零样本新意图 |
| **Query Rewriting** | LLM 改写/补全/纠错模糊查询（如"苹果公司2024年…"→"Apple Inc. 2024 financial results"）|
| **Multi-Query Expansion** | 用 LLM 从原始查询生成多个变体，分别检索后合并 |
| **Cross-lingual Understanding** | 同一种语义在不同语言间检索（中文 Query 检索英文文档） |

### 2. 召回技术全家桶

| 召回类型 | 代表技术 | 适用场景 |
|---------|---------|---------|
| **Sparse（稀疏）** | BM25、倒排索引、词权重 | 精确匹配、专有名词、代码片段 |
| **Dense（稠密）** | DPR、Contriever、GTR | 语义匹配、同义改写、跨语言 |
| **Hybrid** | Sparse + Dense + RRF 融合 | Production 标配，绝大多数场景最优 |
| **Multi-Vector** | ColBERT、ColPali | 文档内细粒度匹配、跨模态 |
| **Multi-Modal** | CLIP、SigLIP | 图文联合检索 |

### 3. 排序架构

```
                       ┌─────────────┐
                       │ 全量索引文档  │
                       └──────┬──────┘
                              │
                     ┌────────▼────────┐
                     │ Recall 取千级   │ 第一级：轻量级模型，高召回
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │ First-Stage     │ 第二级：LTR 模型，百级
                     │ Ranking         │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │ Second-Stage    │ 第三级：深度模型/LLM，十级
                     │ Ranking         │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │ LLM Reranker    │ 终极排序：LLM 理解全文质量
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │   Top-N 结果     │
                     └─────────────────┘
```

### 4. 索引构建（离线管线）

```
原始文档
    │
    ├──→ Document Processing
    │       ├── HTML/PDF/Image Extraction
    │       ├── Chunking & Segmentation
    │       ├── Language Detection
    │       └── Quality Filtering
    │
    ├──→ Indexing
    │       ├── Inverted Index（倒排索引）
    │       ├── Vector Index（向量索引）
    │       ├── Multi-Vector Index
    │       └── Multi-Modal Index
    │
    └──→ Metadata Storage
            ├── Quality Score
            ├── Freshness Score
            ├── Authority Score
            └── Dedup Signature
```

### 5. 混合（Hybrid）检索的 RRF 融合

Hybrid Search = Sparse（BM25） + Dense（向量检索），通过 **RRF（Reciprocal Rank Fusion）** 融合排名：

```
score(d) = Σ 1 / (k + rank_i(d))
```

- k 是平滑常数（通常 60）
- rank_i(d) 是文档 d 在第 i 种检索方式中的排名
- 不依赖分数归一化，直接操作排名值

> 从 [[RAG]] 概念继承的技术，在 AI 搜索中被扩展为多路召回（Multi-stage recall）的统一融合策略。

## 挑战与权衡

### 核心约束三角：成本 × 延迟 × 效果

```
                 效果（Accuracy）
                   ↑
                  ╱╲
                 ╱  ╲
                ╱    ╲
               ╱      ╲
              ╱        ╲
             ╱          ╲
            ╱            ╲
           ╱              ╲
  成本 ←────────────────────→ 延迟
       （Cost）            （Latency）
```

| 瓶颈类型 | 问题 | 典型解法 |
|---------|------|---------|
| **计算瓶颈** | 全量向量检索 + LLM Reranker 计算量太大 | PQ 量化、IVF 索引、Stage-wise 级联 |
| **存储瓶颈** | 向量索引内存占用远超倒排索引 | 量化压缩（FP32→INT8）、磁盘向量索引 |
| **网络瓶颈** | 分布式检索中跨节点通信开销 | RDMA、聚合通信优化、数据本地性 |
| **延迟瓶颈** | 端到端搜索 > 1s 即用户不可感 | 预计算、服务端缓存、推测式执行 |

### 多语言与跨地域

- 不同语言的 Query 结构和索引密度差异巨大（英语搜索 vs 小语种搜索）
- 内容生态差异（不同地区的搜索结果质量不同）
- 解决方案：语言特定的分词器 + 语言适配的索引分片策略

### 搜索质量评估体系

| 评估维度 | 指标 | 自动化程度 |
|---------|------|-----------|
| **相关性** | NDCG、MRR、Recall@K | 可自动化标注 |
| **权威性** | 来源可信度评分 | 半自动化 |
| **时效性** | 结果时效性指标 | 可自动化 |
| **多样性** | 结果覆盖度 | 可自动化 |
| **LLM 适配性** | 检索结果是否被 LLM 有效使用 | 需 LLM-as-Judge |
| **用户满意度** | CTR、停留时间、满意度调研 | 需线上数据 |

---

## 知识冲突

### Sparse vs Dense：谁主沉浮？
- **传统派**：倒排索引 + BM25 足够稳定、可解释、低成本
- **新趋势**：稠密向量检索在语义匹配上全面超越稀疏检索
- **调和**：Production 系统中 Hybrid Search（两者结合 + RRF）被验证为最优方案

### LLM Reranker 的必要性
- **性能派**：Cross-encoder / LLM 重排能显著提升最终排序质量，值得额外延迟
- **效率派**：Stage-wise 级联架构中，第一/二级排序足够好，LLM Reranker 是过度工程
- **调和**：取决于场景——高精度场景（医疗、法律）需要 LLM Reranker；高吞吐场景（通用搜索）可以省略

### "极致简洁" vs "多模态全覆盖"
- **简洁要求**：系统要轻量、少依赖、快速迭代
- **覆盖要求**：多语言、多场景、多模态——天然增加系统复杂度
- **调和**：统一的 Embedding Space + 模态无关的索引结构，以架构简洁应对场景丰富

---

## 关联连接

- [[AI创作数据工程]] — 创作审美评测数据层：将人类审美标准转化为可操作的评测体系与数据管线，驱动模型在文学创作与实用写作领域的能力提升
- [[Agent数据产品工程]] — 评测数据桥梁层：通过评测体系设计与数据生产管线构建，连接产品体验与模型能力；聚焦办公/生活/搜索等通用场景
- [[Agent能力工程]] — 能力构建层：通过 RL 环境构建、评测任务设计和能力短板补齐，系统性地提升模型 Agent 能力
- [[AI产品工程]] — 最上层产品化层：站在模型与世界之间，将 AI 技术能力转化为用户体验的产品化工程层
- [[摘要-deepseek-ai-search-jd]] — 来源资料：本概念的原始 JD 来源
- [[DeepSeek四份JD全景对比]] — 综合报告：DeepSeek 四个团队 JD 的横向对比
- [[RAG]] — AI 搜索的技术基础，检索增强生成
- [[Context_Engineering]] — AI 搜索是 Context Engineering "Select"子问题的搜索引擎尺度扩展
- [[Harness_Engineering]] — 搜索 Pipeline 的系统工程（召回→排序→过滤→评估）
- [[Context_Window]] — LLM 的上下文窗口限制是搜索结果的物理边界
- [[Cost_Optimization]] — 成本-延迟-效果三元平衡的优化策略
- [[Eval_Harness]] — 搜索质量评估体系的评估方法论
- [[Agent_Interfaces]] — 搜索作为 Agent 的感知接口
- [[Agent_Loop]] — 搜索集成进 Agent Loop 的方式
- [[Chunking]] — 索引构建中的文档分割策略
- [[LightRAG]] — GraphRAG 与搜索的结合
- [[Memory_Agent]] — 搜索历史作为 Agent 的长期记忆
- [[DeepSeek]] — DeepSeek 公司实体页面
- [[摘要-deepseek-harness-team-jd]] — 同公司 Harness 团队对比
- [[摘要-deepseek-service-engineer-jd]] — 同公司服务端工程团队对比
- [[摘要-预训练数据工程师-jd]] — 同公司预训练数据团队对比
