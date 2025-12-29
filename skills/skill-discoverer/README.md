# Skill Discoverer

> **Source**: This skill is derived from [anthropics/skills PR #152](https://github.com/anthropics/skills/pull/152) by @khaliqgant. Based on the [PRPM](https://prpm.dev) registry project.

从 PRPM registry 搜索和安装 skills、rules 和 agents。

## 安装

```bash
# 使用 npx（推荐）
npx prpm <command>

# 或全局安装
npm install -g prpm
```

## 快速使用

```bash
# AI 搜索（自然语言）
npx prpm ai-search "帮助我部署应用到云端"

# 关键词搜索
npx prpm search "pulumi infrastructure"

# 集合搜索
npx prpm collection search "frontend"
```

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。

## 资源

- **PRPM Registry**: https://prpm.dev
- **文档**: https://docs.prpm.dev
