---
name: cascade
description: Multi-agent AI research orchestration system for hierarchical workflows (Dream Cascade). Execute parallel research with executive synthesis.
---

# Cascade Skill

> **Source**: This skill is derived from [anthropics/skills PR #151](https://github.com/anthropics/skills/pull/151) by @lukeslp (geepers agent system).

Multi-agent AI research orchestration system for hierarchical workflows.

## Quick Start

```bash
# Execute research workflow
python scripts/research.py "Research AI safety frameworks" --agents 8 --provider xai

# Check workflow status
python scripts/status.py <task_id> --format json

# Cancel running workflow
python scripts/status.py <task_id> --cancel
```

## Architecture

```
Dream Cascade uses a 3-tier hierarchy:

Tier 1 (Belter): Parallel worker agents doing initial research
    ↓
Tier 2 (Drummer): Mid-level synthesis agents
    ↓
Tier 3 (Camina): Executive synthesis and final report
```

## Scripts

### research.py

Execute Dream Cascade hierarchical research workflows.

```bash
python scripts/research.py "Research topic" [options]

Options:
  --title, -t          Custom report title
  --agents, -n         Number of worker agents (default: 8)
  --provider, -p       LLM provider (default: xai)
  --model, -m          Specific model override
  --no-drummer         Disable Drummer synthesis stage
  --no-camina          Disable Camina synthesis stage
  --output, -o         Save results to file
  --format, -f         Output format: markdown, json, text
  --verbose, -v        Show detailed progress
```

**Supported Providers:**

| Provider | Description |
|----------|-------------|
| xai | xAI (Grok) |
| anthropic | Anthropic (Claude) |
| openai | OpenAI (GPT) |
| mistral | Mistral AI |
| gemini | Google Gemini |
| perplexity | Perplexity AI |
| cohere | Cohere |
| groq | Groq |
| huggingface | Hugging Face |
| ollama | Ollama (local) |

### status.py

Check status of running or completed research workflows.

```bash
python scripts/status.py <task_id> [options]

Options:
  --cancel, -c         Cancel the workflow
  --results, -r        Get full results (for completed workflows)
  --output, -o         Save output to file
  --format, -f         Output format: text, json, markdown
```

## Usage Examples

### Basic Research

```bash
# Simple research query
python scripts/research.py "What are the main approaches to reinforcement learning?"

# With custom title and more agents
python scripts/research.py "Compare transformer architectures" \
  --title "Transformer Architecture Analysis" \
  --agents 12 \
  --verbose
```

### Synthesis Controls

```bash
# Skip synthesis stages for raw results
python scripts/research.py "Quick topic scan" --no-synthesis

# Enable only Drummer (mid-level)
python scripts/research.py "Mid-level analysis" --no-camina

# Full synthesis (default)
python scripts/research.py "Comprehensive research" --agents 16
```

### Output Formats

```bash
# JSON for programmatic use
python scripts/research.py "Topic" --format json --output results.json

# Markdown for documentation
python scripts/research.py "Topic" --format markdown --output report.md

# Plain text for quick viewing
python scripts/research.py "Topic" --format text
```

### Status Checking

```bash
# Check running job status
python scripts/status.py research_20241229_143022 --format text

# Get full results
python scripts/status.py research_20241229_143022 --results --format markdown

# Cancel a job
python scripts/status.py research_20241229_143022 --cancel
```

## Configuration

The orchestrator supports 17+ integrated data sources including:

- arXiv (academic papers)
- GitHub (code repositories)
- Census (demographic data)
- Wikipedia (encyclopedia)
- NASA (scientific data)
- And more...

## Resources

- [Dream Cascade Architecture](https://example.com/dream-cascade)
- [MCP Protocol](https://modelcontextprotocol.org/)
