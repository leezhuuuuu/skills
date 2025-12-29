#!/usr/bin/env python3
"""
Service Manager Script

Source: Derived from anthropics/skills PR #151 (geepers agent system)

Manage system services using systemctl.
"""

import argparse
import json
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ServiceInfo:
    """Information about a system service."""
    name: str
    display_name: str
    status: str  # active, inactive, failed, unknown
    enabled: bool
    running: bool


class ServiceManager:
    """Manage system services."""

    def __init__(self):
        self.services: Dict[str, ServiceInfo] = {}

    def get_service_status(self, service_name: str) -> ServiceInfo:
        """Get status of a single service."""
        try:
            # Check if service exists
            result = subprocess.run(
                ["systemctl", "status", service_name],
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Check active status
            active_result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,
                text=True,
                timeout=5,
            )
            status = active_result.stdout.strip()

            # Check enabled status
            enabled_result = subprocess.run(
                ["systemctl", "is-enabled", service_name],
                capture_output=True,
                text=True,
                timeout=5,
            )
            enabled = enabled_result.stdout.strip() == "enabled"

            return ServiceInfo(
                name=service_name,
                display_name=service_name,
                status=status if status in ["active", "inactive", "failed"] else "unknown",
                enabled=enabled,
                running=status == "active",
            )
        except subprocess.TimeoutExpired:
            return ServiceInfo(
                name=service_name,
                display_name=service_name,
                status="unknown",
                enabled=False,
                running=False,
            )
        except FileNotFoundError:
            return ServiceInfo(
                name=service_name,
                display_name=service_name,
                status="unknown",
                enabled=False,
                running=False,
            )
        except Exception:
            return ServiceInfo(
                name=service_name,
                display_name=service_name,
                status="unknown",
                enabled=False,
                running=False,
            )

    def list_services(self) -> List[ServiceInfo]:
        """List status of common services."""
        common_services = [
            "caddy",
            "postgresql",
            "nginx",
            "docker",
            "ssh",
            "cron",
        ]

        services = []
        for name in common_services:
            info = self.get_service_status(name)
            services.append(info)

        return services

    def start_service(self, service_name: str) -> bool:
        """Start a service."""
        try:
            result = subprocess.run(
                ["sudo", "systemctl", "start", service_name],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
        except Exception:
            return False

    def stop_service(self, service_name: str) -> bool:
        """Stop a service."""
        try:
            result = subprocess.run(
                ["sudo", "systemctl", "stop", service_name],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
        except Exception:
            return False

    def restart_service(self, service_name: str) -> bool:
        """Restart a service."""
        try:
            result = subprocess.run(
                ["sudo", "systemctl", "restart", service_name],
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.returncode == 0
        except Exception:
            return False

    def enable_service(self, service_name: str) -> bool:
        """Enable service at boot."""
        try:
            result = subprocess.run(
                ["sudo", "systemctl", "enable", service_name],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
        except Exception:
            return False

    def disable_service(self, service_name: str) -> bool:
        """Disable service at boot."""
        try:
            result = subprocess.run(
                ["sudo", "systemctl", "disable", service_name],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
        except Exception:
            return False


def format_services(services: List[ServiceInfo], format_type: str = "text") -> str:
    """Format service list for display."""
    if format_type == "json":
        return json.dumps(
            [
                {
                    "name": s.name,
                    "display_name": s.display_name,
                    "status": s.status,
                    "enabled": s.enabled,
                    "running": s.running,
                }
                for s in services
            ],
            indent=2,
        )

    lines = ["=== Service Status ===", ""]
    for s in services:
        status_icon = "✓" if s.running else "✗"
        enabled_str = "enabled" if s.enabled else "disabled"
        lines.append(f"{s.name}: {s.status.upper()} {status_icon} ({enabled_str})")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage system services")
    parser.add_argument(
        "command",
        choices=["status", "start", "stop", "restart", "enable", "disable"],
        help="Command to execute",
    )
    parser.add_argument("service", nargs="?", help="Service name")
    parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )

    args = parser.parse_args()

    manager = ServiceManager()

    if args.command == "status":
        if args.service:
            service = manager.get_service_status(args.service)
            if args.json:
                print(json.dumps({
                    "name": service.name,
                    "status": service.status,
                    "running": service.running,
                    "enabled": service.enabled,
                }, indent=2))
            else:
                print(f"Service: {service.name}")
                print(f"Status: {service.status}")
                print(f"Running: {service.running}")
                print(f"Enabled at boot: {service.enabled}")
        else:
            services = manager.list_services()
            print(format_services(services, "json" if args.json else "text"))

    elif args.service:
        success = False
        if args.command == "start":
            success = manager.start_service(args.service)
        elif args.command == "stop":
            success = manager.stop_service(args.service)
        elif args.command == "restart":
            success = manager.restart_service(args.service)
        elif args.command == "enable":
            success = manager.enable_service(args.service)
        elif args.command == "disable":
            success = manager.disable_service(args.service)

        if success:
            print(f"{args.command.capitalize()}ed service: {args.service}")
        else:
            print(f"Failed to {args.command} service: {args.service}")
            exit(1)
