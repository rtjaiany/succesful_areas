# Phase 4: Machine Learning Modeling

## Overview

This phase trains, evaluates, and deploys machine learning models.

## Purpose

- Train models for clustering, regression, or classification
- Evaluate model performance
- Make predictions
- Save trained models for deployment

## Key Scripts

### `train.py` (To Implement)

Trains machine learning models.

**Usage:**

```bash
python src/4_modeling/train.py \
    --data data/features/transformed_features.csv \
    --model clustering \
    --config config/model_config.yaml \
    --output models/trained/clustering_model.pkl
```

### `evaluate.py` (To Implement)

Evaluates model performance.

**Metrics:**

- Clustering: Silhouette score, Davies-Bouldin index
- Regression: RMSE, MAE, R²
- Classification: Accuracy, F1, ROC-AUC

### `predict.py` (To Implement)

Makes predictions using trained models.

## Model Types

### 1. Clustering Models (`models/clustering.py`)

**Purpose**: Group similar municipalities

**Algorithms:**

- K-Means
- DBSCAN
- Hierarchical Clustering
- Gaussian Mixture Models

**Use Cases:**

- Identify municipality types
- Find similar regions
- Detect anomalies

### 2. Regression Models (`models/regression.py`)

**Purpose**: Predict continuous outcomes

**Algorithms:**

- Linear Regression
- Random Forest Regressor
- Gradient Boosting
- Neural Networks

**Use Cases:**

- Predict economic indicators
- Forecast population growth
- Estimate environmental metrics

### 3. Classification Models (`models/classification.py`)

**Purpose**: Categorize municipalities

**Algorithms:**

- Logistic Regression
- Random Forest Classifier
- XGBoost
- Neural Networks

**Use Cases:**

- Classify development levels
- Predict risk categories
- Identify intervention needs

## Workflow

```bash
# 1. Train model
python src/4_modeling/train.py --model clustering --config config/model_config.yaml

# 2. Evaluate model
python src/4_modeling/evaluate.py --model models/trained/clustering_model.pkl

# 3. Make predictions
python src/4_modeling/predict.py \
    --model models/trained/clustering_model.pkl \
    --data data/features/new_data.csv \
    --output outputs/predictions.csv
```

## Model Configuration

**File**: `config/model_config.yaml`

```yaml
clustering:
    algorithm: kmeans
    n_clusters: 5
    random_state: 42

regression:
    algorithm: random_forest
    n_estimators: 100
    max_depth: 10

classification:
    algorithm: xgboost
    n_estimators: 100
    learning_rate: 0.1
```

## Output

**Location**: `models/trained/`

**Files:**

- `{model_name}.pkl` - Trained model
- `{model_name}_metrics.json` - Performance metrics
- `{model_name}_config.yaml` - Model configuration

## Best Practices

1. **Cross-validation** - Use k-fold CV for robust evaluation
2. **Hyperparameter tuning** - Grid search or Bayesian optimization
3. **Feature importance** - Analyze which features matter most
4. **Model versioning** - Track model versions and performance
5. **Reproducibility** - Set random seeds

## Next Steps

1. Implement clustering models
2. Add model evaluation framework
3. Create hyperparameter tuning pipeline
4. Build model comparison dashboard
