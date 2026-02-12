# Data Ingestion & SQL Infrastructure for ChatGPT Reviews

This repository implements the foundational data ingestion and infrastructure layer for collecting, structuring, and storing large-scale user-generated reviews from public web sources.

The objective of this phase is not only to perform descriptive analysis, but to design a reusable and scalable SQL-based ingestion system that supports downstream sentiment modeling, labeling workflows, and iterative experimentation.

---

## Project Objective

To build a modular and automated data pipeline that:

- Collects public user review data
- Cleans and structures semi-structured text content
- Stores the data in a relational SQL database
- Enables scalable querying and downstream NLP tasks

This work aligns with the Phase I objective of establishing a reliable infrastructure layer for future AI-driven sentiment analysis systems.

---

## Data Source

Platform: Google Play Store  
Application: ChatGPT  
Data Type: User reviews including rating, timestamp, text content, and metadata  
Scale: ~100,000 unique reviews  
Time Coverage: Approximately one month of recent data  

Google Play was selected due to its public accessibility, stable structure, and sufficient review volume.

---

##  SQL Schema & Automated Ingestion

### Database Design

Two relational tables are implemented:

apps table:
- app_id (Primary Key)
- app_name
- platform

reviews table:
- review_id (Primary Key)
- app_id (Foreign Key referencing apps.app_id)
- user_name (nullable)
- rating
- content
- thumbs_up
- review_date (ISO 8601 formatted)
- app_version

Design considerations:
- Primary and foreign key relationships enforce structural integrity.
- Nullable fields account for platform-level data variability.
- The schema supports future multi-application expansion.
- Timestamps are normalized for consistency.

---

## Automated Ingestion Pipeline

The ingestion process is fully automated via:

run_pipeline.py

The pipeline performs:

1. Database initialization (table and index creation)
2. CSV ingestion
3. Timestamp normalization
4. Bulk insertion into SQLite
5. Record count verification

To execute:

python run_pipeline.py

This generates a SQLite database file named:

reviews.db

---

## Indexing for Performance

Indexes are created on:

- reviews.app_id
- reviews.review_date
- reviews.rating

These indexes ensure efficient filtering by application, time range, and rating category.

---

## Descriptive Analysis Summary

Basic descriptive analysis was conducted to validate dataset quality.

Rating Distribution:
The dataset is right-skewed, with a majority of 5-star reviews while preserving lower-rated feedback for qualitative analysis.

Review Length Distribution:
Review lengths exhibit a long-tailed pattern, indicating the presence of detailed feedback suitable for downstream NLP tasks.

Temporal Trends:
Daily review counts remain stable across the observed period, suggesting consistent ingestion.

---

## Data Quality Summary

- No duplicate review identifiers detected
- Core fields (rating, content, timestamp) largely complete
- Missing values limited to non-essential metadata
- Dataset structure suitable for NLP modeling

---

## Notes

- Raw CSV files and SQLite database files are excluded from version control.
- The system is designed as a scalable entry point for AI-based sentiment modeling.
- The architecture supports future expansion to additional platforms.

---

This repository represents the completion of Phase I: Data Ingestion & Infrastructure.
