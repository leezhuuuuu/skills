#!/usr/bin/env python3
"""
Test generation module for unit tests.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import ast
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class TestCase:
    """Represents a generated test case."""
    name: str
    function: str
    params: Dict[str, str]
    assertions: List[str]
    setup_code: str = ""
    teardown_code: str = ""


@dataclass
class TestFile:
    """Represents a generated test file."""
    path: str
    imports: List[str]
    fixtures: List[str]
    test_cases: List[TestCase]
    content: str = ""


class PythonTestGenerator:
    """Generate Python unit tests from source code."""

    FRAMEWORK_TEMPLATES = {
        "pytest": {
            "import": "import pytest",
            "fixture": '''
@pytest.fixture
def {fixture_name}():
    """Fixture for {fixture_name}."""
    {setup}
    yield {yield_val}
    {teardown}
''',
            "test": '''
def test_{function_name}_{test_id}():
    """Test {test_docstring}."""
{setup_code}
    result = {function_call}
{assertions}
''',
        },
        "unittest": {
            "import": "import unittest",
            "fixture": "",  # unittest uses setUp/tearDown
            "test": '''
class Test{class_name}(unittest.TestCase):
    def setUp(self):
{setup_code}

    def test_{function_name}_{test_id}(self):
{more_setup}        result = {function_call}
{assertions}

    def tearDown(self):
{teardown_code}
''',
        },
    }

    def __init__(self, framework: str = "pytest", coverage_target: int = 80):
        """
        Initialize the test generator.

        Args:
            framework: Test framework (pytest, unittest)
            coverage_target: Target test coverage percentage
        """
        self.framework = framework
        self.coverage_target = coverage_target
        self.templates = self.FRAMEWORK_TEMPLATES[framework]

    def parse_module(self, file_path: str) -> Dict:
        """Parse a Python module to extract functions and classes."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {"error": "Could not parse file"}

        module_info = {
            "file_path": file_path,
            "classes": [],
            "functions": [],
            "imports": [],
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_info["imports"].append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    module_info["imports"].append(f"from {module} import {alias.name}")
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods": [],
                    "docstring": ast.get_docstring(node) or "",
                }
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                        class_info["methods"].append({
                            "name": item.name,
                            "docstring": ast.get_docstring(item) or "",
                            "args": [arg.arg for arg in item.args.args],
                            "returns": self._get_return_type(item),
                        })
                module_info["classes"].append(class_info)
            elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                module_info["functions"].append({
                    "name": node.name,
                    "docstring": ast.get_docstring(node) or "",
                    "args": [arg.arg for arg in node.args.args],
                    "returns": self._get_return_type(node),
                })

        return module_info

    def _get_return_type(self, node: ast.FunctionDef) -> str:
        """Extract return type annotation from function."""
        if node.returns:
            if isinstance(node.returns, ast.Name):
                return node.returns.id
            elif isinstance(node.returns, ast.Constant):
                return str(node.returns.value)
        return "Any"

    def generate_tests(self, file_path: str) -> TestFile:
        """Generate tests for a Python module."""
        module_info = self.parse_module(file_path)

        if "error" in module_info:
            return TestFile(
                path="",
                imports=[],
                fixtures=[],
                test_cases=[],
                content=f"# Error: {module_info['error']}"
            )

        # Determine module name
        module_name = Path(file_path).stem
        test_module_name = f"test_{module_name}"

        # Build imports
        imports = ["# Auto-generated tests"]
        if self.framework == "pytest":
            imports.append("import pytest")
        imports.append(f"import {module_name}")

        # Generate test cases
        test_cases = []

        # Test functions
        for func in module_info["functions"]:
            test_cases.extend(self._generate_function_tests(func, module_name))

        # Test class methods
        for cls in module_info["classes"]:
            for method in cls["methods"]:
                test_cases.extend(self._generate_method_tests(cls, method, module_name))

        # Generate fixtures
        fixtures = []
        if self.framework == "pytest":
            # Create a fixture for the module
            fixtures.append({
                "name": f"{module_name}_instance",
                "setup": f"{module_name}()",
                "yield_val": "instance",
            })

        # Generate test file content
        content = self._render_test_file(test_module_name, imports, fixtures, test_cases)

        return TestFile(
            path=f"test_{module_name}.py",
            imports=imports,
            fixtures=fixtures,
            test_cases=test_cases,
            content=content,
        )

    def _generate_function_tests(self, func: Dict, module_name: str) -> List[TestCase]:
        """Generate test cases for a function."""
        tests = []

        # Basic functionality test
        args = func["args"]
        if not args:
            test = TestCase(
                name=f"test_{func['name']}_basic",
                function=func["name"],
                params={},
                assertions=[
                    f"assert result is not None",
                ],
                setup_code=f"# Testing {module_name}.{func['name']}()",
            )
            tests.append(test)

        # Test with sample arguments
        if args:
            arg_values = self._generate_sample_args(func["args"])
            param_str = ", ".join(f"{k}={v}" for k, v in arg_values.items())

            test = TestCase(
                name=f"test_{func['name']}_with_args",
                function=func["name"],
                params=arg_values,
                assertions=[
                    f"assert result is not None",
                ],
                setup_code=f"# Testing {module_name}.{func['name']}({param_str})",
            )
            tests.append(test)

        # Edge case tests
        for i, arg in enumerate(args):
            edge_cases = self._generate_edge_cases(arg, i)
            for case_name, case_value in edge_cases.items():
                test = TestCase(
                    name=f"test_{func['name']}_{case_name}",
                    function=func["name"],
                    params={arg: case_value},
                    assertions=[
                        f"assert result is not None",
                    ],
                )
                tests.append(test)

        return tests

    def _generate_method_tests(self, cls: Dict, method: Dict, module_name: str) -> List[TestCase]:
        """Generate test cases for a class method."""
        tests = []
        class_name = cls["name"]
        method_name = method["name"]

        if not method["args"]:
            test = TestCase(
                name=f"test_{class_name}_{method_name}_basic",
                function=f"{class_name}().{method_name}",
                params={},
                assertions=["assert result is not None"],
            )
            tests.append(test)

        return tests

    def _generate_sample_args(self, args: List[str]) -> Dict[str, str]:
        """Generate sample arguments for testing."""
        samples = {}
        for arg in args:
            if arg in ("self", "cls"):
                continue
            samples[arg] = self._sample_for_arg(arg)
        return samples

    def _sample_for_arg(self, arg_name: str) -> str:
        """Generate a sample value for an argument."""
        name_lower = arg_name.lower()

        if "name" in name_lower or "string" in name_lower:
            return f'"{arg_name}_test"'
        elif "count" in name_lower or "num" in name_lower or "id" in name_lower:
            return "1"
        elif "flag" in name_lower or "is_" in name_lower or "enabled" in name_lower:
            return "True"
        elif "list" in name_lower:
            return "[]"
        elif "dict" in name_lower or "data" in name_lower:
            return "{}"
        elif "value" in name_lower or "amount" in name_lower:
            return "0"
        else:
            return "None"

    def _generate_edge_cases(self, arg: str, index: int) -> Dict[str, str]:
        """Generate edge case values for an argument."""
        cases = {}

        if arg in ("self", "cls"):
            return cases

        cases[f"{arg}_empty"] = '""' if "name" in arg.lower() else "None"
        cases[f"{arg}_zero"] = "0"
        cases[f"{arg}_negative"] = "-1"

        return cases

    def _render_test_file(
        self,
        module_name: str,
        imports: List[str],
        fixtures: List[Dict],
        test_cases: List[TestCase]
    ) -> str:
        """Render the complete test file content."""
        lines = []

        # Imports
        for imp in imports:
            lines.append(imp)
        lines.append("")

        # Fixtures (pytest only)
        if self.framework == "pytest" and fixtures:
            for fixture in fixtures:
                lines.append(self.templates["fixture"].format(
                    fixture_name=fixture["name"],
                    setup=f"{fixture['setup']};",
                    yield_val=fixture["yield_val"],
                    teardown=""
                ))
            lines.append("")

        # Test cases
        for test in test_cases:
            lines.append(self.templates["test"].format(
                function_name=test.function,
                test_id=test.name.split("_")[-1],
                test_docstring=test.name.replace("_", " "),
                setup_code=test.setup_code,
                more_setup="    " * 4 if self.framework == "unittest" else "    ",
                function_call=f"{test.function}({', '.join(f'{k}={v}' for k, v in test.params.items())})" if test.params else f"{test.function}()",
                assertions="\n".join(f"    assert {a}" for a in test.assertions),
                class_name=module_name.title().replace("_", ""),
            ))
            lines.append("")

        return "\n".join(lines)

    def generate(self, file_path: str) -> TestFile:
        """Generate tests for a Python file."""
        return self.generate_tests(file_path)

    def save(self, test_file: TestFile, output_path: str = None):
        """Save generated tests to a file."""
        path = output_path or test_file.path
        with open(path, "w", encoding="utf-8") as f:
            f.write(test_file.content)
        print(f"Tests saved to {path}")


class TestGenerator:
    """Multi-language test generator wrapper."""

    GENERATORS = {
        ".py": PythonTestGenerator,
    }

    def __init__(
        self,
        framework: str = "pytest",
        coverage_target: int = 80,
        mock_external: bool = True,
    ):
        """
        Initialize the test generator.

        Args:
            framework: Test framework to generate for
            coverage_target: Target coverage percentage
            mock_external: Whether to mock external dependencies
        """
        self.framework = framework
        self.coverage_target = coverage_target
        self.mock_external = mock_external

    def generate(self, file_path: str) -> TestFile:
        """Generate tests for a source file."""
        suffix = Path(file_path).suffix

        if suffix not in self.GENERATORS:
            raise ValueError(f"No test generator for file type: {suffix}")

        generator_class = self.GENERATORS[suffix]
        generator = generator_class(framework=self.framework, coverage_target=self.coverage_target)

        return generator.generate(file_path)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Generate unit tests")
    parser.add_argument("path", help="Source file or directory to generate tests for")
    parser.add_argument("--framework", "-f", default="pytest",
                        choices=["pytest", "unittest"],
                        help="Test framework")
    parser.add_argument("--coverage", "-c", type=int, default=80,
                        help="Target coverage percentage")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--json", action="store_true",
                        help="Output test info as JSON")

    args = parser.parse_args()

    generator = TestGenerator(
        framework=args.framework,
        coverage_target=args.coverage,
    )

    if os.path.isfile(args.path):
        test_file = generator.generate(args.path)

        if args.json:
            output = {
                "path": test_file.path,
                "imports": test_file.imports,
                "test_count": len(test_file.test_cases),
                "fixtures": len(test_file.fixtures),
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"Generated {len(test_file.test_cases)} tests in {test_file.path}")
            print("\nPreview:")
            print(test_file.content[:500])

        if args.output or not args.json:
            generator.save(test_file, args.output)
    else:
        print("Generating tests for directory not yet supported")
