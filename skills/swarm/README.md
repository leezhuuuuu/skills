# Swarm Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

多代理编排技能，用于协调多个 AI 代理执行任务。

## 核心功能

| 功能 | 描述 |
|------|------|
| **任务分发** | 将任务分发给多个代理 |
| **并行执行** | 支持并行、顺序、混合模式 |
| **结果聚合** | 汇总各代理结果 |
| **会话管理** | 任务状态跟踪和继续 |

## 快速使用

```bash
# 运行 swarm 任务
python scripts/swarm.py --task "研究主题" --agents 4

# 检查状态
python scripts/status.py <session_id>

# 聚合结果
python scripts/aggregate.py <session_id>
```

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。
