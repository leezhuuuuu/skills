---
name: datavis
description: Data visualization toolkit with color-blind safe palettes and D3.js templates. Use for creating accessible visualizations including bar charts, line charts, scatter plots, and force-directed graphs. Includes data validation for visualization.
---

# Data Visualization Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

Data visualization toolkit with accessible, color-blind safe designs and D3.js templates.

## Quick Start

```bash
# Generate a color-blind safe palette
python scripts/color_palette.py --theme scientific

# Create a visualization
python scripts/create_viz.py --type bar --data data.json --output chart.html

# Validate data for visualization
python scripts/validate_data.py --input data.csv
```

## Color Palettes

### Color-Blind Safe Palettes

| Theme | Use Case | Colors |
|-------|----------|--------|
| **Scientific** | Academic publications | Tableau 10, Okabe-Ito |
| **Diverging** | Temperature, sentiment | Blue-White-Orange |
| **Sequential** | Density, intensity | Viridis, Plasma |
| **Categorical** | Discrete categories | Wong's palette |

```python
from color_palette import generate_palette

# Generate palette for scientific publication
palette = generate_palette(
    theme="scientific",
    n_colors=8,
    colorblind_safe=True,
    wcag_aa=True  # WCAG AA compliance
)

print(palette)
# Returns hex codes: ['#0077BB', '#33BBEE', '#009988', ...]
```

### WCAG Contrast Checking

```python
from color_palette import check_contrast

# Check if text is readable on background
result = check_contrast(
    foreground="#0077BB",
    background="#FFFFFF",
    ratio=4.5  # AA standard
)
print(result.compliant)  # True/False
```

## Visualization Templates

### Bar Chart

```python
from create_viz import BarChart

chart = BarChart(
    data= [{"label": "A", "value": 10}, {"label": "B", "value": 20}],
    title="Sample Bar Chart",
    x_label="Category",
    y_label="Value",
    color_palette="scientific"
)
chart.save("bar_chart.html")
```

### Line Chart

```python
from create_viz import LineChart

chart = LineChart(
    data=[{"x": 1, "y": 10}, {"x": 2, "y": 15}, {"x": 3, "y": 12}],
    title="Time Series",
    x_label="Time",
    y_label="Value",
    interactive=True  # D3.js hover effects
)
chart.save("line_chart.html")
```

### Scatter Plot

```python
from create_viz import ScatterPlot

plot = ScatterPlot(
    data=[{"x": 10, "y": 20, "group": "A"}, {"x": 15, "y": 25, "group": "B"}],
    x_label="X Axis",
    y_label="Y Axis",
    color_by="group",
    regression_line=True
)
plot.save("scatter.html")
```

### Force-Directed Graph

```python
from create_viz import ForceGraph

graph = ForceGraph(
    nodes=[{"id": "A"}, {"id": "B"}, {"id": "C"}],
    links=[{"source": "A", "target": "B"}, {"source": "B", "target": "C"}],
    physics_enabled=True,
    charge_strength=-300
)
graph.save("network.html")
```

## Data Validation

```python
from validate_data import validate_for_viz

# Validate data before visualization
validation = validate_for_viz(
    data="sales_data.csv",
    required_columns=["category", "value"],
    checks=["completeness", "range", "type"]
)

print(validation.is_valid)
print(validation.issues)
```

### Validation Checks

| Check | Description | Example Issue |
|-------|-------------|---------------|
| **Completeness** | No missing values | Null values in key column |
| **Range** | Values in expected range | Negative value for percentage |
| **Type** | Correct data types | String in numeric column |
| **Uniqueness** | No duplicate keys | Duplicate category names |
| **Ordering** | Sorted for line charts | Unsorted time series |

## Accessibility Features

### Color Blindness Simulation

```python
from accessibility import simulate_cvd

# Simulate how your chart looks to color blind users
chart = load_chart("my_chart.html")

# Check different CVD types
for cvd_type in ['protanopia', 'deuteranopia', 'tritanopia']:
    simulated = simulate_cvd(chart, cvd_type)
    save(simulated, f"chart_{cvd_type}.html")
```

### Accessibility Checklist

```markdown
## Visualization Accessibility
- [ ] Color-blind safe palette used
- [ ] Patterns/textures for key区分
- [ ] Alternative text for screen readers
- [ ] High contrast ratios (4.5:1 minimum)
- [ ] Interactive elements keyboard accessible
- [ ] Color not sole information carrier
```

## D3.js Templates

### Template Types

| Template | Best For | Complexity |
|----------|----------|------------|
| **BarChart** | Categorical comparisons | Basic |
| **LineChart** | Time series, trends | Basic |
| **ScatterPlot** | Correlations, distributions | Intermediate |
| **HeatMap** | Dense matrices, correlations | Intermediate |
| **ForceGraph** | Networks, hierarchies | Advanced |
| **TreeMap** | Hierarchical proportions | Advanced |
| **Choropleth** | Geographic data | Advanced |

### Customization

```python
from create_viz import ChartTemplate

template = ChartTemplate(
    base_type="bar",
    width=800,
    height=500,
    margin={"top": 40, "right": 40, "bottom": 60, "left": 60},
    font_family="Arial, sans-serif",
    title_font_size=18,
    animation_duration=500,
    responsive=True
)
```

## Output Formats

| Format | Use Case |
|--------|----------|
| **HTML** | Interactive web visualizations |
| **PNG** | Static images for documents |
| **SVG** | Scalable, editable graphics |
| **JSON** | Data for other tools |

## Resources

- **D3.js Documentation**: https://d3js.org/
- **Color Blindness Simulators**: https://www.color-blindness.com/
- **WCAG Contrast Guidelines**: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- **Scientific Color Palettes**: https://matplotlib.org/stable/tutorials/colors/colormaps.html
