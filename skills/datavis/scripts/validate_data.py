#!/usr/bin/env python3
"""
Data validation script for visualization.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import csv
import json
import pandas as pd
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    type: str
    column: Optional[str]
    row: Optional[int]
    message: str
    severity: str = "error"  # error, warning, info


@dataclass
class ValidationResult:
    """Result of data validation."""
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)

    def add_issue(self, issue: ValidationIssue):
        self.issues.append(issue)
        self.summary[issue.severity] = self.summary.get(issue.severity, 0) + 1
        if issue.severity == "error":
            self.is_valid = False


def load_data(input_path: str) -> Tuple[List[Dict], str]:
    """Load data from CSV or JSON file."""
    if input_path.endswith(".csv"):
        with open(input_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data, "csv"
    elif input_path.endswith(".json"):
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data], "json"
    else:
        raise ValueError(f"Unsupported file format: {input_path}")


def check_completeness(data: List[Dict], required_columns: List[str]) -> List[ValidationIssue]:
    """Check for missing values in required columns."""
    issues = []

    for idx, row in enumerate(data):
        for col in required_columns:
            value = row.get(col)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                issues.append(ValidationIssue(
                    type="completeness",
                    column=col,
                    row=idx + 1,
                    message=f"Missing value in column '{col}' at row {idx + 1}",
                    severity="error"
                ))

    return issues


def check_range(data: List[Dict], column_ranges: Dict[str, Tuple[float, float]]) -> List[ValidationIssue]:
    """Check if values are within expected ranges."""
    issues = []

    for idx, row in enumerate(data):
        for col, (min_val, max_val) in column_ranges.items():
            value_str = row.get(col)
            if value_str is not None and value_str != "":
                try:
                    value = float(value_str)
                    if value < min_val or value > max_val:
                        issues.append(ValidationIssue(
                            type="range",
                            column=col,
                            row=idx + 1,
                            message=f"Value {value} in '{col}' is outside range [{min_val}, {max_val}]",
                            severity="warning"
                        ))
                except ValueError:
                    pass  # Type check will catch non-numeric values

    return issues


def check_type(data: List[Dict], column_types: Dict[str, str]) -> List[ValidationIssue]:
    """Check if values have correct data types."""
    issues = []

    for idx, row in enumerate(data):
        for col, expected_type in column_types.items():
            value = row.get(col)
            if value is None or value == "":
                continue

            try:
                if expected_type == "numeric":
                    float(value)
                elif expected_type == "integer":
                    int(value)
                elif expected_type == "boolean":
                    if value.lower() not in ["true", "false", "1", "0"]:
                        raise ValueError("Not a boolean")
            except ValueError:
                issues.append(ValidationIssue(
                    type="type",
                    column=col,
                    row=idx + 1,
                    message=f"Value '{value}' in '{col}' is not {expected_type}",
                    severity="error"
                ))

    return issues


def check_uniqueness(data: List[Dict], key_columns: List[str]) -> List[ValidationIssue]:
    """Check for duplicate keys."""
    issues = []
    seen: Set[Tuple] = set()

    for idx, row in enumerate(data):
        key = tuple(row.get(col) for col in key_columns)
        if key in seen:
            issues.append(ValidationIssue(
                type="uniqueness",
                column=", ".join(key_columns),
                row=idx + 1,
                message=f"Duplicate key found: {key}",
                severity="error"
            ))
        else:
            seen.add(key)

    return issues


def check_ordering(data: List[Dict], order_columns: List[str], ascending: List[bool] = None) -> List[ValidationIssue]:
    """Check if data is properly sorted for visualization."""
    if ascending is None:
        ascending = [True] * len(order_columns)

    issues = []

    for idx in range(1, len(data)):
        for col, asc in zip(order_columns, ascending):
            val1 = float(data[idx - 1].get(col, 0))
            val2 = float(data[idx].get(col, 0))

            if asc and val1 > val2:
                issues.append(ValidationIssue(
                    type="ordering",
                    column=col,
                    row=idx + 1,
                    message=f"Data not sorted correctly in '{col}' at row {idx + 1}",
                    severity="warning"
                ))
                break
            elif not asc and val1 < val2:
                issues.append(ValidationIssue(
                    type="ordering",
                    column=col,
                    row=idx + 1,
                    message=f"Data not sorted correctly in '{col}' at row {idx + 1}",
                    severity="warning"
                ))
                break

    return issues


def validate_for_viz(
    data: List[Dict],
    required_columns: List[str] = None,
    column_ranges: Dict[str, Tuple[float, float]] = None,
    column_types: Dict[str, str] = None,
    key_columns: List[str] = None,
    order_columns: List[str] = None,
    checks: List[str] = None,
) -> ValidationResult:
    """
    Validate data for visualization.

    Args:
        data: List of dictionaries representing rows
        required_columns: Columns that must have values
        column_ranges: Dict of column -> (min, max) tuples
        column_types: Dict of column -> type (numeric, integer, boolean)
        key_columns: Columns that form unique keys
        order_columns: Columns that should be ordered
        checks: List of checks to perform (completeness, range, type, uniqueness, ordering)

    Returns:
        ValidationResult with is_valid status and any issues

    Examples:
        >>> result = validate_for_viz(
        ...     data=data,
        ...     required_columns=["category", "value"],
        ...     checks=["completeness", "range", "type"]
        ... )
        >>> print(result.is_valid)
        True
    """
    result = ValidationResult(is_valid=True)
    checks = checks or ["completeness", "type", "range"]

    if "completeness" in checks and required_columns:
        result.issues.extend(check_completeness(data, required_columns))

    if "range" in checks and column_ranges:
        result.issues.extend(check_range(data, column_ranges))

    if "type" in checks and column_types:
        result.issues.extend(check_type(data, column_types))

    if "uniqueness" in checks and key_columns:
        result.issues.extend(check_uniqueness(data, key_columns))

    if "ordering" in checks and order_columns:
        result.issues.extend(check_ordering(data, order_columns))

    # Recalculate summary
    result.summary = {}
    for issue in result.issues:
        result.summary[issue.severity] = result.summary.get(issue.severity, 0) + 1
        if issue.severity == "error":
            result.is_valid = False

    return result


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Validate data for visualization")
    parser.add_argument("--input", required=True, help="Input CSV or JSON file")
    parser.add_argument("--required", nargs="+", help="Required columns")
    parser.add_argument("--ranges", nargs="+", help="Column:min:max (e.g., value:0:100)")
    parser.add_argument("--types", nargs="+", help="Column:type (e.g., value:numeric)")
    parser.add_argument("--checks", nargs="+", default=["completeness", "type"],
                        choices=["completeness", "range", "type", "uniqueness", "ordering"])

    args = parser.parse_args()

    data, _ = load_data(args.input)

    # Parse column ranges
    column_ranges = {}
    if args.ranges:
        for r in args.ranges:
            parts = r.split(":")
            if len(parts) == 3:
                column_ranges[parts[0]] = (float(parts[1]), float(parts[2]))

    # Parse column types
    column_types = {}
    if args.types:
        for t in args.types:
            parts = t.split(":")
            if len(parts) == 2:
                column_types[parts[0]] = parts[1]

    result = validate_for_viz(
        data=data,
        required_columns=args.required,
        column_ranges=column_ranges,
        column_types=column_types,
        checks=args.checks,
    )

    print(f"Valid: {result.is_valid}")
    print(f"Issues: {len(result.issues)}")

    for issue in result.issues:
        print(f"  [{issue.severity.upper()}] {issue.type}: {issue.message}")

    sys.exit(0 if result.is_valid else 1)
