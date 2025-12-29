---
name: skill-discoverer
description: Search and install skills from the PRPM registry (7,500+ packages). Use when Claude needs to find and integrate domain-specific knowledge, rules, or agents from the community ecosystem. Supports AI-assisted search, keyword search, and collection-based discovery.
---

# Skill Discoverer

> **Source**: This skill is derived from [anthropics/skills PR #152](https://github.com/anthropics/skills/pull/152) by @khaliqgant. Based on the [PRPM](https://prpm.dev) registry project.

Search and install skills, rules, and agents from the PRPM registry to enhance Claude's capabilities in specific task domains.

## Quick Start

Install the PRPM CLI:

```bash
npm install -g prpm
# Or use npx directly
npx prpm <command>
```

## Core Capabilities

### AI-Assisted Search

For natural language queries when user intent is unclear:

```bash
npx prpm ai-search "help me deploy my app to the cloud"
npx prpm ai-search "I need help with testing my web app"
```

### Keyword Search

For specific tool or technology searches:

```bash
# Search by keyword
npx prpm search "pulumi beanstalk infrastructure"
npx prpm search "react" --subtype rule

# Filter by type
npx prpm search "deployment" --type skill
npx prpm search "validation" --type rule
```

### Collection Search

Discover curated sets of related packages:

```bash
# Browse collections
npx prpm collection search "frontend"
npx prpm collection search "devops"

# Install entire collection
npx prpm install essential-dev-agents
```

## Trigger Patterns

Use this skill when users request help with:

### Infrastructure & Cloud
```
aws, pulumi, terraform, kubernetes, docker, beanstalk, azure, gcp
```

### Testing & QA
```
test, playwright, jest, cypress, vitest, e2e, testing, coverage
```

### Deployment & CI/CD
```
ci/cd, github-actions, gitlab-ci, deploy, workflow, cicd, pipeline
```

### Frameworks & Libraries
```
react, vue, next.js, express, fastify, django, svelte, angular
```

## Installation Workflow

### Step 1: Analyze Request

```python
# Determine search strategy based on request clarity
request = "Help me set up Pulumi infrastructure"

if has_specific_tools(request):
    strategy = "keyword_search"  # "pulumi"
elif has_broad_intent(request):
    strategy = "ai_search"       # "infrastructure setup"
```

### Step 2: Search Registry

```bash
# Keyword search for specific tools
npx prpm search "pulumi infrastructure"

# AI search for general requests
npx prpm ai-search "help me set up cloud infrastructure"
```

### Step 3: Evaluate Results

Package quality indicators:

| Indicator | High Confidence | Medium Confidence |
|-----------|-----------------|-------------------|
| Official | @prpm/* packages | - |
| Downloads | >1,000 | 100-1,000 |
| Verification | Verified author | Community |
| Featured | Featured badge | - |

### Step 4: Suggest Installation

```python
# High confidence: Auto-suggest
@prpm/pulumi-infrastructure (Official, 3.2K downloads)

# Medium confidence: Present options
- @user/react-utils (100 downloads)
- @org/react-helper (250 downloads)
```

### Step 5: Install (with approval)

```bash
# Install single package
npx prpm install @prpm/pulumi-infrastructure --as claude

# Install collection
npx prpm install essential-dev-agents
```

## Example Workflows

### Infrastructure Setup

```bash
# User: "Help me build Pulumi + Beanstalk infrastructure"

# 1. Search for relevant packages
npx prpm search "pulumi beanstalk infrastructure"

# 2. Find best match
# @prpm/pulumi-infrastructure (Official, 3.2K downloads)

# 3. Suggest installation
# "I found @prpm/pulumi-infrastructure. Should I install it?"

# 4. Install with approval
npx prpm install @prpm/pulumi-infrastructure --as claude

# 5. Apply knowledge to task
```

### Testing Setup

```bash
# User: "I need help with E2E testing"

# 1. AI search for relevant packages
npx prpm ai-search "E2E testing frameworks"

# 2. Present options
# - @prpm/playwright-helper (Official, 2.1K downloads)
# - @org/cypress-utils (500 downloads)

# 3. User selects, then install
npx prpm install @prpm/playwright-helper --as claude
```

### Collection Installation

```bash
# Browse essential development tools
npx prpm collection search "essential-dev-agents"

# Install curated collection
npx prpm install essential-dev-agents
```

## Privacy & Security

| Guarantee | Description |
|-----------|-------------|
| **Local Search** | All searches execute locally |
| **No Data Sharing** | Search queries not sent to PRPM |
| **Minimal Tracking** | Only download counts tracked |
| **User Approval** | Installation requires explicit approval |

## Registry Stats

- **7,500+** packages available
- **100+** curated collections
- **18+** AI tool formats supported
- **Official** @prpm/* packages verified

## Resources

- **PRPM Registry**: https://prpm.dev
- **Documentation**: https://docs.prpm.dev
- **GitHub**: https://github.com/pr-pm/prpm
- **npm**: https://www.npmjs.com/package/prpm
