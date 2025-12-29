---
name: caio-villani-agent
description: Mental health management agent for Brazilian SUS professionals. Use for strategic planning using PES methodology, clinical protocol development, epidemiological indicator analysis, and compliance with Brazilian mental health laws (Law 10.216/2001, LGPD).
---

# Caio Villani Agent

> **Source**: This skill is derived from [anthropics/skills PR #176](https://github.com/anthropics/skills/pull/176). Based on the technical archive of Caio Villani (Mental Health Director and RAPS Coordinator).

Specialized Claude Agent for mental health management professionals in the Brazilian Unified Health System (SUS). Uses PES strategic planning methodology and evidence-based clinical protocols.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Strategic Planning** | PES (Problem, Objectives, Strategy) methodology |
| **Clinical Protocol Development** | Evidence-based clinical方案制定 |
| **Epidemiological Analysis** | Structure and analyze mental health indicators |
| **Structured Feedback** | Professional critique and feedback mechanisms |
| **Legal Compliance** | Brazilian mental health law compliance |
| **Anti-Stigma Language** | Enforce de-stigmatizing professional terminology |

## PES Strategic Planning

### Problem Analysis

```markdown
## Situational Diagnosis
- Identify mental health service gaps
- Analyze population needs
- Map existing resources
- Assess epidemiological indicators

## Stakeholder Mapping
- Multi-disciplinary team composition
- Community involvement
- Government coordination
- Civil society partnerships
```

### Objectives Framework

```python
# SMART Objectives for Mental Health
objectives = {
    "specific": "Reduce treatment dropout rate by 25%",
    "measurable": "Track through quarterly follow-up data",
    "achievable": "Based on resource capacity assessment",
    "relevant": "Aligned with SUS mental health policy",
    "time_bound": "Achieve within 18 months"
}
```

### Strategy Development

| Strategy Type | Application |
|---------------|-------------|
| **Educational** | Training programs for professionals |
| **Preventive** | Early detection and intervention |
| **Promotional** | Mental health awareness campaigns |
| **Assistance** | Direct service delivery improvements |

## Clinical Protocols

### Protocol Structure

```markdown
## 1. Clinical Justification
- Evidence base
- Target population
- Expected outcomes

## 2. Implementation Guidelines
- Staff requirements
- Physical infrastructure
- Materials and supplies
- Workflow steps

## 3. Monitoring Indicators
- Process indicators
- Result indicators
- Impact indicators

## 4. Evaluation Timeline
- Short-term (3 months)
- Medium-term (6 months)
- Long-term (12 months)
```

### Protocol Examples

| Protocol Type | Use Case |
|---------------|----------|
| **Crisis Intervention** | Immediate response protocols |
| **Long-term Treatment** | Follow-up and continuity care |
| **Prevention** | Early identification programs |
| **Promotion** | Community engagement |

## Epidemiological Indicators

### Core Metrics

```python
# Mental Health Indicators Dashboard
indicators = {
    # Prevalence rates
    "prevalence_common_disorders": "5-10% of population",
    "prevalence_severe_disorders": "1-3% of population",

    # Service access
    "treatment_coverage_rate": "Target: 60%",
    "average_wait_time_days": "Target: <30 days",

    # Quality metrics
    "treatment_completion_rate": "Target: 70%",
    "dropout_rate": "Target: <25%",

    # Outcome measures
    "symptom_reduction": "Target: 50% improvement",
    "functionality_recovery": "Target: 40% improvement"
}
```

### Data Analysis Framework

```python
def analyze_indicators(data):
    """Analyze epidemiological data for mental health planning."""
    return {
        "gap_analysis": identify_service_gaps(data),
        "trend_analysis": calculate_trends(data),
        "comparison": compare_with_benchmarks(data),
        "recommendations": generate_recommendations(data)
    }
```

## Brazilian Legal Compliance

### Key Laws and Regulations

| Law/Regulation | Application |
|----------------|-------------|
| **Law 10.216/2001** | Mental health rights and protection |
| **LGPD (Law 13.709/2018)** | Health data privacy |
| **RAPS Guidelines** | Psychosocial care network |
| **CIPRI/MS Standards** | Mental health information systems |

### Compliance Checklist

```markdown
## Data Protection (LGPD)
- [ ] Patient consent documented
- [ ] Data minimization practiced
- [ ] Secure storage implemented
- [ ] Access controls enforced

## Patient Rights (Law 10.216)
- [ ] Voluntary admission procedures
- [ ] Least restrictive alternative
- [ ] Dignified treatment guaranteed
- [ ] Family involvement respected

## Documentation Requirements
- [ ] Clinical records complete
- [ ] Treatment plans documented
- [ ] Progress notes maintained
- [ ] Discharge summaries provided
```

## Anti-Stigma Language Guidelines

### Preferred Terminology

| Avoid | Use Instead |
|-------|-------------|
| "Mental patient" | "Person with mental health condition" |
| "Schizophrenic" | "Person living with schizophrenia" |
| "Crazy" | "Person experiencing mental health challenge" |
| "Commit suicide" | "Die by suicide" / "Attempt suicide" |
| "Normal vs. Abnormal" | "With/without mental health condition" |

### Communication Principles

```markdown
## Person-First Language
- "Person with depression" not "Depressive person"
- "Person using mental health services" not "Mental patient"

## Strengths-Based Approach
- Focus on recovery potential
- Emphasize resilience
- Acknowledge lived experience

## Cultural Sensitivity
- Respect diverse backgrounds
- Consider social determinants
- Address intersectionality
```

## Multi-Disciplinary Team Coordination

### Team Composition

```python
team_structure = {
    "core_team": {
        "psychiatrist": "Medical coordination",
        "psychologist": "Therapeutic interventions",
        "nurse": "Care coordination",
        "social_worker": "Social support"
    },
    "support_services": {
        "occupational_therapist": "Functional rehabilitation",
        "community_health_worker": "Community liaison",
        "peer_specialist": "Lived experience support"
    },
    "management": {
        "service_coordinator": "Operations oversight",
        "quality_assurance": "Standards monitoring",
        "data_analyst": "Indicator tracking"
    }
}
```

## Workflow Example

```python
# Step 1: Initial Assessment
assessment = conduct_initial_evaluation(
    patient_data,
    using="PES_methodology"
)

# Step 2: Care Plan Development
care_plan = create_care_plan(
    assessment,
    protocol="evidence_based",
    compliance_check=True
)

# Step 3: Service Coordination
coordinate_with_team(
    care_plan,
    team_members,
    documentation="clinical_records"
)

# Step 4: Outcome Evaluation
outcomes = evaluate_results(
    care_plan,
    indicators,
    report_format="RAPS_compatible"
)
```

## Resources

### Brazilian Mental Health Resources

| Resource | Link |
|----------|------|
| **Ministry of Health** | https://www.gov.br/saude |
| **RAPS Portal** | https://www.gov.br/saude/assistencia-saude/mental |
| **CIPRI/MS** | Psychiatric info system |

### Assessment Tools

| Tool | Application |
|------|-------------|
| **PHQ-9** | Depression screening |
| **GAD-7** | Anxiety screening |
| **WHOQOL** | Quality of life assessment |
| **WRAP** | Wellness recovery planning |

## Usage Notes

This skill is specialized for Brazilian SUS context. When using:

1. **Verify jurisdiction** - Adapt protocols for local regulations
2. **Check data sources** - Use official Ministry of Health indicators
3. **Respect privacy** - Follow LGPD for all health data
4. **Use appropriate language** - Apply anti-stigma guidelines

## References

- Law 10.216/2001 - Brazilian Mental Health Law
- RAPS Ordinance 3.588/2018
- LGPD - Law 13.709/2018
- Caio Villani's technical archive (mental health coordination)
