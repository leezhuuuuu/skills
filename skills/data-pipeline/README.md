# Data Pipeline Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

数据管道工具包，用于 ETL 操作，支持数据获取、验证和转换。

## 核心功能

| 功能 | 描述 |
|------|------|
| **数据获取** | HTTP API、数据库、文件源支持 |
| **数据验证** | JSON Schema 验证 |
| **数据转换** | 清洗、归一化、去重 |
| **批处理** | 大规模数据处理 |

## 安装

```bash
pip install requests jsonschema pandas
```

## 快速使用

```bash
# 获取数据
python scripts/fetch.py --url "https://api.example.com/data" --output data.json

# 验证数据
python scripts/validate.py --input data.json --schema schema.json

# 转换数据
python scripts/transform.py --input data.json --output cleaned.json
```

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。
