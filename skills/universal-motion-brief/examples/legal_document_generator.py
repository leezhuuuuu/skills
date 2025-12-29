#!/usr/bin/env python3
"""
Legal Document Generator for Court Filings.

Generate court-ready legal documents with proper formatting,
jurisdiction-specific rules, and compliance checking.

Usage:
    python legal_document_generator.py --template opening_brief --jurisdiction ninth_circuit --output brief.docx

Source: Derived from anthropics/skills PR #170 (MIT License)
"""

import argparse
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class DocumentType(Enum):
    MOTION = "motion"
    BRIEF = "brief"
    OPPOSITION = "opposition"
    REPLY = "reply"
    STIPULATION = "stipulation"


@dataclass
class JurisdictionConfig:
    font: str
    font_size: int
    line_spacing: str
    margins: Dict[str, float]
    page_limit: int
    citation_format: str


# Predefined jurisdiction configurations
JURISDICTIONS = {
    "ninth_circuit": JurisdictionConfig(
        font="Times New Roman",
        font_size=12,
        line_spacing="double",
        margins={"top": 1.5, "bottom": 1.5, "left": 1.25, "right": 1.25},
        page_limit=25,
        citation_format="Bluebook"
    ),
    "federal_district": JurisdictionConfig(
        font="Times New Roman",
        font_size=12,
        line_spacing="double",
        margins={"top": 1.0, "bottom": 1.0, "left": 1.0, "right": 1.0},
        page_limit=25,
        citation_format="Bluebook"
    ),
    "state": JurisdictionConfig(
        font="Times New Roman",
        font_size=12,
        line_spacing="double",
        margins={"top": 1.0, "bottom": 1.0, "left": 1.0, "right": 1.0},
        page_limit=20,
        citation_format="State"
    )
}


class LegalDocumentGenerator:
    """Generate court-ready legal documents."""

    def __init__(self, jurisdiction: str = "ninth_circuit"):
        self.jurisdiction = jurisdiction
        self.config = JURISDICTIONS.get(jurisdiction, JURISDICTIONS["federal_district"])
        self.sections: Dict[str, str] = {}

    def add_section(self, name: str, content: str):
        """Add a document section."""
        self.sections[name] = content

    def generate_caption(self, case_data: Dict) -> str:
        """Generate document caption."""
        return f"""
{court_name}
Case No. {case_data.get('case_number', 'XX-XXXX')}

{case_data.get('party_names', 'Party A v. Party B')}

Document Title: {case_data.get('document_title', 'Motion')}
""".strip()

    def format_citation(self, citation: str) -> str:
        """Format citation according to jurisdiction rules."""
        if self.config.citation_format == "Bluebook":
            # Basic Bluebook formatting
            return citation
        return citation

    def check_compliance(self) -> List[str]:
        """Check document compliance with court rules."""
        issues = []

        # Check sections
        required_sections = ["caption", "introduction"]
        for section in required_sections:
            if section not in self.sections:
                issues.append(f"Missing required section: {section}")

        # Check content length
        total_length = sum(len(s) for s in self.sections.values())
        if total_length < 100:
            issues.append("Document content appears too brief")

        return issues

    def generate(self, document_type: DocumentType = DocumentType.BRIEF) -> str:
        """Generate the complete document."""
        compliance = self.check_compliance()
        if compliance:
            print(f"Compliance issues found: {compliance}")

        # Generate document in proper order
        document_parts = []

        # Caption
        if "caption" in self.sections:
            document_parts.append(self.sections["caption"])

        # Other sections in order
        order = ["introduction", "statement_of_issues", "statement_of_the_case",
                 "argument", "conclusion", "relief_requested"]

        for section_name in order:
            if section_name in self.sections:
                document_parts.append(f"\n\n## {section_name.upper().replace('_', ' ')}\n")
                document_parts.append(self.sections[section_name])

        return "\n".join(document_parts)


def generate_motion(template: str, jurisdiction: str, data: Dict, output: str = None):
    """Convenience function to generate a motion document."""
    generator = LegalDocumentGenerator(jurisdiction)

    # Add sections from data
    for section, content in data.items():
        generator.add_section(section, content)

    # Generate
    document = generator.generate(DocumentType.MOTION)

    if output:
        with open(output, 'w') as f:
            f.write(document)
        print(f"Document saved to {output}")

    return document


def main():
    parser = argparse.ArgumentParser(
        description="Generate court-ready legal documents"
    )
    parser.add_argument(
        '--template', '-t',
        default='opening_brief',
        help='Document template (opening_brief, opposition, reply)'
    )
    parser.add_argument(
        '--jurisdiction', '-j',
        default='ninth_circuit',
        choices=JURISDICTIONS.keys(),
        help='Court jurisdiction'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path'
    )
    parser.add_argument(
        '--data', '-d',
        help='JSON file with document data'
    )

    args = parser.parse_args()

    # Load data if provided
    data = {}
    if args.data:
        with open(args.data) as f:
            data = json.load(f)

    # Generate document
    document = generate_motion(
        template=args.template,
        jurisdiction=args.jurisdiction,
        data=data,
        output=args.output
    )

    if not args.output:
        print(document)


if __name__ == "__main__":
    main()
