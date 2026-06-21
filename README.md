# Customer Churn Prediction

## Personal Learnings

While working on this project, I spent significant time understanding the data instead of only training models.

Some important things I learned:

* A feature is useful when it changes the baseline churn probability.
* A feature does not need perfect separation to be useful.
* Churners and non-churners often overlap in the same regions of the feature space.
* Many prediction mistakes come from overlap in the data rather than model choice.
* Logistic Regression performed better than more complex models on this dataset.
* Reducing False Negatives usually increases False Positives.
* Class imbalance affects how the model learns and makes predictions.
* Removing repeated information from features made the data cleaner, but did not automatically improve model performance.
* Understanding why a model makes mistakes is as important as improving accuracy.

## Project Overview

The goal of this project is to predict whether a customer will churn or stay using the Telco Customer Churn dataset.

This project was not only focused on model training. A major part of the work was understanding the data, identifying which features contain useful information, analyzing model errors, and understanding how class imbalance affects predictions.

---

# Dataset Information

Target Variable:

* Churn

  * Yes = Customer left the company
  * No = Customer stayed

Dataset Size:

* Total Customers: 7043

Class Distribution:

| Churn Status | Count |
| ------------ | ----- |
| No           | 5174  |
| Yes          | 1869  |

Baseline Probabilities:

* P(Churn) = 26.5%
* P(Non-Churn) = 73.5%

---

## Phase 1: Data Quality Analysis

Before training any model, I checked the quality of the data.

Things I checked:

* Missing values
* Duplicate rows
* Invalid values
* Inconsistent category names
* Wrong data types

### Findings

I did not find any major data quality issues.

This helped me understand that if the model makes mistakes later, the reason is not bad data quality.

---

# Phase 2: Descriptive Statistics

Numerical Features Analyzed:

* tenure
* MonthlyCharges
* TotalCharges
* SeniorCitizen

Summary Statistics:

| Feature        | Mean    | Std     |
| -------------- | ------- | ------- |
| tenure         | 32.37   | 24.56   |
| MonthlyCharges | 64.76   | 30.09   |
| TotalCharges   | 2279.73 | 2266.79 |

## Observation

The mean is not saying that every customer has that value.

It is only a reference point used to understand where the data is concentrated.

Standard deviation helps measure how spread out customers are from the center.

Descriptive statistics summarize the dataset but do not explain churn by themselves.

---

# Phase 3: Exploratory Data Analysis

## Tenure vs Churn

Customers were divided into tenure groups.

| Tenure Group | Non-Churn | Churn |
| ------------ | --------- | ----- |
| 0-12 Months  | 52.3%     | 47.7% |
| 12-24 Months | 71.3%     | 28.7% |
| 24-48 Months | 79.6%     | 20.4% |
| 48-72 Months | 90.5%     | 9.5%  |

### Observation

The baseline churn rate was 26%.

Customers with tenure between 0 and 12 months had a churn rate of 47.7%, while customers with tenure above 48 months had only 9.5% churn.

This indicates that tenure contains useful information for churn prediction.

---

## Monthly Charges vs Churn

| Monthly Charges Range | Non-Churn | Churn |
| --------------------- | --------- | ----- |
| 18 - 38               | 88.6%     | 11.4% |
| 38 - 58               | 73.0%     | 27.0% |
| 58 - 78               | 70.5%     | 29.5% |
| 78 - 98               | 63.0%     | 37.0% |
| 98 - 118              | 69.9%     | 30.1% |

### Observation:

Customers paying higher monthly charges generally showed higher churn rates compared to the dataset baseline.

---

## Total Charges vs Churn

| Total Charges Range | Non-Churn | Churn |
| ------------------- | --------- | ----- |
| 0 - 1737            | 67.2%     | 32.8% |
| 1737 - 3474         | 75.4%     | 24.6% |
| 3474 - 5211         | 83.3%     | 16.7% |
| 5211 - 6948         | 85.3%     | 14.7% |
| 6948 - 8685         | 89.3%     | 10.7% |

### Observation:

Customers with lower total charges churned more frequently than customers with higher total charges.

---

# Conditional Probability Analysis

One of the main goals of the analysis was to identify features that significantly changed the baseline churn probability.

Example:

Baseline Churn Rate:

* 26.5%

InternetService Analysis:

| Internet Service | Non-Churn | Churn |
| ---------------- | --------- | ----- |
| DSL              | 81.0%     | 19.0% |
| Fiber Optic      | 58.1%     | 41.9% |
| No Internet      | 92.6%     | 7.4%  |

### Observation:

Fiber optic customers churned much more frequently than the baseline rate.

Customers without internet service had very low churn rates.

This showed that InternetService contains strong predictive information.

---

# Feature Engineering

During analysis, repeated information was identified.

Examples:

* OnlineSecurity = No internet service
* OnlineBackup = No internet service
* DeviceProtection = No internet service
* TechSupport = No internet service
* StreamingTV = No internet service
* StreamingMovies = No internet service

These categories repeated the information already present in InternetService.

Feature engineering was performed to remove this duplication and create cleaner features.

## Result:

The model performance changed very little.

This taught me that removing duplicated information does not automatically improve accuracy.

Sometimes it only creates a cleaner representation of the same information.

---

# Models Evaluated

Models Trained:

1. Logistic Regression
2. Support Vector Machine (SVC)
3. Decision Tree
4. Random Forest
5. AdaBoost
6. XGBoost


### Observation

Logistic Regression consistently performed the best on this dataset.

This taught me that a simple model can outperform complex models when the data already contains useful signal

---

# Error Analysis

Initial Logistic Regression Confusion Matrix:

```text
[[1154 128]
 [ 201 278]]
```

Interpretation:

* True Negatives = 1154
* False Positives = 128
* False Negatives = 201
* True Positives = 278

### Findings

False Negatives often looked similar to True Negatives.

This means many churn customers shared characteristics with customers who stayed.

Many model mistakes were caused by overlap in the data rather than model complexity.

---

# Class Imbalance Experiment

Dataset Distribution:

* Non-Churn = 74%
* Churn = 26%

To reduce False Negatives, Logistic Regression was retrained using:

```python
class_weight="balanced"
```

Confusion Matrix:

```text
[[934 348]
 [ 80 399]]
```

Comparison:

| Metric          | Original | Balanced |
| --------------- | -------- | -------- |
| False Negatives | 201      | 80       |
| False Positives | 128      | 348      |

Observation:

Balancing the classes significantly reduced False Negatives.

However, this came at the cost of a large increase in False Positives.

This demonstrated the tradeoff between catching more churners and incorrectly flagging loyal customers.

---

## Main Lessons Learned

I learned:

* How to perform Data Quality Analysis.
* How to use Descriptive Statistics.
* How to perform Exploratory Data Analysis.
* How to use Conditional Probability to evaluate features.
* Why overlap creates prediction errors.
* Why class imbalance affects model behavior.
* Why a feature can be useful even when overlap exists.
* Why a simple model can sometimes beat complex models.
* How to analyze False Positives and False Negatives.
* How feature engineering does not always improve performance.

---

# Final Conclusion

The main challenge in this dataset was not model complexity but overlap between churners and non-churners.

Several features such as tenure, InternetService, MonthlyCharges, and TotalCharges provided useful information, but none could perfectly separate the classes.

Experiments with balancing techniques showed that improving recall for churn customers increased False Positives, highlighting the tradeoff between different types of prediction errors.

This project helped build a deeper understanding of data analysis, feature evaluation, class imbalance, model behavior, and error analysis rather than focusing only on model accuracy.
