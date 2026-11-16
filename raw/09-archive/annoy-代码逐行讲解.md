# 逐行理解这段 Annoy 代码
Annoy 是 Spotify 开源的**近似最近邻检索库**，用来快速在海量向量里找相似向量（比如文本向量、图片向量检索），不是精确搜索，速度快，适合召回场景。

```python
# Create the search index, pass the size of embedding
search_index = AnnoyIndex(embeds.shape[1], 'angular')
```
1. 新建索引对象
- `embeds`：一般是一个二维数组，`(样本数量, 向量维度)`，也就是一堆 embedding 向量
- `embeds.shape[1]`：**单个向量的维度**（比如768维、512维）
- `'angular'`：距离度量方式，**角距离**，等价于余弦相似度（适合embedding向量，最常用）
> 其他可选：`euclidean`欧氏距离、`manhattan`曼哈顿距离等

```python
# Add all the vectors to the search index
for i in range(len(embeds)):
    search_index.add_item(i, embeds[i])
```
2. 把所有向量放进索引
- `i`：给每个向量分配一个**编号id**（0,1,2,3……），后面检索出来的就是这个id，你可以根据id找到对应的原始文本/图片
- `embeds[i]`：第i个向量

> ⚠️ 注意：add_item 只是加到内存里，还不能检索！必须 build

```python
search_index.build(10) # 10 trees
```
3. 构建森林（Annoy核心：随机投影树森林）
- `10` = 树的数量（n_trees=10）
- 原理：Annoy会建多棵独立的二叉树，查询的时候在多棵树里面分别搜索，合并候选结果，平衡**速度和准确率**
  - 树越多：召回准确率越高，但是构建索引、查询会更慢，占用内存更大
  - 树越少：速度快，更容易漏掉相似向量
> 经验值：一般 10~100，根据你的数据规模调

```python
search_index.save('test.ann')
```
4. 把建好的索引保存到本地文件 `test.ann`
- 作用：下次不用重新加载全部向量、重新build，直接 `AnnoyIndex.load("test.ann")` 加载索引，直接检索，节省时间

---

# 完整配套：加载索引 + 查询（你这段代码没有写，经常一起用）
```python
# 加载索引（维度、距离类型要和构建时一模一样！）
search_index = AnnoyIndex(768, 'angular')
search_index.load("test.ann")

# 拿一个待查询向量，找top5最相似的向量id
query_vec = embeds[0]
nearest_ids = search_index.get_nns_by_vector(query_vec, n=5)
print(nearest_ids)
```

# 一句话总结整体流程
**读取一批向量 → 创建索引容器 → 逐个存入向量 → 构建多棵随机树（建立检索结构）→ 保存索引文件，后续用来做向量相似度检索**

# 重要坑提醒
1. build 之后**不能再 add_item**！建好树就不能再加新向量了。如果有新增数据，只能重新build整个索引
2. load 的时候，维度和距离参数必须和build时完全一致，否则报错
3. 是**近似检索**，不是100%精准，树的数量影响召回效果

如果你想要，我可以给你写一份**可直接运行的完整demo（含造测试向量）**。
