# PostgreSQL Query Skill

> **Source**: This skill is derived from [anthropics/skills PR #182](https://github.com/anthropics/skills/pull/182) by @kevics1.

PostgreSQL 数据库查询和安全连接工具。

## 安装

```bash
pip install psycopg2-binary
```

## 快速使用

### 设置环境变量

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mydb
export PGUSER=myuser
export PGPASSWORD=mypassword
```

### 执行查询

```bash
# 只读查询（默认）
python scripts/query_postgres.py --query "SELECT * FROM users LIMIT 10"

# 列出所有表
python scripts/list_tables.py
```

## 安全特性

- 参数化查询防止 SQL 注入
- 默认只读模式
- LIMIT 限制返回行数

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。
