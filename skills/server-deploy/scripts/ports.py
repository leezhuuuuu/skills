#!/usr/bin/env python3
"""
Port Management Script

Source: Derived from anthropics/skills PR #151 (geepers agent system)

Map and manage port allocations.
"""

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PortInfo:
    """Information about a port."""
    port: int
    protocol: str
    process: Optional[str] = None
    pid: Optional[int] = None
    status: str = "in_use"
    reserved: bool = False


@dataclass
class PortMap:
    """Port allocation map."""
    ports: Dict[int, PortInfo] = field(default_factory=dict)
    reservations: Dict[int, str] = field(default_factory=dict)

    def add_port(self, port: PortInfo):
        self.ports[port.port] = port

    def reserve(self, port: int, description: str = ""):
        self.reservations[port] = description

    def free(self, port: int):
        if port in self.reservations:
            del self.reservations[port]


class PortManager:
    """Manage port allocations."""

    # Well-known ports to skip
    SKIP_PORTS = {22, 80, 443}

    # Common port ranges
    COMMON_PORTS = {
        80: "HTTP",
        443: "HTTPS",
        22: "SSH",
        3306: "MySQL",
        5432: "PostgreSQL",
        6379: "Redis",
        8080: "HTTP Alt",
        8443: "HTTPS Alt",
        27017: "MongoDB",
    }

    def __init__(self):
        self.port_map = PortMap()

    def scan_ports(self, start: int = 1, end: int = 65535) -> List[PortInfo]:
        """Scan for active ports."""
        ports = []

        # Try to get from ss or netstat
        try:
            result = subprocess.run(
                ["ss", "-tlnp"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            ports = self._parse_ss_output(result.stdout)
        except FileNotFoundError:
            try:
                result = subprocess.run(
                    ["netstat", "-tlnp"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                ports = self._parse_netstat_output(result.stdout)
            except FileNotFoundError:
                # Fallback: manual scan for common ports
                ports = self._scan_common_ports()

        return ports

    def _parse_ss_output(self, output: str) -> List[PortInfo]:
        """Parse ss command output."""
        ports = []
        for line in output.split("\n"):
            if line.startswith("LISTEN"):
                parts = line.split()
                if len(parts) >= 5:
                    # Parse local address
                    addr = parts[3]
                    match = re.match(r"(.+):(\d+)", addr)
                    if match:
                        port = int(match.group(2))
                        # Get process info
                        proc = None
                        pid = None
                        for part in parts[4:]:
                            if "pid=" in part:
                                pid_match = re.search(r"pid=(\d+)", part)
                                if pid_match:
                                    pid = int(pid_match.group(1))
                                proc = part.split("=")[-1] if "=" in part else part
                        ports.append(
                            PortInfo(
                                port=port,
                                protocol="tcp",
                                process=proc,
                                pid=pid,
                            )
                        )
        return ports

    def _parse_netstat_output(self, output: str) -> List[PortInfo]:
        """Parse netstat command output."""
        ports = []
        for line in output.split("\n"):
            if "LISTEN" in line:
                parts = line.split()
                if len(parts) >= 4:
                    addr = parts[3]
                    match = re.match(r"(.+):(\d+)", addr)
                    if match:
                        port = int(match.group(2))
                        protocol = "tcp" if "tcp" in line.lower() else "udp"
                        ports.append(PortInfo(port=port, protocol=protocol))
        return ports

    def _scan_common_ports(self) -> List[PortInfo]:
        """Scan common ports manually."""
        ports = []
        for port, service in self.COMMON_PORTS.items():
            if self._check_port(port):
                ports.append(
                    PortInfo(
                        port=port,
                        protocol="tcp",
                        process=service,
                        status="in_use",
                    )
                )
        return ports

    def _check_port(self, port: int) -> bool:
        """Check if a port is in use."""
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex(("localhost", port))
            return result == 0
        except:
            return False
        finally:
            sock.close()

    def check_port(self, port: int) -> PortInfo:
        """Check if a specific port is available."""
        in_use = self._check_port(port)
        return PortInfo(
            port=port,
            protocol="tcp",
            status="available" if not in_use else "in_use",
        )

    def find_available(self, start: int = 8000, end: int = 9000, count: int = 1) -> List[int]:
        """Find available ports in a range."""
        available = []
        for port in range(start, end + 1):
            if port in self.SKIP_PORTS:
                continue
            if not self._check_port(port):
                available.append(port)
                if len(available) >= count:
                    break
        return available

    def find_process(self, port: int) -> Optional[PortInfo]:
        """Find process using a port."""
        for p in self.scan_ports():
            if p.port == port:
                return p
        return None

    def get_port_map(self) -> PortMap:
        """Get complete port map."""
        self.port_map = PortMap()
        for port_info in self.scan_ports():
            self.port_map.add_port(port_info)
        return self.port_map


def format_port_map(port_map: PortMap, format_type: str = "text") -> str:
    """Format port map for display."""
    if format_type == "json":
        return json.dumps(
            {
                "ports": [
                    {
                        "port": p.port,
                        "protocol": p.protocol,
                        "process": p.process,
                        "pid": p.pid,
                    }
                    for p in port_map.ports.values()
                ],
                "reservations": port_map.reservations,
            },
            indent=2,
        )

    lines = ["=== Port Map ===", ""]

    # Group by status
    reserved = []
    in_use = []
    available = []

    for port, info in sorted(port_map.ports.items()):
        in_use.append(info)

    for port, desc in sorted(port_map.reservations.items()):
        reserved.append((port, desc))

    if reserved:
        lines.append("Reserved Ports:")
        for port, desc in reserved:
            lines.append(f"  {port}: {desc}")
        lines.append("")

    if in_use:
        lines.append("Active Ports:")
        for info in in_use:
            proc = info.process or "unknown"
            pid = f" (PID: {info.pid})" if info.pid else ""
            lines.append(f"  {info.port}/{info.protocol}: {proc}{pid}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port management")
    parser.add_argument(
        "command",
        choices=["map", "check", "find", "alloc", "free"],
        help="Command to execute",
    )
    parser.add_argument("target", nargs="?", help="Port or other target")
    parser.add_argument("--description", "-d", help="Description for reservation")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--start", type=int, default=8000, help="Start port for search"
    )
    parser.add_argument("--end", type=int, default=9000, help="End port for search")

    args = parser.parse_args()

    manager = PortManager()

    if args.command == "map":
        port_map = manager.get_port_map()
        print(format_port_map(port_map, "json" if args.json else "text"))

    elif args.command == "check":
        if args.target:
            port = int(args.target)
            info = manager.check_port(port)
            if args.json:
                print(json.dumps({"port": port, "status": info.status}, indent=2))
            else:
                status = "available" if info.status == "available" else "in use"
                print(f"Port {port}: {status}")
        else:
            print("Error: Port number required")

    elif args.command == "find":
        if args.target:
            port = int(args.target)
            info = manager.find_process(port)
            if args.json:
                if info:
                    print(json.dumps({
                        "port": info.port,
                        "process": info.process,
                        "pid": info.pid,
                    }, indent=2))
                else:
                    print(json.dumps({"error": "No process found"}, indent=2))
            else:
                if info:
                    print(f"Port {port}: {info.process} (PID: {info.pid})")
                else:
                    print(f"No process found using port {port}")
        else:
            print("Error: Port number required")

    elif args.command == "alloc":
        if args.target:
            port = int(args.target)
            manager.port_map.reserve(port, args.description or "")
            print(f"Port {port} reserved")
        else:
            # Auto-allocate
            available = manager.find_available(args.start, args.end)
            if available:
                port = available[0]
                manager.port_map.reserve(port, args.description or "")
                print(f"Port {port} allocated and reserved")
            else:
                print("No available ports in range")
                exit(1)

    elif args.command == "free":
        if args.target:
            port = int(args.target)
            manager.port_map.free(port)
            print(f"Port {port} reservation removed")
        else:
            print("Error: Port number required")
