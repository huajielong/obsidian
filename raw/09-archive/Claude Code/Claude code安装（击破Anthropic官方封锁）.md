---
title: "Claude code安装（击破Anthropic官方封锁）"
source: "feishu/wiki/Claude Code"
node_token: "WQUpwYmTmivJ3Yk4fFXccoUVnfd"
obj_token: "VFc3depRHoBVP1xGxEBcCJJTnBP"
export_date: "2026-07-03"
---

# Claude code安装（击破Anthropic官方封锁）

<callout emoji="💡">
#                                  安装依赖 (part1)
</callout>

Claude Code 是基于 Node.js 运行的，因此你必须先安装 Node.js。

## **下载 Node.js**：

- 访问 Node.js 官网(https://nodejs.org/zh-cn/download)。
- 下载 **LTS 版本**（长期支持版，目前通常是 v20 或 v22）。
- 默认配置，一路点击 "Next" 安装即可。

## **添加path环境变量**

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OThkOGZjZGM4ZDRjNTA0OWM2NDAzZmNlODYyMTdmODhfNTVhZjY2MTkwNDRiYzA1Y2U0OTQwZTc4NzZiZjRlODBfSUQ6NzU5OTk0ODQ5NjAyODY1MDQ0MF8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

## **验证安装**：

- 打开你的终端（Windows 下用 CMD 或 PowerShell，Mac/Linux 用 Terminal）。
- 输入 node -v，如果出现类似 v20.x.x 的版本号，说明环境准备好了。

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MjdlZWMzYjkzYmZmOTY5ZWRhMzRjMDVmMzgxNzliZGZfZTU4NjI0ZjNkYTFjZDRjNmNjMzcyMTM5N2RlMGViYTBfSUQ6NzU5OTk3ODg3Mjg2NTgwMzIwOF8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)





<callout emoji="💡">
#                                   安装Claude code (part2)
</callout>

## 执行安装命令

在终端中输入以下命令（使用国内镜像源，下载速度更快）：

```Plain Text
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
```

卸载命令：

```Plain Text
npm uninstall -g @anthropic-ai/claude-code
```

## 安装后验证版本

```Plain Text
 C:\Users\huajielong-win11> claude --version
```

## 启动claude

创建测试目录，用命令行窗口进入目录执行

```Scheme
PS D:\vibe_coding_project1>claude
```

Anthropic官方封锁限制，报错下截图：

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTk5YTAyZjQyOTk2ODQxYjgwZGVlYzIxMzJkZDNlNWVfMDAyMTEwZDY0NjVlYzc2MGNlYWQwYjgzM2I0NmQ4NWZfSUQ6NzU5OTk1MDUwNjQxNjUwNzg0Nl8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

## 添加配置解除封锁

路径：C:\Users\huajielong-win11\\.claude.json

```Scheme
 "hasCompletedOnboarding": true,
```

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ODU1YWE5NjYxZGE5MzU3MzA5OTFiNGQ5MDNiODJkODZfZGM4NjQ1MDk4NTAyMmUxY2NkYWM1N2M5MTRjNTM2NDdfSUQ6NzU5OTk0NzM5NTY2NTA3MTMwN18xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

## 重启终端，再次运行claude

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OThjNzFkZDZmZjljZjk1MmY4OWI0NTJlNzdjNDM4ZGZfMDU0OTY4M2RlZGQ4YTM1Y2UwMjQzYjJiNWY3YjZhYTNfSUQ6NzU5OTk1MzcwMjYwNjY3MDgwOV8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

说明已安装Claude code成功 (中国大陆IP用户，可以顺畅使用Claude Code)





<callout emoji="💡">
#                                  配置模型和APIKey (part3)
</callout>

cc-switch 可以方便的对接入claude code的大模型进行管理和切换。

## 下载和安装cc-switch

github地址：https://github.com/farion1231/cc-switch/releases

<callout emoji="💡">
滚动页面可找到下载入口，下载[CC-Switch-v3.10.2-Windows.msi](https://github.com/farion1231/cc-switch/releases/download/v3.10.2/CC-Switch-v3.10.2-Windows.msi)
</callout>

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDZlMjQ0NmYyYzJkOWUxNmJlNGVkMjFlMzlmNjAxZTFfYjcyZjViZjNhYmM5MjkwZTM5MTMyMDVmYTljNDY5YTBfSUQ6NzU5OTk2MDU0NTkyODE3MDQ0MF8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

## 通过cc-switch设置AI IDE 和 LLM

<callout emoji="💡">
  首先，选择AI编程IDE，这边选择Claude. 目前支持（Claude、Codex、Gemini、OpenCode）
</callout>

接下来，为AI IDE，设置LLM大模型。

- 这边举例，选择智普大模型（GLM-4.7)，也可其他或自定义

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Y2Y1M2EzZTE1ODllZTc0YWFjMzZiOGRkNDI5YzdlZGRfNjdhYjAyZjA3ZGU5MWVlN2UzMTE1YWZiYTkzMmE5MThfSUQ6NzU5OTk2ODEyNjMwMTg1MDU3MV8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

- **填写API Key（**[**需提前在智普官网付费开通**](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)**）**

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ODgxYjQyM2Q3Mzc1ZWM3ZTE0NTFmNGMzOTEzNmU4MjZfNDY4OGQ1ZWMzZDNlZGU1NjgwZDcxYTcyZGRiYmY4Y2RfSUQ6NzU5OTk3MTMzMDIyMjI2MzUxNV8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

- **添加后界面变化如下**  

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTYzZjg0ZDZjMmNmM2YzMzU3MzNjNWM3Njg2NGZiNjhfODUzZTZkNmIxZWQyZTNiMjZjNmVlZDE0YmNmOTRkYjBfSUQ6NzU5OTk3MjExMjgzMzc2MDIwNV8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

## 测试claude是否配置成功

再次重启终端，在测试目录运行claude

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZDZmMmQzYWE0NmI0NzYwOTY2NmIzZDRhMWE1YTMxZmJfNmRkZTc2ZGMzN2JjNjA4ZmMxZTFhNzk3NjUwNmQ0ZDZfSUQ6NzU5OTk3MzI4MzU3Njg0MzQ4NV8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)

选择Yes. 成功配置的界面如下

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTk3OGJjNDY4ODM4OTE0YzM3NTljZDE4YzI0MjdiNThfNGI5YzY1NGRhNDVkNmI4NDQ4M2RlNDFjM2NjNTE2YjBfSUQ6NzU5OTk3MzQ3Nzc2ODQwMDA5Nl8xNzgzMDcwMDUwOjE3ODMwNzM2NTBfVjM)





<callout emoji="💡">
#                           Claude Code的基本使用 (part4)
</callout>

常见工作流程：https://code.claude.com/docs/zh-CN/common-workflows

把这个文档看完，就可以把claude code的基本用法使用起来了  
