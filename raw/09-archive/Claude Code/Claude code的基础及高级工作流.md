---
title: "Claude code的基础及高级工作流"
source: "feishu/wiki/Claude Code"
node_token: "GNs1wMQ7cisARYkc19Acj3U6nQd"
obj_token: "YOuOdTN4woXUK3xjhEdcEU8MnKf"
export_date: "2026-07-03"
---

# Claude code的基础及高级工作流



1.一键安装  
irm https://claude.ai/install.ps1 | iex

2.更新Claude code

claude update

3.权限修改（shift + tab)

case1:  无任何提示。只读，写文件、执行bash命令需要征得我的同意。  
case2: accept edits on 。 "接受编辑",可读写文件，无需征得我的同意。执行bash命令需要征得我的同意。

case3: bypass permissions on 。特殊权限设置，需要以"claude --dangerously-skip-permissions"方式启动

                                             读写文件、执行bash命令，无需征得我的同意。

case4: plan mode on。规划模式开启，和/plan一样的效果。先让claude方案并和我讨论后，再实现方案。

case5: auto mode on。开启自动模式。避免频繁中断确认（涉及敏感操作或超出请求范围时还需征得我同意）

4.常用/命令

(1)/model

(2)/rewind

(3)/context 当上文达到50%，大致12万token。AI 效能会急剧下降。需要进行/compact 或/clear



5.git和github

   使用github-cli提交并推送代码到github仓库



6.调试

（功能设计）：事先具备完整的日志功能。  
（开发过程）：以TDD的模式来执行任务  
（报错阶段）：将报错日志贴入到claude。 或者截图给claude分析。



7.网络搜索  
  将这个app看起来更加美观（用你的网络搜索功能去查找2026年UI设计的最佳实践）  
  
8.plan计划结合讨论

复杂应用plan模式本身会提问我们确认细节。如果要从黑暗中瞎摸乱转中走出来。  
直接让Claude code指条明路，一劲的问：

（1）我还有什么地方没有考虑到的？

（2）这么做是最佳方案吗？  
（3）在我正在做的这个项目上，顶尖专家会怎么做，他们碰到这种情况会怎么处理？  
（4）你为什么这么做？原理是什么？有没有更好的办法？



9.skills

/plugins 

安装 context7...



10.智能体团队

use agent teams to add some features, i want one improving the UI, one coming up with a plan for authetinication, one working specifically on a CTA, and one creating a blog setup



11.mcp服务器  
举例

方式1：claude mcp add -- transport http canva [https://mcp.canva.com/mcp](https://mcp.canva.com/mcp)

方式2：帮我设置下 xxx mpc服务器（网络上搜索教程，照着做）



12.claude 代码框架

如GSD开发框架，在claude基础上，开发复杂项目。



13.工作树（worktree)

使用claude code同时处理不同的任务。在不同的git分支上运作。

窗口1：claude --worktree feature-dark-mode

窗口2：claude --worktree feature-export-pdf  
  
搞定后。将feature-dark-mode 、feature-export-pdf分支 合入到feature分支



  
  
