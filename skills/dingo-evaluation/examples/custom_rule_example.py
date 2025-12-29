#!/usr/bin/env python3
"""
Custom rule registration example for Dingo.

This script demonstrates how to:
1. Register domain-specific quality rules
2. Create custom evaluation logic
3. Integrate custom rules into the evaluation pipeline

Usage:
    python custom_rule_example.py

Source: Derived from anthropics/skills PR #183 (Apache 2.0 License)
"""

from dingo.model import Model
from dingo.model.rule.base import BaseRule
from dingo.io import Data, InputDataset
from dingo.config import InputArgs
from dingo.exec import Executor


# Example 1: Domain-specific validation rule
@Model.rule_register('QUALITY_BAD_DOMAIN_SPECIFIC', ['default'])
class DomainSpecificRule(BaseRule):
    """Custom rule for domain-specific validation."""

    @classmethod
    def eval(cls, input_data: Data) -> dict:
        """
        Evaluate data against domain-specific rules.

        Args:
            input_data: Input data containing the content to validate

        Returns:
            dict with evaluation result containing:
                - metric: Rule name
                - status: True if passes, False if fails
                - label: Quality category
                - reason: Explanation of the result
        """
        content = input_data.content if hasattr(input_data, 'content') else ""

        # Your domain-specific validation logic here
        # Example: Check for specific patterns, formats, etc.

        # Simple example: content must be non-empty and reasonable length
        is_valid = bool(content) and 10 < len(content) < 10000

        return {
            "metric": cls.__name__,
            "status": not is_valid,  # status True means bad quality
            "label": ['QUALITY_GOOD' if is_valid else 'QUALITY_BAD_DOMAIN_SPECIFIC'],
            "reason": [
                "Content validation passed" if is_valid
                else f"Content failed validation: empty={not bool(content)}, length={len(content)}"
            ]
        }


# Example 2: Custom LLM-based evaluator
@Model.llm_register('CustomLLMEvaluator')
class CustomLLMEvaluator:
    """Custom LLM-based quality evaluator."""

    # Define metric metadata
    _metric_info = {
        "metric_name": "CustomLLMEvaluator",
        "metric_type": "LLM-Based Quality",
        "category": "Custom Category"
    }

    # Custom prompt for evaluation
    prompt = """You are a quality expert. Evaluate the following content.

Content: {content}

Rate the quality on a scale of 1-5. Return only the numeric rating."""

    @classmethod
    def eval(cls, input_data: Data) -> dict:
        """Evaluate content using custom LLM prompt."""
        # Implementation would call LLM with custom prompt
        # This is a simplified example
        content = input_data.content if hasattr(input_data, 'content') else ""

        # Placeholder: actual implementation would call LLM API
        score = 4  # Would be replaced with actual LLM call

        return {
            "metric": cls.__name__,
            "status": score >= 3,
            "label": [f"quality_score_{score}"],
            "reason": [f"LLM quality score: {score}/5"]
        }


def evaluate_with_custom_rules():
    """Run evaluation using custom rules."""

    # Configuration with custom rules
    input_data = {
        "input_path": "path/to/data.jsonl",
        "dataset": {"source": "local", "format": "jsonl"},
        "executor": {
            "result_save": {
                "bad": True,
                "save_dir": "./output/custom_rules"
            }
        },
        "evaluator": [
            {
                "evals": [
                    # Built-in rules
                    {"name": "RuleEmptyField"},
                    {"name": "RuleDuplicateRow"},
                    # Custom domain-specific rule
                    {"name": "DomainSpecificRule"},
                    # Custom LLM evaluator
                    {"name": "CustomLLMEvaluator"}
                ]
            }
        ]
    }

    input_args = InputArgs(**input_data)
    executor = Executor.exec_map["local"](input_args)

    print("Running evaluation with custom rules...")
    result = executor.execute()

    summary = executor.get_summary()
    print(f"\nEvaluation Complete!")
    print(f"Total: {summary['total']}, Good: {summary['num_good']}, Bad: {summary['num_bad']}")
    print(f"Score: {summary['score']:.2f}%")

    return result


if __name__ == "__main__":
    evaluate_with_custom_rules()
