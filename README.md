# Data Ingestion & Exploratory Analysis of ChatGPT Reviews

This repository contains the Phase I implementation of a data ingestion and exploratory analysis pipeline for user-generated reviews, developed as part of a broader effort to support scalable sentiment understanding and downstream machine learning workflows.

The goal of this phase is to establish a reliable entry point for transforming raw, public web data into structured, analyzable artifacts that can support labeling, modeling, and iterative analysis.

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
- **Scale:** ~100,000 unique reviews  
- **Time coverage:** Approximately one month of recent data  

Google Play was selected due to its public accessibility, stable structure, and sufficient volume of user-generated content, making it suitable for automated ingestion and structured analysis.

---

## Repository Structure

.
├── data_collection/
│ └── google_chatgpt.py # Automated script for collecting reviews
│
├── analysis/
│ └── DQ_check.ipynb # Exploratory data analysis and data quality checks
│
├── figures/
│ ├── ratings.png # Rating distribution
│ ├── review length.png # Review length distribution
│ └── daily volumn.png # Daily review volume over time
│
├── .gitignore # Excludes raw data files (e.g., CSVs)
└── README.md

Raw review data files are intentionally excluded from version control to keep the repository lightweight and focused on reproducible code and analysis.

---

## Exploratory Analysis Summary

The exploratory data analysis focuses on three core aspects:

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
