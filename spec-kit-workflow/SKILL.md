---
name: spec-kit-workflow
description: >
  使用简化版 Spec-Kit 工作流快速开发 Web 应用。包含：需求规格生成、技术计划、完整代码实现、ngrok 发布。
  当用户想要开发一个 Web 应用并快速发布到公网时使用此 skill。
disable-model-invocation: false
allowed-tools: [Read, Write, Edit, Bash, WebFetch, WebSearch, Browser]
---

# Spec-Kit 简化工作流

快速开发 Web 应用的完整工作流。

## 工作流步骤

### 1. 准备项目目录

```bash
mkdir ~/my-project && cd ~/my-project
```

### 2. 调用 Claude Code（英文）

使用以下命令调用 Claude Code：

```bash
/Users/lzb/.local/bin/claude --print --dangerously-skip-permissions
```

### 3. 英文提示词模板

复制以下内容发送给 Claude Code：

```
You are working on a simplified spec-driven development workflow.

STEP 1 - SPECIFY: Create a SPEC.md file describing [你的项目描述]

Include:
- Core features
- User interface requirements
- Data handling
- Any specific constraints

STEP 2 - PLAN: Create a PLAN.md file with:
- Technology: [如: Vanilla HTML/CSS/JS, React, Vue, etc.]
- [其他技术细节]

STEP 3 - IMPLEMENT: Create the complete [文件名] with:
- All functionality as specified in SPEC.md
- [具体实现要求]

STEP 4 - SERVE: After creating the files, start HTTP server on port [端口如 8097] and start ngrok tunnel.
Confirm each step as you complete it and list the files created.
```

### 4. 启动 ngrok 隧道

如果 Claude Code 没有自动启动 ngrok，手动启动：

```bash
ngrok http [端口号]
```

## 工具安装

### Claude Code
```bash
# 检查是否已安装
which claude
# 或
/Users/lzb/.local/bin/claude --version
```

### uv (Python 包管理)
```bash
brew install uv
```

### ngrok
```bash
brew install ngrok

# 配置 authtoken（需要从 https://dashboard.ngrok.com 获取）
ngrok config add-authtoken YOUR_TOKEN_HERE
```

## 示例项目

### 科技风格待办事项应用
- 项目位置: ~/todo-app-spec5/
- 本地访问: http://localhost:8097
- Spec: SPEC.md
- Plan: PLAN.md
- 实现: index.html

## 重要提示

- 官方 spec-kit（/speckit.* 命令）需要交互式 Claude Code 会话
- 简化版工作流使用 --print 模式，更适合自动化
- 确保 ngrok 已配置 authtoken 才能正常使用

## 相关资源

- Claude Code: https://code.claude.com/
- Spec-Kit: https://github.com/github/spec-kit
- ngrok: https://ngrok.com/
