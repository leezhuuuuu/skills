# Dingo Evaluation Skill

> **Source**: This skill is derived from [anthropics/skills PR #183](https://github.com/anthropics/skills/pull/183) by @e06084. Based on the [Dingo](https://github.com/MigoXLab/dingo) project (Apache 2.0 License).

AI 数据质量评估工具，支持预训练数据、RAG 系统和幻觉检测。

## 安装

```bash
pip install dingo-python
```

## 快速开始

### 规则基础评估

```python
from dingo.config import InputArgs
from dingo.exec import Executor

input_data = {
    "input_path": "path/to/data.jsonl",
    "evaluator": [
        {"evals": [
            {"name": "RuleColonEnd"},
            {"name": "RuleSpecialCharacter"}
        ]}
    ]
}

input_args = InputArgs(**input_data)
executor = Executor.exec_map["local"](input_args)
result = executor.execute()
```

### LLM 深度评估

```python
from dingo.config.input_args import EvaluatorLLMArgs
from dingo.io.input import Data
from dingo.model.llm.text_quality.llm_text_quality_v5 import LLMTextQualityV5

data = Data(
    data_id='123',
    prompt="hello",
    content="Hello! The world is vast..."
)

LLMTextQualityV5.dynamic_config = EvaluatorLLMArgs(
    key='YOUR_API_KEY',
    api_url='https://api.openai.com/v1/chat/completions',
    model='gpt-4o',
)
res = LLMTextQualityV5.eval(data)
```

## 示例脚本

- `examples/evaluate_pretraining_data.py` - 预训练数据评估
- `examples/evaluate_rag_system.py` - RAG 系统评估
- `examples/custom_rule_example.py` - 自定义规则

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。

## 资源

- **Dingo GitHub**: https://github.com/MigoXLab/dingo
- **PyPI**: https://pypi.org/project/dingo-python/
