#!/usr/bin/env python3
"""
Dream Cascade/Swarm Workflow Status Script

Source: Derived from anthropics/skills PR #151 (geepers agent system)

Check status of running or completed research workflows.
Supports cancellation and results retrieval.
"""

import argparse
import json
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, Optional


# Simulated workflow storage (replace with MCP server in production)
WORKFLOW_STORE: Dict[str, Dict] = {}


def generate_task_id() -> str:
    """Generate a new task ID."""
    return f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"


def create_mock_workflow(task: str, task_id: str = None) -> Dict[str, Any]:
    """Create a mock workflow for testing."""
    task_id = task_id or generate_task_id()
    return {
        "task_id": task_id,
        "task": task,
        "status": "running",
        "orchestrator_type": "dream-cascade",
        "created_at": datetime.now().isoformat(),
        "started_at": datetime.now().isoformat(),
        "completed_at": None,
        "result": {
            "progress": 45,
            "agents_completed": 4,
            "total_agents": 8,
            "execution_time": 12.5,
            "estimated_cost": 0.15,
        },
    }


def get_status(task_id: str) -> Dict[str, Any]:
    """Get workflow status."""
    if task_id not in WORKFLOW_STORE:
        # Return mock status for demo
        return create_mock_workflow("Demo task", task_id)

    return WORKFLOW_STORE.get(task_id, {"error": "Workflow not found"})


def cancel_workflow(task_id: str) -> Dict[str, Any]:
    """Cancel a running workflow."""
    if task_id in WORKFLOW_STORE:
        WORKFLOW_STORE[task_id]["status"] = "cancelled"
        WORKFLOW_STORE[task_id]["completed_at"] = datetime.now().isoformat()
        return {"cancelled": True, "task_id": task_id}

    return {"cancelled": False, "error": "Workflow not found"}


def get_results(task_id: str) -> Dict[str, Any]:
    """Get full results of a completed workflow."""
    status = get_status(task_id)

    if "error" in status:
        return status

    if status.get("status") == "completed":
        return status.get("result", {"error": "No results available"})

    return {
        "error": f"Workflow not completed. Current status: {status.get('status', 'unknown')}",
        "status": status,
    }


def format_status(status: Dict, format_type: str = "text") -> str:
    """Format status for display."""
    if format_type == "json":
        return json.dumps(status, indent=2, default=str)

    if "error" in status:
        return f"Error: {status['error']}"

    lines = [
        f"Task ID: {status.get('task_id', 'N/A')}",
        f"Status: {status.get('status', 'unknown').upper()}",
        f"Type: {status.get('orchestrator_type', 'N/A')}",
        "",
    ]

    result = status.get("result", {})

    if status.get("status") == "running":
        progress = result.get("progress", 0)
        lines.extend([
            f"Progress: {progress}%",
            f"Agents completed: {result.get('agents_completed', '?')}/{result.get('total_agents', '?')}",
            f"Execution time: {result.get('execution_time', 0):.1f}s",
            f"Estimated cost: ${result.get('estimated_cost', 0):.4f}",
        ])
    elif status.get("status") == "completed":
        lines.extend([
            f"Execution time: {result.get('execution_time', 0):.1f}s",
            f"Total cost: ${result.get('total_cost', 0):.4f}",
            f"Agents: {result.get('agent_count', 'N/A')}",
            f"Documents generated: {result.get('documents_generated', 0)}",
        ])
    elif status.get("status") == "cancelled":
        lines.append("Workflow was cancelled before completion")

    lines.extend([
        "",
        f"Created: {status.get('created_at', 'N/A')}",
        f"Started: {status.get('started_at', 'N/A')}",
        f"Completed: {status.get('completed_at', 'N/A')}",
    ])

    return "\n".join(lines)


def format_results(results: Dict, format_type: str = "markdown") -> str:
    """Format full results for display."""
    if format_type == "json":
        return json.dumps(results, indent=2, default=str)

    if "error" in results:
        return f"Error: {results['error']}"

    lines = [
        "# Research Results",
        "",
        f"**Task ID**: {results.get('task_id', 'N/A')}",
        "",
    ]

    # Executive summary
    if results.get("executive_summary"):
        lines.extend([
            "## Executive Summary",
            "",
            results["executive_summary"],
            "",
        ])

    # Camina synthesis
    if results.get("camina_synthesis"):
        lines.extend([
            "## Final Report",
            "",
            results["camina_synthesis"].get("content", ""),
            "",
        ])

    # Sections
    sections = results.get("sections", [])
    if sections:
        lines.extend(["## Detailed Findings", ""])
        for i, section in enumerate(sections):
            if isinstance(section, dict):
                lines.append(f"### {section.get('title', f'Section {i+1}')}")
                lines.append("")
                lines.append(section.get("content", ""))
            else:
                lines.append(f"### Section {i+1}")
                lines.append("")
                lines.append(str(section))
            lines.append("")

    # Metadata
    meta = results.get("metadata", {})
    if meta:
        lines.extend([
            "## Metadata",
            "",
            f"- Agents: {meta.get('agent_count', 'N/A')}",
            f"- Execution time: {meta.get('execution_time', 0):.1f}s",
            f"- Total cost: ${meta.get('total_cost', 0):.4f}",
        ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Check status of Dream Cascade/Swarm workflows"
    )
    parser.add_argument("task_id", help="Workflow task ID to check (or 'demo' for example)")
    parser.add_argument(
        "--cancel", "-c", action="store_true",
        help="Cancel the workflow"
    )
    parser.add_argument(
        "--results", "-r", action="store_true",
        help="Get full results (for completed workflows)"
    )
    parser.add_argument("--output", "-o", help="Save output to file")
    parser.add_argument(
        "--format", "-f", choices=["text", "json", "markdown"],
        default="text", help="Output format (default: text)"
    )

    args = parser.parse_args()

    # Handle demo mode
    if args.task_id == "demo":
        demo_status = create_mock_workflow("Demo research task")
        output = format_status(demo_status, args.format)
        print(output)
        print(f"\n[DEMO] Use task_id: {demo_status['task_id']} for further commands")
        return

    # Execute requested action
    if args.cancel:
        result = cancel_workflow(args.task_id)
        if args.format == "json":
            output = json.dumps(result, indent=2)
        else:
            output = (
                f"Workflow {args.task_id} cancelled"
                if result.get("cancelled")
                else f"Error: {result.get('error', 'Unknown')}"
            )
    elif args.results:
        result = get_results(args.task_id)
        output = format_results(result, args.format)
    else:
        result = get_status(args.task_id)
        output = format_status(result, args.format)

    # Output
    if args.output:
        Path(args.output).write_text(output)
        print(f"Saved to: {args.output}")
    else:
        print(output)

    # Exit code
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
