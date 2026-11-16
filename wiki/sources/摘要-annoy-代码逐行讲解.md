---
title: "摘要-Annoy 代码逐行讲解"
type: source
tags: [来源, Annoy, 向量索引, 近似最近邻, 向量检索]
sources: [raw/01-articles/annoy-代码逐行讲解.md]
last_updated: 2026-11-04
---

# 摘要：Annoy 代码逐行讲解

## 核心摘要

这份笔记逐行拆解了 [[Annoy]] 的**四步建索引流程**：用 `AnnoyIndex(维度, 'angular')` 创建索引容器 → 用 `add_item(id, vector)` 逐个写入向量 → 用 `build(n_trees)` 构建随机投影树森林 → 用 `save(path)` 持久化索引文件。查询时用相同的维度与距离度量 `load()` 索引，再调用 `get_nns_by_vector(query, n)` 拿到 top-k 的 item id，并靠 id 回查原文/元数据。

核心取舍是**速度与召回率**：Annoy 是[[近似最近邻检索]]，不是精确搜索；`n_trees` 越大召回越高，但构建、查询和内存开销也越大，经验值一般取 10~100。笔记还给出了三个高频坑：build 后不能再 `add_item`、load 参数必须与 build 时一致、新增数据只能重建索引。

## 四步建索引流程

| 步骤 | API | 作用 | 关键点 |
|------|-----|------|--------|
| 1. 创建索引 | `AnnoyIndex(embeds.shape[1], 'angular')` | 指定向量维度与距离度量 | `embeds.shape[1]` 是单向量维度；`angular` 适合 embedding |
| 2. 写入向量 | `add_item(i, embeds[i])` | 给每个向量分配整数 id | 只进内存，此时还不能检索 |
| 3. 构建森林 | `build(10)` | 建 10 棵随机投影树 | 树越多越准越慢；一般 10~100 |
| 4. 保存索引 | `save('test.ann')` | 索引落盘 | 下次可直接 `load()`，无需重新 build |

```python
from annoy import AnnoyIndex

search_index = AnnoyIndex(embeds.shape[1], 'angular')

for i in range(len(embeds)):
    search_index.add_item(i, embeds[i])

search_index.build(10)      # 10 trees
search_index.save('test.ann')
```

## 加载与查询

```python
# 维度与距离度量必须和构建时完全一致
search_index = AnnoyIndex(768, 'angular')
search_index.load('test.ann')

query_vec = embeds[0]
nearest_ids = search_index.get_nns_by_vector(query_vec, n=5)
print(nearest_ids)
```

- `get_nns_by_vector` 返回的是 **item id 列表**，不是原文；应用层需要维护 `id → 原文/元数据` 的映射。
- 该接口与 [[Vector_Index]] 的「只存向量、元数据自己管」定位一致。

## 距离度量

| 度量 | 含义 | 适用场景 |
|------|------|---------|
| `angular` | 角距离，排序等价于余弦相似度 | embedding 向量检索（最常用） |
| `euclidean` | 欧氏距离 | 向量已归一化或关注绝对距离 |
| `manhattan` | 曼哈顿距离 | 关注 L1 距离的场景 |

> `angular` 下向量是否归一化不影响排序结果；但与其他库比较距离数值时要注意口径。

## n_trees 与召回率权衡

| 树数量 | 召回率 | 构建/查询速度 | 内存 |
|--------|--------|---------------|------|
| 少（如 10） | 较低，可能漏相似向量 | 快 | 小 |
| 多（如 100） | 较高 | 慢 | 大 |

经验值：一般 10~100，按数据规模与召回要求调整。

## 重要坑

1. **build 后不能再 `add_item`**：树结构已定型，新增数据只能重建整个索引。
2. **load 参数必须与 build 时一致**：维度、距离度量不一致会报错或得到错误结果。
3. **近似而非精确**：返回的是高概率近邻，不保证 100% 精准；树数量直接影响召回。
4. **id 对齐**：索引只返回 id，原文/元数据映射一旦错位，检索结果会整体串行（参见 [[Vector_Index]]）。

## 关联连接

- [[Annoy]] — 本文讲解的向量索引库
- [[近似最近邻检索]] — Annoy 所属的检索范式
- [[Vector_Index]] — 向量索引库概念
- [[Vector_Database]] — 完整数据库对照
- [[FAISS]] — 另一款高性能向量索引库
- [[RAG]] — Annoy 可用于小规模 RAG 原型
- [[摘要-向量数据库与向量索引库]] — 姊妹来源：讲「选型」，本文讲「用法」
