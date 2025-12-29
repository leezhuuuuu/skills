#!/usr/bin/env python3
"""
Data validation module with JSON Schema support.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path


@dataclass
class ValidationError:
    """Represents a validation error."""
    path: str
    message: str
    expected: Optional[str] = None
    actual: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of data validation."""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)

    def add_error(self, error: ValidationError):
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, error: ValidationError):
        self.warnings.append(error)


class DataValidator:
    """Validate data against JSON Schema."""

    # Common schema patterns
    SCHEMA_PATTERNS = {
        "email": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        "uuid": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        "date": r"^\d{4}-\d{2}-\d{2}$",
        "datetime": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})?$",
        "url": r"^https?://[^\s]+$",
        "phone": r"^\+?[\d\s-]{10,}$",
    }

    def __init__(self, schema: Dict = None, schema_path: str = None):
        """
        Initialize the validator.

        Args:
            schema: JSON Schema dictionary
            schema_path: Path to schema JSON file
        """
        if schema_path:
            with open(schema_path, "r") as f:
                schema = json.load(f)
        self.schema = schema or {}
        self.errors = []

    def validate(self, data: Any) -> ValidationResult:
        """
        Validate data against the schema.

        Args:
            data: Data to validate

        Returns:
            ValidationResult with is_valid status and any errors
        """
        result = ValidationResult(is_valid=True)

        if not self.schema:
            return result

        self._validate_recursive(data, self.schema, "", result)

        return result

    def _validate_recursive(
        self,
        data: Any,
        schema: Dict,
        path: str,
        result: ValidationResult
    ):
        """Recursively validate data against schema."""
        if schema.get("type"):
            expected_type = schema["type"]
            actual_type = self._get_type(data)

            if expected_type != actual_type and expected_type != "any":
                result.add_error(ValidationError(
                    path=path,
                    message=f"Expected {expected_type}, got {actual_type}",
                    expected=expected_type,
                    actual=actual_type
                ))
                return  # Skip further validation on type mismatch

        # Check required fields
        if "required" in schema and isinstance(data, dict):
            for field_name in schema["required"]:
                if field_name not in data:
                    result.add_error(ValidationError(
                        path=f"{path}.{field_name}",
                        message=f"Missing required field: {field_name}"
                    ))

        # Check enum values
        if "enum" in schema and data not in schema["enum"]:
            result.add_error(ValidationError(
                path=path,
                message=f"Value must be one of: {schema['enum']}",
                expected=str(schema["enum"]),
                actual=str(data)
            ))

        # Check pattern
        if "pattern" in schema and isinstance(data, str):
            import re
            if not re.match(schema["pattern"], data):
                result.add_error(ValidationError(
                    path=path,
                    message=f"String does not match pattern: {schema['pattern']}"
                ))

        # Check minimum/maximum
        if isinstance(data, (int, float)):
            if "minimum" in schema and data < schema["minimum"]:
                result.add_error(ValidationError(
                    path=path,
                    message=f"Value {data} is below minimum {schema['minimum']}",
                    expected=f">= {schema['minimum']}",
                    actual=str(data)
                ))

            if "maximum" in schema and data > schema["maximum"]:
                result.add_error(ValidationError(
                    path=path,
                    message=f"Value {data} exceeds maximum {schema['maximum']}",
                    expected=f"<= {schema['maximum']}",
                    actual=str(data)
                ))

        # Check string length
        if isinstance(data, str):
            if "minLength" in schema and len(data) < schema["minLength"]:
                result.add_error(ValidationError(
                    path=path,
                    message=f"String length {len(data)} is below minimum {schema['minLength']}"
                ))

            if "maxLength" in schema and len(data) > schema["maxLength"]:
                result.add_error(ValidationError(
                    path=path,
                    message=f"String length {len(data)} exceeds maximum {schema['maxLength']}"
                ))

        # Check array items
        if "items" in schema and isinstance(data, list):
            for i, item in enumerate(data):
                item_path = f"{path}[{i}]"
                self._validate_recursive(item, schema["items"], item_path, result)

        # Check object properties
        if "properties" in schema and isinstance(data, dict):
            for prop_name, prop_schema in schema["properties"].items():
                if prop_name in data:
                    prop_path = f"{path}.{prop_name}"
                    self._validate_recursive(data[prop_name], prop_schema, prop_path, result)

        # Check additional properties
        if "additionalProperties" in schema and isinstance(data, dict):
            if not schema["additionalProperties"]:
                allowed_props = set(schema.get("properties", {}).keys())
                for prop_name in data.keys():
                    if prop_name not in allowed_props:
                        result.add_error(ValidationError(
                            path=f"{path}.{prop_name}",
                            message=f"Additional property '{prop_name}' not allowed"
                        ))

    def _get_type(self, value: Any) -> str:
        """Get the JSON schema type of a value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "string"


def create_schema_from_sample(samples: List[Dict], strict: bool = False) -> Dict:
    """
    Generate a JSON Schema from sample data.

    Args:
        samples: List of sample data dictionaries
        strict: If True, require all fields present in all samples

    Returns:
        JSON Schema dictionary
    """
    if not samples:
        return {"type": "object", "properties": {}}

    all_keys = set()
    for sample in samples:
        if isinstance(sample, dict):
            all_keys.update(sample.keys())

    properties = {}
    required = []

    for key in all_keys:
        values = [s[key] for s in samples if isinstance(s, dict) and key in s]

        if values:
            # Infer type from first non-null value
            sample_value = next((v for v in values if v is not None), "")
            prop_schema = {"type": _infer_type(sample_value)}

            # Add format if detectable
            if isinstance(sample_value, str):
                if "@" in sample_value and "." in sample_value:
                    prop_schema["format"] = "email"

            # Check if all values match a pattern
            if all(isinstance(v, str) for v in values):
                try:
                    import re
                    pattern = re.compile(re.escape(values[0]))
                    for v in values[1:]:
                        if not pattern.match(v):
                            break
                    else:
                        prop_schema["pattern"] = re.escape(values[0])
                except:
                    pass

            properties[key] = prop_schema

            if strict or all(key in s for s in samples if isinstance(s, dict)):
                required.append(key)

    return {
        "type": "object",
        "properties": properties,
        "required": required if required else None,
    }


def _infer_type(value: Any) -> str:
    """Infer JSON schema type from a Python value."""
    if value is None:
        return "string"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "array"
    else:
        return "string"


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Validate data against JSON Schema")
    parser.add_argument("--input", "-i", required=True, help="Input data file (JSON)")
    parser.add_argument("--schema", "-s", required=True, help="Schema file (JSON)")
    parser.add_argument("--output", "-o", help="Output report file")
    parser.add_argument("--generate", "-g", action="store_true",
                        help="Generate schema from input")

    args = parser.parse_args()

    # Load data
    with open(args.input, "r") as f:
        data = json.load(f)

    if args.generate:
        if isinstance(data, list):
            samples = data[:10]  # Use first 10 samples
        else:
            samples = [data]
        schema = create_schema_from_sample(samples)
        print(json.dumps(schema, indent=2))
        sys.exit(0)

    # Validate
    with open(args.schema, "r") as f:
        schema = json.load(f)

    validator = DataValidator(schema=schema)
    result = validator.validate(data)

    if result.is_valid:
        print("✓ Data is valid")
        sys.exit(0)
    else:
        print("✗ Validation failed:")
        for error in result.errors:
            print(f"  {error.path}: {error.message}")
        sys.exit(1)
