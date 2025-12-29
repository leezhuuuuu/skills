#!/usr/bin/env python3
"""
Evaluate pre-training data quality using Dingo.

This script demonstrates how to:
1. Configure input data from HuggingFace
2. Apply rule-based evaluation metrics
3. Process and save evaluation results

Usage:
    python evaluate_pretraining_data.py

Source: Derived from anthropics/skills PR #183 (Apache 2.0 License)
"""

from dingo.config import InputArgs
from dingo.exec import Executor


def evaluate_pretraining_data():
    """Evaluate quality of pre-training dataset."""

    # Configuration for pre-training data evaluation
    input_data = {
        # Input source: HuggingFace dataset
        "input_path": "tatsu-lab/alpaca",
        "dataset": {
            "source": "hugging_face",
            "format": "plaintext"
        },
        # Execution settings
        "executor": {
            # Save failed samples for review
            "result_save": {
                "bad": True,
                "save_dir": "./output/pretraining"
            }
        },
        # Evaluation pipeline
        "evaluator": [
            {
                "evals": [
                    # Basic text quality rules
                    {"name": "RuleColonEnd"},
                    {"name": "RuleSpecialCharacter"},
                    {"name": "RuleEnterAndSpace"},
                    {"name": "RuleEmptyField"},
                    # Content validation
                    {"name": "RuleAbnormalChar"},
                    {"name": "RuleContentLength"}
                ]
            }
        ]
    }

    # Create executor and run evaluation
    input_args = InputArgs(**input_data)
    executor = Executor.exec_map["local"](input_args)

    print("Starting pre-training data evaluation...")
    result = executor.execute()

    # Retrieve and display results
    summary = executor.get_summary()
    bad_data = executor.get_bad_info_list()

    print(f"\nEvaluation Complete!")
    print(f"Total samples: {summary['total']}")
    print(f"Good samples: {summary['num_good']}")
    print(f"Bad samples: {summary['num_bad']}")
    print(f"Quality score: {summary['score']:.2f}%")

    if bad_data:
        print(f"\nFailed samples saved to: ./output/pretraining")

    return result


if __name__ == "__main__":
    evaluate_pretraining_data()
