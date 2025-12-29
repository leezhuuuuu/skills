# AFO Trinity Score Calculator

> **Source**: This skill is derived from [anthropics/skills PR #174](https://github.com/anthropics/skills/pull/174) by @lofibrainwav.

基于五支柱眞善美孝永评估系统质量的计算器。

## 五支柱

| 支柱 | 权重 | 描述 |
|------|------|------|
| 眞 (Truth) | 35% | 技术准确性 |
| 善 (Goodness) | 35% | 伦理健全性 |
| 美 (Beauty) | 20% | 设计优雅性 |
| 孝 (Serenity) | 8% | 操作无摩擦 |
| 永 (Eternity) | 2% | 长期可持续性 |

## 使用

```python
from trinity_calculator import calculate_trinity_score

input_data = {
    "truth_base": 95,
    "goodness_base": 90,
    "beauty_base": 85,
    "risk_score": 5,
    "friction": 3,
    "eternity_base": 88
}

result = calculate_trinity_score(input_data)
# Returns: trinity_score, decision, balance_status
```

## 决策阈值

- **AUTO_RUN**: 分数 ≥ 90 且 风险 ≤ 10
- **ASK_COMMANDER**: 分数 70-89 或 风险 11-30
- **BLOCK**: 分数 < 70 或 风险 > 30

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。
