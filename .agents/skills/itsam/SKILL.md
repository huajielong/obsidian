---
name: itsam

description: 伊特萨姆三问学习法技能——基于 MIT 研究生伊特沙姆·阿里（Ittesham Ali）的"三个关键问题"方法，借助 NotebookLM CLI 在两天内系统掌握任何陌生领域。支持 `/itsam <主题>` 和 `/itsam <主题> --files <路径>`。

user-invocable: true
---

# /itsam 技能 — 伊特萨姆三问学习法

## 核心理念

伊特萨姆学习法的本质是：**用 AI 作为对抗性考官，通过三个关键问题逼自己从"知道"到"真懂"**。

```
┌─────────────────────────────────────────────────┐
│  ① 提取思维框架  →  ② 了解领域格局  →  ③ 鉴别性测试  │
│  (建立骨架)         (俯瞰全貌)         (暴露盲区)     │
└─────────────────────────────────────────────────┘
                       ↓
              ④ 死磕追问（核心环节）
              答错 → 追问 → 修正 → 再测
```

---

## 触发方式

| 命令 | 说明 |
|------|------|
| `/itsam <主题>` | 对一个陌生领域执行三问学习法（不依赖本地素材） |
| `/itsam <主题> --files <路径>` | 将本地素材喂入 NotebookLM 后执行三问 |
| `/itsam <主题> --url <URL>` | 将网页素材喂入 NotebookLM 后执行三问 |
| `/itsam <主题> --deep` | 使用 NotebookLM deep research 模式先行搜集资料 |

---

## 第一步：前置检查

### 1.1 检查 notebooklm-py 是否安装

```bash
notebooklm --version 2>/dev/null || {
  echo "❌ notebooklm-py 未安装。请运行:"
  echo "  pip install \"notebooklm-py[browser]\""
  echo ""
  echo "安装后运行: notebooklm login 完成 Google 登录"
  exit 1
}
```

### 1.2 检查登录状态

```bash
notebooklm auth check --test --json 2>&1 | jq -r '.status' | grep -q ok || {
  echo "❌ 未登录或 Token 过期。请运行:"
  echo "  notebooklm login"
  exit 1
}
```

### 1.3 如果未安装 → 引导用户安装

> 如果 `notebooklm` 命令不存在，请提示用户：
> ```bash
> pip install "notebooklm-py[browser]"
> notebooklm login
> ```
> 然后重新运行 `/itsam` 命令。

---

## 第二步：准备 Notebook

为本次学习创建一个独立的 Notebook：

```bash
# 生成 Notebook 名称
NOTEBOOK_NAME="itsam-$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr -c '[:alnum:]\n' '-' | sed 's/--*/-/g; s/-$//')"

# 创建 Notebook（如果不存在）
NOTEBOOK_ID=$(notebooklm create "$NOTEBOOK_NAME: $TOPIC" --json 2>/dev/null | jq -r '.notebook.id')

# 如果创建失败，尝试从现有列表中查找
if [ -z "$NOTEBOOK_ID" ] || [ "$NOTEBOOK_ID" = "null" ]; then
  NOTEBOOK_ID=$(notebooklm list --json 2>/dev/null | jq -r --arg name "$NOTEBOOK_NAME" '.notebooks[] | select(.title | startswith($name)) | .id' | head -1)
fi

if [ -z "$NOTEBOOK_ID" ] || [ "$NOTEBOOK_ID" = "null" ]; then
  echo "❌ 无法创建 Notebook。请检查网络连接后重试。"
  exit 1
fi

echo "✅ Notebook ID: $NOTEBOOK_ID"
```

---

## 第三步：喂入素材（可选）

### 3.1 通过 --files 参数指定的本地素材

如果用户提供了 `--files` 参数，遍历文件并添加：

```bash
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    echo "📄 添加素材: $f"
    notebooklm source add "$NOTEBOOK_ID" --file "$f" 2>&1
  elif [ -d "$f" ]; then
    find "$f" -type f \( -name "*.md" -o -name "*.pdf" -o -name "*.txt" \) | while read -r file; do
      echo "📄 添加素材: $file"
      notebooklm source add "$NOTEBOOK_ID" --file "$file" 2>&1
    done
  fi
done
```

### 3.2 通过 --url 参数指定的网页

```bash
notebooklm source add "$NOTEBOOK_ID" --url "$URL" 2>&1
```

### 3.3 通过 --deep 参数使用 Deep Research

```bash
echo "🔍 启动 Deep Research..."
notebooklm source add-research "$NOTEBOOK_ID" "$TOPIC" --mode deep 2>&1
```

### 3.4 使用 vault 中已有的 raw/ 素材（隐式）

如果用户没有指定素材，但 `raw/01-articles/` 或 `raw/02-papers/` 中存在与主题相关的文件：

```bash
# 在 raw/ 中搜索主题相关文件
RELATED_FILES=$(grep -ril "$TOPIC" raw/01-articles/ raw/02-papers/ 2>/dev/null | head -5)
if [ -n "$RELATED_FILES" ]; then
  echo "💡 在 vault 中发现相关素材，自动添加..."
  for f in $RELATED_FILES; do
    notebooklm source add "$NOTEBOOK_ID" --file "$f" 2>&1
  done
fi
```

---

## 第四步：执行三问（核心）

这是伊特萨姆方法的核心环节。三个问题依次执行，**必须按顺序，不可跳过**。

### Q1：提取思维框架

**目标**：获取该领域专家们的底层思维模型，建立学科骨架。

```bash
echo ""
echo "═══════════════════════════════════════════"
echo "  🌲 Q1: 提取5个核心思维模型"
echo "═══════════════════════════════════════════"
echo ""

notebooklm ask "$NOTEBOOK_ID" \
  "你是一个世界级的领域专家。关于「$TOPIC」这个领域：

  1. 请列出所有专家都认可的 **5个核心思维模型**（mental models）是什么？
  2. 对每个模型，请按以下格式回答：
     - **模型名称**：（一句话命名）
     - **核心含义**：（这个模型本质上在说什么）
     - **适用场景**：（什么情况下用这个模型思考）
     - **为什么重要**：（专家依赖它的原因）
  3. 最后，用一句话说明这5个模型之间的关系（它们如何构成一个思考体系）"
```

### Q2：了解领域格局

**目标**：掌握全貌——共识、争议、未解决问题。

```bash
echo ""
echo "═══════════════════════════════════════════"
echo "  🗺️  Q2: 了解领域格局"
echo "═══════════════════════════════════════════"
echo ""

notebooklm ask "$NOTEBOOK_ID" \
  "关于「$TOPIC」这个领域，请从格局层面分析：

  1. **已达成共识的基础知识**：这个领域里什么是公认正确的？
  2. **争论最激烈的3个问题**：每个问题请列出：
     - 争议焦点是什么
     - 正方最强论据
     - 反方最强论据
     - 目前哪方占优（或僵持不下）
  3. **尚未解决的问题**：学界/业界公认的开放挑战有哪些？
  4. **未来方向**：这个领域正在往哪个方向演进？"
```

### Q3：鉴别性测试（核心中的核心）

**目标**：用10道鉴别题暴露出理解盲区。这是伊特萨姆方法最关键的步骤。

```bash
echo ""
echo "═══════════════════════════════════════════"
echo "  🩺 Q3: 鉴别性测试——10道真懂检验题"
echo "═══════════════════════════════════════════"
echo ""

notebooklm ask "$NOTEBOOK_ID" \
  "关于「$TOPIC」这个领域，请扮演一个严格的导师。

  设计 **10道能一眼区分一个人是真懂还是死记硬背的鉴别性问题**。

  每个问题的格式：
  ---
  Q{N}：「问题本身」
  ✅ 正确答案：[简洁准确的答案]
  ❌ 常见错误：[新手最容易犯的误解]
  🔍 暴露盲区：[这道题能检验出什么深层次的理解漏洞]
  💡 检验信号：[如果一个人能答对这题，说明他掌握了什么]
  ---

  要求：
  - 问题要有深度，不能是简单的定义复述
  - 要能区分"背过"vs"真懂"
  - 每个问题暴露不同的盲区（不要重复）
  - 涵盖理论理解、实践陷阱、边界条件、常见误区等不同维度"
```

---

## 第五步：死磕追问（互动环节）

这是区分"知道"和"真懂"的关键。**在 Q3 结果返回后**，引导用户进行以下互动：

```bash
echo ""
echo "═══════════════════════════════════════════"
echo "  ⚔️  死磕环节开始！"
echo "═══════════════════════════════════════════"
echo ""
echo "📋 上面10道题中，请逐题作答。"
echo "   答完一题后，我会帮你验证并揭示盲区。"
echo ""
echo "💡 提示格式:"
echo "   \"/itsam 继续 关于Q1，我的理解是...\""
echo ""
```

当用户回答某题后，执行追问：

```bash
# 用户答完一题后，用 NotebookLM 进行深度追问
notebooklm ask "$NOTEBOOK_ID" \
  "关于问题「${QUESTION}」，用户的理解是：「${USER_ANSWER}」。

  请：
  1. 判断用户的理解是否正确（是/部分正确/否）
  2. 如果不对，精确指出错误在哪里
  3. 给出一个反例或边界情况，进一步检验理解深度
  4. 用费曼检验法：要求用户用最简单的类比重新解释这个概念"
```

**追问策略示例**（三种深度层层递进）：

| 轮次 | 追问方式 | 示例 |
|------|---------|------|
| 1 | 反例检验 | "如果边界条件变成 X，你的结论还成立吗？" |
| 2 | 类比检验 | "请用给 10 岁小孩能懂的语言重新解释这个原理" |
| 3 | 关联检验 | "这个概念和 Q1 中第3个思维模型有什么联系？" |

---

## 第六步：学习成果固化（保存到 vault）

学习完成后，将成果保存到 vault 中：

### 6.1 生成 synthesis 页面

在 `wiki/syntheses/` 创建一个综合页面，格式如下：

```markdown
---
title: "伊特萨姆学习 - 主题名"
type: synthesis
tags: [学习笔记, itsam]
sources: []
last_updated: YYYY-MM-DD
---

# 伊特萨姆学习：主题名

## 核心思维模型
1. **模型1** — 一句话定义
2. **模型2** — 一句话定义
...

## 领域格局
- 共识：
- 争议：
- 未解问题：

## 盲区记录
- 我最初的理解偏差：
- 暴露的关键盲区：
- 修正后的理解：

## 关联连接
- [[相关概念或实体]]
```

### 6.2 更新 index.md

将新页面添加到 `wiki/index.md` 的 Syntheses 分类下。

### 6.3 更新 log.md

追加操作日志：
```markdown
## [YYYY-MM-DD] itsam | 伊特萨姆学习法: [主题]
- **输出**: 新增 [[伊特萨姆学习 - 主题名]]
```

---

## 用户交互流程总图

```
用户: /itsam Transformer 注意力机制
                    │
                    ▼
          ┌─────────────────────┐
          │  ① 前置检查          │
          │  notebooklm --version │
          │  auth check          │
          └─────────┬───────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │  ② 创建 Notebook     │
          └─────────┬───────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │  ③ 可选：喂入素材     │
          │  --files / --url    │
          │  --deep / vault自动 │
          └─────────┬───────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │  ④ 三问执行(自动)    │
          │  Q1: 思维框架        │
          │  Q2: 领域格局        │
          │  Q3: 鉴别性测试      │
          └─────────┬───────────┘
                    │
                    ▼
          ┌─────────────────────────┐
          │  ⑤ 死磕追问(手动交互)    │
          │  用户逐题作答            │
          │  AI 指出盲区            │
          │  → 追问 → 修正 → 再测   │
          └─────────┬─────────────┘
                    │
                    ▼
          ┌─────────────────────────┐
          │  ⑥ 成果固化(可选)        │
          │  保存到 wiki/syntheses/  │
          │  更新 index + log       │
          └─────────────────────────┘
```

---

## 关联连接

- [[wiki/concepts/Feynman_Technique]] — 费曼学习法，与 Q3 的类比检验一致
- [[wiki/concepts/Naval_Rapid_Research_Method]] — 纳瓦尔极速研究法，另一种快速入门方法论
- [[wiki/concepts/Naval_Ravikant]] — 纳瓦尔·拉维坎特
