# Data Ingestion & descriptive Analysis of ChatGPT Reviews

This repository contains the implementation of a data ingestion and descriptive analysis pipeline for user-generated reviews, developed as part of a broader effort to support scalable sentiment understanding and downstream machine learning workflows.

The goal is to establish a reliable entry point for transforming raw, public web data into structured, analyzable artifacts that can support labeling, modeling, and iterative analysis.

---

## Project Context

Understanding user sentiment at scale requires more than isolated classification models. It depends on a robust data foundation that can continuously collect, clean, structure, and store user feedback in a reusable and extensible way.

This project focuses on building that foundational layer by:
- identifying a suitable public data source,
- automating data collection,
- performing basic data quality checks and exploratory analysis, and
- documenting findings and limitations for downstream use.

This work aligns with the objectives outlined in the project brief for the data ingestion and infrastructure phase. :contentReference[oaicite:0]{index=0}

---

## Data Source

- **Platform:** Google Play Store  
- **Application:** ChatGPT  
- **Data type:** User reviews with ratings, timestamps, and textual feedback  
- **Scale:** ~1000,000 unique reviews  
- **Time coverage:** Approximately one month of recent data  

Google Play was selected due to its public accessibility, stable structure, and sufficient volume of user-generated content, making it suitable for automated ingestion and structured analysis.

---

## Descriptive Analysis Summary

The descriptive data analysis focuses on three core aspects:

### 1. Rating Distribution
User ratings are heavily right-skewed, with a majority of 5-star reviews. However, a substantial number of lower-rated reviews (1–3 stars) are present, providing meaningful signal for qualitative analysis and issue discovery.

### 2. Review Length Distribution
Review text lengths exhibit a long-tailed distribution. While most reviews are brief, a subset contains detailed feedback that is particularly valuable for downstream tasks such as topic modeling or complaint analysis.

### 3. Temporal Trends
Daily review volume remains relatively stable across the observed period, indicating consistent data collection without major gaps. A decline on the final day reflects partial-day data rather than a pipeline issue.

---

## Data Quality Considerations

- No duplicate review identifiers were observed.
- Critical fields such as ratings, timestamps, and review text are nearly complete.
- Missing values are limited to non-essential metadata fields (e.g., app version).
- The primary limitation of the dataset is limited historical coverage, which constrains long-term trend analysis.

---


## Notes

This repository is intended to serve as a clean, reproducible foundation for downstream sentiment analysis and modeling rather than a one-off exploratory exercise.
