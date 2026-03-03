---
name: claude-code-guide
description: >
  Claude Code Skills 完整指南。包含 skill 格式、调用方式、最佳实践。
  当需要创建、修改或调用 skills 时参考此 skill。
  适用于理解 Agent Skills 架构、创建自定义 skills、集成 Claude Code 功能。
disable-model-invocation: false
---

# Claude Code Skills 完整指南

## 什么是 Skills？

Skills 是 Claude Code 的扩展机制，让你添加自定义指令、工作流和可复用的知识。

## Skill 目录结构

```
my-skill/
├── SKILL.md           # 必需 - 主指令文件
├── reference.md       # 可选 - 参考文档
├── examples.md       # 可选 - 使用示例
└── scripts/
    └── helper.sh     # 可选 - 可执行脚本
```

## SKILL.md 格式

```yaml
---
name: skill-name
description: 描述 skill 的用途和何时使用
disable-model-invocation: false  # 是否禁止 Claude 自动调用
allowed-tools: [Read, Grep, Bash]  # 限制可用工具
---

# 你的指令内容...

## 变量替换

$ARGUMENTS    # 调用时传入的参数
$ARGUMENTS[0] # 第一个参数
$0            # 同上，简写形式
${CLAUDE_SESSION_ID}  # 当前会话 ID
```

## 调用方式

1. **手动调用**: 输入 `/skill-name` 或 `/skill-name 参数`
2. **自动调用**: Claude 根据 description 判断何时使用

## Frontmatter 字段说明

| 字段 | 说明 |
|------|------|
| name | Skill 名称（小写字母、数字、短横线） |
| description | 描述，帮助 Claude 判断使用场景 |
| disable-model-invocation | true = 只允许手动调用 |
| allowed-tools | 允许使用的工具列表 |
| context | 设为 "fork" 在子代理中运行 |
| agent | 子代理类型 (Explore, Plan, general-purpose) |

## 重要链接

- 官方文档: https://code.claude.com/docs/en/skills
- Agent Skills 标准: https://agentskills.io

## 创建新 Skill 的步骤

1. 创建目录: `mkdir -p ~/.claude/skills/<name>`
2. 创建 SKILL.md 文件
3. 编写 frontmatter + 指令内容
4. 测试调用: `/<name>`

## 在 OpenClaw 中使用

OpenClaw 的 skills 目录:
- 个人: `~/.openclaw/skills/skills/<name>/`
- 项目: `<project>/.claude/skills/<name>/`

## 推送 Skill 到 GitHub

```bash
cd ~/.openclaw/skills/skills/<skill-name>
git init
git add .
git commit -m "Add <skill-name> skill"
gh repo create <skill-name> --public --push
```

## 常用 Skills 示例

### 1. 代码审查 Skill
```yaml
---
name: code-review
description: 执行代码审查，检查质量、安全性和性能
context: fork
agent: Explore
---
审查以下代码:
$ARGUMENTS

检查要点:
1. 代码质量
2. 安全漏洞
3. 性能问题
4. 最佳实践
```

### 2. 部署 Skill
```yaml
---
name: deploy
description: 部署应用到生产环境
disable-model-invocation: true
---
部署步骤:
1. 运行测试
2. 构建应用
3. 推送到部署目标
4. 验证部署成功
```

---

**提示**: 保持 SKILL.md 在 500 行以内，详细内容放到 supporting files。
