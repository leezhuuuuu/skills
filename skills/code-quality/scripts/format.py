#!/usr/bin/env python3
"""
Code formatting module for consistent style.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class FormatChange:
    """Represents a formatting change."""
    file: str
    line: int
    old_line: str
    new_line: str
    change_type: str  # indent, whitespace, line_ending


@dataclass
class FormatReport:
    """Summary of formatting changes."""
    total_files: int = 0
    files_changed: int = 0
    total_changes: int = 0
    changes: List[FormatChange] = field(default_factory=list)


class PythonFormatter:
    """Python code formatter with PEP 8 support."""

    def __init__(
        self,
        indent_size: int = 4,
        line_length: int = 100,
        remove_trailing: bool = True,
        ensure_newline: bool = True,
    ):
        """
        Initialize the formatter.

        Args:
            indent_size: Spaces per indent level
            line_length: Maximum line length
            remove_trailing: Remove trailing whitespace
            ensure_newline: Ensure newline at EOF
        """
        self.indent_size = indent_size
        self.line_length = line_length
        self.remove_trailing = remove_trailing
        self.ensure_newline = ensure_newline

    def format_file(self, file_path: str, fix: bool = False) -> Tuple[str, List[FormatChange]]:
        """Format a single Python file."""
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()

        changes = []
        lines = original.split("\n")
        new_lines = []

        for i, line in enumerate(lines):
            new_line = line

            # Remove trailing whitespace
            if self.remove_trailing:
                stripped = line.rstrip()
                if stripped != line:
                    changes.append(FormatChange(
                        file=file_path,
                        line=i + 1,
                        old_line=line,
                        new_line=stripped,
                        change_type="whitespace"
                    ))
                    new_line = stripped

            new_lines.append(new_line)

        # Ensure newline at EOF
        if self.ensure_newline and new_lines:
            if new_lines[-1] != "":
                # Check if original had trailing newline
                if original.endswith("\n") or original.split("\n")[-1] != "":
                    changes.append(FormatChange(
                        file=file_path,
                        line=len(lines),
                        old_line=new_lines[-1],
                        new_line="",
                        change_type="line_ending"
                    ))
                    new_lines[-1] = ""

        new_content = "\n".join(new_lines)

        if fix and new_content != original:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

        return file_path, changes

    def format_directory(
        self,
        path: str,
        fix: bool = False,
        recursive: bool = True
    ) -> FormatReport:
        """Format all Python files in a directory."""
        report = FormatReport()
        path_obj = Path(path)

        if path_obj.is_file() and path_obj.suffix == ".py":
            files = [path_obj]
        else:
            pattern = "**/*.py" if recursive else "*.py"
            files = list(path_obj.glob(pattern))

        report.total_files = len(files)

        for file_path in files:
            _, changes = self.format_file(str(file_path), fix=fix)
            for change in changes:
                change.file = str(file_path.relative_to(path_obj))
            report.changes.extend(changes)

        if changes:
            report.files_changed = len(set(c.file for c in report.changes))
        report.total_changes = len(report.changes)

        return report


class JavaScriptFormatter:
    """JavaScript code formatter."""

    def __init__(self, indent_size: int = 2, line_length: int = 100):
        self.indent_size = indent_size
        self.line_length = line_length

    def format_file(self, file_path: str, fix: bool = False) -> Tuple[str, List[FormatChange]]:
        """Format a single JavaScript file."""
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()

        changes = []
        lines = original.split("\n")
        new_lines = []
        indent_level = 0
        in_string = False
        string_char = None

        for i, line in enumerate(lines):
            new_line = line
            original_line = line

            # Track brace indentation
            stripped = line.strip()

            # Count braces (not in strings)
            j = 0
            while j < len(line):
                char = line[j]
                if char in ('"', "'") and (j == 0 or line[j-1] != '\\'):
                    in_string = not in_string
                    string_char = char if in_string else None
                elif not in_string:
                    if char == '{':
                        indent_level += 1
                    elif char == '}':
                        indent_level = max(0, indent_level - 1)

                j += 1

            # Remove trailing whitespace
            stripped_line = line.rstrip()
            if stripped_line != line:
                changes.append(FormatChange(
                    file=file_path,
                    line=i + 1,
                    old_line=line,
                    new_line=stripped_line,
                    change_type="whitespace"
                ))
                new_line = stripped_line

            new_lines.append(new_line)

        new_content = "\n".join(new_lines)

        if fix and new_content != original:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

        return file_path, changes

    def format_directory(self, path: str, fix: bool = False, recursive: bool = True) -> FormatReport:
        """Format all JavaScript files in a directory."""
        report = FormatReport()
        path_obj = Path(path)

        pattern = "**/*.js" if recursive else "*.js"
        files = list(path_obj.glob(pattern))
        report.total_files = len(files)

        for file_path in files:
            _, changes = self.format_file(str(file_path), fix=fix)
            for change in changes:
                change.file = str(file_path.relative_to(path_obj))
            report.changes.extend(changes)

        if changes:
            report.files_changed = len(set(c.file for c in report.changes))
        report.total_changes = len(report.changes)

        return report


class CodeFormatter:
    """Multi-language code formatter wrapper."""

    FORMATTERS = {
        ".py": PythonFormatter,
        ".js": JavaScriptFormatter,
        ".jsx": JavaScriptFormatter,
        ".ts": JavaScriptFormatter,
        ".tsx": JavaScriptFormatter,
    }

    def __init__(
        self,
        style: str = "pep8",
        line_length: int = 100,
        indent_size: int = None,
        fix: bool = False,
    ):
        """
        Initialize the formatter.

        Args:
            style: Code style (pep8, google, django)
            line_length: Maximum line length
            indent_size: Spaces per indent
            fix: Whether to apply fixes
        """
        self.style = style
        self.line_length = line_length
        self.indent_size = indent_size or (2 if style in ["js", "javascript"] else 4)
        self.fix = fix

    def format(self, path: str, recursive: bool = True) -> FormatReport:
        """Format code at the given path."""
        path_obj = Path(path)

        if path_obj.is_file():
            suffix = path_obj.suffix
            if suffix in self.FORMATTERS:
                formatter = self.FORMATTERS[suffix](
                    indent_size=self.indent_size,
                    line_length=self.line_length
                )
                return formatter.format_directory(str(path_obj), fix=self.fix, recursive=False)
            else:
                return FormatReport(total_files=1)
        else:
            report = FormatReport()
            for suffix, formatter_class in self.FORMATTERS.items():
                formatter = formatter_class(
                    indent_size=self.indent_size,
                    line_length=self.line_length
                )
                sub_report = formatter.format_directory(path, fix=self.fix, recursive=recursive)
                report.total_files += sub_report.total_files
                report.changes.extend(sub_report.changes)

            if report.changes:
                report.files_changed = len(set(c.file for c in report.changes))
            report.total_changes = len(report.changes)

            return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Format code for consistent style")
    parser.add_argument("path", help="File or directory to format")
    parser.add_argument("--style", "-s", default="pep8",
                        choices=["pep8", "google", "django", "js"],
                        help="Code style")
    parser.add_argument("--line-length", "-l", type=int, default=100)
    parser.add_argument("--indent", "-i", type=int,
                        help="Indent size (default: 2 for JS, 4 for Python)")
    parser.add_argument("--fix", "-f", action="store_true",
                        help="Apply formatting changes")
    parser.add_argument("--no-recursive", "-n", action="store_true",
                        help="Don't recursively process subdirectories")

    args = parser.parse_args()

    formatter = CodeFormatter(
        style=args.style,
        line_length=args.line_length,
        indent_size=args.indent,
        fix=args.fix
    )

    report = formatter.format(args.path, recursive=not args.no_recursive)

    print(f"Files processed: {report.total_files}")
    print(f"Files changed: {report.files_changed}")
    print(f"Total changes: {report.total_changes}")

    if report.changes and args.fix:
        print("\nChanges applied:")
        for change in report.changes[:20]:
            print(f"  {change.file}:{change.line} - {change.change_type}")

        if len(report.changes) > 20:
            print(f"  ... and {len(report.changes) - 20} more")
