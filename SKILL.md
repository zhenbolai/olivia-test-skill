---
name: olivia-test
description: 这是一个测试 skill，用于验证 OpenClaw 是否可以调用 Claude Code 格式的 skills。当用户说"测试"或"test"时使用。
disable-model-invocation: false
---

# 测试 Skill

你好！这是 Olivia 的测试 skill 运行成功 🎉

## 功能

这个 skill 用来测试 OpenClaw 是否正确读取了 Claude Code 格式的 skill。

## 如何扩展

你可以创建更多 skills：
- 参考文档：https://code.claude.com/docs/en/skills
- 放在 `~/.claude/skills/` 目录下（个人）或项目的 `.claude/skills/` 目录下

## Skill 特性

- **name**: skill 的名称（调用时用 `/olivia-test`）
- **description**: 描述，让 Claude 知道何时自动使用
- **disable-model-invocation**: 设为 true 则只允许手动调用
- **allowed-tools**: 限制可用的工具

