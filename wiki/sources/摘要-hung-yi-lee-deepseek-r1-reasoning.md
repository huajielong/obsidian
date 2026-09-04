---
title: "摘要-李宏毅-DeepSeek-R1-深度思考"
type: source
tags: [来源, 转录, 李宏毅, DeepSeek-R1, 推理, reasoning, 生成式AI, 机器学习课程]
sources: [raw/09-archive/【生成式AI時代下的機器學習(2025)】第七講：DeepSeek-R1 這類大型語言模型是如何進行「深度思考」（Reasoning）的？.md]
last_updated: 2026-08-05
---

## 核心摘要

李宏毅《生成式AI時代下的機器學習(2025)》第七讲，聚焦一个核心问题：**如何打造能进行"深度思考"（Reasoning）的大型语言模型**。深度思考指模型在给出最终答案前，先产生一段很长的思考过程（通常包裹在 `think`/`/think` 标记中，供界面选择是否展示），这个过程被称为 **reasoning**，是 **Test-Time Compute（测试时计算）** 的一种——"深度不够、长度来凑"，在推理阶段投入更多算力换取更好的结果。

讲座归纳了四种打造推理模型的方法，并强调**四种方法并不互斥**：

1. **更强的思维链（CoT）**：从 Few-shot CoT、Zero-shot CoT（"Let's think step by step"）到 **Supervised CoT**（把思考流程/验算要求写进 prompt），无需微调即可让强模型表现出一部分深度思考能力（GPT-4o 演示；弱模型如 Llama 3 读不懂复杂指令）。
2. **为模型提供推理工作流程**：让模型对同一问题采样几千上万次（Large Language Monkeys），再用 **Majority Vote / Self-Consistency**、**Confidence**、**Verifier + Best-of-N**、**Process Verifier + Beam Search** 选出正确答案；1B 模型靠这套工作流甚至能超越 8B 模型。
3. **教导模型推理过程（Imitation Learning）**：用"问题+答案+推理过程"训练数据教模型推理；推理过程可由 LLM 生成、用树状搜索 + 过程验证器筛选，并引入 **Stream of Search / Journey Learning** 让模型学会"知错能改"（只教全对路径的 Shortcut Learning 效果更差）；也可直接向已有推理模型做 **Knowledge Distillation**。
4. **以结果为导向学习推理（Reinforcement Learning）**：只看最终答案对错给 reward，不管推理过程（DeepSeek-R1 主打）。R1-Zero 纯 RL 训练后 AIME 逼近 o1，并自发涌现 **Aha moment**，但因推理过程难读而不可用；真正的 R1 是"R1-Zero 生成数据→人工改写→模仿学习→RL→再生成数据→再模仿学习→RL（安全/有用性）"的复杂流水线，四类方法全部用上。RL 只强化模型已有能力，蒸馏（方法 3）对中小模型更有效。

## 课程信息

- **来源**：YouTube《【生成式AI時代下的機器學習(2025)】第七講：DeepSeek-R1 這類大型語言模型是如何進行「深度思考」（Reasoning）的？》
- **URL**：https://www.youtube.com/watch?v=bJFtcwLSNxI
- **讲师**：[[Hung_yi_Lee]]（李宏毅，台湾大学）
- **发布**：2025-04-26
- **投影片**：Google Slides 链接见原始文件
- **性质**：课程转录（繁体中文 → 简体中文提炼）；本讲为"深度思考模型"系列前半段，后半段（推理模型的挑战与未来）留待下一讲

## 一、什么是深度思考（Reasoning）

### 行为特征

- **深度思考模型**：ChatGPT o 系列、DeepSeek R 系列、Gemini Flash Thinking、Claude 3.7 Sonnet Extended Thinking 等。回答前先给一段很长的思考过程，再给出答案。
- 思考过程通常包裹在 `think` 与 `/think` 两个标记之间，**加标记主要是为了界面呈现方便**——设计界面时可以决定要不要把里面的内容展示出来。
- 思考过程中模型常有的行为：**验证**刚才的答案（"Let me check the answer"）、**探索**其他可能性、**规划**解题步骤。

### Reasoning vs Inference 辨析

| 词 | 中文 | 含义 |
|----|------|------|
| **Inference** | 推论 | 使用模型（让模型产生答案）的动作本身 |
| **Reasoning** | 推理 | 模型在产生答案时输出特别长的思考过程这一行为 |

- 李宏毅强调：称其为"推理"**不代表模型的行为与人类推理相同**，只是直接借用这个词。

### Test-Time Compute

- 深度思考行为是 **Testing Time Compute（测试时计算）** 的一种：在测试阶段投入更大算力，可能得到更好结果——"深度不够、长度来凑"。
- 例证：**AlphaGo** 在训练时用 Policy Network + Value Network，但测试时用 **Monte Carlo Tree Search（MCTS）** 做巨额运算（脑内模拟落子后局面、预测胜率、选最优位置）。
- **Test-Time Scaling**：思考越多往往结果越好。上古论文（棋类游戏）已显示：同样分数，可把算力投在训练（更大的 policy network）或测试（更大规模 MCTS 搜索）上，两者可互相成就；且当时作者惊叹"测试时只用少量算力就能减少大量训练算力"。

## 二、方法一：更强的思维链（Better Chain-of-Thought）

> 无需微调参数，只改 prompt。**只适用于较强的模型。**

- **Few-shot CoT**（2022）：给模型"问题→解法→答案"范例，引导它先写过程再给答案。
- **Zero-shot CoT**：直接说 "Let's think step by step"，模型自动列过程。
- **Long CoT vs Short CoT**：现在推理模型的思考过程往往很长，被称为 **Long Chain-of-Thought**；2022 年的 CoT 被称为 Short CoT。长/短没有固定分界标准。
- **Supervised CoT**：不只是叫模型 think step by step，而是**用人类知识把"怎么想"写进 prompt**（不是机器学习里的 supervised learning）。例：告诉模型"回答前先深入解析题目要求、定出完整解题计划、列出子计划、每步多次验算、考量所有可能解法、思考过程放在 think 标记中间"。
  - 演示（GPT-4o 算 123×456）：模型先做题目分析、制定计划（拆解 400+50+6）、分步计算、做了三次验算（直式乘法重算 / 估算上下界 / 乘法交换律重拆），甚至学会"算到一半发现这招没用就果断略过"（"无明确帮助略过"）。
  - **局限**：弱模型（如 Llama 3）无法读懂这么复杂的指令，不能照做多次验算。

## 三、方法二：为模型提供推理工作流程（Reasoning Workflow）

> 无需微调参数，**对弱模型也能大幅强化**。核心思想：把"探索→验证→择优"的工作流程显式交给模型。

### 大规模采样：Large Language Monkeys

- 灵感来自**无限猴子定理**：让模型对同一个问题回答几千几万次（每次输出不同），总有机会"赛到"正确答案。
- 论文实验（纵轴 Coverage：只要某一次输出正确就算对）：Llama-3 70B 试较少的次数就能答对；Llama-3 8B / Gemma 7B 试到上万次也能覆盖到正确答案；但特别弱的模型（**Pythia 70M**，参数仅百万级）试上万次也很难答对。
- 难点：模型产生上万个结果，**怎么知道哪一个是正确答案？**

### 选出正确答案的方法

| 方法 | 做法 | 备注 |
|------|------|------|
| **Majority Vote / Self-Consistency** | 看哪个答案出现次数最多 | 简单但非常强，建议作为 baseline；通常强制模型把答案放在 `answer`/`/answer` 标记中便于提取 |
| **Confidence** | 用模型产生该答案的机率作为置信度 | 用于 CoT-decoding |
| **Verifier + Best-of-N** | 训练/使用一个验证器给每个候选答案打分，选最高分 | 验证器可现成用 LLM"反思"判断，也可用"问题+正确答案"数据训练（答对输出 1、答错输出 0） |
| **Process Verifier + Beam Search** | 边解边验证中间步骤，只保留最好的 n 条路径 | 能避免"第一步错、白算很久" |

### 关键实验（Hugging Face Blog）

- Majority Vote 让 Llama 3.2 1B 远好于原版，但仍不如 8B；Best-of-N 更好；**Beam Search（Bin Search）最好——用 1B 模型即可超越 8B 模型**。
- Beam Search 步骤：让模型只输出第一步（用 `step`/`/step` 标记 + 遇到 `/step` 就停止生成）→ 用 Process Verifier 给每步打分 → 只保留最好 n 条路径继续 → 重复。这本质是**启发式搜索**，A* 与 MCTS 都可以套进同一框架（2024 年夏有大量论文把 MCTS 用于 LLM 推理）。
- **DVTS** 是 Beam Search 变体（保留更多样化的路径），但效果不显著。
- **并行（parallel）与串行（sequential）** 两种范式可结合：先并行解出多个答案，再根据前一轮解法串行迭代。

### 中途验证的重要性

- 现在的深度思考模型往往**解到一半就开始验证中间步骤**（DeepSeek 算 123×456 花 59 秒，先分解 450+6，算 123×4=492 时先验算这一步），避免"一步错、步步错、最后白算"。

## 四、方法三：教导模型推理过程（Imitation Learning）

> 需要微调参数，可视为上一讲"后训练（Post-training）"的特例。**训练数据 = 问题 + 答案 + 推理过程。**

### 核心难点：推理过程从哪来？

- 通常只有"问题+正确答案"而没有推理过程；让人写太贵。
- **用 LLM 自己生成推理过程**：让模型按 CoT 详细解题 → 只有答对的 reasoning 过程才拿来当训练资料（假设"答案对 ⇒ 推理过程大概率对"）；无标准答案的问题可用 verifier（甚至现成的 LLM）判断答案好坏。
- 更严格：用**树状搜索 + Process Verifier** 逐步验证，只保留验证通过的正确路径拼成推理过程。

### 关键洞察：不要只教"全对的推理"

- 若训练数据每一步推理都是对的，模型**不知道推理过程可能会错**——前面错了也不知道，只会一直硬凹下去（一步错、步步错）。
- 应该教模型**知错能改**：
  - **Stream of Search**：在树状结构上做深度优先搜索，把**包含错误路径的推理过程**也放进训练数据（如"先走 step1→step2（错）→退回来换 step2'→再错→回到原点重试"）。
  - **Journey Learning**：与只选全对路径的 **Shortcut Learning** 相对，包含错误路径的"完整旅程"让模型学会**逆势翻盘**。Math500 实验：两个不同基座模型上 Journey Learning 正确率均高于 Shortcut Learning。
  - 为了让人类读起来顺，可在错误步骤与修正之间**插入 verifier 的反馈句子**（"这一步的答案有误，我们换个解法"），或用更强的模型**改写**整个搜索过程、加连接词。
- 副作用：这样训练出的模型（如早期 o1）思考会**比较跳跃、前言不对后语**。

### Knowledge Distillation（知识蒸馏）

- 已有现成的 reasoning 模型时，不必费劲自造推理数据——直接让强推理模型（老师）生成推理过程+答案，让学生模型学习。
- 案例：**SkyT1、S1** 都用蒸馏；DeepSeek-R1 论文展示用 R1 当老师蒸馏 Qwen、Llama（8B/70B）后，数学/编程能力"起飞"，可媲美强模型。

## 五、方法四：以结果为导向学习推理（Reinforcement Learning）

> 需要微调参数。**只看最终答案对不对给 reward，完全不在乎推理过程内容**——这是 DeepSeek-R1 系列主打的方法。

### RL for Reasoning 的基本设定

- 训练数据：问题 + 正确答案。把问题给模型要求它先做 reasoning 再给答案；对答案给 reward（对→正，错→负）。**推理过程说什么不重要。**
- 与方法三的本质区别：方法三在意推理过程长什么样；方法四只问结果。

### DeepSeek-R1-Zero：纯 RL 的产物

- 用 **DeepSeek-V3-Base** 当 Foundation Model，只做 RL；reward 有两个：**正确率 reward** + **Format reward**（要求模型输出 `think` token）。这就是为什么 RL 完模型会产出 think token。
- AIME（数学竞赛难题）评测：R1-Zero 逼近 o1；对每个题采样 16 个答案做 majority vote 后，可与 o1 做 majority vote 一样好，比 o1 不做 majority vote 更好。→ **四大方法可自由组合**（RL 训练 + 推理时 majority vote）。
- **Aha moment（顿悟时刻）**：RL 训练中模型自发学会"发现问题、重新思考"，如自己说出"等等，这里可能有错，我要重新想"——作者强调这不是人刻意教的，是 RL 自行涌现的。但有论文检验发现 **DeepSeek-V3-Base 在做 RL 之前本来就会"啊哈"**（会自我质疑、会 check 错误），RL 只是强化了已有能力。

### R1-Zero 为什么不可用

- 推理过程**非常难读、多语言混杂**——因为训练时只在意结果，从没要求推理过程的文字质量。

### 真正的 DeepSeek-R1 是怎么打造的（四类方法全用上）

```
DeepSeek-V3-Base
   │  RL（正确率 + Format reward）
   ▼
R1-Zero（推理过程难读但能力强）
   │  用 R1-Zero 生成大量推理过程数据
   │  + 另一个模型用 Few-shot CoT / Supervised CoT（要求 detail + reflection + verification）生成数据
   │  + 大量人工介入：筛选/改写推理过程
   ▼
Imitation Learning 重新训练 V3 → 模型 A（未命名）
   │  RL（正确率 reward + 语言一致性 reward：要求推理全程用同一语言）
   ▼
模型 B（比 R1-Zero 可读性更好，整体正确率略降但可接受）
   │  模型 B 在多样任务上生成推理数据（60 万条，自动产出）
   │  + DeepSeek-V3 做 SFT 数据 20 万条（防遗忘）
   │  用 DeepSeek-V3 当 verifier 判断无标准答案问题的答案好坏
   │  用规则过滤掉多语言混杂/过长/含代码的推理过程
   ▼
Imitation Learning 重新训练 V3 → 模型 C
   │  RL 强化 safety 与 helpfulness
   ▼
DeepSeek-R1
```

- 技术报告中这部分写得很隐晦，只提到"耗费大量人力修改 R1-Zero 输出"；"只用 RL"是農場文的过度简化。
- DeepSeek 也尝试过 Process Verifier 与 MCTS，但最终没有做起来、没有取得好结果。

### RL 只强化已有能力（Qwen 对照）

- 直接对 **Qwen2.5-32B-Base** 做 R1-Zero 式 RL，提升有限（≈ QWQ-32B）；而 RL 能大幅强化 DeepSeek-V3（500B+ 巨模型）。
- 原因：**RL 的前提是模型自己产生过正确答案**——RL 强化的是模型原有的能力，模型本身不够强时 RL 无法"无中生有"。
- 因此对中小模型，**蒸馏（方法三）比 RL 更有效**：Qwen-32B 直接向 R1 学习可大幅增强。

## 下集预告：推理模型的挑战

- 最大挑战：产生超长推理过程**花钱又花算力**，希望模型把力量用在刀口上——该 reasoning 时才 reasoning。
- 现在深度思考模型常做**无谓的推理**：DeepSeek 算 123×456 一开始就心算对了（56088），却反复用各种方法（分解计算、直式运算、估算、多次 breakdown、逐项展开九项）验算了很多遍，浪费大量 token。→ "能否让模型缩短推理过程"是下一讲主题。

## 关联连接

- [[Hung_yi_Lee]] — 讲师实体
- [[DeepSeek_R1]] — 本讲核心实体（R1-Zero / R1 训练流水线）
- [[DeepSeek]] — DeepSeek 公司实体
- [[Reasoning]] — 本讲主题概念：深度思考/推理
- [[Test_Time_Compute]] — 深度思考的理论框架（测试时计算 / 测试时缩放）
- [[Chain_of_Thought]] — 方法一：更强的思维链
- [[Self_Consistency]] — 多数投票选出正确答案
- [[Process_Verifier]] — 逐步验证的中间步骤验证器
- [[Imitation_Learning]] — 方法三：教导模型推理过程
- [[Knowledge_Distillation]] — 向强推理模型学习
- [[Reinforcement_Learning]] — 方法四：以结果为导向的 RL
- [[Over_Thinking]] — 过度思考 / 无谓推理（下一讲主题的伏笔）
- [[AlphaGo]] — Test-Time Compute 的早期经典案例（MCTS）
- [[OpenAI]] — o1/o3 系列推理模型
- [[Anthropic]] — Claude 3.7 Sonnet Extended Thinking
- [[Hugging_Face]] — Beam Search 实验来源
- [[Llama]] — 弱模型读不懂 Supervised CoT 的对照
- [[Gemma]] — 采样覆盖实验中的模型
- [[Qwen]] — Qwen-32B RL 效果有限、蒸馏更有效的对照
