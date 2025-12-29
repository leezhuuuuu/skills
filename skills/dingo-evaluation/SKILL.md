---
name: dingo-evaluation
description: AI data quality assessment for datasets, RAG systems, and hallucination detection using Dingo. Use when Claude needs to evaluate data quality for ML training, validate RAG systems, or detect AI hallucinations. Supports rule-based, LLM-based, and hybrid evaluation strategies with 70+ metrics across multiple data sources.
---

# Dingo Evaluation Skill

> **Source**: This skill is derived from [anthropics/skills PR #183](https://github.com/anthropics/skills/pull/183) by @e06084. Based on the [Dingo](https://github.com/MigoXLab/dingo) project (Apache 2.0 License).

Use Dingo to assess and improve the quality of datasets, RAG systems, and AI applications. Dingo provides 70+ evaluation metrics spanning pre-training data quality, SFT data quality, RAG evaluation, and hallucination detection.

## Quick Start

Install the Dingo Python SDK:

```bash
pip install dingo-python
```

## Core Evaluation Strategies

### Rule-Based Evaluation

For fast, deterministic checks on large datasets:

```python
from dingo.config import InputArgs
from dingo.exec import Executor

input_data = {
    "input_path": "path/to/your/data.jsonl",
    "executor": {"result_save": {"bad": True}},
    "evaluator": [
        {"evals": [
            {"name": "RuleColonEnd"},
            {"name": "RuleSpecialCharacter"},
            {"name": "RuleEnterAndSpace"}
        ]}
    ]
}

input_args = InputArgs(**input_data)
executor = Executor.exec_map["local"](input_args)
result = executor.execute()
```

### LLM-Based Evaluation

For deep semantic analysis of content quality:

```python
from dingo.config.input_args import EvaluatorLLMArgs
from dingo.io.input import Data
from dingo.model.llm.text_quality.llm_text_quality_v5 import LLMTextQualityV5

data = Data(
    data_id='123',
    prompt="hello, introduce the world",
    content="Hello! The world is a vast and diverse place..."
)

LLMTextQualityV5.dynamic_config = EvaluatorLLMArgs(
    key='YOUR_API_KEY',
    api_url='https://api.openai.com/v1/chat/completions',
    model='gpt-4o',
)
res = LLMTextQualityV5.eval(data)
```

### Hybrid Strategy

Combine rule-based and LLM-based evaluation for cost-effective quality assurance:

```python
# Rules catch obvious issues (100% of data)
# LLM provides deep analysis (sampled subset)
evaluator = [
    {"evals": [
        {"name": "RuleEmptyField"},
        {"name": "RuleDuplicateRow"},
        {"name": "RuleRegexMatch", "params": {"pattern": r"^[a-zA-Z]"}}
    ]},
    {"evals": [
        {"name": "LLMTextQualityV5", "params": {"sample_rate": 0.1}}
    ]}
]
```

## RAG System Evaluation

Evaluate retrieval-augmented generation systems using academic metrics:

```python
from dingo.config import InputArgs
from dingo.exec import Executor

input_data = {
    "input_path": "path/to/rag_data.jsonl",
    "evaluator": [
        {"evals": [
            {"name": "RAGEvaluation"},
            {"name": "Faithfulness"},
            {"name": "AnswerRelevancy"},
            {"name": "ContextPrecision"},
            {"name": "ContextRecall"}
        ]}
    ]
}

input_args = InputArgs(**input_data)
executor = Executor.exec_map["local"](input_args)
result = executor.execute()
```

## Multi-Field Evaluation

Apply different rules to different fields in your data:

```python
input_data = {
    "input_path": "path/to/data.jsonl",
    "evaluator": [
        {"fields": {"content": "isbn"}, "evals": [{"name": "RuleIsbn"}]},
        {"fields": {"content": "title"}, "evals": [{"name": "RuleAbnormalChar"}]},
        {"fields": {"content": "description"}, "evals": [{"name": "LLMTextQualityV5"}]},
        {"fields": {"content": "category"}, "evals": [{"name": "RuleValidCategory"}]}
    ]
}
```

## Data Source Support

### Local Files

```python
# JSONL, CSV, TXT, Parquet
input_data = {
    "input_path": "path/to/data.jsonl",
    "dataset": {"source": "local", "format": "jsonl"}
}
```

### HuggingFace Datasets

```python
input_data = {
    "input_path": "tatsu-lab/alpaca",
    "dataset": {"source": "hugging_face", "format": "plaintext"}
}
```

### SQL Databases

```python
input_data = {
    "input_path": "postgresql://user:pass@localhost:5432/db",
    "dataset": {"source": "sql", "table": "your_table"}
}
```

### AWS S3

```python
input_data = {
    "input_path": "s3://bucket/path/to/data.jsonl",
    "dataset": {"source": "s3"}
}
```

## Custom Rules

Register domain-specific quality rules:

```python
from dingo.model import Model
from dingo.model.rule.base import BaseRule
from dingo.io import InputDataset, Data

@Model.rule_register('QUALITY_BAD_MY_RULE', ['default'])
class MyCustomRule(BaseRule):
    @classmethod
    def eval(cls, input_data: Data) -> dict:
        # Your custom validation logic
        is_valid = validate_domain_specific(input_data.content)
        return {
            "metric": cls.__name__,
            "status": not is_valid,
            "label": ['QUALITY_GOOD' if is_valid else 'QUALITY_BAD_MY_RULE'],
            "reason": ["Reason for the result"]
        }
```

## Large-Scale Processing

For production workloads with billions of records:

```python
from dingo.config import InputArgs
from dingo.exec import Executor

input_args = InputArgs(**input_data)
executor = Executor.exec_map["spark"](
    input_args,
    spark_session=your_spark_session,
    spark_rdd=your_data_rdd
)
result = executor.execute()
```

## Evaluation Metrics Reference

| Category | Metrics |
|----------|---------|
| Pre-training Text | Completeness, validity, similarity, safety |
| SFT Data | Helpfulness, honesty, harmlessness (3H) |
| RAG Evaluation | Faithfulness, context precision, answer relevancy |
| Hallucination | HHEM-2.1-Open, factuality checks |
| Classification | Topic classification, content labeling |
| Multi-modal | Image-text relevance, VLM quality |
| Security | PII detection, toxicity detection |

## Examples

See the `examples/` directory for complete, production-ready scripts:

- `examples/evaluate_pretraining_data.py` - Pre-training data validation
- `examples/evaluate_rag_system.py` - RAG system quality assessment
- `examples/custom_rule_example.py` - Custom rule registration patterns

## Resources

- **GitHub**: https://github.com/MigoXLab/dingo
- **PyPI**: https://pypi.org/project/dingo-python/
- **Documentation**: https://github.com/MigoXLab/dingo/blob/main/README.md
