# MultilingualSentX Dataset

## Overview

This directory contains the datasets used for multilingual and code-mixed product review sentiment analysis in the **MultilingualSentX** project.

The dataset focuses on product reviews written in:

* English
* Hindi
* Marathi
* Hindi-English code-mixed text
* Marathi-English code-mixed text
* Hindi-Marathi code-mixed text
* Hindi-English-Marathi code-mixed text

The primary objective is to support sentiment analysis and aspect-based analysis of Indian multilingual product reviews.

---

## Dataset Structure

```text
data/
├── raw/
│   ├── codemix_product_reviews_60k.csv
│   └── starter_product_reviews_600.csv
│
└── README.md
```

### Raw Dataset

#### `codemix_product_reviews_60k.csv`

This is the primary dataset used for model development and experimentation.

* Records: **60,000**
* Sentiment classes: **Positive, Negative, Neutral**
* Sentiment distribution:

  * Positive: 20,000
  * Negative: 20,000
  * Neutral: 20,000
* Contains English, Hindi, Marathi and code-mixed reviews.
* Contains product-related reviews and aspect information.
* The dataset includes language/script metadata and annotation information.

Important columns include:

| Column               | Description                                |
| -------------------- | ------------------------------------------ |
| `comment_id`         | Unique identifier for each review          |
| `raw_comment`        | Original review text                       |
| `normalized_comment` | Normalized version of the review           |
| `language_pattern`   | Language combination present in the review |
| `script_mix`         | Script information                         |
| `emoji_present`      | Whether the review contains emojis         |
| `emoji_count`        | Number of emojis                           |
| `emoji_tokens`       | Extracted emoji information                |
| `sentiment`          | Positive, Negative or Neutral              |
| `aspect`             | Main product aspect discussed              |
| `aspect_sentiment`   | Sentiment associated with the aspect       |
| `source_type`        | Source/category of the data                |
| `data_origin`        | Origin of the review                       |
| `product_review`     | Indicates product-review content           |
| `annotation_status`  | Annotation/validation status               |
| `split`              | Dataset split information                  |

---

### Starter Dataset

#### `starter_product_reviews_600.csv`

This is a smaller supplementary dataset containing **600 product reviews**.

It is primarily intended for:

* Testing preprocessing scripts
* Testing data-loading functionality
* Debugging the dataset pipeline
* Validating multilingual and code-mixed processing
* Testing Marathi Devanagari handling

The starter dataset contains English, Hindi, Marathi and code-mixed reviews.

---

## Marathi Language Handling

Marathi data should be handled carefully because multilingual datasets may contain Marathi written in different scripts.

The project distinguishes between:

* Marathi written in **Devanagari**
* Romanized Marathi
* Marathi-English code-mixed text
* Hindi-Marathi code-mixed text
* Hindi-English-Marathi code-mixed text

For research experiments specifically requiring native Marathi script, Marathi Devanagari records should be identified and validated separately.

Romanized Marathi should not automatically be treated as Devanagari Marathi.

---

## Data Processing Pipeline

The raw datasets should not be modified directly.

The expected processing pipeline is:

```text
Raw Dataset
     |
     v
Data Validation
     |
     v
Text Cleaning
     |
     v
Unicode Normalization
     |
     v
Language / Script Detection
     |
     v
Code-Mix Identification
     |
     v
Duplicate Removal
     |
     v
Sentiment Validation
     |
     v
Aspect Validation
     |
     v
Quality Filtering
     |
     v
Processed Dataset
     |
     +----------+----------+
     |          |          |
     v          v          v
   Train       Val        Test
```

---

## Dataset Usage

The datasets are intended for:

1. Multilingual sentiment classification
2. Code-mixed sentiment classification
3. Aspect-based sentiment analysis
4. Language/script analysis
5. Explainable sentiment analysis
6. Evaluation of multilingual language models

Potential model families include multilingual transformer models such as:

* IndicBERT
* MuRIL
* XLM-R
* Other suitable multilingual/code-mixed language models

---

## Important Data Management Rules

### 1. Do not duplicate the 60K dataset

The CSV and Excel versions of the 60K dataset represent the same dataset.

Only the CSV should be used as the primary machine-learning input.

### 2. Keep raw data unchanged

Files inside `data/raw/` should be treated as source data.

Cleaning and transformation should create new processed files rather than overwriting the raw dataset.

### 3. Avoid duplicate records

Before combining additional datasets, check for duplicate reviews using the review ID and normalized text.

### 4. Preserve metadata

Language, script, sentiment, aspect and source information should be preserved whenever possible.

### 5. Track synthetic/generated data

If generated or augmented reviews are added, they should be explicitly marked using a metadata field such as:

```text
is_synthetic
```

This prevents generated data from being confused with original/collected data during research evaluation.

---

## Recommended Processed Dataset Structure

After preprocessing, the project may contain:

```text
data/
├── raw/
│   ├── codemix_product_reviews_60k.csv
│   └── starter_product_reviews_600.csv
│
├── processed/
│   ├── cleaned_reviews.csv
│   ├── train.csv
│   ├── validation.csv
│   └── test.csv
│
└── README.md
```

The processed files should be generated by reproducible preprocessing scripts rather than manually edited.

---

## Dataset Quality Checks

Before model training, verify:

* Number of records
* Missing values
* Duplicate records
* Sentiment distribution
* Language distribution
* Script distribution
* Code-mixing distribution
* Aspect distribution
* Train/validation/test distribution
* Invalid or empty reviews
* Marathi Devanagari versus Romanized Marathi
* Class imbalance

Example checks:

```python
df.shape
df.isnull().sum()
df.duplicated().sum()
df["sentiment"].value_counts()
df["language_pattern"].value_counts()
```

---

## Reproducibility

All preprocessing, cleaning, filtering and dataset-splitting operations should be implemented through scripts or notebooks stored in the project repository.

Raw datasets should remain unchanged so that experiments can be reproduced from the original input data.

---

## Status

**Current dataset status:**

* Primary dataset: 60,000 records
* Starter dataset: 600 records
* Languages: English, Hindi, Marathi
* Code-mixed data: Available
* Sentiment classes: Positive, Negative, Neutral
* Product-review domain: Yes
* Preprocessing pipeline: To be integrated with the project

---

## Project

**MultilingualSentX**

An explainable multilingual and code-mixed sentiment analysis project focused on Indian-language product reviews.
