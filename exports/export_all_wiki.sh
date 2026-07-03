#!/usr/bin/env bash
# 批量导出飞书知识库全部文档为 Markdown
set +e  # 避免 jq 解析错误导致脚本退出
set -u
shopt -s lastpipe

BASE_DIR="D:/obsidian"
OUTPUT_DIR="${BASE_DIR}/raw/01-articles"
TEMP_DIR="${BASE_DIR}/exports/tmp"
mkdir -p "$OUTPUT_DIR" "$TEMP_DIR"

# ---- 配置：12 个知识空间 (space_id, space_name) ----
SPACES=(
  "7643471648691063764|harness-engineering"
  "7599946870453963742|Claude Code"
  "7617411312947055555|技术资源库"
  "7649423750332419004|Agentic ai"
  "7643383831004728251|紫金智信-面试准备"
  "7641246344583465929|主力监控"
  "7617411309579357133|变现项目库"
  "7604397849657806050|字字动画学习记录"
  "7617411306111978436|AI工具库"
  "7617411302268373982|学习笔记库"
  "7621236942574717901|OpenClaw变现日记"
  "7618944227614985161|OpenClaw信息库"
)

# ---- 全局统计 ----
TOTAL_DOCS=0
ERROR_DOCS=0
SKIPPED_DOCS=0

# ---- 清理文件名中的非法字符 ----
sanitize_name() {
  local name="$1"
  # 替换 Windows 文件名非法字符: \ / : * ? " < > |
  name="${name//\\/ }"
  name="${name//\// }"
  name="${name//:/：}"
  name="${name//\*/ }"
  name="${name//\?/ }"
  name="${name//\"/ }"
  name="${name//</ }"
  name="${name//>/ }"
  name="${name//|/ }"
  # 去除首尾空格和多余空格
  name="$(echo "$name" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | tr -s ' ')"
  # 如果为空,返回 token
  if [ -z "$name" ]; then
    echo "$2"
  else
    echo "$name"
  fi
}

# ---- 递归遍历并导出节点 ----
export_node() {
  local space_id="$1"
  local space_dir="$2"
  local parent_node_token="$3"
  local parent_path="$4"

  # 列出该目录下的所有节点
  local nodes_json
  local raw_output
  if [ -z "$parent_node_token" ]; then
    raw_output=$(lark-cli wiki +node-list --space-id "$space_id" --as user --page-all --format json 2>/dev/null || echo '{"ok":false}')
  else
    raw_output=$(lark-cli wiki +node-list --space-id "$space_id" --parent-node-token "$parent_node_token" --as user --page-all --format json 2>/dev/null || echo '{"ok":false}')
  fi
  # 去除 "Found N node(s)" 前缀行，取 JSON 部分
  nodes_json=$(echo "$raw_output" | sed -n '/^{/,$ p')

  # 检查是否成功
  local ok
  ok=$(echo "$nodes_json" | jq -r '.ok // false')
  if [ "$ok" != "true" ]; then
    echo "  [错误] 无法列出节点 (parent=$parent_node_token): $(echo "$nodes_json" | jq -r '.error.message // "unknown"')"
    return
  fi

  # 提取节点列表
  local node_count
  node_count=$(echo "$nodes_json" | jq '.data.nodes | length')
  if [ "$node_count" -eq 0 ]; then
    return
  fi

  # 遍历每个节点
  for i in $(seq 0 $((node_count - 1))); do
    local node_json
    node_json=$(echo "$nodes_json" | jq ".data.nodes[$i]")

    local node_token obj_token obj_type title has_child
    node_token=$(echo "$node_json" | jq -r '.node_token // ""')
    obj_token=$(echo "$node_json" | jq -r '.obj_token // ""')
    obj_type=$(echo "$node_json" | jq -r '.obj_type // ""')
    title=$(echo "$node_json" | jq -r '.title // ""')
    has_child=$(echo "$node_json" | jq -r '.has_child // false')

    # 跳过首页（通常不需要导出）
    if [ "$title" = "首页" ] && [ "$obj_type" = "docx" ]; then
      echo "  [跳过] 首页文档"
      SKIPPED_DOCS=$((SKIPPED_DOCS + 1))
      # 但如果有子节点仍需遍历
      if [ "$has_child" = "true" ]; then
        export_node "$space_id" "$space_dir" "$node_token" "$parent_path"
      fi
      continue
    fi

    # 清理标题作为文件名
    local safe_title
    safe_title=$(sanitize_name "$title" "$obj_token")

    # 如果是文档——导出它
    if [ "$obj_type" = "docx" ] && [ -n "$obj_token" ]; then
      local target_dir="${OUTPUT_DIR}/${space_dir}${parent_path:+/}${parent_path}"
      mkdir -p "$target_dir"

      local filepath="${target_dir}/${safe_title}.md"

      # 避免重复文件名（加 token 后缀）
      if [ -f "$filepath" ]; then
        filepath="${target_dir}/${safe_title}-${obj_token}.md"
      fi

      echo "  [导出] $safe_title"

      # 获取文档 Markdown 内容
      local fetch_result
      fetch_result=$(lark-cli docs +fetch --doc "$obj_token" --doc-format markdown --as user --format json 2>/dev/null || echo '{"ok":false}')

      local fetch_ok
      fetch_ok=$(echo "$fetch_result" | jq -r '.ok // false')
      if [ "$fetch_ok" = "true" ]; then
        local content
        content=$(echo "$fetch_result" | jq -r '.data.document.content // ""')
        local space_name
        space_name=$(echo "$SPACE_ENTRY" | cut -d'|' -f2)

        {
          echo "---"
          echo "title: \"$title\""
          echo "source: \"feishu/wiki/$space_name\""
          echo "node_token: \"$node_token\""
          echo "obj_token: \"$obj_token\""
          echo "export_date: \"$(date +%Y-%m-%d)\""
          echo "---"
          echo ""
          echo "$content"
        } > "$filepath"

        local lines
        lines=$(wc -l < "$filepath")
        TOTAL_DOCS=$((TOTAL_DOCS + 1))
        echo "    ✓ 已保存 ($lines 行)"
      else
        local err_msg
        err_msg=$(echo "$fetch_result" | jq -r '.error.message // "unknown"')
        echo "    ✗ 导出失败: $err_msg"
        ERROR_DOCS=$((ERROR_DOCS + 1))
      fi

      # 节流: 避免请求过快
      sleep 0.3
    fi

    # 如果有子节点——递归进入
    if [ "$has_child" = "true" ]; then
      local new_path="${parent_path:+"${parent_path}/"}${safe_title}"
      echo "  [目录] $safe_title"
      export_node "$space_id" "$space_dir" "$node_token" "$new_path"
    fi
  done
}

# ---- 主流程 ----
echo "========================================="
echo "开始导出飞书知识库全部文档"
echo "目标目录: $OUTPUT_DIR"
echo "========================================="

for SPACE_ENTRY in "${SPACES[@]}"; do
  SPACE_ID="${SPACE_ENTRY%%|*}"
  SPACE_NAME="${SPACE_ENTRY#*|}"
  # 清理空间名作为目录名
  SPACE_DIR=$(sanitize_name "$SPACE_NAME" "$SPACE_ID")

  echo ""
  echo "━━━ 知识空间: $SPACE_NAME ━━━"

  # 创建空间目录
  mkdir -p "${OUTPUT_DIR}/${SPACE_DIR}"

  # 从根节点开始递归遍历
  export_node "$SPACE_ID" "$SPACE_DIR" "" ""
done

# ---- 输出统计 ----
echo ""
echo "========================================="
echo "导出完成！"
echo "  成功: $TOTAL_DOCS 篇"
echo "  跳过: $SKIPPED_DOCS 篇"
echo "  失败: $ERROR_DOCS 篇"
echo "  目录: $OUTPUT_DIR"
echo "========================================="
