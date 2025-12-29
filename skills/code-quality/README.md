# Code Quality Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

代码质量工具包，包含代码检查、格式化和测试生成功能。

## 核心功能

| 功能 | 描述 |
|------|------|
| **代码检查** | Linting, 安全检查, 最佳实践 |
| **代码格式化** | 多语言格式化支持 |
| **测试生成** | 单元测试模板生成 |
| **质量报告** | 代码复杂度, 覆盖率报告 |

## 安装

```bash
pip install ast flake8 black isort
```

## 快速使用

```bash
# 代码检查
python scripts/lint.py --path src/ --rules basic,security

# 代码格式化
python scripts/format.py --path src/ --style pep8 --fix

# 测试生成
python scripts/test.py --path src/module.py --framework pytest
```

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。
