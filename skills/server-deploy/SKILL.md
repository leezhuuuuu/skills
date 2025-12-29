---
name: server-deploy
description: Infrastructure management toolkit for services, health checks, and port allocation. Monitor CPU, memory, disk, and web services.
---

# Server Deploy Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

Infrastructure management toolkit for services and system health.

## Quick Start

```bash
# Run system health check
python scripts/health.py

# Check service status
python scripts/service.py status

# Map port usage
python scripts/ports.py map
```

## Core Features

| 功能 | 描述 |
|------|------|
| **服务管理** | 服务启停、状态查询、重启 |
| **健康检查** | CPU、内存、磁盘、服务监控 |
| **端口管理** | 端口映射、可用性检查 |

## Scripts

### health.py

System health checks for infrastructure monitoring.

```bash
python scripts/health.py [options]

Options:
  --cpu             Check CPU usage
  --memory          Check memory usage
  --disk            Check disk space
  --caddy           Check Caddy web server
  --all             Run all checks (default)
  --json            Output in JSON format
  --threshold       Custom threshold (default: 80%)
```

**Health Metrics:**

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| CPU Usage | < 70% | 70-85% | > 85% |
| Memory Usage | < 75% | 75-90% | > 90% |
| Disk Usage | < 80% | 80-95% | > 95% |

**Example Output:**
```
=== System Health Check ===

CPU: 45% ✓
Memory: 62% ✓
Disk: 35% ✓
Caddy: RUNNING ✓

Overall: HEALTHY
```

### service.py

Service manager integration for system services.

```bash
python scripts/service.py <command> [service_name]

Commands:
  status          Show all service statuses
  start           Start a service
  stop            Stop a service
  restart         Restart a service
  enable          Enable service at boot
  disable         Disable service at boot
```

**Example:**
```bash
# Check all services
python scripts/service.py status

# Restart web server
python scripts/service.py restart caddy

# Start database
python scripts/service.py start postgresql
```

### ports.py

Port allocation and availability mapping.

```bash
python scripts/ports.py <command>

Commands:
  map             Show port usage map
  check <port>    Check if port is available
  find <port>     Find process using port
  alloc <port>    Reserve a port
  free <port>     Release a port reservation
```

**Example:**
```bash
# Show all port usage
python scripts/ports.py map

# Check specific port
python scripts/ports.py check 8080

# Find what's using port 80
python scripts/ports.py find 80
```

## Common Use Cases

### Health Monitoring Script

```bash
#!/bin/bash
# Check system health and alert if issues

python scripts/health.py --json > /tmp/health.json

if [ $(cat /tmp/health.json | jq '.healthy') = "false" ]; then
    echo "System health check failed!"
    # Send alert...
fi
```

### Service Management

```python
from service import ServiceManager

manager = ServiceManager()

# Check if service is running
if manager.is_running("caddy"):
    print("Web server is running")

# Restart service if not healthy
if not manager.is_healthy("postgresql"):
    manager.restart("postgresql")
```

### Port Management

```python
from ports import PortManager

manager = PortManager()

# Find available port
port = manager.find_available(start=8000, end=9000)
print(f"Available port: {port}")

# Check if port is in use
if manager.is_available(8080):
    print("Port 8080 is available")
```

## Configuration

Create `config.yaml` for custom settings:

```yaml
services:
  caddy:
    name: "Web Server"
    check_cmd: "curl -f http://localhost/health"
  postgresql:
    name: "Database"
    check_cmd: "pg_isready"

thresholds:
  cpu_warning: 70
  cpu_critical: 85
  memory_warning: 75
  memory_critical: 90
  disk_warning: 80
  disk_critical: 95

alerts:
  webhook_url: "https://hooks.example.com/alerts"
  email: "admin@example.com"
```

## Resources

- [Systemd Service Management](https://www.freedesktop.org/software/systemd/man/systemctl.html)
- [Caddy Server](https://caddyserver.com/)
