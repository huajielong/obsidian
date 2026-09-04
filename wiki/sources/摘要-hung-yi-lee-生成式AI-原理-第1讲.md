---
title: "摘要-李宏毅-生成式AI-原理-第1讲"
type: source
tags: [来源, 转录, 生成式AI, 李宏毅, LLM基础, 机器学习课程]
sources: [raw/09-archive/【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理.md]
last_updated: 2026-08-05
---

## 核心摘要

李宏毅《生成式人工智慧與機器學習導論2025》第一讲"一堂课搞懂生成式人工智慧的原理"，用一堂课讲清 **生成式 AI / LLM 的核心原理**。核心论点：ChatGPT / Gemini / Claude 这类平台**真正会做的事只有一件——文字接龙**（给一段未完成的文字，预测下一个 Token），配合平台偷偷加上的 **Chat Template**，才能"回答"用户的问题。

讲座拆解了语言模型运作的完整链路：Token / Vocabulary / Prompt 基础概念 → 概率分布 + 掷骰子采样（所以每次答案都不同）→ 语言知识与世界知识两大能力来源 → 百亿级参数 → 三大学习来源（网络数据 / 人工标注 / 用户反馈）→ Chat Template 让模型回答问题 → 多轮对话本质是拼接历史记录 → **AI 幻觉**的根源（模型背后没有数据库，一切答案都是接龙"梦"出来的）→ System Prompt 注入基础信息（如"今天是几月几号"）→ **Context Engineering**（人类确保 Prompt 信息足够）→ 图片/声音生成也是 Token 接龙（encoder 压缩成 Token → decoder 还原）。最后定义**生成式 AI**：让机器学会产生"复杂而有结构的物件"，其基本单位是有限的 Token，组合起来却有无限可能；并给出生成策略的专名 **Auto-Regressive Generation**，以及另一种生成策略 Diffusion Model 的预告。

课程后半段为动手实操：用 Hugging Face 平台 + Transformers 套件在 Colab 上跑开源模型 **Llama-3.2-3B-Instruct**，实操 Tokenizer 的 encode/decode（词汇表 128,000 个 Token）、手写/调用 `model.generate` 做文字接龙、按概率采样与 Top-K、加上官方 Chat Template、设置 System Prompt 控制模型身份、用 Pipeline 一行调用，最终复刻出一个"有 87% 像 ChatGPT"的多轮对话机器人。

## 课程信息

- **来源**：YouTube《【生成式人工智慧與機器學習導論2025】第１講：一堂課搞懂生成式人工智慧的原理》
- **URL**：https://www.youtube.com/watch?v=TigfpYPJk1s
- **讲师**：[[Hung_yi_Lee]]（李宏毅，台湾大学）
- **发布**：2025-09-15
- **投影片**：https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall.php
- **Colab 链接**：https://colab.research.google.com/drive/1EjiX46muxSMy0avtHPXiulVUhmu37Kyi
- **性质**：课程转录（繁体中文 → 简体中文提炼）

## 一、语言模型 = 文字接龙（Next Token Prediction）

- ChatGPT / Gemini / Claude 本质都是**语言模型（Language Model）**，一言以蔽之：一个在做**文字接龙**的 AI。给它一个未完成的句子（Prompt），它预测下一个字。
- **Token**：模型做接龙时可选择的输出单位（不只是"代币"），可以是字、单词、符号，甚至图片/声音的压缩符号。
- **Prompt**：给语言模型的输入（未完成的句子）。
- **Vocabulary**：模型所有可选 Token 的集合，通常极其庞大——现代语言模型常有**数十万**个 Token（演示的 Llama-3.2-3B 为 128,000 个），涵盖多语言文字、各类符号。

### 回答问题的过程

1. 用户输入问题（如"台湾最高的山是哪座？"）→ 当作未完成句子开始接龙
2. 模型对每个候选 Token 给一个**概率**，根据概率分布"掷骰子"选一个 Token
3. 把选出的 Token 拼到 Prompt 后面 → 再预测下一个 → 直到输出**结束符（EOS）**
4. 一串 Token 合起来就是答案

> **为什么每次答案不同？** 因为每一步都在按概率掷骰子——高概率 Token 通常被选中，但低概率 Token 也有可能被掷到（如"玉山"→ 也可能"市"→"是玉山"）。低概率 Token 若真的被选中，就会产出荒谬答案（如"冰淇淋"），但这类答案概率极低，几乎不会出现。

### 做好文字接龙需要两类知识

| 知识类型 | 内容 | 学习难度 |
|---------|------|---------|
| **语言知识** | 文法、词性搭配（"黄色的"后接名词概率高、接动词低） | 容易，上百万篇文章即可学会，很少犯文法错误 |
| **世界知识** | 对物理世界的真实认识（水的沸点是 100℃；0.5 大气压下降为低于 100℃） | 很难，无穷无尽学不完 |

### 参数规模

- 语言模型可视为函数 `f(x)=ax+b`，输入 Prompt x，输出概率分布 f(x)，a/b 即**参数（Parameter）**。
- 因输入输出关系复杂，LLM 需要**非常大量参数**："百亿参数遍地走，十亿参数谁都有"——只有十亿（1B）参数不好意思叫"大型"语言模型。
- 参数不是人工设定的，而是**通过数据自动学习**得到（机器学习概念，后续课程展开）。

### 三大学习来源

1. **网络爬取的大量文本**：每个句子都是接龙教材（"人工智慧真神奇" → 人→工→智→慧）
2. **人类标注**：开发者告诉模型"台湾最高的山？→ 玉山"
3. **用户反馈（RLHF 雏形）**：按赞/倒赞调整回答概率（"教我做枪"的坏答案降概率、好答案升概率）

## 二、为什么接龙能"回答问题"：Chat Template

- 单纯接龙不一定接出答案（"台湾最高的山？"后面也可以接"谁告诉我呀"或出成考题）。
- 平台偷偷"加料"：在你输入的 Prompt 前后加上额外内容，如 `使用者問：台灣最高的山是哪座？AI回答：`，让接龙只能顺着"AI回答："接下去 → 这就是 **Chat Template**。
- 每个模型的 Chat Template 都不同且不公开（ChatGPT 的我们不知道；Llama 的可在实操中看到）。
- **多轮对话**：把过去所有对话记录（同样套上 Chat Template）拼到新问题前面一起接龙，模型就能知道"第二高的呢"指"第二高的山"。记忆仅限同一聊天内，按"新聊天"即遗忘（跨对话记忆留待后续课程）。

## 三、AI 幻觉（Hallucination）

- 例：问 ChatGPT"台湾大專院校人工智慧學程聯盟 本学期有哪些课程 + 官网网址"，它给了像模像样的介绍和 `AI-college.org`——**网址根本不存在，是编造的**。
- **根源**：语言模型背后**没有数据库**，一切答案都是接龙"梦/幻觉"出来的——每个字都是概率采样接出来的。真正该意外的是：在它的幻觉里，居然有一些与现实相符。
- **减少幻觉**：把搜索搭配 AI 一起使用 = **RAG**（第二讲展开，作业二即做一个 RAG 系统）。主流平台默认开启"联网/RAG"，要复现幻觉需先关闭搜索功能；但有搜索也不保证答案正确。

## 四、System Prompt 与 Context Engineering

- 语言模型像"关在暗无天日小房间里的人"，只会文字接龙，看不到外面的世界 → 问"今天是几月几号"只能瞎猜。
- **人类的责任：确保输入 Prompt 里的信息足够**，让模型有机会接出正确结果——这就是 **Context Engineering**（本讲给出直观定义）。
- **System Prompt**：开发者在每次对话前**预先塞入的基础信息**（如今天是几月几号、模型叫什么名字），叠加在 Chat Template 与用户问题之前，是模型实际看到输入的最前面部分。用户不被告知具体加了什么。
- 与此对应，**User Prompt** 是用户直接输入的 Prompt。

## 五、生成图片与声音 = Token 接龙

- 一个可能的方法：**像素接龙**（逐像素生成，2016 年李宏毅课上演示过用像素接龙生成宝可梦；2020 年 OpenAI 出过影像版 GPT）与**采样点接龙**（声音由采样点构成，Google DeepMind 的 **WaveNet** 逐个采样点生成真实语音）。
- **致命问题**：工程量过大——1024×1024 图片 = 100 万次像素接龙，比写一部《红楼梦》还巨大；22K 采样率下一分钟语音 = 132 万次采样点接龙。
- **现在的做法**：先用 **Encoder（编码器）** 把图片/声音压缩成 Token（图片常用 16×16 区域一个符号，表示"草地/眼睛/毛茸茸"等 pattern；声音每 0.02 秒一个符号），接龙后再用 **Decoder（解码器）** 还原。
- 多模态生成（文字→图片、图片→风格转换、语音对话）本质相同：图片/声音 Token 与文字 Token 拼在一起喂给语言模型，继续 Token 接龙。
- **黄仁勳（COMPUTEX 2024）**："万事万物都是 token"——words / image / 图表 / 歌 / 语音 / 影片都是 Token，生成式 AI 的核心就是把万物表示成 Token 再做 Token 接龙。（不是"代币"的意思。）

## 六、生成式 AI 的定义与 Auto-Regressive Generation

- **定义**：生成式 AI = 让机器学会产生**复杂而有结构的物件**。"有结构"= 由**有限可能的基本单位（Token）**构成，组合起来却有无穷可能。
  - 文字：基本单位是字（中文常用约 4,000 字），组合出无穷文章
  - 图片：Token 组合出千变万化的图
  - 声音：采样点（有限取值）拼出千变万化的声音
  - 蛋白质：胺基酸种类有限，组合出各式蛋白质（生成式 AI 制药）
- **不只是生成，而是根据输入进行生成**：输入 X → 输出 Y（复杂而有结构的物件），才能打造有用应用。
- **生成策略 = 选择 Token 的顺序**，最基本的策略就是文字接龙，专名 **Auto-Regressive Generation**：输入 Z₁…Zₜ₋₁ → 预测下一个 Zₜ → 贴回输入 → 直到结束符。
- 每次"给一串 Token 选下一个"本质是**分类问题（选择题）**——机器学习早已会做选择题，这是生成问题可解的关键。
- 文字接龙不是唯一生成策略，**Diffusion Model** 是影像生成领域更常听到的另一种策略（后续课程展开）。

## 七、实操：用开源模型复刻 ChatGPT

### 开源 vs 非开源

- **非开源**（闭源）：Gemini / ChatGPT / Claude——可通过网页或 API 交互，但背后的函数 F、参数量、参数数值均不公开。
- **开源**：Meta **LLaMA**、**Mistral**、Google **Gemma**——参数可下载，知道 F 长什么样、参数量与数值（完整"如何训练"仍不公开，严格来说不算完全开源）。

### 工具链

- **Hugging Face**：开源模型/数据集平台，被形容为"模型的 Facebook"（每个模型有说明、下载次数、按赞数）。
- **Transformers 套件**（HuggingFace 开发）：通用工具，所有 HF 上的模型（无论 PyTorch/JAX 训练）都可用它运行；比 Ollama 等效率略低但**弹性高、覆盖全**。
- **Colab**：跑示例代码的平台，选 GPU（A100 最佳；免费版 T4 需换 1B 小模型）。
- 演示模型：`meta-llama/Llama-3.2-3B-Instruct`（3.2 = 版本，3B = 30 亿参数，Instruct = 理解指令并回复）；作业用 `google/gemma-3-4b-it`（it = instruction-tuned，性能优于 Llama 3 代）。

### Tokenizer 实操

- 每个模型下载两部分：**Tokenizer**（存 Vocabulary 定义，决定能产生哪些 Token）与 **Model**（参数）。
- `tokenizer.vocab_size` → Llama-3.2-3B 有 **128,000** 个 Token（编号 0~127,999）。
- `tokenizer.decode(编号)` → 转文字；`tokenizer.encode(文字)` → 转编号。
- 词汇表包罗万象：0 号是感叹号 `!`、有阿拉伯文/日文/中文（最后一个 Token 是"锦"）、128 个连续空格的 Token、爱心符号、`地球`、`互聯網` 等。
- **有趣现象**：同一个英文单词"GOOD"，在句首（前无空格）与词中（前有空格）是**不同 Token**（19045 vs 1695）；`HI` / `Hi` / `hi` 大小写不同也对应不同 Token。
- `encode` 默认会加一个"句子开头"特殊符号（编号 128000，即 `<|begin_of_text|>`）；`add_special_tokens=False` 可关闭。

### 文字接龙实操

- `model` 本身是函数：输入 Token ID → 输出各 Token 概率分布（隐藏在庞杂输出中，需取出 logits）。
- 例：Prompt `1+1=` → 模型给"2"65.7% 概率、"3"12% 概率；改成"在二进位中1+1=" → "10"70.12% 概率、"2"仅 0.13%——模型**能根据输入改变概率分布**。
- 手写 `for` 循环逐个选最高概率 Token 生成多 Token；或用现成的 **`model.generate`**（停止条件：遇到 EOS 或到达 max_length）。
- **采样（Sampling）与 Top-K**：
  - 完全按概率掷骰子容易中途掷到低概率 Token 后"全盘皆错、开始乱讲"（如"你是谁"接出乱码日文、XD）。
  - 真正做法：**只有概率前 Top-K 的 Token 能参与掷骰子**。Top-K=1 等价贪婪解码（确定性）；Top-K 设大≈不设；实践中常取 K=3 等较小值，兼顾多样与稳定。

### Chat Template 实操

- 不加 Chat Template，模型不会回答问题（"你是谁"接出"你是谁的朋友 我是小明"）；随便发明模板效果不佳（模型接了"使用者说"却没接完就达长度上限）。
- **必须用官方 Chat Template**：`tokenizer.apply_chat_template(messages)` 自动加模板 + 编码。messages 格式：`[{"role": "system", ...}, {"role": "user", ...}]`。
- Llama 官方模板可见：`<|start_header_id|>system<|end_header_id|>` 包裹 System Prompt（默认已塞入"我的知识到 2023 年 12 月、今天是 2025 年 9 月 12 日"等基础信息），随后是 user 内容、轮到 `assistant` 说话。
- **身份幻觉**：没设 System Prompt 时 Llama 会觉得自己是 GPT-3.5（训练数据里常见）；在 System Prompt 中写"你的名字是 Llama"即可纠正。
- **强制预设回答**：把模型"没说过的话"塞进 messages 的 assistant 角色（如"我是李宏"），模型只能顺着接龙（接出"李宏基的 Llama"）——可用来强制模型进入特定回答开头。

### 多轮对话与 Pipeline

- 多轮对话 = 每轮把完整历史 messages 全部传给 `apply_chat_template` → `model.generate`。演示结果"跟 ChatGPT 有 87% 像"。
- **Pipeline**：`pipe = pipeline("text-generation", model_id)`，直接传文字即可，自动处理 encode/decode，一行换模型（改 model_id）。
- 作业一：用 Hugging Face Token + Llama 授权（需填表等邮件批准，可能数小时）下载模型，把演示模型的 model_id 换成 `google/gemma-3-4b-it` 跑通聊天机器人。

## 关联连接

- [[Hung_yi_Lee]] — 讲师实体
- [[Generative_AI]] — 生成式 AI 概念（本讲给出"复杂有结构物件 + Token"的严格定义）
- [[Auto_Regressive_Generation]] — 本讲核心生成策略（文字接龙）
- [[AI_Hallucination]] — 幻觉现象及其根源（背后无数据库）
- [[Chat_Template]] — 让语言模型"回答问题"的模板机制
- [[System_Prompt]] — 开发者预设的输入前缀（含日期/身份等基础信息）
- [[Context_Engineering]] — 本讲定义：人类确保 Prompt 信息足够
- [[RAG]] — 减少幻觉的手段（搜索 + AI）
- [[BPE_Tokenizer]] — Tokenizer 机制与词汇表实操
- [[Temperature_Parameter]] — 概率采样 / Top-K 相关内容
- [[Diffusion_Model]] — 另一种生成策略（影像生成）
- [[Llama]] — 演示用开源模型（Llama-3.2-3B-Instruct）
- [[Gemma]] — 作业用开源模型（Gemma-3-4B-it）
- [[Hugging_Face]] — 开源模型平台
- [[WaveNet]] — 采样点接龙生成语音的早期模型
- [[Mistral]] — 开源模型公司
- [[Jensen_Huang]] — "万事万物都是 token" 出处
- [[摘要-hung-yi-lee-ai-agent-原理]] — 李宏毅《生成式AI時代下的機器學習(2025)》第二讲（AI Agent 原理），同系列课程的姊妹讲
