# SAP RPT-1-OSS Predictor

> **Source**: This skill is derived from [anthropics/skills PR #181](https://github.com/anthropics/skills/pull/181) by @amitlals. Based on [SAP RPT-1-OSS](https://github.com/SAP-samples/sap-rpt-1-oss) (Apache 2.0 License).

使用 SAP 开源的 RPT-1-OSS 模型进行表格数据预测。

## 安装

```bash
pip install git+https://github.com/SAP-samples/sap-rpt-1-oss
pip install huggingface_hub
huggingface-cli login
```

## 快速使用

### 分类预测（客户流失）

```python
from sap_rpt_oss import SAP_RPT_OSS_Classifier

clf = SAP_RPT_OSS_Classifier(max_context_size=4096, bagging=4)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
```

### 回归预测（交付延迟）

```python
from sap_rpt_oss import SAP_RPT_OSS_Regressor

reg = SAP_RPT_OSS_Regressor(max_context_size=4096, bagging=4)
reg.fit(X_train, y_train)
predictions = reg.predict(X_test)
```

## SAP 业务场景

| 模块 | 用例 | SAP 表 |
|------|------|--------|
| FI-AR | 付款违约风险 | BSID, BSAD |
| SD | 交付延迟预测 | VBAK, VBAP |
| SD | 客户流失分析 | VBRK, VBRP |
| MM | 供应商绩效 | EKKO, EKPO |

## 硬件要求

| GPU 显存 | 上下文大小 | 用途 |
|----------|------------|------|
| 80GB (A100) | 8192 | 生产环境 |
| 40GB (A6000) | 4096 | 均衡之选 |
| 24GB (RTX 4090) | 2048 | 开发测试 |

## 文档

完整文档请查看 [SKILL.md](SKILL.md)。

## 资源

- [SAP RPT-1-OSS GitHub](https://github.com/SAP-samples/sap-rpt-1-oss)
- [HuggingFace 模型](https://huggingface.co/SAP/sap-rpt-1-oss)
