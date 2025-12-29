# Data Visualization Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

数据可视化工具包，包含色盲安全调色板和 D3.js 模板。

## 功能

| 功能 | 描述 |
|------|------|
| **色盲安全调色板** | WCAG AA 合规，颜色对比检查 |
| **可视化模板** | 柱状图、折线图、散点图、力导向图 |
| **数据验证** | 可视化前数据验证 |
| **无障碍设计** | 色盲模拟，无障碍检查 |

## 快速使用

```bash
# 生成色盲安全调色板
python scripts/color_palette.py --theme scientific

# 创建可视化
python scripts/create_viz.py --type bar --data data.json

# 验证数据
python scripts/validate_data.py --input data.csv
```

## 可视化类型

- **BarChart** - 分类比较
- **LineChart** - 时间序列
- **ScatterPlot** - 相关性分析
- **ForceGraph** - 网络关系
- **HeatMap** - 密度矩阵
- **TreeMap** - 层次结构

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。

## 资源

- [D3.js](https://d3js.org/)
- [WCAG 指南](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
