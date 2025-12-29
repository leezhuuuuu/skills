#!/usr/bin/env python3
"""
Evaluate RAG system quality using Dingo.

This script demonstrates how to:
1. Configure RAG evaluation with academic metrics
2. Evaluate faithfulness, relevancy, precision, and recall
3. Generate quality reports for RAG pipelines

Usage:
    python evaluate_rag_system.py

Source: Derived from anthropics/skills PR #183 (Apache 2.0 License)
"""

from dingo.config import InputArgs
from dingo.exec import Executor


def evaluate_rag_system():
    """Evaluate RAG system quality using academic metrics."""

    # Configuration for RAG evaluation
    input_data = {
        # Input source: local JSONL file with RAG data
        "input_path": "path/to/rag_data.jsonl",
        "dataset": {
            "source": "local",
            "format": "jsonl"
        },
        "executor": {
            "result_save": {
                "bad": True,
                "save_dir": "./output/rag_evaluation"
            }
        },
        # RAG-specific evaluation metrics
        "evaluator": [
            {
                "evals": [
                    # Core RAG metrics from academic research
                    {"name": "RAGEvaluation"},
                    # Faithfulness: Does the answer align with the context?
                    {"name": "Faithfulness"},
                    # Answer Relevancy: Is the answer relevant to the question?
                    {"name": "AnswerRelevancy"},
                    # Context Precision: Is the retrieved context precise?
                    {"name": "ContextPrecision"},
                    # Context Recall: Does the context contain the answer?
                    {"name": "ContextRecall"},
                    # Additional quality checks
                    {"name": "AnswerCorrectness"},
                    {"name": "AnswerSimilarity"}
                ]
            }
        ]
    }

    # Create executor and run evaluation
    input_args = InputArgs(**input_data)
    executor = Executor.exec_map["local"](input_args)

    print("Starting RAG system evaluation...")
    result = executor.execute()

    # Retrieve and display results
    summary = executor.get_summary()
    bad_data = executor.get_bad_info_list()

    print(f"\nRAG Evaluation Complete!")
    print(f"Total test cases: {summary['total']}")
    print(f"Passed cases: {summary['num_good']}")
    print(f"Failed cases: {summary['num_bad']}")
    print(f"Overall quality score: {summary['score']:.2f}%")

    # Display breakdown by metric type
    if 'type_ratio' in summary:
        print("\nMetric breakdown:")
        for field, metrics in summary['type_ratio'].items():
            print(f"  {field}:")
            for metric, ratio in metrics.items():
                print(f"    - {metric}: {ratio:.2%}")

    if bad_data:
        print(f"\nFailed samples saved to: ./output/rag_evaluation")

    return result


if __name__ == "__main__":
    evaluate_rag_system()
