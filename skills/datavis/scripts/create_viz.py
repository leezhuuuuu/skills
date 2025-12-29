#!/usr/bin/env python3
"""
Data visualization template generator using D3.js concepts.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChartTemplate:
    """Base configuration for all charts."""
    base_type: str = "bar"
    width: int = 800
    height: int = 500
    margin: Dict[str, int] = field(default_factory=lambda: {"top": 40, "right": 40, "bottom": 60, "left": 60})
    font_family: str = "Arial, sans-serif"
    title_font_size: int = 18
    animation_duration: int = 500
    responsive: bool = True


class BaseChart(ABC):
    """Base class for all chart types."""

    def __init__(
        self,
        data: List[Dict],
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        color_palette: str = "scientific",
        template: ChartTemplate = None,
    ):
        self.data = data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color_palette = color_palette
        self.template = template or ChartTemplate()

    @abstractmethod
    def generate_html(self) -> str:
        """Generate HTML for the chart."""
        pass

    def save(self, filename: str):
        """Save chart to HTML file."""
        html = self.generate_html()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Chart saved to {filename}")


class BarChart(BaseChart):
    """Bar chart for categorical comparisons."""

    def generate_html(self) -> str:
        m = self.template.margin
        w = self.template.width - m["left"] - m["right"]
        h = self.template.height - m["top"] - m["bottom"]

        labels = [d.get("label", d.get("category", f"Item {i}")) for i, d in enumerate(self.data)]
        values = [float(d.get("value", d.get("count", 0))) for d in self.data]

        max_val = max(values) if values else 1
        bar_width = w / len(values) if values else 0

        bars = []
        for i, (d, val) in enumerate(zip(self.data, values)):
            label = labels[i]
            bar_h = (val / max_val) * h
            x = i * bar_width
            y = h - bar_h
            color = d.get("color", f"url(#gradient-{i % 5})")

            bars.append(f'''
            <rect class="bar" x="{x + 2}" y="{y}" width="{bar_width - 4}" height="{bar_h}"
                  fill="{color}" opacity="0.9">
                <title>{label}: {val}</title>
            </rect>
            <text x="{x + bar_width/2}" y="{h + 20}" text-anchor="middle"
                  font-size="12">{label}</text>
            <text x="{x + bar_width/2}" y="{y - 5}" text-anchor="middle"
                  font-size="11" fill="#555">{val}</text>
            ''')

        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <style>
        body {{ font-family: {self.template.font_family}; margin: 20px; }}
        .bar:hover {{ opacity: 1 !important; cursor: pointer; }}
        .axis-label {{ font-size: 14px; font-weight: bold; }}
        .title {{ font-size: {self.template.title_font_size}px; text-anchor: middle; }}
        .grid line {{ stroke: #ddd; stroke-dasharray: 3; }}
    </style>
</head>
<body>
    <h2 style="text-align: center;">{self.title}</h2>
    <svg width="{self.template.width}" height="{self.template.height}">
        <defs>
            <linearGradient id="gradient-0" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#0077BB"/>
                <stop offset="100%" style="stop-color:#005588"/>
            </linearGradient>
            <linearGradient id="gradient-1" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#33BBEE"/>
                <stop offset="100%" style="stop-color:#1199AA"/>
            </linearGradient>
            <linearGradient id="gradient-2" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#009988"/>
                <stop offset="100%" style="stop-color:#007766"/>
            </linearGradient>
            <linearGradient id="gradient-3" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#EE7733"/>
                <stop offset="100%" style="stop-color:#CC5522"/>
            </linearGradient>
            <linearGradient id="gradient-4" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#CC3311"/>
                <stop offset="100%" style="stop-color:#AA2200"/>
            </linearGradient>
        </defs>
        <g transform="translate({m['left']},{m['top']})">
            <line x1="0" y1="{h}" x2="{w}" y2="{h}" stroke="#333"/>
            <line x1="0" y1="0" x2="0" y2="{h}" stroke="#333"/>
            {''.join(bars)}
            <text x="{w/2}" y="{h + 45}" text-anchor="middle" class="axis-label">{self.x_label}</text>
            <text x="-{h/2}" y="-40" text-anchor="middle" transform="rotate(-90)" class="axis-label">{self.y_label}</text>
            <text x="{w/2}" y="-15" text-anchor="middle" class="title">{self.title}</text>
        </g>
    </svg>
</body>
</html>'''


class LineChart(BaseChart):
    """Line chart for time series and trends."""

    def generate_html(self) -> str:
        m = self.template.margin
        w = self.template.width - m["left"] - m["right"]
        h = self.template.height - m["top"] - m["bottom"]

        x_vals = [float(d.get("x", d.get("time", d.get("date", i)))) for i, d in enumerate(self.data)]
        y_vals = [float(d.get("y", d.get("value", 0))) for d in self.data]

        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)
        x_range = max_x - min_x if max_x != min_x else 1
        y_range = max_y - min_y if max_y != min_y else 1

        def scale_x(x):
            return ((x - min_x) / x_range) * w

        def scale_y(y):
            return h - ((y - min_y) / y_range) * h

        points = [f"{scale_x(x_vals[i])},{scale_y(y_vals[i])}" for i in range(len(self.data))]
        line_path = "M" + " L".join([f"{scale_x(x_vals[i])},{scale_y(y_vals[i])}" for i in range(len(self.data))])

        dots = []
        for i, (x, y) in enumerate(zip(x_vals, y_vals)):
            sx, sy = scale_x(x), scale_y(y)
            dots.append(f'''
            <circle cx="{sx}" cy="{sy}" r="4" fill="#0077BB">
                <title>{x}: {y}</title>
            </circle>
            ''')

        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <style>
        body {{ font-family: {self.template.font_family}; margin: 20px; }}
        .line {{ fill: none; stroke: #0077BB; stroke-width: 2.5; }}
        .dot:hover {{ r: 6; cursor: pointer; }}
        .axis-label {{ font-size: 14px; font-weight: bold; }}
    </style>
</head>
<body>
    <h2 style="text-align: center;">{self.title}</h2>
    <svg width="{self.template.width}" height="{self.template.height}">
        <g transform="translate({m['left']},{m['top']})">
            <line x1="0" y1="{h}" x2="{w}" y2="{h}" stroke="#333"/>
            <line x1="0" y1="0" x2="0" y2="{h}" stroke="#333"/>
            <path class="line" d="{line_path}"/>
            {''.join(dots)}
            <text x="{w/2}" y="{h + 45}" text-anchor="middle" class="axis-label">{self.x_label}</text>
            <text x="-{h/2}" y="-40" text-anchor="middle" transform="rotate(-90)" class="axis-label">{self.y_label}</text>
        </g>
    </svg>
</body>
</html>'''


class ScatterPlot(BaseChart):
    """Scatter plot for correlations and distributions."""

    def __init__(
        self,
        data: List[Dict],
        x_label: str = "",
        y_label: str = "",
        color_by: str = "",
        regression_line: bool = False,
        **kwargs
    ):
        super().__init__(data, "", x_label, y_label, **kwargs)
        self.color_by = color_by
        self.regression_line = regression_line

    def generate_html(self) -> str:
        m = self.template.margin
        w = self.template.width - m["left"] - m["right"]
        h = self.template.height - m["top"] - m["bottom"]

        x_vals = [float(d.get("x", 0)) for d in self.data]
        y_vals = [float(d.get("y", 0)) for d in self.data]

        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)
        x_range = max_x - min_x if max_x != min_x else 1
        y_range = max_y - min_y if max_y != min_y else 1

        colors = ["#0077BB", "#EE7733", "#009988", "#CC3311", "#33BBEE"]

        dots = []
        for i, d in enumerate(self.data):
            x = float(d.get("x", 0))
            y = float(d.get("y", 0))
            sx = ((x - min_x) / x_range) * w
            sy = h - ((y - min_y) / y_range) * h

            group = d.get(self.color_by, "default") if self.color_by else "default"
            color_idx = hash(group) % len(colors) if isinstance(group, str) else 0
            color = colors[color_idx]

            dots.append(f'''
            <circle cx="{sx}" cy="{sy}" r="6" fill="{color}" opacity="0.7">
                <title>({x}, {y})</title>
            </circle>
            ''')

        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Scatter Plot</title>
    <style>
        body {{ font-family: {self.template.font_family}; margin: 20px; }}
        circle {{ cursor: pointer; }}
        circle:hover {{ opacity: 1; }}
    </style>
</head>
<body>
    <svg width="{self.template.width}" height="{self.template.height}">
        <g transform="translate({m['left']},{m['top']})">
            <line x1="0" y1="{h}" x2="{w}" y2="{h}" stroke="#333"/>
            <line x1="0" y1="0" x2="0" y2="{h}" stroke="#333"/>
            {''.join(dots)}
            <text x="{w/2}" y="{h + 45}" text-anchor="middle">{self.x_label}</text>
            <text x="-{h/2}" y="-40" text-anchor="middle" transform="rotate(-90)">{self.y_label}</text>
        </g>
    </svg>
</body>
</html>'''


class ForceGraph(BaseChart):
    """Force-directed graph for networks."""

    def __init__(self, nodes: List[Dict], links: List[Dict], **kwargs):
        super().__init__([], "", "", "", **kwargs)
        self.nodes = nodes
        self.links = links

    def generate_html(self) -> str:
        nodes_json = json.dumps(self.nodes)
        links_json = json.dumps(self.links)

        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Force-Directed Graph</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{ font-family: {self.template.font_family}; margin: 20px; }}
        .link {{ stroke: #999; stroke-opacity: 0.6; }}
        .node {{ fill: #0077BB; stroke: #fff; stroke-width: 1.5px; cursor: pointer; }}
        text {{ font-size: 12px; pointer-events: none; }}
    </style>
</head>
<body>
    <svg width="{self.template.width}" height="{self.template.height}">
        <g></g>
    </svg>
    <script>
        const width = {self.template.width};
        const height = {self.template.height};

        const nodes = {nodes_json};
        const links = {links_json};

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width/2, height/2));

        const svg = d3.select("svg g");
        const link = svg.append("g")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("class", "link")
            .attr("stroke-width", 2);

        const node = svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 8)
            .call(drag(simulation));

        const label = svg.append("g")
            .selectAll("text")
            .data(nodes)
            .enter().append("text")
            .text(d => d.id)
            .attr("dx", 12)
            .attr("dy", 4);

        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);

            label
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        }});

        function drag(simulation) {{
            function dragstarted(event) {{
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }}
            function dragged(event) {{
                event.subject.fx = event.x;
                event.subject.fy = event.y;
            }}
            function dragended(event) {{
                if (!event.active) simulation.alphaTarget(0);
                event.subject.fx = null;
                event.subject.fy = null;
            }}
            return d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        }}
    </script>
</body>
</html>'''


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create data visualizations")
    parser.add_argument("--type", required=True,
                        choices=["bar", "line", "scatter", "force"],
                        help="Chart type")
    parser.add_argument("--data", required=True, help="Input JSON data file")
    parser.add_argument("--output", required=True, help="Output HTML file")
    parser.add_argument("--title", default="Chart", help="Chart title")
    parser.add_argument("--x-label", default="X Axis", help="X-axis label")
    parser.add_argument("--y-label", default="Y Axis", help="Y-axis label")

    args = parser.parse_args()

    with open(args.data, "r") as f:
        data = json.load(f)

    if not isinstance(data, list):
        data = [data]

    template = ChartTemplate(title=args.title)

    if args.type == "bar":
        chart = BarChart(data, args.title, args.x_label, args.y_label, template=template)
    elif args.type == "line":
        chart = LineChart(data, args.title, args.x_label, args.y_label, template=template)
    elif args.type == "scatter":
        chart = ScatterPlot(data, args.x_label, args.y_label, template=template)
    elif args.type == "force":
        nodes = data[0].get("nodes", [])
        links = data[0].get("links", [])
        chart = ForceGraph(nodes, links, template=template)

    chart.save(args.output)
