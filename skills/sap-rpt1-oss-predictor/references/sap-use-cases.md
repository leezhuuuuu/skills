# SAP Use Cases for RPT-1-OSS

> **Source**: Derived from anthropics/skills PR #181 (Apache 2.0 License)

This document describes common SAP business scenarios where RPT-1-OSS can be applied.

## Financial Accounting (FI)

### FI-AR: Payment Default Prediction

**Use Case**: Predict probability of customer payment default

**Related Tables**:
- `BSID` - Customer Documents (India)
- `BSAD` - Customer Documents (Cleared)
- `KNA1` - Customer Master

**Features to Extract**:
- Days Sales Outstanding (DSO)
- Payment history patterns
- Credit utilization
- Customer age and segment

**Target**: Payment status (PAID / DEFAULT)

### FI-GL: Journal Entry Anomaly Detection

**Use Case**: Detect unusual journal entries

**Related Tables**:
- `ACDOCA` - Universal Journal Entry
- `BKPF` - Document Header

**Features**:
- Document amounts
- Posting dates
- Account combinations
- Transaction types

**Target**: Anomaly score (normal / suspicious)

## Sales and Distribution (SD)

### SD: Delivery Delay Prediction

**Use Case**: Predict potential delivery delays

**Related Tables**:
- `VBAK` - Sales Order Header
- `VBAP` - Sales Order Item
- `LIKP` - Delivery Header

**Features**:
- Order to delivery time
- Shipping point capacity
- Material availability
- Customer priority

**Target**: Days of delay (regression)

### SD: Customer Churn Analysis

**Use Case**: Identify at-risk customers

**Related Tables**:
- `VBRK` - Billing Document Header
- `VBRP` - Billing Document Item
- `KNA1` - Customer Master

**Features**:
- Order frequency
- Revenue trends
- Payment behavior
- Complaint frequency

**Target**: Churn status (ACTIVE / AT_RISK / CHURNED)

## Materials Management (MM)

### MM: Supplier Performance Scoring

**Use Case**: Score supplier reliability

**Related Tables**:
- `EKKO` - Purchase Order Header
- `EKPO` - Purchase Order Item
- `EBAN` - Purchase Requisition

**Features**:
- On-time delivery rate
- Quality rejections
- Price variances
- Contract compliance

**Target**: Performance score (regression)

## Production Planning (PP)

### PP: Production Delay Risk

**Use Case**: Identify production orders at risk

**Related Tables**:
- `AFKO` - Production Order Header
- `AFPO` - Production Order Item

**Features**:
- Material availability
- Capacity utilization
- Operation progress
- Quality issues

**Target**: Delay risk (probability)

## Data Preparation Tips

### Technical to Semantic Mapping

```python
# Before: SAP technical field names
df = pd.read_csv("sap_extract.csv")
# Columns: KUNAG, FKORG, FKDAT, NETWR, ...

# After: Semantic field names
df = df.rename(columns={
    "KUNAG": "CUSTOMER_NUMBER",
    "FKORG": "SALES_ORGANIZATION",
    "FKDAT": "BILLING_DATE",
    "NETWR": "NET_VALUE",
    # ...
})
# Better accuracy with semantic names
```

### Feature Engineering

1. **Temporal Features**:
   - Days since last order
   - Order frequency (last 3/6/12 months)
   - Revenue trend (YoY, MoM)

2. **Aggregated Features**:
   - Average order value
   - Total revenue
   - Payment delay average

3. **Derived Features**:
   - Credit utilization ratio
   - Customer lifetime value
   - Risk score composite

## Model Configuration by Use Case

| Use Case | Context Size | Bagging | GPU Memory |
|----------|--------------|---------|------------|
| Payment Default | 4096 | 4 | 40GB |
| Churn Prediction | 4096 | 4 | 40GB |
| Delivery Delay | 2048 | 2 | 24GB |
| Anomaly Detection | 4096 | 4 | 40GB |
