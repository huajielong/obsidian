---
title: "安装Remotion Skills + Claude code"
source: "feishu/wiki/Claude Code"
node_token: "Oyh9wALPUiysqnkXWr6c69HnnFg"
obj_token: "Tgrjd7HiwoMnWwxFJz3cY3wfnAg"
export_date: "2026-07-03"
---

<title>安装Remotion Skills + Claude code</title>

<callout emoji="💡">
**从零完整实操、大白话、一步一步、复制就能用**的方式，给你整套完整教程，把所有概念彻底串明白，
你照着做一遍就全部懂了。
</callout>

先把所有涉及的名词概念解释一遍，防止混淆：

1. **Node.js**：底层运行环境，所有东西都靠它跑
2. **Remotion**：用 React 代码生成 MP4 视频的框架
3. **React 组件**：视频画面的积木（字幕、背景、动画）
4. **TailwindCSS**：给组件美化排版、颜色、大小
5. **Claude Code**：能直接操作你电脑文件夹、自动写代码、跑命令的**本地AI程序员**
6. **remotion-dev/skills**：Remotion 官方给 Claude Code 专用的**AI技能包**，教AI**标准、正确、不报错、带完美动画**的 Remotion 写法，是官方专属知识库。

# 一、整体工作流程

你只需要**用中文说话**，比如：

> 帮我做一个9秒竖屏短视频，黑色背景，居中白色大字幕，字幕从透明淡入，带轻微缩放动画，底部加小字，使用Tailwind，可直接渲染导出mp4



**Claude Code 全程自动完成：**

创建项目 → 安装依赖 → 写 React 组件 → 写帧动画 → 配置 Tailwind → 启动预览 → 渲染导出视频

**你完全不用手写代码**



# 二、前置准备（必须先装好）

## 1. 确认已安装 Node.js

打开电脑终端（CMD/终端/PowerShell）输入

```Bash
node -v
```

出现版本号就说明装好了，没装先装 Node.js 官网LTS版。



## 2. 安装 Claude Code

Claude Code 是 Anthropic 官方终端 AI 工具，直接全局安装

终端执行：

```Bash
npm install -g @anthropic-ai/claude
```

模型配置参见[文档](https://my.feishu.cn/wiki/WQUpwYmTmivJ3Yk4fFXccoUVnfd)

安装完成验证：

```Bash
claude --version
```

出现版本号即成功。



# 三、安装 remotion-dev/skills 官方技能包（最关键一步）

这个就是你问的 **remotion-dev/skills**

它是**专门给 Claude Code 用的 Remotion 领域知识库、最佳实践、全部API规范、动画写法、组件模板、Tailwind 规范、避坑大全**。

没有这个技能包，AI写的Remotion代码经常报错、动画写错、`interpolate`用错、Composition格式不对、Tailwind引入错误、组件写法不规范。



## 安装命令（直接复制终端运行）

```Bash
claude skills add remotion-dev/skills
```

执行完成提示成功即可。



你可以查看已安装技能：

```Bash
claude skills list
```

会显示：`remotion-dev/skills`



## 这个 skills 里面到底内置了什么（全是你做视频要用的）

1. Remotion 完整项目标准结构
2. Composition 画布（分辨率、时长、帧率）标准写法
3. `useCurrentFrame`、`interpolate`、spring 弹簧动画全部最优写法
4. React 组件封装规范
5. TailwindCSS 在 Remotion 内**正确配置方案**（原生很多人配置会报错）
6. 字幕、图片、背景、入场动画、滚动动画模板
7. 音频、字体加载、视频合成规范
8. 渲染导出命令、FFmpeg 相关规范
9. 所有常见报错解决方案

# 四、从零开始：AI一键生成完整Remotion视频项目（全套实操）

## 步骤1：新建一个空文件夹

比如桌面新建文件夹 `remotion-ai-video`，**终端进入这个文件夹**

```Bash
cd 桌面\remotion-ai-video
```



## 步骤2、启动 Claude Code

终端输入，直接回车：

```Bash
claude
```

进入 Claude Code 交互式 AI 编程界面，此时 AI 已经**自动读取了你安装的 remotion-dev/skills**。



## 步骤3、直接复制下面这段**万能中文提示词**发给 AI

这是适配 `remotion-dev/skills` 专属优化提示词，直接完整复制发送：

```Plain Text
请基于Remotion最新版，结合你内置的remotion-dev/skills全部规范，
从零搭建一个完整可直接运行的视频项目，要求：
1. 视频尺寸：竖屏 1080×1920，短视频9秒，30帧
2. 使用React组件写法，所有画面全部封装组件
3. 完整集成TailwindCSS，所有样式使用Tailwind，不写原生css
4. 黑色背景，画面中间大标题字幕，带淡入+轻微缩放入场动画
5. 底部有固定小字备注
6. 代码规范、动画使用useCurrentFrame和interpolate标准写法
7. 自动安装全部依赖，自动配置项目，给出启动预览命令、渲染导出mp4完整命令
8. 代码可直接运行无报错，结构清晰，组件化拆分
```



## 步骤4：AI会全自动完成全部操作

Claude Code 会依次自动执行：

1. 初始化 Remotion 项目
2. 自动安装所有依赖（react、remotion、tailwind相关包）
3. 按照官方 skills 规范写**React组件**
4. 写好视频画布 Composition
5. 写字幕组件、动画逻辑
6. 完整配置 TailwindCSS
7. 给出启动预览命令、最终渲染导出MP4命令

# 五、AI生成完后，你手动执行的最终命令

## 1. 另启终端，本地网页预览视频效果

```Bash
npm run dev
```

浏览器打开地址，就能实时看每一帧动画效果。



## 2. 正式渲染导出 MP4 视频文件

```Bash
npm run build
```

执行完毕，项目out文件夹里直接生成成品 mp4 视频。



# 六、把所有概念再次打通（结合本次全套流程终极总结）

## 1. remotion-dev/skills 本质

**技能库 / 专业手册**

存在于 Claude Code 内部，不是你项目里的代码文件，是AI的「专业知识库」。

作用：强制AI必须按照Remotion官方标准写代码，动画、组件、Tailwind、结构全部规范，**不会瞎写、不会报错**。



## 2. Claude Code 本质

**本地AI程序员**

- 能进你的文件夹
- 能新建文件、写代码
- 能安装依赖、跑Node命令
- 能读skills手册，生成专业项目
- 能启动预览、渲染视频

## 3. 整条完整完整链路（你所有提问全部闭环）

```Plain Text
电脑系统
    ↓
Node.js 运行环境（所有代码底层底座）
    ↓
Claude Code（AI编程助手）
    ↓ 读取内置知识库
remotion-dev/skills（Remotion官方专业技能规范）
    ↓ AI按照规则生成代码
Remotion 视频渲染框架
    ↓ 画面全部由
React 组件（字幕、背景、动画积木）
    ↓ 组件美化排版
TailwindCSS（颜色、大小、间距、布局）
    ↓ 逐帧渲染
最终导出 MP4 视频
```



# 七、你最容易混淆的几个点（避坑）

1. **remotion-dev/skills 不是库，不是npm包，不用npm安装**

它是 **Claude Code 专属技能包**，只用 `claude skills add` 安装。

1. **Claude Code 不是网页版Claude**

网页版只能聊天发代码；Claude Code 能**操作你电脑、改文件、跑命令、跑Node、渲染视频**。

1. **为什么必须装skills？**

普通AI写Remotion经常出错：

- 动画插值函数写错
- Composition参数格式错误
- Tailwind配置混乱无法生效
- React组件嵌套错误
- 渲染命令不对

装完skills之后，AI自带官方最佳实践，一次成型。

1. **整个流程你全程不需要手写一行代码**

所有组件、动画、Tailwind样式、项目配置全部AI生成。



# 八、额外附赠：我给你一份AI生成完的**标准代码长什么样**

你看完就能对应上之前问的**React组件**结构：

```JavaScript
import { Composition } from "remotion";
import { useCurrentFrame, interpolate } from "remotion";

// 大字幕 React 组件
const MainTitle = () => {
  const frame = useCurrentFrame();
  // 标准入场动画
  const opacity = interpolate(frame, [0, 15], [0, 1]);
  const scale = interpolate(frame, [0, 15], [0.9, 1]);

  return (
    <div
      className="text-white text-6xl font-bold"
      style={{ opacity, transform: `scale(${scale})` }}
    >
      AI生成视频
    </div>
  );
};

// 底部小字组件
const FooterText = () => {
  return <div className="text-gray-400 text-lg absolute bottom-20">Remotion视频</div>;
};

// 整个视频根组件
const MyVideo = () => {
  return (
    <div className="w-full h-full bg-black flex flex-col justify-center items-center">
      <MainTitle />
      <FooterText />
    </div>
  );
};

// 视频画布定义
export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="Video"
        component={MyVideo}
        durationInFrames={270}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
```

可以清晰看到：

- 一个个**React组件**（`MainTitle`、`FooterText`、`MyVideo`）
- **Tailwind类名**（`bg-black`、`text-white`、`flex justify-center`）
- Remotion标准**帧动画**
- 完全符合 `remotion-dev/skills` 官方规范

现在照着上面步骤一步步操作就行，中途遇到任何报错、AI生成不对、命令运行失败、Tailwind不生效，直接把问题发给我，我直接帮你解决。

 
