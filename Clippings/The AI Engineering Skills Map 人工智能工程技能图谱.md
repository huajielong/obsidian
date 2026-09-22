---
title: "The AI Engineering Skills Map 人工智能工程技能图谱"
source: "https://x.com/AndrewYNg/status/2088302050706686198"
author:
  - "[[@AndrewYNg]]"
published: 2026-08-15
created: 2026-09-22
description: "I am delighted to present The AI Engineering Skills Map. AI allows us to build software very differently today than in 2022, and everyone wi..."
tags:
  - "clippings"
---
I am delighted to present The AI Engineering Skills Map. AI allows us to build software very differently today than in 2022, and everyone with the skills to take advantage of this shift has numerous exciting project and job opportunities. But with the noisy, hype-filled, information environment around AI, what are the most valuable skills for you to learn? I have been working with my team to synthesize a map of AI engineering skills in order to help (i) developers prioritize what to learn, and (ii) employers hire skilled developers.

Based on an analysis of over 10,000 job postings; carrying out dozens of structured interviews with AI experts, hiring managers, and recruiters; gathering data through surveys; and synthesizing other online data, here are the four most important AI engineering skills:

- Building and deploying AI applications
- Software engineering fundamentals
- Using coding agents
- Shaping the build

You can informally think of our process as akin to running clustering on a massive dataset of jobs and expert interviews to identify the most important skills, not just today but also in the near future.

A note on terminology: I talk about AI Engineering skills rather than the “AI Engineer” role (someone whose job is to build AI systems), because the former is much broader. All developers today should know how to work with the cloud, and only a smaller number have a “Cloud engineer” title. Similarly, all developers — full-stack engineers, data engineers, DevOps engineers, machine learning engineers, and, yes, AI engineers — will need AI engineering skills.

Building and deploying AI applications. The key difference between AI and non-AI applications is that the former has unpredictable outputs. When you prompt an LLM, you don’t know what you’ll get back. When you train a deep learning algorithm, you don’t know what prediction it will make on new examples. In contrast, traditional software behaves more predictably.构建和部署人工智能应用程序。人工智能应用程序与非人工智能应用程序的关键区别在于，前者的输出具有不可预测性。当你向大语言模型（LLM）发出提示时，你无法预知会得到什么结果；当你训练一个深度学习算法时，你也无法确定它会对新样本做出何种预测。相比之下，传统软件的行为则更具可预测性。

People who are skilled at building and deploying AI applications understand the building blocks of AI (such as LLMs, context engineering, RAG, agentic workflows, machine learning and deep learning) and, importantly, how to use statistical techniques to measure, steer, and govern AI systems so that they behave more predictably. A core skill in doing so is knowing how to drive disciplined evals and error analysis loops.

Software engineering fundamentals. When you deeply understand how software works, you can build much more effectively. Engineering software requires making tradeoffs between cost, scalability, reliability, speed, and more. Security and privacy add further complexity.软件工程基础。当你深入理解软件的工作原理时，就能更高效地进行开发。软件工程需要在成本、可扩展性、可靠性、速度等方面做出权衡。安全性和隐私性进一步增加了复杂性。

Understanding software fundamentals allows you to recognize what tradeoffs even exist. This leads to better decisions in choosing your software stack, designing system architecture, designing your data store, testing, and so on. It also leads to much better outcomes than those for an inexperienced developer who vibe codes a solution without knowing the tradeoffs their coding agent is making — which will often be poor ones, because they don’t know what context to give their coding agent. Understanding software engineering fundamentals lets you make good tradeoffs by steering coding agents using the precise language of software engineering.理解软件基础原理能让你认清存在哪些权衡取舍。这会帮助你在选择软件栈、设计系统架构、设计数据存储、进行测试等环节做出更优决策。与缺乏经验的开发者相比，你的成果也会好得多——后者仅凭感觉编写解决方案，却不清楚自己的编码智能体在做出哪些权衡，而这些权衡往往是糟糕的，因为他们不知道该为编码智能体提供怎样的上下文。理解软件工程基础原理，能让你借助软件工程的精准语言引导编码智能体，从而做出合理的权衡。

Using coding agents. Using agentic coding effectively is now a key skill for every developer. When you have this skill, you have a good mental model for how agents work. You understand their limitations and how to work around them, and are able to quickly steer them — knowing how much to intervene and how much to leave them alone — to build robust software without wasting excessive time or tokens.使用编程智能体。如今，高效运用具备自主能力的编程智能体已成为每位开发者的核心技能。掌握这一技能，你就能清晰理解智能体的工作原理，知晓其局限性并找到规避方法，还能精准操控它们——清楚何时该介入、何时该放手——从而构建稳定可靠的软件，同时避免浪费过多时间和令牌。

This requires your knowing how to manage a coding agent’s context, make tradeoffs between planning and execution, and help the agent autonomously close loops by providing verifiers or evals. You also need to know how to work with a clear spec (and when not to bother doing so), orchestrate multiple agents that work together, and avoid pitfalls like risk an agent messing up your production database. Because agentic coding is evolving quickly, using coding agents skillfully means not only knowing cutting-edge practices, but also having routines to keep trying new tools and evolve your workflows as best practices change.这需要你了解如何管理编码智能体的上下文，在规划与执行之间做出权衡，并通过提供验证器或评估工具帮助智能体自主完成闭环。你还需要知道如何遵循清晰的规范（以及何时无需遵循），协调多个协同工作的智能体，并规避各类风险，比如智能体误操作你的生产数据库。由于智能体编码技术发展迅速，熟练运用编码智能体不仅意味着掌握前沿实践，还需要建立一套方法，在最佳实践不断更新时持续尝试新工具并优化工作流程。

Shaping the build. Given a clear spec, coding agents are rapidly improving at delivering to it. Thus, our work as engineers is shifting toward deciding what should be in the spec. Engineers should no longer expect to be given a pixel-perfect design and asked only to implement it. Instead, effective AI engineering requires having product sense and understanding business context and customer goals, so you can participate in shaping and driving the build.打造构建方案。有了清晰的规范，编码智能体在按要求交付方面的能力正在快速提升。因此，工程师的工作重心正转向确定规范中应包含哪些内容。工程师不应再期待拿到一个像素级完美的设计，而只负责执行。相反，高效的人工智能工程工作需要具备产品思维，理解业务背景和客户目标，这样才能参与并推动构建方案的制定。

AI also gives you the opportunity to take on greater ownership and agency than before. You can identify interesting problems and opportunities, and execute to take advantage of them in responsible ways. Taking advantage of this opportunity requires knowing how to drive projects forward. For example, knowing when to quickly build an MVP to take to users for testing, and when to slow down and take longer in order to build more carefully.人工智能也让你有机会比以往更主动地承担责任、拥有更大的自主权。你可以发现有趣的问题和机遇，并以负责任的方式付诸行动抓住这些机会。把握这一机遇需要懂得如何推动项目进展。例如，要知道何时快速打造最小可行产品（MVP）供用户测试，何时放慢节奏、投入更多时间以更严谨地进行开发。

Underlying all these skills is a mindset of continuous learning. AI continues to change quickly, so we must all keep learning and evolving our skills to adopt emerging best practices.所有这些技能的核心是一种持续学习的思维模式。人工智能的发展日新月异，因此我们所有人都必须不断学习、提升自身技能，以适应新兴的最佳实践。

[DeepLearning.AI](//DeepLearning.AI)

’s principal focus is to help developers gain these AI engineering skills. I have more to say about each of these four skills, and will flesh out each of them in upcoming posts and share a more detailed AI Engineering Skills Map. As I look at where AI Engineering is going, I am incredibly excited about what all of us will be able to build. I hope you will play an exciting role in this future.[DeepLearning.AI](//DeepLearning.AI)的核心重点是帮助开发者掌握这些人工智能工程技能。我会对这四项技能分别展开阐述，并在后续的文章中对每一项进行详细说明，同时分享一份更详尽的人工智能工程技能图谱。展望人工智能工程的发展方向，我对我们所有人都能创造出的成果感到无比振奋。希望你能在这个未来中扮演精彩的角色。