# Shodh Memory Skill

> **Source**: This skill is derived from [anthropics/skills PR #154](https://github.com/anthropics/skills/pull/154) by @varun29ankuS. Based on [shodh-memory](https://github.com/roshera/shodh-memory) project.

AI 代理的持久化记忆系统，存储决策、学习内容和上下文。

## 安装

### Claude Code

```bash
claude mcp add shodh-memory -- npx -y @anthropic-ai/shodh-memory
```

### MCP Server

```bash
npx -y @anthropic-ai/shodh-memory
```

## 核心功能

| 工具 | 用途 |
|------|------|
| `proactive_context` | 每条消息调用，检索相关记忆 |
| `remember` | 存储新记忆 |
| `recall` | 语义搜索记忆 |
| `recall_by_tags` | 按标签过滤 |
| `forget` | 删除记忆 |
| `memory_stats` | 获取统计信息 |

## 记忆类型

| 类型 | 用途 |
|------|------|
| `Decision` | 用户选择、架构决策 |
| `Learning` | 新获取的知识 |
| `Error` | 发现的错误和修复 |
| `Discovery` | 洞察、顿悟 |
| `Pattern` | 重复行为模式 |
| `Context` | 背景信息 |
| `Task` | 进行中的工作 |
| `Observation` | 一般性笔记 |

## 工作流程

```
用户消息 → proactive_context() → 检索记忆 → 响应时融入上下文 → remember() 存储新记忆
```

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。

## 资源

- [GitHub](https://github.com/roshera/shodh-memory)
- [MCP Server](https://www.npmjs.com/package/@anthropic-ai/shodh-memory)
