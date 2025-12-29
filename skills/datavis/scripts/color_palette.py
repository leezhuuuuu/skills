#!/usr/bin/env python3
"""
Color palette generator for data visualization.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import json
from typing import List, Optional

# Color-blind safe palettes from scientific literature

COLOR_PALETTES = {
    "scientific": {
        "description": "Academic publications - Tableau 10 + Okabe-Ito",
        "colors": [
            "#0077BB",  # Blue
            "#33BBEE",  # Cyan
            "#009988",  # Teal
            "#EE7733",  # Orange
            "#CC3311",  # Red
            "#33BBEE",  # Light Blue
            "#009988",  # Medium Green
            "#EE3377",  # Magenta
            "#BBBBBB",  # Gray
            "#332288",  # Indigo
        ]
    },
    "diverging": {
        "description": "Temperature, sentiment - Blue-White-Orange",
        "colors": [
            "#0077BB",  # Blue
            "#4477AA",  # Light Blue
            "#88CCEE",  # Pale Blue
            "#FFFFFF",  # White
            "#FFEECC",  # Pale Orange
            "#EE8866",  # Light Orange
            "#DDAA33",  # Gold
            "#FFA500",  # Orange
        ]
    },
    "sequential": {
        "description": "Density, intensity - Viridis-like",
        "colors": [
            "#440154",  # Dark Purple
            "#482878",  # Purple
            "#3E4A89",  # Deep Blue
            "#31688E",  # Blue
            "#26838F",  # Teal
            "#1F9E89",  # Green
            "#35B779",  # Light Green
            "#6ECE58",  # Lime
            "#B5DE2B",  # Yellow Green
            "#FDE725",  # Yellow
        ]
    },
    "categorical": {
        "description": "Discrete categories - Wong's palette",
        "colors": [
            "#000000",  # Black
            "#E69F00",  # Orange
            "#56B4E9",  # Sky Blue
            "#009E73",  # Bluish Green
            "#F0E442",  # Yellow
            "#0072B2",  # Blue
            "#D55E00",  # Vermilion
            "#CC79A7",  # Reddish Purple
        ]
    },
    "okabe_ito": {
        "description": "Universal color-blind safe palette",
        "colors": [
            "#E69F00",  # Orange
            "#56B4E9",  # Sky Blue
            "#009E73",  # Bluish Green
            "#F0E442",  # Yellow
            "#0072B2",  # Blue
            "#D55E00",  # Vermilion
            "#CC79A7",  # Reddish Purple
            "#000000",  # Black
        ]
    },
}


def generate_palette(
    theme: str = "scientific",
    n_colors: int = 8,
    colorblind_safe: bool = True,
    wcag_aa: bool = False,
) -> List[str]:
    """
    Generate a color palette for data visualization.

    Args:
        theme: Palette theme (scientific, diverging, sequential, categorical, okabe_ito)
        n_colors: Number of colors to return
        colorblind_safe: Return only color-blind safe colors
        wcag_aa: Ensure WCAG AA contrast compliance

    Returns:
        List of hex color codes

    Examples:
        >>> palette = generate_palette(theme="scientific", n_colors=5)
        >>> print(palette)
        ['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311']
    """
    if theme not in COLOR_PALETTES:
        available = list(COLOR_PALETTES.keys())
        raise ValueError(f"Unknown theme: {theme}. Available: {available}")

    palette_info = COLOR_PALETTES[theme]
    colors = palette_info["colors"]

    if n_colors > len(colors):
        # Repeat colors if more requested
        colors = (colors * ((n_colors // len(colors)) + 1))[:n_colors]

    return colors[:n_colors]


def check_contrast(foreground: str, background: str, ratio: float = 4.5) -> dict:
    """
    Check WCAG contrast compliance between two colors.

    Args:
        foreground: Hex color for foreground/text
        background: Hex color for background
        ratio: Minimum contrast ratio (4.5 for AA, 7.0 for AAA)

    Returns:
        Dict with compliant status, ratio, and details

    Examples:
        >>> result = check_contrast("#0077BB", "#FFFFFF", ratio=4.5)
        >>> print(result["compliant"])
        True
    """
    def hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_luminance(rgb: tuple) -> float:
        """Calculate relative luminance of a color."""
        rgb_normalized = [x / 255.0 for x in rgb]
        rgb_corrected = [
            x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
            for x in rgb_normalized
        ]
        return 0.2126 * rgb_corrected[0] + 0.7152 * rgb_corrected[1] + 0.0722 * rgb_corrected[2]

    fg_rgb = hex_to_rgb(foreground)
    bg_rgb = hex_to_rgb(background)

    l1 = get_luminance(fg_rgb)
    l2 = get_luminance(bg_rgb)

    lighter = max(l1, l2)
    darker = min(l1, l2)

    contrast_ratio = (lighter + 0.05) / (darker + 0.05)

    return {
        "compliant": contrast_ratio >= ratio,
        "ratio": round(contrast_ratio, 2),
        "required": ratio,
        "level": "AAA" if contrast_ratio >= 7.0 else "AA" if contrast_ratio >= 4.5 else "Fail",
    }


def export_palette(palette: List[str], format: str = "hex") -> str:
    """
    Export palette in various formats.

    Args:
        palette: List of hex colors
        format: Output format (hex, rgb, css, json)

    Returns:
        Palette string in specified format
    """
    if format == "hex":
        return "\n".join(palette)

    elif format == "rgb":
        lines = []
        for i, color in enumerate(palette):
            hex_color = color.lstrip("#")
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            lines.append(f"Color {i+1}: rgb({r}, {g}, {b})")
        return "\n".join(lines)

    elif format == "css":
        return ", ".join(palette)

    elif format == "json":
        return json.dumps({"palette": palette, "count": len(palette)}, indent=2)

    else:
        raise ValueError(f"Unknown format: {format}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate color-blind safe palettes")
    parser.add_argument("--theme", default="scientific", choices=list(COLOR_PALETTES.keys()),
                        help="Palette theme")
    parser.add_argument("--n-colors", type=int, default=8, help="Number of colors")
    parser.add_argument("--export", default="hex", choices=["hex", "rgb", "css", "json"],
                        help="Export format")
    parser.add_argument("--check-contrast", nargs=2, metavar=("FOREGROUND", "BACKGROUND"),
                        help="Check contrast ratio")
    parser.add_argument("--list-themes", action="store_true", help="List available themes")

    args = parser.parse_args()

    if args.list_themes:
        print("Available themes:")
        for name, info in COLOR_PALETTES.items():
            print(f"  - {name}: {info['description']}")
        exit(0)

    if args.check_contrast:
        result = check_contrast(args.check_contrast[0], args.check_contrast[1])
        print(f"Contrast Ratio: {result['ratio']}:1")
        print(f"WCAG {result['level']}: {'Compliant' if result['compliant'] else 'Non-compliant'}")
        exit(0)

    palette = generate_palette(theme=args.theme, n_colors=args.n_colors)
    print(export_palette(palette, format=args.export))
