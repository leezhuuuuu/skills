#!/usr/bin/env python3
"""
System Health Check Script

Source: Derived from anthropics/skills PR #151 (geepers agent system)

Monitor system health including CPU, memory, disk, and services.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class HealthCheckResult:
    """Result of a health check."""
    name: str
    status: str  # healthy, warning, critical, unknown
    message: str
    value: Optional[str] = None
    threshold: Optional[str] = None


@dataclass
class HealthReport:
    """Overall health report."""
    checks: List[HealthCheckResult] = field(default_factory=list)
    overall_status: str = "unknown"
    timestamp: str = ""

    def add_check(self, check: HealthCheckResult):
        self.checks.append(check)

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "overall": self.overall_status,
            "checks": [
                {
                    "name": c.name,
                    "status": c.status,
                    "message": c.message,
                    "value": c.value,
                    "threshold": c.threshold,
                }
                for c in self.checks
            ],
        }


class HealthChecker:
    """System health checker."""

    THRESHOLDS = {
        "cpu_warning": 70,
        "cpu_critical": 85,
        "memory_warning": 75,
        "memory_critical": 90,
        "disk_warning": 80,
        "disk_critical": 95,
    }

    def __init__(self, custom_thresholds: Dict[str, int] = None):
        self.thresholds = {**self.THRESHOLDS, **(custom_thresholds or {})}

    def check_cpu(self) -> HealthCheckResult:
        """Check CPU usage."""
        try:
            # Try to get CPU usage from psutil or top
            usage = self._get_cpu_usage()
            if usage is None:
                return HealthCheckResult(
                    name="cpu", status="unknown", message="Unable to read CPU usage"
                )

            if usage < self.thresholds["cpu_warning"]:
                return HealthCheckResult(
                    name="cpu",
                    status="healthy",
                    message="CPU usage is normal",
                    value=f"{usage}%",
                    threshold=f"<{self.thresholds['cpu_warning']}%",
                )
            elif usage < self.thresholds["cpu_critical"]:
                return HealthCheckResult(
                    name="cpu",
                    status="warning",
                    message="CPU usage is elevated",
                    value=f"{usage}%",
                    threshold=f">{self.thresholds['cpu_warning']}%",
                )
            else:
                return HealthCheckResult(
                    name="cpu",
                    status="critical",
                    message="CPU usage is critical",
                    value=f"{usage}%",
                    threshold=f">{self.thresholds['cpu_critical']}%",
                )
        except Exception as e:
            return HealthCheckResult(
                name="cpu", status="unknown", message=f"Error: {str(e)}"
            )

    def _get_cpu_usage(self) -> Optional[float]:
        """Get CPU usage percentage."""
        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except ImportError:
            pass

        # Fallback: parse /proc/stat
        try:
            with open("/proc/stat", "r") as f:
                line = f.readline()
            idle = int(line.split()[4])
            total = sum(int(x) for x in line.split()[1:5])
            usage = 100 - (idle / total * 100)
            return round(usage, 1)
        except:
            return None

    def check_memory(self) -> HealthCheckResult:
        """Check memory usage."""
        try:
            import psutil
            mem = psutil.virtual_memory()
            usage = mem.percent

            if usage < self.thresholds["memory_warning"]:
                return HealthCheckResult(
                    name="memory",
                    status="healthy",
                    message="Memory usage is normal",
                    value=f"{usage}%",
                    threshold=f"<{self.thresholds['memory_warning']}%",
                )
            elif usage < self.thresholds["memory_critical"]:
                return HealthCheckResult(
                    name="memory",
                    status="warning",
                    message="Memory usage is elevated",
                    value=f"{usage}%",
                    threshold=f">{self.thresholds['memory_warning']}%",
                )
            else:
                return HealthCheckResult(
                    name="memory",
                    status="critical",
                    message="Memory usage is critical",
                    value=f"{usage}%",
                    threshold=f">{self.thresholds['memory_critical']}%",
                )
        except ImportError:
            return HealthCheckResult(
                name="memory", status="unknown", message="psutil not installed"
            )
        except Exception as e:
            return HealthCheckResult(
                name="memory", status="unknown", message=f"Error: {str(e)}"
            )

    def check_disk(self, path: str = "/") -> HealthCheckResult:
        """Check disk usage."""
        try:
            usage = shutil.disk_usage(path)
            percent = (usage.used / usage.total) * 100

            if percent < self.thresholds["disk_warning"]:
                return HealthCheckResult(
                    name="disk",
                    status="healthy",
                    message="Disk usage is normal",
                    value=f"{percent:.1f}%",
                    threshold=f"<{self.thresholds['disk_warning']}%",
                )
            elif percent < self.thresholds["disk_critical"]:
                return HealthCheckResult(
                    name="disk",
                    status="warning",
                    message="Disk usage is elevated",
                    value=f"{percent:.1f}%",
                    threshold=f">{self.thresholds['disk_warning']}%",
                )
            else:
                return HealthCheckResult(
                    name="disk",
                    status="critical",
                    message="Disk usage is critical",
                    value=f"{percent:.1f}%",
                    threshold=f">{self.thresholds['disk_critical']}%",
                )
        except Exception as e:
            return HealthCheckResult(
                name="disk", status="unknown", message=f"Error: {str(e)}"
            )

    def check_caddy(self) -> HealthCheckResult:
        """Check Caddy web server status."""
        try:
            # Check if caddy process is running
            result = subprocess.run(
                ["pgrep", "-x", "caddy"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return HealthCheckResult(
                    name="caddy",
                    status="healthy",
                    message="Caddy server is running",
                )
            else:
                return HealthCheckResult(
                    name="caddy",
                    status="critical",
                    message="Caddy server is not running",
                )
        except subprocess.TimeoutExpired:
            return HealthCheckResult(
                name="caddy", status="unknown", message="Check timed out"
            )
        except FileNotFoundError:
            return HealthCheckResult(
                name="caddy", status="unknown", message="pgrep not available"
            )
        except Exception as e:
            return HealthCheckResult(
                name="caddy", status="unknown", message=f"Error: {str(e)}"
            )

    def check_service(self, service_name: str) -> HealthCheckResult:
        """Check a system service using systemctl."""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip() == "active":
                return HealthCheckResult(
                    name=service_name,
                    status="healthy",
                    message=f"Service {service_name} is running",
                )
            else:
                status = result.stdout.strip() or "unknown"
                return HealthCheckResult(
                    name=service_name,
                    status="critical",
                    message=f"Service {service_name} is {status}",
                )
        except FileNotFoundError:
            return HealthCheckResult(
                name=service_name, status="unknown", message="systemctl not available"
            )
        except Exception as e:
            return HealthCheckResult(
                name=service_name, status="unknown", message=f"Error: {str(e)}"
            )

    def run_all_checks(self) -> HealthReport:
        """Run all health checks."""
        from datetime import datetime

        report = HealthReport()
        report.timestamp = datetime.now().isoformat()

        report.add_check(self.check_cpu())
        report.add_check(self.check_memory())
        report.add_check(self.check_disk())
        report.add_check(self.check_caddy())

        # Determine overall status
        statuses = [c.status for c in report.checks]
        if "critical" in statuses:
            report.overall_status = "critical"
        elif "warning" in statuses:
            report.overall_status = "warning"
        elif all(s == "healthy" for s in statuses):
            report.overall_status = "healthy"
        else:
            report.overall_status = "unknown"

        return report


def format_report(report: HealthReport, format_type: str = "text") -> str:
    """Format health report for display."""
    if format_type == "json":
        return json.dumps(report.to_dict(), indent=2)

    lines = ["=== System Health Check ===", ""]

    for check in report.checks:
        status_icon = {
            "healthy": "✓",
            "warning": "!",
            "critical": "✗",
            "unknown": "?",
        }.get(check.status, "?")

        lines.append(f"{check.name.upper()}: {check.value or 'N/A'} {status_icon}")

        if check.message:
            lines.append(f"  {check.message}")

        if check.threshold:
            lines.append(f"  Threshold: {check.threshold}")

    lines.append("")
    status_messages = {
        "healthy": "Overall: HEALTHY",
        "warning": "Overall: WARNING - Some checks need attention",
        "critical": "Overall: CRITICAL - Immediate action required",
        "unknown": "Overall: UNKNOWN - Unable to determine status",
    }
    lines.append(status_messages.get(report.overall_status, ""))

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="System health check")
    parser.add_argument("--cpu", action="store_true", help="Check CPU only")
    parser.add_argument("--memory", action="store_true", help="Check memory only")
    parser.add_argument("--disk", action="store_true", help="Check disk only")
    parser.add_argument("--caddy", action="store_true", help="Check Caddy only")
    parser.add_argument("--service", metavar="NAME", help="Check specific service")
    parser.add_argument("--all", action="store_true", default=True, help="Run all checks")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--threshold", type=int, help="Custom warning threshold percentage"
    )

    args = parser.parse_args()

    checker = HealthChecker()
    report = HealthReport()

    if args.cpu:
        report.add_check(checker.check_cpu())
    elif args.memory:
        report.add_check(checker.check_memory())
    elif args.disk:
        report.add_check(checker.check_disk())
    elif args.caddy:
        report.add_check(checker.check_caddy())
    elif args.service:
        report.add_check(checker.check_service(args.service))
    else:
        report = checker.run_all_checks()

    print(format_report(report, "json" if args.json else "text"))

    # Exit code based on status
    if report.overall_status == "critical":
        sys.exit(2)
    elif report.overall_status == "warning":
        sys.exit(1)
