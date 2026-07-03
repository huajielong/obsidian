---
title: "Chrome DevTools（Chrome 开发者工具）"
source: "feishu/wiki/harness-engineering"
node_token: "TF3iwUAkRiKzOskbIpKcC0v7nBc"
obj_token: "EnB6d8siporOGmxxgCQcnlEdnUb"
export_date: "2026-07-03"
---

# Chrome DevTools（Chrome 开发者工具）

### 1. 是什么

Chrome 自带的一套**网页调试/分析工具**，按 F12 或 Ctrl+Shift+I 打开。



### 2. 核心用途

- **调试前端代码**：断点、看变量、查报错、改 JS/CSS 实时生效
- **查看/修改页面结构**：HTML 节点、CSS 样式、布局、颜色
- **网络抓包**：看请求/响应、接口、耗时、资源加载情况
- **性能分析**：页面卡顿、内存泄漏、渲染性能
- **移动端调试**：模拟手机、真机调试
- **日志/存储**：Console 控制台、Cookie、LocalStorage

### 3. 和文中的关系

文中说：把 **Chrome DevTools 协议接入智能体**，让 Codex 能：

- 自动打开页面、操作 DOM
- 截图、复现 bug
- 验证 UI 修复

也就是**智能体直接操控浏览器、看页面状态，不需要人工介入**。
