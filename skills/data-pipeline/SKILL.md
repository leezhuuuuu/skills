---
name: data-pipeline
description: Data pipeline toolkit for ETL operations with validation and transformation capabilities.
---

# Data Pipeline Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

Data pipeline toolkit for ETL operations with validation and transformation.

## Quick Start

```bash
# Fetch data from API
python scripts/fetch.py --url "https://api.example.com/data" --output data.json

# Validate data
python scripts/validate.py --input data.json --schema schema.json

# Transform data
python scripts/transform.py --input data.json --output cleaned.json --operations normalize,dedupe
```

## Core Features

| 功能 | 描述 |
|------|------|
| **数据获取** | HTTP API、数据库、文件源 |
| **数据验证** | JSON Schema 验证 |
| **数据转换** | 清洗、归一化、去重 |
| **错误处理** | 详细错误报告和重试机制 |

## 数据获取

```python
from fetch import DataFetcher

fetcher = DataFetcher(
    base_url="https://api.example.com",
    auth_token="your-token",
    max_retries=3,
    timeout=30
)

# 获取单个资源
data = fetcher.get("/users/123")

# 批量获取
results = fetcher.batch_get(["/users/1", "/users/2", "/users/3"])

# 分页获取
all_data = fetcher.paginate("/items", page_size=100)
```

## 数据验证

```python
from validate import DataValidator

validator = DataValidator(schema_path="schema.json")

# 验证数据
result = validator.validate(data)

if result.is_valid:
    print("数据有效")
else:
    print(f"错误: {result.errors}")
```

## 数据转换

```python
from transform import DataTransformer

transformer = DataTransformer()

# 应用转换操作
cleaned = transformer.process(
    data,
    operations=[
        "normalize_dates",      # 标准化日期格式
        "normalize_text",       # 文本规范化
        "dedupe",               # 去重
        "fill_missing",         # 填充缺失值
        "type_conversion",      # 类型转换
    ]
)
```

## 操作详解

### fetch.py 选项

| 参数 | 描述 |
|------|------|
| `--url` | API 端点 URL |
| `--output` | 输出文件路径 |
| `--method` | HTTP 方法 (GET, POST, etc.) |
| `--headers` | 请求头 JSON |
| `--auth` | 认证令牌 |

### validate.py 选项

| 参数 | 描述 |
|------|------|
| `--input` | 输入数据文件 |
| `--schema` | JSON Schema 文件 |
| `--output` | 验证报告输出路径 |

### transform.py 选项

| 参数 | 描述 |
|------|------|
| `--input` | 输入数据文件 |
| `--output` | 输出文件路径 |
| `--operations` | 转换操作列表 |

## 批处理模式

```python
from pipeline import Pipeline

pipeline = Pipeline(
    name="my_etl",
    config="pipeline.yaml"
)

pipeline.run(
    source="api://example.com/data",
    transformations=["clean", "aggregate"],
    destination="database://localhost/main"
)
```

## 资源

- [JSON Schema](https://json-schema.org/)
- [ETL 最佳实践](https://www.example.com/etl-best-practices)
