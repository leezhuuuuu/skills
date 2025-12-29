---
name: shodh-memory
description: Persistent memory system for AI agents. Store decisions, learnings, errors, and context that persists across conversations. Use proactive_context every message to surface relevant memories before responding.
---

# Shodh Memory Skill

> **Source**: This skill is derived from [anthropics/skills PR #154](https://github.com/anthropics/skills/pull/154) by @varun29ankuS. Based on [shodh-memory](https://github.com/roshera/shodh-memory) project (MCP Server: @anthropic-ai/shodh-memory).

Persistent memory system for AI agents. Store decisions, learnings, errors, and context that persists across conversations, enabling continuous learning across sessions.

## Installation

### Claude Code

```bash
claude mcp add shodh-memory -- npx -y @anthropic-ai/shodh-memory
```

### MCP Server (Local)

```bash
# Using npx (no installation required)
npx -y @anthropic-ai/shodh-memory

# Or install globally with cargo
cargo install shodh-memory
shodh-memory
```

## Core Concept

Shodh (Sanskrit: "discovery") is a neuroscience-inspired memory system that:

- **Surfaces relevant memories** before every response
- **Stores decisions, learnings, and context** across conversations
- **Mimics human memory consolidation** (working → session → long-term memory)
- **Enables continuous learning** for AI agents

## Memory Types

Use the appropriate memory type for different situations:

| Type | Purpose | Example |
|------|---------|---------|
| **Decision** | User choices, architecture decisions | "User chose React over Vue for the frontend" |
| **Learning** | New knowledge acquired | "API requires OAuth2 with PKCE flow" |
| **Error** | Bugs discovered and fixes | "TypeError fixed by adding null check" |
| **Discovery** | Insights and epiphanies | "N+1 query causing performance issue" |
| **Pattern** | Repeated behavioral patterns | "User prefers functional components" |
| **Context** | Background information | "Working on e-commerce platform" |
| **Task** | Work in progress | "Currently refactoring payment module" |
| **Observation** | General notes | "User typically works in morning hours" |

## Core Tools

### Proactive Context (Call Every Message)

```python
# This MUST be called at the start of every response
proactive_context()

# Returns relevant memories based on current conversation
# Automatically surfaces:
# - Recent learnings
# - Relevant decisions
# - Active tasks
# - Related context
```

### Memory Management

```python
# Store a new memory
remember(
    content="User prefers dark mode for coding",
    memory_type="observation",
    tags=["preference", "ui", "workflow"]
)

# Search memories by meaning
memories = recall(query="authentication approach")

# Filter by tags
memories = recall_by_tags(tags=["security", "api"])

# Delete specific memory
forget(memory_id="mem_123")

# Delete by tags
forget_by_tags(tags=["outdated", "deprecated"])
```

### Diagnostic Tools

```python
# Get memory statistics
stats = memory_stats()
# Returns: total memories, memories by type, tag counts

# Quick overview of recent learnings
summary = context_summary()
# Returns: recent memories, active tasks, key decisions

# See what the system is learning
report = consolidation_report()
# Returns: learning patterns, memory health
```

## Workflow Example

```python
# User asks a question
User: "What authentication approach should we use?"

# 1. Call proactive_context to retrieve relevant memories
relevant = proactive_context()

# 2. Recall any security-related memories
auth_memories = recall(query="authentication security")

# 3. Respond with context-aware recommendation
Response: "Based on your previous project, you used OAuth2.
          For this new service, I'd recommend continuing with
          OAuth2 using the PKCE flow we discussed before."

# 4. Store the new decision
remember(
    content="Chose OAuth2 with PKCE for new authentication service",
    memory_type="decision",
    tags=["authentication", "security", "oauth2"]
)
```

## Memory Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│  New Memory → Working Memory (hot, fast access)             │
│                    ↓                                        │
│              Session Memory (warm, recent context)          │
│                    ↓                                        │
│         Long-term Memory (persistent, searchable)           │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

### 1. Call proactive_context Every Message

```python
# Always start with this
proactive_context()

# Don't skip it - it's the foundation of persistent memory
```

### 2. Write Searchable Memories

```python
# Good: Rich, searchable content
remember(
    "API endpoint /api/v1/users/{id} requires Bearer token
     authentication. Returns 401 for missing token.",
    memory_type="learning",
    tags=["api", "authentication", "security"]
)

# Avoid: Vague or unsearchable
remember("API uses auth", memory_type="learning")
```

### 3. Use Tags Effectively

```python
# Tag with multiple dimensions
tags=["project", "component", "status", "priority"]
# Examples: ["payment", "api", "in-progress", "high"]
```

### 4. Choose Correct Memory Type

| Situation | Use Type |
|-----------|----------|
| User made a choice | `decision` |
| Discovered how something works | `learning` |
| Fixed a bug | `error` |
| Noticed a pattern | `pattern` |
| Background context | `context` |
| Work in progress | `task` |
| General note | `observation` |

### 5. Use Appropriate Recall Mode

| Mode | When to Use |
|------|-------------|
| **Semantic** | Finding conceptually related memories |
| **Associative** | Finding by tag or topic |
| **Hybrid** | Combining both for best results |

## Integration Examples

### Project Management

```python
# Remember project context
remember(
    "Building a React-based e-commerce platform with Node.js backend",
    memory_type="context",
    tags=["project", "tech-stack", "ecommerce"]
)

# Store decisions
remember(
    "Chose Stripe for payment processing due to developer experience",
    memory_type="decision",
    tags=["payment", "stripe", "decision"]
)
```

### Codebase Learning

```python
# Document code patterns
remember(
    "The codebase uses repository pattern with dependency injection.
     BaseRepository class handles CRUD operations.",
    memory_type="learning",
    tags=["architecture", "patterns", "repository"]
)

# Remember fixes
remember(
    "Fixed race condition in user login by adding mutex lock
     on token generation",
    memory_type="error",
    tags=["bugfix", "concurrency", "auth"]
)
```

## Configuration

### Environment Variables

```bash
# Storage location (default: ~/.shodh-memory)
SHODH_STORAGE_PATH=./.shodh-memory

# Context window size
SHODH_CONTEXT_LIMIT=20

# Memory consolidation threshold
SHODH_CONSOLIDATION_THRESHOLD=0.7
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No memories returned | Check if proactive_context was called |
| Memories not persisting | Verify storage path is writable |
| Slow recall | Reduce context_limit or run consolidation |
| Tags not working | Use consistent tag naming |

## Resources

- **GitHub**: https://github.com/roshera/shodh-memory
- **MCP Server**: https://www.npmjs.com/package/@anthropic-ai/shodh-memory
- **Documentation**: https://shodh-memory.dev/docs
