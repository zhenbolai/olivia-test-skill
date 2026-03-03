# OpenClaw Skills for Olivia

这里存放 Olivia 的 OpenClaw 自定义 skills。

## 包含的 Skills

### 1. dianxiaomi-stats 📊
店小秘店铺业绩统计工具。支持：
- 查询全部店铺或指定店铺业绩
- 支持指定日期查询
- 获取订单量、付款金额、退款金额

**使用示例:**
```bash
python3 dianxiaomi-stats/get_store_stats.py          # 查询全部昨日
python3 dianxiaomi-stats/get_store_stats.py 20       # 查询20店昨日
python3 dianxiaomi-stats/get_store_stats.py 20 2026-02-28  # 查询20店2月28日
```

### 2. claude-code-guide
Claude Code Skills 完整指南，包含 skill 格式、调用方式、最佳实践。

### 3. spec-kit-workflow 🚀
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

- [店小秘统计](./dianxiaomi-stats/SKILL.md)
- [Claude Code Guide](./claude-code-guide/SKILL.md)
- [Spec-Kit Workflow](./spec-kit-workflow/SKILL.md)
