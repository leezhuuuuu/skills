---
name: sap-rpt1-oss-predictor
description: Predict tabular business data using SAP RPT-1-OSS model. Use for customer churn prediction, payment default detection, delivery delay forecasting, and other tabular prediction tasks on SAP business data.
---

# SAP RPT-1-OSS Predictor

> **Source**: This skill is derived from [anthropics/skills PR #181](https://github.com/anthropics/skills/pull/181) by @amitlals. Based on [SAP RPT-1-OSS](https://github.com/SAP-samples/sap-rpt-1-oss) (Apache 2.0 License).

Predict tabular business data using SAP's open-source RPT-1-OSS model. This skill enables Claude to perform classification and regression predictions on structured business data without training custom models.

## Installation

```bash
# Install from GitHub
pip install git+https://github.com/SAP-samples/sap-rpt-1-oss

# Install HuggingFace utilities
pip install huggingface_hub

# Login to HuggingFace (required for model access)
huggingface-cli login
```

**Important**: Accept the model license at https://huggingface.co/SAP/sap-rpt-1-oss

## Quick Start

### Classification (Customer Churn Prediction)

```python
import pandas as pd
from sap_rpt_oss import SAP_RPT_OSS_Classifier

# Load data
df = pd.read_csv("customer_data.csv")
X = df.drop(columns=["CHURN_STATUS"])
y = df["CHURN_STATUS"]

# Split data
X_train, X_test = X[:400], X[400:]
y_train, y_test = y[:400], y[400:]

# Predict
clf = SAP_RPT_OSS_Classifier(max_context_size=4096, bagging=4)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
probabilities = clf.predict_proba(X_test)
```

### Regression (Delivery Delay Prediction)

```python
from sap_rpt_oss import SAP_RPT_OSS_Regressor

reg = SAP_RPT_OSS_Regressor(max_context_size=4096, bagging=4)
reg.fit(X_train, y_train)
predictions = reg.predict(X_test)
```

## Use Cases

### SAP Business Scenarios

| Module | Use Case | SAP Tables |
|--------|----------|------------|
| FI-AR | Payment Default Risk | BSID, BSAD, KNA1 |
| FI-GL | Journal Entry Anomaly | ACDOCA, BKPF |
| SD | Delivery Delay Prediction | VBAK, VBAP, LIKP |
| SD | Customer Churn Analysis | VBRK, VBRP, KNA1 |
| MM | Supplier Performance | EKKO, EKPO, EBAN |
| PP | Production Delay Risk | AFKO, AFPO |

### Supported Task Types

| Task | Description |
|------|-------------|
| **Classification** | Customer churn, payment default, fraud detection |
| **Regression** | Delivery delay, demand forecasting, anomaly scores |

## Hardware Requirements

| GPU Memory | Context Size | Bagging | Use Case |
|------------|--------------|---------|----------|
| 80GB (A100) | 8192 | 8 | Production |
| 40GB (A6000) | 4096 | 4 | Balanced |
| 24GB (RTX 4090) | 2048 | 2 | Development |
| CPU only | 1024 | 1 | Testing only |

## Data Requirements

| Parameter | Requirement |
|-----------|-------------|
| Min samples | 50 rows |
| Recommended | 200-500 rows |
| Max context | 8192 rows (GPU dependent) |
| Column naming | Semantic names improve accuracy |

## Example Workflow

### 1. Prepare SAP Data

```python
# Convert SAP technical fields to semantic names
from scripts.prepare_sap_data import prepare_customer_churn_data

df = prepare_customer_churn_data(sap_table_data)
df.to_csv("customer_churn_sample.csv", index=False)
```

### 2. Run Batch Prediction

```python
from scripts.batch_predict import run_classification

results = run_classification(
    data_path="examples/customer_churn_sample.csv",
    target_column="CHURN_STATUS",
    output_path="output/predictions.csv"
)
```

### 3. Evaluate Results

```python
from sklearn.metrics import classification_report, accuracy_score

print(classification_report(y_test, predictions))
print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")
```

## Sample Data Format

### Customer Churn Prediction

```
CUSTOMER_NUMBER,CUSTOMER_NAME,COUNTRY,ACCOUNT_GROUP,CREDIT_LIMIT,
ORDERS_LAST_12M,REVENUE_LAST_12M,DAYS_SINCE_LAST_ORDER,AVG_ORDER_VALUE,
AVG_PAYMENT_DELAY,LATE_PAYMENTS_COUNT,CREDIT_UTILIZATION,CHURN_STATUS

Target values: ACTIVE, AT_RISK, CHURNED, [PREDICT]
```

### Payment Default Prediction

```
CUSTOMER_NUMBER,COMPANY_CODE,DOCUMENT_NUMBER,FISCAL_YEAR,INVOICE_AMOUNT,
CURRENCY,PAYMENT_TERMS_DAYS,CREDIT_LIMIT,OUTSTANDING_BALANCE,
HIST_AVG_DELAY,HIST_SEVERE_DELAYS,CUSTOMER_AGE_DAYS,INDUSTRY_CODE,PAYMENT_STATUS

Target values: PAID, DEFAULT, [PREDICT]
```

## Limitations

- **Tabular data only** - Does not support images or documents
- **Requires labeled data** - In-context learning needs training samples
- **First prediction slow** - Model loading time
- **GPU recommended** - CPU mode is very slow for production

## Resources

- **SAP RPT-1-OSS GitHub**: https://github.com/SAP-samples/sap-rpt-1-oss
- **Model on HuggingFace**: https://huggingface.co/SAP/sap-rpt-1-oss
- **SAP Use Cases**: See `references/sap-use-cases.md`
- **API Reference**: See `references/api-reference.md`
