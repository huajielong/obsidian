---
title: "KV Cache 存储系统"
type: concept
tags: [分布式存储, KV Cache, 推理优化, 低延迟存储, 高性能I/O, 基础设施]
sources:
  - wiki/sources/摘要-hpc-distributed-storage-jd.md
last_updated: 2026-07-22
---

# KV Cache 存储系统（KV Cache Storage Systems）

## 定义

KV Cache 存储系统是**为 LLM 推理场景设计的分布式键值缓存基础设施**，解决的核心问题是：如何在分布式集群中为推理请求提供低延迟、高可用、大容量的 KV Cache 服务。

它是 [[AI存储工程]] 三大存储系统之一，位于 GPU 显存（HBM）与持久化存储之间的**第二级缓存层**，是连接推理引擎与持久化存储的关键桥梁。

---

## 架构层次

```
推理请求 → vLLM/SGLang 推理引擎
              ↓
        本地 KV Cache（GPU HBM）      ← 第一级：显存缓存（ns 级延迟，容量小）
              ↓（换出）
        分布式 KV Cache 存储          ← 第二级：本系统 ★（μs-ms 级延迟，TB-PB 级容量）
              ↓（持久化）
        分布式文件系统 / 对象存储      ← 第三级：持久化存储（ms-s 级延迟，无限容量）
```

### 三级缓存对比

| 维度 | GPU HBM | 分布式 KV Cache 存储 | 持久化存储 |
|------|---------|---------------------|-----------|
| **介质** | HBM3/3E | DRAM + NVMe SSD | NVMe SSD / HDD / 对象存储 |
| **延迟** | ~ns | ~μs-ms | ~ms-s |
| **容量** | GB 级（单卡 ~80-144GB） | TB-PB 级 | PB-EB 级 |
| **成本** | 极高 | 中等 | 低 |
| **访问协议** | GPU 内部 | RDMA / TCP | POSIX / S3 API |

---

## 关键需求与指标

| 需求 | 目标指标 | 实现手段 |
|------|---------|---------|
| **极低延迟** | P99 < 1ms | RDMA 零拷贝 + SPDK 用户态 I/O |
| **超高吞吐** | 上亿级 IOPS | 分布式架构 + 多副本并行 + SSD 聚合 |
| **高可用** | 99.99%+ | Raft 共识 + 自动故障切换 |
| **大容量** | TB-PB 级 | 多节点 SSD 聚合 + DRAM 缓存 + 分层存储 |
| **一致性** | 最终一致性即可 | 推理场景可容忍少量过时 Cache |

> **延迟-容量悖论**：KV Cache 需要极低延迟（毫秒级），又要大容量（TB-PB 级），两者天然矛盾。核心平衡策略是**多级缓存 + 智能预取**——预测哪些 KV Cache 即将被访问，提前从慢层加载到快层。

---

## 核心技术栈

### 高性能 I/O 路径

从应用到 NVMe SSD 的完整 I/O 路径：

```
应用逻辑（KV Cache 查询/写入）
    ↓
序列化/反序列化（Protobuf / Cap'n Proto / FlatBuffers）
    ↓
存储引擎（LSM-Tree / B-Tree，基于 RocksDB 或定制引擎）
    ↓
I/O 框架（io_uring / SPDK）
    ↓
NVMe 驱动（内核态 / 用户态 SPDK）
    ↓
NVMe SSD（PCIe Gen4/Gen5）
```

### io_uring vs SPDK

| 维度 | io_uring | SPDK |
|------|---------|------|
| **操作模式** | 内核辅助的异步 I/O | 用户态轮询 |
| **延迟** | 低（~1-5μs） | 极低（~0.5-1μs） |
| **CPU 占用** | 低（中断驱动） | 高（轮询占满核心） |
| **适用场景** | 通用存储引擎 | KV Cache、极致低延迟场景 |
| **开发复杂度** | 中等 | 高 |

### RDMA 零拷贝

RDMA 跳过 CPU 和内核网络栈，直接在存储节点和应用内存之间传输数据：

```
传统路径：  存储节点内存 → CPU → 内核栈 → NIC → 网络 → NIC → 内核栈 → CPU → 应用内存
RDMA 路径： 存储节点内存 → NIC（RDMA 引擎）→ 网络 → NIC（RDMA 引擎）→ 应用内存
                     跳过 CPU 和内核                  直接内存访问
```

### 本地存储引擎

| 技术 | 特点 | 适用 |
|------|------|------|
| **RocksDB**（LSM-Tree） | 写优化、压缩、范围查询 | KV Cache 本地存储默认选项 |
| **WiredTiger**（B-Tree + LSM） | 读写平衡、多线程 | 元数据存储 |
| **自研引擎**（基于 io_uring/SPDK） | 针对 KV Cache 模式极致优化 | 大规模自建场景 |

---

## 与推理框架的协作

[[AI训练推理系统工程]] 中的 KV Cache 优化技术在此落地：

| 推理框架侧 | 存储侧响应 |
|-----------|-----------|
| **PagedAttention** 管理显存 KV Cache | 换出到存储系统，按 Page 粒度管理 |
| **Prefix Caching** 识别共享前缀 | 存储系统提供前缀索引和快速查找 |
| **KV Cache 磁盘持久化** | 存储系统提供跨 session 的持久化 Bucket |

### 典型工作流

```
1. 推理请求进入，vLLM/SGLang 分配 GPU HBM 空间
2. 检查本地 Prefix Cache → 命中则跳过已计算部分
3. 检查分布式 KV Cache → 命中则 RDMA 拉回，不用重算
4. 逐 Token 生成，新的 KV Cache 写入本地 HBM
5. HBM 满时，Least Recently Used 页面换出到分布式存储
6. Session 结束时，持久化到文件系统（可选）
```

---

## 设计挑战

### 1. 延迟-容量悖论（核心矛盾）

```
低延迟 ←──────────────────────────────────→ 大容量
   DRAM（ns 级）    SSD（μs-ms 级）     HDD/对象存储（ms-s 级）
   ↑ 小容量              ↑ 本系统                ↑ 大容量
```

**平衡策略**：
- **智能预取**：预测即将访问的 KV Cache，提前从 SSD 加载到 DRAM
- **分层存储**：热 Cache 在 DRAM / 温 Cache 在 SSD / 冷 Cache 在远端
- **自适应换入换出**：基于访问频率和大小的换页策略

### 2. 一致性 vs 性能

| 操作 | 需要的一致性 | 折衷方案 |
|------|------------|---------|
| KV Cache 读取 | 最终一致即可 | 旧 Cache 最多导致重新计算，无害 |
| 元数据操作 | **强一致必须** | Raft 共识确保元数据一致性 |
| Cache 失效 | 最终一致 | 异步广播失效，容忍短暂不一致 |

### 3. 分布式扩展

- **数据分片**：一致性哈希 / Range-based 分片
- **副本策略**：2-3 副本 + Quorum 读写
- **故障恢复**：Raft Leader 切换 → 降级读 → 数据重建

---

## 与 Harness Engineering 的关系

| Harness 元件 | KV Cache 存储贡献 |
|-------------|------------------|
| **① Agent Loop** | 推理状态缓存加速 Agent 多轮交互 |
| **⑧ Cost / Latency** | **最直接关联**：Cache 命中减少重复计算，直接降低推理成本和延迟 |

> KV Cache 存储系统是 Cost Optimization 在基础设施层的物理实现之一——在 [[Harness_Engineering]] 8 核心元件中，它主要通过第 8 元件（Cost/Latency）体现价值。

---

## 行业实现

| 类型 | 代表 | 特点 |
|------|------|------|
| **推理框架内置** | vLLM（Prefix Caching）、SGLang（RadixAttention） | 框架原生集成，部署简单 |
| **分布式缓存系统** | Redis / Memcached / KeyDB | 通用 KV 缓存，延迟低但容量有限 |
| **AI 专用存储** | DeepSeek（自研 KV Cache 存储） | 针对推理模式极致优化，RDMA 原生 |
| **云服务** | AWS ElastiCache / GCP Memorystore | 托管服务，按需付费 |

---

## 关联连接

- [[AI存储工程]] — 母概念：三大存储系统之一的独立展开
- [[AI训练推理系统工程]] — 推理框架侧：PagedAttention / Prefix Caching 等与存储的协作
- [[Harness_Engineering]] — Harness 第 8 元件（Cost/Latency）的物理实现
- [[Cost_Optimization]] — KV Cache 存储直接降低推理 Token 的重复计算成本
- [[Agent_Loop]] — Agent 多轮对话中利用 KV Cache 存储加速重复上下文
- [[超算集群工程]] — 分布式存储的物理运行环境
- [[摘要-hpc-distributed-storage-jd]] — 来源 JD：高性能分布式存储工程师职位描述
- [[AI搜索工程]] — 搜索场景的向量索引与 KV Cache 共享低延迟存储设计范式
- [[Agent沙箱工程]] — Agent 执行环境快照的存储与 KV Cache 存储共用底层基础设施
