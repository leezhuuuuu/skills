---
name: code-quality
description: Code quality toolkit with linting, formatting, and test generation for multiple languages.
---

# Code Quality Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

Code quality toolkit with linting, formatting, and test generation.

## Quick Start

```bash
# Run linter
python scripts/lint.py --path src/ --rules basic,security,best-practices

# Format code
python scripts/format.py --path src/ --style pep8 --fix

# Generate tests
python scripts/test.py --path src/module.py --coverage 80
```

## Core Features

| 功能 | 描述 |
|------|------|
| **代码检查** | Linting, 安全检查, 最佳实践 |
| **代码格式化** | 多语言格式化支持 |
| **测试生成** | 单元测试模板生成 |
| **质量报告** | 代码复杂度, 覆盖率报告 |

## Linting

```python
from lint import CodeLinter

linter = CodeLinter(
    rules=["basic", "security", "best-practices"],
    exclude_patterns=["*.pyc", "__pycache__/*"]
)

# 分析代码
report = linter.analyze("src/")

print(f"Issues found: {report.total_issues}")
for issue in report.issues:
    print(f"[{issue.severity}] {issue.file}:{issue.line} - {issue.message}")
```

### Linting Rules

| 规则集 | 描述 | 检查项 |
|--------|------|--------|
| **basic** | 基础检查 | 语法错误, 未使用变量 |
| **security** | 安全检查 | SQL注入, XSS, 硬编码密码 |
| **best-practices** | 最佳实践 | DRY, SOLID, 文档要求 |
| **performance** | 性能检查 | 循环优化, 内存使用 |

## 代码格式化

```python
from format import CodeFormatter

formatter = CodeFormatter(
    style="pep8",
    line_length=100,
    indent_size=4
)

# 格式化代码（自动修复）
changes = formatter.format("src/", fix=True)

print(f"Files modified: {len(changes)}")
```

### 支持的语言

- **Python** - PEP 8, Black 风格
- **JavaScript** - ESLint, Prettier
- **Java** - Google Java Format
- **Go** - gofmt
- **Rust** - rustfmt

## 测试生成

```python
from test import TestGenerator

generator = TestGenerator(
    framework="pytest",
    coverage_target=80
)

# 为模块生成测试
tests = generator.generate("src/utils.py")

# 保存测试文件
generator.save(tests, "tests/test_utils.py")
```

### 测试框架支持

| 框架 | 语言 | 特点 |
|------|------|------|
| pytest | Python | 主流, 简洁 |
| unittest | Python | 标准库 |
| Jest | JavaScript | Facebook 推荐 |
| JUnit | Java | 企业标准 |
| go test | Go | 标准测试 |

## 质量指标

```python
from metrics import CodeMetrics

metrics = CodeMetrics.analyze("src/")

print(f"Lines of code: {metrics.loc}")
print(f"Complexity: {metrics.cyclomatic_complexity}")
print(f"Coverage: {metrics.test_coverage}%")
```

## 配置

创建 `.quality.yaml` 配置文件：

```yaml
lint:
  rules:
    - basic
    - security
    - performance
  exclude:
    - "**/test_*.py"
    - "**/*_test.js"

format:
  style: pep8
  line_length: 100
  fix: true

test:
  framework: pytest
  coverage_target: 80
  mock_external: true
```

## 资源

- [PEP 8 Style Guide](https://pep8.org/)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [pytest Documentation](https://docs.pytest.org/)
