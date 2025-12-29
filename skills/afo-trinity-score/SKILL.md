---
name: afo-trinity-score
description: Calculate the AFO Kingdom Trinity Score for evaluating system quality. Use when assessing code quality, decision-making, or system evaluation based on five philosophical pillars (Truth, Goodness, Beauty, Serenity, Eternity).
---

# AFO Trinity Score Calculator

> **Source**: This skill is derived from [anthropics/skills PR #174](https://github.com/anthropics/skills/pull/174) by @lofibrainwav.

Calculate the Trinity Score (眞善美孝永) for evaluating system quality and making decisions based on five philosophical pillars.

## The Five Pillars

| Pillar | Korean | Weight | Description |
|--------|--------|--------|-------------|
| **Truth (眞)** | 진 | 35% | Technical accuracy, verifiability, factual correctness |
| **Goodness (善)** | 선 | 35% | Ethical soundness, system stability, harmlessness |
| **Beauty (美)** | 미 | 20% | Clear structure, elegant design, UX clarity |
| **Serenity (孝)** | 효 | 8% | Frictionless operation, low cognitive load |
| **Eternity (永)** | 영 | 2% | Long-term sustainability, reproducibility |

## Usage

### Basic Calculation

```python
# Input scores (0-100 scale)
input_data = {
    "truth_base": 95,      # Technical accuracy score
    "goodness_base": 90,   # Ethical soundness score
    "beauty_base": 85,     # Design quality score
    "risk_score": 5,       # Risk factor (lower is better)
    "friction": 3,         # Friction score (lower is better)
    "eternity_base": 88    # Sustainability score
}

# Calculate Trinity Score
trinity_score = calculate_trinity_score(input_data)
```

### Understanding the Score

```python
def interpret_score(score, risk_score):
    """Interpret Trinity Score and recommend action."""

    if score >= 90 and risk_score <= 10:
        return "AUTO_RUN"  # Approved for automatic execution
    elif score >= 70 and risk_score <= 30:
        return "ASK_COMMANDER"  # Requires human approval
    else:
        return "BLOCK"  # Not approved, needs review
```

## Output Format

```json
{
  "trinity_score": 0.92,
  "balance_status": "balanced",
  "decision": "AUTO_RUN",
  "pillar_scores": {
    "truth": 0.95,
    "goodness": 0.90,
    "beauty": 0.85,
    "filial_serenity": 0.88,
    "eternity": 0.90
  }
}
```

## Decision Thresholds

| Decision | Condition |
|----------|-----------|
| **AUTO_RUN** | Trinity Score ≥ 90 AND Risk Score ≤ 10 |
| **ASK_COMMANDER** | Trinity Score 70-89 OR Risk Score 11-30 |
| **BLOCK** | Trinity Score < 70 OR Risk Score > 30 |

## Balance Status

| Status | Trinity Score Range |
|--------|---------------------|
| **Outstanding** | ≥ 95 |
| **Balanced** | 85-94 |
| **Acceptable** | 70-84 |
| **Needs Work** | < 70 |

## Example Workflow

### Evaluating a Code Change

```python
# Evaluate a proposed code change
evaluation = {
    "truth_base": 92,      # Code is technically sound
    "goodness_base": 95,   # No security concerns
    "beauty_base": 88,     # Well-structured
    "risk_score": 3,       # Low risk
    "friction": 2,         # Easy to understand
    "eternity_base": 90    # Maintainable
}

result = calculate_trinity_score(evaluation)

# Decision: AUTO_RUN
# The change meets all quality thresholds
```

### Evaluating a New Feature

```python
# Evaluate a new feature proposal
feature_eval = {
    "truth_base": 85,      # Some uncertainty in implementation
    "goodness_base": 90,   # No ethical issues
    "beauty_base": 80,     # Standard implementation
    "risk_score": 15,      # Moderate risk
    "friction": 5,         # Some learning curve
    "eternity_base": 75    # May need refactoring later
}

result = calculate_trinity_score(feature_eval)

# Decision: ASK_COMMANDER
# Requires human review before proceeding
```

## Integration

This skill integrates with:
- **Chancellor Graph** - Decision routing
- **MCP Tool Bridge** - External validation
- **AFO Skills** - Philosophy alignment tracking

## Resources

- **AFO Kingdom Philosophy**: A framework for balanced decision-making
- **Compatible Platforms**: claude-code, codex, cursor
