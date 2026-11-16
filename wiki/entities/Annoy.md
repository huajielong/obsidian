---
title: "Annoy"
type: entity
tags: [向量索引, 向量检索, Spotify, 近似最近邻, 工具]
sources: [raw/01-articles/向量数据库与向量索引库-课程笔记.md, raw/01-articles/annoy-代码逐行讲解.md]
last_updated: 2026-11-04
---

# Annoy

## 定义

Annoy（Approximate Nearest Neighbors Oh Yeah）是 Spotify 开源的**轻量级向量索引库**，用于小到中等规模的近似最近邻搜索。它 API 简单、上手最快，但同样只存向量，不存原文和元数据。

> 定位：[[Vector_Index|向量索引库]]，适合课程演示、小数据集和快速验证。

## 关键信息

| 维度 | 说明 |
|------|------|
| **开发者** | Spotify |
| **核心优势** | 上手最简单，适合小到中等规模向量 |
| **核心结构** | 随机投影树森林（多棵独立二叉树） |
| **距离度量** | `angular`（默认，适合 embedding）/ `euclidean` / `manhattan` |
| **建索引参数** | `n_trees` 一般 10~100，越大召回越高、越慢 |
| **索引持久化** | 可保存索引到本地文件并加载 |
| **存储内容** | **只有向量**，原文需自己单独管理 |
| **关键词检索** | ❌ 没有 BM25 |
| **复杂过滤** | ❌ 不支持 |
| **内置向量化** | ❌ 需自己调用 embedding |
| **精度 / 规模** | 弱于 [[FAISS]]；规模上限较低 |
| **适用规模** | 小到中等规模 |

## 构建流程（四步）

```python
from annoy import AnnoyIndex

# 1. 创建索引：维度 + 距离度量
search_index = AnnoyIndex(embeds.shape[1], "angular")

# 2. 逐个写入向量，id 由应用层分配
for i in range(len(embeds)):
    search_index.add_item(i, embeds[i])

# 3. 构建随机投影树森林
search_index.build(10)   # 10 trees

# 4. 保存索引文件
search_index.save("test.ann")
```

| 步骤 | 说明 |
|------|------|
| `AnnoyIndex(dim, metric)` | `dim` 是单个向量维度；`metric` 选 `angular` / `euclidean` / `manhattan` |
| `add_item(i, vector)` | 只写入内存，此时还不能检索；`i` 是之后检索返回的 item id |
| `build(n_trees)` | 构建 `n_trees` 棵随机投影树；建完树后不能再 `add_item` |
| `save(path)` | 索引落盘；只保存向量索引，不保存原文/元数据 |

## 核心机制：随机投影树森林

Annoy 会构建多棵独立的二叉树，每个内部节点用一个随机超平面把空间分成两半。查询时在多棵树中分别下行搜索，合并各树候选后再排序，用「多棵树投票」的方式平衡**速度与召回率**：

- **树越多**：召回率越高，但构建索引、查询更慢，占用内存更大；
- **树越少**：速度快，但更容易漏掉相似向量；
- **经验值**：`n_trees` 一般取 10~100，按数据规模与召回要求调整。

## 查询流程（load + get_nns_by_vector）

```python
# 维度与距离度量必须和构建时一模一样
search_index = AnnoyIndex(768, "angular")
search_index.load("test.ann")

query_vec = embeds[0]
nearest_ids = search_index.get_nns_by_vector(query_vec, n=5)
print(nearest_ids)
```

- `get_nns_by_vector` 返回的是 **item id 列表**，不是原文；需要用 id 回查自己维护的 `id → 原文/元数据` 映射。
- `load()` 只加载索引，不校验业务数据；原文与元数据仍需另行保存。
- 召回率与成本的通用权衡见 [[近似最近邻检索]]。

## 重要限制与坑

1. **build 后不能再 `add_item`**：树结构已定型，新增向量只能重建整个索引。
2. **load 参数必须与 build 一致**：维度、距离度量不一致会报错或得到错误结果。
3. **近似而非精确**：Annoy 返回高概率近邻，不保证 100% 精准；`n_trees` 直接影响召回。
4. **id 必须与原文对齐**：索引只返回 id，映射错位会导致检索结果整体串行。

## 适用场景

- 课程演示
- 小数据集
- 只想快速测试向量相似度
- 不需要 BM25、过滤和数据库能力

## 不适用场景

- 百万级以上的大规模向量
- 需要高精度检索
- 需要关键词/混合检索
- 需要条件过滤或长期数据管理

以上场景应选择 [[FAISS]]（规模/速度）或[[Vector_Database|向量数据库]]（完整能力）。

## 关联连接

- [[Vector_Index]] — Annoy 所属的产品类别
- [[近似最近邻检索]] — Annoy 所属的 ANN 检索范式
- [[Vector_Database]] — 完整数据库对照
- [[FAISS]] — 同类别的高性能索引库
- [[Weaviate]] — 完整向量数据库代表
- [[Cohere]] — 提供向量化的上游服务
- [[RAG]] — Annoy 可用于小规模 RAG 原型
- [[摘要-向量数据库与向量索引库]] — 本实体的选型来源
- [[摘要-annoy-代码逐行讲解]] — 本实体的代码用法来源
