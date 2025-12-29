# Cascade Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

多代理 AI 研究编排系统，执行层次化研究工作流。

## 核心功能

| 功能 | 描述 |
|------|------|
| **层次化研究** | Belter → Drummer → Camina 三层架构 |
| **多代理并行** | 支持 8-16 个并行工作代理 |
| **多 LLM 提供商** | 支持 12+ LLM 提供商 |
| **工作流管理** | 状态检查、取消、结果获取 |

## 快速使用

```bash
# 执行研究工作流
python scripts/research.py "研究 AI 安全框架"

# 检查工作流状态
python scripts/status.py <task_id>

# 取消工作流
python scripts/status.py <task_id> --cancel
```

## 架构

```
Tier 1 (Belter): 并行工作代理
    ↓
Tier 2 (Drummer): 中级综合代理
    ↓
Tier 3 (Camina): 执行综合与最终报告
```

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。
