#!/usr/bin/env python3
"""
Code linting module for quality analysis.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import ast
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class LintIssue:
    """Represents a linting issue."""
    file: str
    line: int
    column: int
    rule_id: str
    severity: str  # error, warning, info
    message: str
    code: str = ""


@dataclass
class LintReport:
    """Summary of linting results."""
    total_files: int = 0
    total_issues: int = 0
    issues_by_severity: Dict[str, int] = field(default_factory=dict)
    issues_by_rule: Dict[str, int] = field(default_factory=dict)
    issues: List[LintIssue] = field(default_factory=list)

    def add_issue(self, issue: LintIssue):
        self.issues.append(issue)
        self.total_issues += 1
        self.issues_by_severity[issue.severity] = self.issues_by_severity.get(issue.severity, 0) + 1
        self.issues_by_rule[issue.rule_id] = self.issues_by_rule.get(issue.rule_id, 0) + 1


class PythonLinter:
    """Python code linter with security and best practices checks."""

    # Security patterns (high severity)
    SECURITY_PATTERNS = [
        (r"(password|secret|api_key|auth_token)\s*=\s*['\"][^'\"]+['\"]", "security", "Hardcoded credential found"),
        (r"os\.system\s*\(", "security", "os.system() call - potential command injection"),
        (r"eval\s*\(", "security", "eval() call - potential code injection"),
        (r"exec\s*\(", "security", "exec() call - potential code injection"),
        (r"pickle\.load\s*\(", "security", "pickle.load() - unsafe deserialization"),
        (r"YAML\.load\s*\([^)]without\s+Loader", "security", "YAML load without safe Loader"),
        (r"sqlalchemy\.text\s*\([^)]%\s*", "security", "SQL injection vulnerability - use parameterized queries"),
        (r"'.*%s.*'.*%", "security", "String formatting with % operator - potential injection"),
        (r"format\s*\(.*\{.*\}", "security", "str.format() without safe filtering"),
    ]

    # Best practice patterns (warning severity)
    PRACTICE_PATTERNS = [
        (r"print\s*\(", "best-practice", "Use logging instead of print()"),
        (r"pass\s*#\s*todo", "best-practice", "TODO comment found - complete the implementation"),
        (r"except\s*:\s*$", "best-practice", "Bare except clause - catch specific exceptions"),
        (r"import\s+\*\s*$", "best-practice", "Avoid wildcard imports"),
        (r"\.append\s*\(\s*\)", "best-practice", "Consider list comprehension over repeated append"),
        (r"for\s+.*\s+in\s+range\s*\(\s*len\s*\(", "best-practice", "Use enumerate() instead of range(len())"),
        (r"==\s*(True|False|None)\s*$", "best-practice", "Use 'is' for identity comparisons"),
    ]

    # Basic patterns (info severity)
    BASIC_PATTERNS = [
        (r"\s+$", "basic", "Trailing whitespace"),
        (r"\t", "basic", "Tab character used - use spaces"),
        (r"^#{1,5}\s*$", "basic", "Empty comment line"),
        (r"if\s+__name__\s*==\s*['\"]__main__['\"]:", "basic", "Main guard present"),
    ]

    def __init__(self, rules: List[str] = None, exclude_patterns: List[str] = None):
        """
        Initialize the linter.

        Args:
            rules: Rule sets to apply (basic, security, best-practices, performance)
            exclude_patterns: Patterns of files to exclude
        """
        self.rules = rules or ["basic", "security", "best-practices"]
        self.exclude_patterns = exclude_patterns or []

    def should_exclude(self, file_path: str) -> bool:
        """Check if file should be excluded."""
        for pattern in self.exclude_patterns:
            if pattern.replace("*", "") in file_path:
                return True
        return False

    def lint_file(self, file_path: str) -> List[LintIssue]:
        """Lint a single Python file."""
        issues = []

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")

        # AST-based checks
        try:
            tree = ast.parse(content)
            issues.extend(self._check_ast(tree, file_path, lines))
        except SyntaxError as e:
            issues.append(LintIssue(
                file=file_path,
                line=e.lineno or 1,
                column=e.offset or 0,
                rule_id="syntax-error",
                severity="error",
                message=f"Syntax error: {e.msg}",
                code=content.split("\n")[min(e.lineno - 1, len(content.split("\n")) - 1)].strip()
            ))
            return issues

        # Pattern-based checks
        if "security" in self.rules:
            issues.extend(self._check_patterns(file_path, lines, self.SECURITY_PATTERNS, "security"))

        if "best-practices" in self.rules:
            issues.extend(self._check_patterns(file_path, lines, self.PRACTICE_PATTERNS, "warning"))

        if "basic" in self.rules:
            issues.extend(self._check_patterns(file_path, lines, self.BASIC_PATTERNS, "info"))

        return issues

    def _check_ast(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[LintIssue]:
        """Check code using AST analysis."""
        issues = []
        complex_functions = []

        for node in ast.walk(tree):
            # Check for complex functions
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > 10:
                    issues.append(LintIssue(
                        file=file_path,
                        line=node.lineno,
                        column=0,
                        rule_id="complexity",
                        severity="warning",
                        message=f"Function '{node.name}' has complexity {complexity} (> 10)",
                    ))

                if len(node.args.args) > 5:
                    issues.append(LintIssue(
                        file=file_path,
                        line=node.lineno,
                        column=0,
                        rule_id="too-many-args",
                        severity="warning",
                        message=f"Function '{node.name}' has {len(node.args.args)} parameters (> 5)",
                    ))

            # Check for long functions
            if isinstance(node, ast.FunctionDef):
                func_end = node.end_lineno or node.lineno
                if func_end - node.lineno > 50:
                    issues.append(LintIssue(
                        file=file_path,
                        line=node.lineno,
                        column=0,
                        rule_id="long-function",
                        severity="info",
                        message=f"Function '{node.name}' is {func_end - node.lineno} lines (> 50)",
                    ))

        return issues

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Assert, ast.BoolOp)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.FunctionDef):
                complexity += 1  # Nested function
        return complexity

    def _check_patterns(
        self,
        file_path: str,
        lines: List[str],
        patterns: List[Tuple[str, str, str]],
        default_severity: str
    ) -> List[LintIssue]:
        """Check code for patterns."""
        issues = []

        for line_num, line in enumerate(lines, 1):
            for pattern, rule_id, message in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(LintIssue(
                        file=file_path,
                        line=line_num,
                        column=0,
                        rule_id=rule_id,
                        severity=default_severity,
                        message=message,
                        code=line.strip()
                    ))

        return issues

    def lint_directory(self, path: str, recursive: bool = True) -> LintReport:
        """Lint all Python files in a directory."""
        report = LintReport()
        path_obj = Path(path)

        if path_obj.is_file() and path_obj.suffix == ".py":
            files = [path_obj]
        else:
            pattern = "**/*.py" if recursive else "*.py"
            files = list(path_obj.glob(pattern))

        report.total_files = len(files)

        for file_path in files:
            if not self.should_exclude(str(file_path)):
                issues = self.lint_file(str(file_path))
                for issue in issues:
                    issue.file = str(file_path.relative_to(path_obj))
                report.issues.extend(issues)

        return report


class CodeLinter:
    """Multi-language code linter wrapper."""

    def __init__(self, rules: List[str] = None, exclude_patterns: List[str] = None):
        self.linters = {
            ".py": PythonLinter(rules, exclude_patterns),
        }
        self.rules = rules or ["basic"]
        self.exclude_patterns = exclude_patterns or []

    def analyze(self, path: str, recursive: bool = True) -> LintReport:
        """Analyze code at the given path."""
        path_obj = Path(path)

        if path_obj.is_file():
            suffix = path_obj.suffix
            if suffix in self.linters:
                issues = self.linters[suffix].lint_file(str(path_obj))
                report = LintReport(total_files=1, issues=issues)
            else:
                report = LintReport(total_files=1)
        else:
            report = LintReport()
            for suffix, linter in self.linters.items():
                linter = type(linter)(self.rules, self.exclude_patterns)
                sub_report = linter.lint_directory(path, recursive)
                report.total_files += sub_report.total_files
                report.issues.extend(sub_report.issues)

        return report


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Lint code for quality issues")
    parser.add_argument("path", help="File or directory to lint")
    parser.add_argument("--rules", nargs="+",
                        choices=["basic", "security", "best-practices", "performance"],
                        default=["basic", "security", "best-practices"],
                        help="Rule sets to apply")
    parser.add_argument("--exclude", nargs="+", help="Patterns to exclude")
    parser.add_argument("--recursive", "-r", action="store_true", default=True)
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    linter = CodeLinter(rules=args.rules, exclude_patterns=args.exclude)
    report = linter.analyze(args.path, recursive=args.recursive)

    if args.json:
        import json
        output = {
            "total_files": report.total_files,
            "total_issues": report.total_issues,
            "by_severity": report.issues_by_severity,
            "by_rule": report.issues_by_rule,
            "issues": [
                {
                    "file": i.file,
                    "line": i.line,
                    "rule": i.rule_id,
                    "severity": i.severity,
                    "message": i.message,
                }
                for i in report.issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Files analyzed: {report.total_files}")
        print(f"Total issues: {report.total_issues}")
        print(f"  Errors: {report.issues_by_severity.get('error', 0)}")
        print(f"  Warnings: {report.issues_by_severity.get('warning', 0)}")
        print(f"  Info: {report.issues_by_severity.get('info', 0)}")
        print()

        for issue in report.issues[:50]:  # Show first 50 issues
            print(f"[{issue.severity.upper():5}] {issue.file}:{issue.line} {issue.message}")
            if issue.code:
                print(f"           {issue.code[:60]}")

        if len(report.issues) > 50:
            print(f"\n... and {len(report.issues) - 50} more issues")

    sys.exit(1 if report.issues_by_severity.get("error", 0) > 0 else 0)
