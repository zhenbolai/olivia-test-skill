# OpenClaw Skills for Olivia

这里存放 Olivia 的 OpenClaw 自定义 skills。

## 包含的 Skills

### 1. claude-code-guide
Claude Code Skills 完整指南，包含 skill 格式、调用方式、最佳实践。

### 2. spec-kit-workflow 🚀
使用简化版 Spec-Kit 工作流快速开发 Web 应用并发布到公网。

## 快速开始

### 安装工具

```bash
# 安装 uv
brew install uv

# 安装 ngrok
brew install ngrok

# 配置 ngrok (需要从 https://dashboard.ngrok.com 获取 token)
ngrok config add-authtoken YOUR_TOKEN
```

### 调用 Claude Code

```bash
/Users/lzb/.local/bin/claude --print --dangerously-skip-permissions
```

## 文档

- [Claude Code Guide](./claude-code-guide/SKILL.md)
- [Spec-Kit Workflow](./spec-kit-workflow/SKILL.md)
