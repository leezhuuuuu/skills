# Server Deploy Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

基础设施管理工具包，用于服务管理、健康检查和端口分配。

## 核心功能

| 功能 | 描述 |
|------|------|
| **服务管理** | 服务启停、状态查询、重启 |
| **健康检查** | CPU、内存、磁盘、Caddy 服务监控 |
| **端口管理** | 端口映射、可用性检查 |

## 快速使用

```bash
# 系统健康检查
python scripts/health.py

# 服务状态
python scripts/service.py status

# 端口映射
python scripts/ports.py map
```

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。
