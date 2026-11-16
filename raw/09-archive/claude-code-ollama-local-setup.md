---
title: "Claude Code + Ollama 完全本地化安装指南"
source: 用户对话输入
captured: 2026-11-02
---

# Claude Code + Ollama 完全本地化安装指南

## Step 0 — Install Node.js (skip if already installed)

Go to https://nodejs.org, download the LTS version, run the installer

Verify: node --version

## Step 1 — Install Claude Code

npm install -g @anthropic-ai/claude-code

Verify: claude --version

## Step 2 — Install Ollama

Mac/Linux: curl -fsSL https://ollama.com/install.sh | sh

Windows: Go to https://ollama.com, download the installer, run it

Verify: ollama --version

## Step 3 — Pull Your Model

Check your RAM first:

- 16GB or less → ollama pull qwen2.5-coder:14b
- 32GB → ollama pull glm-4.7-flash (recommended)
- 48GB+ → ollama pull glm-4.7

ollama pull glm-4.7-flash

~19GB download. Show the progress bar on screen.

## Step 4 — Create an Alias

"Instead of setting environment variables that mess with your normal Claude Code, we're going to create a shortcut. One alias gives you a second command — claude-local — that runs Claude Code through Ollama. Your regular claude command stays untouched."

Mac/Linux — add this one line to ~/.bashrc or ~/.zshrc:

alias claude-local='ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model glm-4.7-flash'

Then run source ~/.bashrc (or restart terminal).

Windows (Git Bash) — add to ~/.bashrc:

alias claude-local='ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model glm-4.7-flash'

Then restart your terminal or run source ~/.bashrc.

Windows (PowerShell):

1. Open PowerShell
2. Run notepad $PROFILE (this opens your profile file — if it asks to create it, click Yes)
3. Paste this single line into the file, save, and close:

function claude-local { $env:ANTHROPIC_AUTH_TOKEN="ollama"; $env:ANTHROPIC_API_KEY=""; $env:ANTHROPIC_BASE_URL="http://localhost:11434"; claude --model glm-4.7-flash @args }

4. Restart PowerShell (or run . $PROFILE to reload)

Note: You can't just paste this into a PowerShell window and have it stick — it needs to go in your profile file so it loads every time you open a terminal.

## Step 5 — Launch

Now you have two commands:

- claude → normal Claude Code (Anthropic servers, your subscription)
- claude-local → 100% free, 100% private, 100% local

claude-local

That's it. All normal flags still work — claude-local --dangerously-skip-permissions, etc.
