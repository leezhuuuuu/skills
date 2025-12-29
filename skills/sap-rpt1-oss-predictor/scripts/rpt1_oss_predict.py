#!/usr/bin/env python3
"""
SAP RPT-1-OSS Predictor Wrapper.

This script provides a simple interface for classification and regression
predictions using the SAP RPT-1-OSS model.

Usage:
    python scripts/rpt1_oss_predict.py --task classification --data data.csv --target CHURN_STATUS
    python scripts/rpt1_oss_predict.py --task regression --data data.csv --target DELAY_DAYS

Source: Derived from anthropics/skills PR #181 (Apache 2.0 License)
"""

import argparse
import pandas as pd
import sys

try:
    from sap_rpt_oss import SAP_RPT_OSS_Classifier, SAP_RPT_OSS_Regressor
except ImportError:
    print("Error: sap_rpt_oss not installed.")
    print("Run: pip install git+https://github.com/SAP-samples/sap-rpt-1-oss")
    sys.exit(1)


def load_data(data_path):
    """Load CSV data."""
    try:
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} rows from {data_path}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def run_classification(data_path, target_column, output_path=None, max_context=4096, bagging=4):
    """Run classification prediction."""
    df = load_data(data_path)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Simple train/test split
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples")

    # Initialize and fit model
    model = SAP_RPT_OSS_Classifier(max_context_size=max_context, bagging=bagging)
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    # Print results
    print(f"\nPredictions: {len(predictions)}")
    print(f"Unique classes: {list(model.classes_)}")

    if output_path:
        results_df = X_test.copy()
        results_df['actual'] = y_test
        results_df['predicted'] = predictions
        results_df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")

    return predictions


def run_regression(data_path, target_column, output_path=None, max_context=4096, bagging=4):
    """Run regression prediction."""
    df = load_data(data_path)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Simple train/test split
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples")

    # Initialize and fit model
    model = SAP_RPT_OSS_Regressor(max_context_size=max_context, bagging=bagging)
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)

    # Print results
    print(f"\nPredictions: {len(predictions)}")
    print(f"Mean prediction: {predictions.mean():.2f}")
    print(f"Std prediction: {predictions.std():.2f}")

    if output_path:
        results_df = X_test.copy()
        results_df['actual'] = y_test
        results_df['predicted'] = predictions
        results_df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")

    return predictions


def main():
    parser = argparse.ArgumentParser(
        description="SAP RPT-1-OSS Predictor"
    )
    parser.add_argument(
        '--task', '-t',
        choices=['classification', 'regression'],
        required=True,
        help="Prediction task type"
    )
    parser.add_argument(
        '--data', '-d',
        required=True,
        help="Path to CSV data file"
    )
    parser.add_argument(
        '--target', '-y',
        required=True,
        help="Target column name"
    )
    parser.add_argument(
        '--output', '-o',
        help="Output path for predictions"
    )
    parser.add_argument(
        '--max-context',
        type=int,
        default=4096,
        help="Maximum context size (default: 4096)"
    )
    parser.add_argument(
        '--bagging', '-b',
        type=int,
        default=4,
        help="Number of bagging iterations (default: 4)"
    )

    args = parser.parse_args()

    if args.task == 'classification':
        run_classification(
            args.data, args.target,
            output_path=args.output,
            max_context=args.max_context,
            bagging=args.bagging
        )
    else:
        run_regression(
            args.data, args.target,
            output_path=args.output,
            max_context=args.max_context,
            bagging=args.bagging
        )


if __name__ == "__main__":
    main()
