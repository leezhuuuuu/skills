#!/usr/bin/env python3
"""
Data transformation module for ETL pipelines.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import json
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime


@dataclass
class TransformResult:
    """Result of a transformation operation."""
    success: bool
    output: Any
    stats: Dict[str, int] = None
    errors: List[str] = None


class DataTransformer:
    """Transform and clean data for analysis."""

    def __init__(self):
        self.transformations: List[Callable] = []
        self._stats = {"processed": 0, "modified": 0, "removed": 0}

    def process(
        self,
        data: Any,
        operations: List[str] = None,
        column_mapping: Dict[str, str] = None,
        custom_transforms: Dict[str, Callable] = None,
    ) -> Any:
        """
        Apply transformations to data.

        Args:
            data: Input data (list of dicts or single dict)
            operations: List of operations to apply
            column_mapping: Map old column names to new names
            custom_transforms: Custom transformation functions

        Returns:
            Transformed data

        Examples:
            >>> transformer = DataTransformer()
            >>> cleaned = transformer.process(data, operations=["dedupe", "normalize_text"])
        """
        if isinstance(data, dict):
            data = [data]

        self._stats = {"processed": len(data), "modified": 0, "removed": 0}

        # Apply column mapping first
        if column_mapping:
            data = self._rename_columns(data, column_mapping)

        # Apply operations
        operations = operations or []
        custom_transforms = custom_transforms or {}

        for op in operations:
            if op in self.OPERATION_MAP:
                data = self.OPERATION_MAP[op](data)
            else:
                raise ValueError(f"Unknown operation: {op}")

        # Apply custom transforms
        for col, transform in custom_transforms.items():
            data = self._apply_transform(data, col, transform)

        return data

    def _rename_columns(self, data: List[Dict], mapping: Dict[str, str]) -> List[Dict]:
        """Rename columns according to mapping."""
        result = []
        for row in data:
            new_row = {mapping.get(k, k): v for k, v in row.items()}
            result.append(new_row)
            if new_row != row:
                self._stats["modified"] += 1
        return result

    def _apply_transform(self, data: List[Dict], column: str, transform: Callable) -> List[Dict]:
        """Apply a custom transform function to a column."""
        result = []
        for row in data:
            if column in row:
                row[column] = transform(row[column])
                self._stats["modified"] += 1
            result.append(row)
        return result

    # Built-in transformation operations

    def _normalize_dates(self, data: List[Dict]) -> List[Dict]:
        """Normalize date formats to ISO 8601."""
        result = []
        date_patterns = [
            (r"(\d{4})-(\d{2})-(\d{2})", "%Y-%m-%d"),
            (r"(\d{2})/(\d{2})/(\d{4})", "%m/%d/%Y"),
            (r"(\d{2})-(\d{2})-(\d{4})", "%d-%m-%Y"),
            (r"(\d{4})/(\d{2})/(\d{2})", "%Y/%m/%d"),
        ]

        for row in data:
            new_row = dict(row)
            for key, value in row.items():
                if isinstance(value, str):
                    for pattern, fmt in date_patterns:
                        if re.match(pattern, value):
                            try:
                                dt = datetime.strptime(value, fmt)
                                new_row[key] = dt.strftime("%Y-%m-%d")
                                self._stats["modified"] += 1
                                break
                            except ValueError:
                                continue
            result.append(new_row)

        return result

    def _normalize_text(self, data: List[Dict]) -> List[Dict]:
        """Normalize text: lowercase, strip whitespace."""
        result = []
        for row in data:
            new_row = {}
            for key, value in row.items():
                if isinstance(value, str):
                    new_row[key] = value.strip().lower()
                else:
                    new_row[key] = value
            if new_row != row:
                self._stats["modified"] += 1
            result.append(new_row)
        return result

    def _dedupe(self, data: List[Dict]) -> List[Dict]:
        """Remove duplicate rows."""
        seen = set()
        result = []
        for row in row:
            row_tuple = tuple(sorted(row.items()))
            if row_tuple not in seen:
                seen.add(row_tuple)
                result.append(row)
            else:
                self._stats["removed"] += 1
        return result

    def _fill_missing(self, data: List[Dict], default: Any = None) -> List[Dict]:
        """Fill missing values with defaults."""
        result = []
        for row in data:
            new_row = dict(row)
            for key in new_row:
                if new_row[key] is None or new_row[key] == "":
                    new_row[key] = default if default is not None else self._get_default_for_type(data, key)
                    self._stats["modified"] += 1
            result.append(new_row)
        return result

    def _get_default_for_type(self, data: List[Dict], key: str) -> Any:
        """Get a sensible default based on other values."""
        values = [row.get(key) for row in data if row.get(key) is not None and row.get(key) != ""]
        if not values:
            return ""
        if all(isinstance(v, (int, float)) for v in values):
            return 0
        if all(isinstance(v, bool) for v in values):
            return False
        return ""

    def _type_conversion(self, data: List[Dict]) -> List[Dict]:
        """Convert string values to appropriate types."""
        result = []
        for row in data:
            new_row = dict(row)
            for key, value in new_row.items():
                if isinstance(value, str):
                    # Try integer
                    try:
                        if "." in value:
                            new_row[key] = float(value)
                            continue
                        else:
                            new_row[key] = int(value)
                            continue
                    except ValueError:
                        pass

                    # Try boolean
                    if value.lower() in ("true", "yes", "1"):
                        new_row[key] = True
                    elif value.lower() in ("false", "no", "0"):
                        new_row[key] = False
            result.append(new_row)
        return result

    def _filter_empty(self, data: List[Dict], keep_if_any: List[str] = None) -> List[Dict]:
        """Remove rows with all empty values."""
        result = []
        for row in data:
            has_value = False
            for key, value in row.items():
                if value not in (None, "", [], {}):
                    has_value = True
                    break
            if has_value:
                result.append(row)
            else:
                self._stats["removed"] += 1
        return result

    def _aggregate(self, data: List[Dict], group_by: str, aggregations: Dict[str, str]) -> List[Dict]:
        """Aggregate data by a key field."""
        groups: Dict[str, List[Dict]] = {}

        for row in data:
            key = row.get(group_by, "unknown")
            if key not in groups:
                groups[key] = []
            groups[key].append(row)

        result = []
        for key, group in groups.items():
            aggregated = {group_by: key}
            for target_field, agg_type in aggregations.items():
                values = [r.get(target_field) for r in group if r.get(target_field) is not None]

                if not values:
                    aggregated[target_field] = None
                elif agg_type == "sum":
                    aggregated[target_field] = sum(v for v in values if isinstance(v, (int, float)))
                elif agg_type == "avg":
                    aggregated[target_field] = sum(v for v in values if isinstance(v, (int, float))) / len(values)
                elif agg_type == "min":
                    aggregated[target_field] = min(values)
                elif agg_type == "max":
                    aggregated[target_field] = max(values)
                elif agg_type == "count":
                    aggregated[target_field] = len(values)
                elif agg_type == "first":
                    aggregated[target_field] = values[0]
                elif agg_type == "last":
                    aggregated[target_field] = values[-1]

            result.append(aggregated)

        return result

    # Operation registry
    OPERATION_MAP = {
        "normalize_dates": lambda d: DataTransformer()._normalize_dates(d),
        "normalize_text": lambda d: DataTransformer()._normalize_text(d),
        "dedupe": lambda d: DataTransformer()._dedupe(d),
        "fill_missing": lambda d: DataTransformer()._fill_missing(d),
        "type_conversion": lambda d: DataTransformer()._type_conversion(d),
        "filter_empty": lambda d: DataTransformer()._filter_empty(d),
    }


def transform_data(
    input_path: str,
    output_path: str,
    operations: List[str] = None,
    **kwargs
) -> TransformResult:
    """
    Transform data from input file to output file.

    Args:
        input_path: Input JSON file path
        output_path: Output JSON file path
        operations: List of operations to apply
        **kwargs: Additional arguments (column_mapping, etc.)

    Returns:
        TransformResult with stats and errors
    """
    # Load data
    with open(input_path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    # Transform
    transformer = DataTransformer()
    result = transformer.process(data, operations=operations, **kwargs)

    # Save output
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return TransformResult(
        success=True,
        output=result,
        stats=transformer._stats,
        errors=[]
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transform data")
    parser.add_argument("--input", "-i", required=True, help="Input JSON file")
    parser.add_argument("--output", "-o", required=True, help="Output JSON file")
    parser.add_argument("--operations", "-n", nargs="+",
                        choices=["normalize_dates", "normalize_text", "dedupe",
                                 "fill_missing", "type_conversion", "filter_empty"],
                        default=["normalize_text", "dedupe"],
                        help="Operations to apply")
    parser.add_argument("--rename", nargs="+",
                        help="Column renames (old:new pairs)")

    args = parser.parse_args()

    # Parse column mapping
    column_mapping = {}
    if args.rename:
        for pair in args.rename:
            if ":" in pair:
                old, new = pair.split(":", 1)
                column_mapping[old] = new

    result = transform_data(
        args.input,
        args.output,
        operations=args.operations,
        column_mapping=column_mapping
    )

    print(f"Transformation complete:")
    print(f"  Processed: {result.stats['processed']}")
    print(f"  Modified: {result.stats['modified']}")
    print(f"  Removed: {result.stats['removed']}")
