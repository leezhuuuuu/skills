---
name: swarm
description: Multi-agent orchestration skill for coordinating multiple AI agents with task distribution and result aggregation.
---

# Swarm Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

Multi-agent orchestration for coordinating multiple AI agents.

## Quick Start

```bash
# Run swarm with tasks
python scripts/swarm.py --task "Research topic" --agents 4

# Check swarm status
python scripts/swarm.py --status

# Aggregate results
python scripts/aggregate.py <session_id>
```

## Architecture

```
Swarm Orchestrator
    ├── Task Dispatcher
    │   ├── Agent Pool (configurable size)
    │   └── Task Queue
    ├── Communication Layer
    │   └── Result Aggregator
    └── State Manager
        └── Session Tracking
```

## Scripts

### swarm.py

Execute multi-agent swarm tasks.

```bash
python scripts/swarm.py [options]

Required:
  --task, -t        Task description for the swarm

Options:
  --agents, -n      Number of agents (default: 4)
  --provider, -p    LLM provider (default: xai)
  --model, -m       Specific model
  --mode, -o        Execution mode: parallel, sequential, hybrid
  --output, -f      Output format: json, markdown, text
  --session, -s     Session ID for continuing swarm
  --verbose, -v     Verbose output
```

**Execution Modes:**

| Mode | Description |
|------|-------------|
| **parallel** | All agents work simultaneously (fastest) |
| **sequential** | Agents work one after another (most reliable) |
| **hybrid** | Phased execution (balance of speed and reliability) |

### status.py

Check swarm session status.

```bash
python scripts/status.py <session_id> [options]

Options:
  --json            Output as JSON
  --verbose         Show agent details
```

### aggregate.py

Aggregate results from swarm session.

```bash
python scripts/aggregate.py <session_id> [options]

Options:
  --format          Output format: markdown, json, report
  --output          Save to file
  --summarize       Generate executive summary
```

## Usage Examples

### Basic Swarm

```bash
# Parallel execution (default)
python scripts/swarm.py --task "Analyze these customer reviews" --agents 4

# Sequential execution
python scripts/swarm.py --task "Write a comprehensive report" \
  --mode sequential --agents 3

# Hybrid mode
python scripts/swarm.py --task "Multi-phase analysis" \
  --mode hybrid --agents 6
```

### Continued Session

```bash
# Continue a previous session
python scripts/swarm.py --session abc123 --task "Additional analysis"

# Check status
python scripts/status.py abc123 --json

# Aggregate final results
python scripts/aggregate.py abc123 --format markdown --output report.md
```

### Programmatic Usage

```python
from swarm import SwarmOrchestrator, SwarmConfig

# Create orchestrator
config = SwarmConfig(
    num_agents=4,
    provider="anthropic",
    mode="parallel"
)

orchestrator = SwarmOrchestrator(config)

# Execute swarm
result = orchestrator.run(
    task="Analyze market trends",
    context={"industry": "technology"}
)

# Get aggregated results
summary = result.get_summary()
print(summary)
```

## Task Types

| Task Type | Description | Best Mode |
|-----------|-------------|-----------|
| **Research** | Information gathering | parallel |
| **Analysis** | Data interpretation | sequential |
| **Generation** | Content creation | sequential |
| **Review** | Quality assessment | parallel |

## Configuration

Create `swarm.yaml`:

```yaml
swarm:
  default_agents: 4
  max_agents: 16
  timeout: 300
  retry_failed: true

providers:
  default: xai
  fallback: anthropic

communication:
  protocol: mcp
  base_url: http://localhost:5060

output:
  format: markdown
  include_metadata: true
```

## Integration

### With Cascade

```python
# Use swarm for sub-tasks within cascade
from cascade import DreamCascadeOrchestrator
from swarm import SwarmOrchestrator

# Swarm handles parallel research
swarm = SwarmOrchestrator()
results = swarm.run("Gather data on topic X")

# Cascade synthesizes results
cascade = DreamCascadeOrchestrator()
final = cascade.synthesize(results)
```

## Resources

- [MCP Protocol](https://modelcontextprotocol.org/)
- [Agent Communication Patterns](https://example.com/agent-patterns)
