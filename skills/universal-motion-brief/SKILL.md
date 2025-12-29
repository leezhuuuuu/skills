---
name: universal-motion-brief
description: Generate court-ready legal documents for pro se litigants. Use for creating motions, briefs, and legal filings with proper court formatting. Supports jurisdiction-specific rules, template-based document generation, and court compliance checking.
---

# Universal Motion Brief Skill

> **Source**: This skill is derived from [anthropics/skills PR #170](https://github.com/anthropics/skills/pull/170) by @TylerALofall. A comprehensive legal document formatting system for pro se litigants.

Generate court-ready legal documents with proper formatting, jurisdiction-specific rules, and court compliance checking.

## Quick Start

```python
from legal_document_generator import generate_motion

# Generate a motion document
motion = generate_motion(
    template="opening_brief",
    jurisdiction="ninth_circuit",
    data={
        "case_number": "23-1234",
        "party_name": "John Doe",
        "relief_requested": "Summary Judgment"
    }
)
motion.save("motion.docx")
```

## Core Features

### Document Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Motion** | Request to the court | "I move for summary judgment" |
| **Brief** | Written argument | Supporting your motion with law |
| **Opposition** | Response to motion | Opposing the other party's motion |
| **Reply** | Response to opposition | Final word on your motion |
| **Stipulation** | Agreement between parties | Proposing a settlement |

### Jurisdiction Support

```python
# Configure for specific court
jurisdiction_config = {
    "ninth_circuit": {
        "font": "Times New Roman",
        "font_size": 12,
        "line_spacing": "double",
        "margins": {
            "top": 1.5,
            "bottom": 1.5,
            "left": 1.25,
            "right": 1.25
        },
        "page_limit": 25,  # pages for opening brief
        "citation_format": "Bluebook"
    },
    "federal_district": {
        "font": "Times New Roman",
        "font_size": 12,
        "line_spacing": "double",
        "margins": {"all": 1.0},
        "citation_format": "Bluebook"
    }
}
```

### Court Compliance Checklist

```python
from court_compliance import check_compliance

document = load_docx("motion.docx")
report = check_compliance(document, jurisdiction="ninth_circuit")

if report.is_compliant:
    print("Document is court-ready!")
else:
    print("Issues found:")
    for issue in report.issues:
        print(f"  - {issue}")
```

## Document Structure

### Standard Motion Components

```markdown
1. Caption
   - Court name
   - Case number
   - Party names

2. Table of Contents (if > 10 pages)

3. Table of Authorities
   - Cases
   - Statutes
   - Other authorities

4. Introduction
   - Nature of the case
   - Relief sought

5. Statement of Issues
   - Questions presented

6. Statement of the Case
   - Procedural history
   - Facts

7. Argument
   - Legal standards
   - Analysis
   - Conclusion

8. Relief Requested

9. Signature Block
```

### Brief Components

```markdown
1. Cover Page
   - Case number (centered, 1" from top)
   - Party names
   - Document title

2. Table of Contents

3. Table of Authorities

4. Jurisdictional Statement

5. Statement of Issues

6. Statement of the Case

7. Summary of Argument

8. Argument
   - I. [First Issue]
   - II. [Second Issue]
   ...

9. Conclusion

10. Certificate of Service

11. Signature
```

## Common Authorities

### Standards of Review

| Standard | Description | When Used |
|----------|-------------|-----------|
| **De Novo** | Court reviews from scratch | Legal questions, summary judgment |
| **Clear Error** | Deference to trial court | Factual findings |
| **Abuse of Discretion** | High deference | Discovery rulings, sanctions |
| **Plenty Deference** | For agency decisions | Chevron deference |

### Citation Format (Bluebook)

```markdown
# Cases
Doe v. Smith, 123 F.3d 456 (9th Cir. 2020)

# Statutes
42 U.S.C. § 1983

# Law Reviews
John Doe, The Future of Civil Rights, 123 HARV. L. REV. 456 (2020)

# Court Rules
Fed. R. Civ. P. 12(b)(6)
```

## Workflow Example

```python
from document_builder import LegalDocumentBuilder
from template_manager import TemplateManager

# 1. Load template
builder = LegalDocumentBuilder()
builder.load_template("opening_brief")

# 2. Set jurisdiction
builder.set_jurisdiction("ninth_circuit")

# 3. Add content sections
builder.add_section("caption", {
    "court": "United States Court of Appeals for the Ninth Circuit",
    "case_number": "23-1234",
    "party_name": "John Doe, Plaintiff-Appellant"
})

builder.add_section("introduction", {
    "text": "Plaintiff-Appellant John Doe appeals from..."
})

builder.add_section("argument", {
    "issue": "Whether the district court erred...",
    "argument": "The district court committed clear error..."
})

# 4. Format for court
builder.apply_formatting()

# 5. Generate document
builder.generate("brief.docx")

# 6. Check compliance
from court_compliance import check_compliance
report = check_compliance("brief.docx", "ninth_circuit")
```

## Data Collection

```python
from case_collector import CaseCollector

# Collect case information
collector = CaseCollector()

# Store in structured format
case_data = {
    "parties": {
        "plaintiff": "John Doe",
        "defendant": "Jane Smith"
    },
    "court": "Ninth Circuit Court of Appeals",
    "case_number": "23-1234",
    "filing_type": "opening_brief",
    "deadline": "2024-03-15"
}

# Save for persistence
collector.save(case_data)
```

## Document Sections Management

```python
from section_manager import SectionManager

# Sections are stored in sections.json
manager = SectionManager("my_brief")

# Add new section
manager.add_section("statement_of_facts", """
    On January 1, 2023, Plaintiff filed this action...
""")

# List all sections
print(manager.list_sections())
# ['caption', 'introduction', 'statement_of_issues',
#  'statement_of_the_case', 'argument', 'conclusion']

# Generate document from sections
manager.generate_document("final_brief.docx")
```

## Resources

- **Ninth Circuit Rules**: https://www.ca9.uscourts.gov/rules
- **Federal Rules of Civil Procedure**: https://www.uscourts.gov/rules-policies/current-federal-rules-civil-procedure
- **Bluebook Citation**: https://www.legalbluebook.com
- **Court Forms**: www.uscourts.gov/forms
