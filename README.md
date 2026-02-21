# Data Ingestion & Monitored SQL Infrastructure for ChatGPT Reviews

This repository implements a modular, SQL-based data ingestion system for collecting, structuring, and persistently storing large-scale user-generated reviews from public web sources.

Beyond basic ingestion, the system includes a lightweight automated monitoring layer that enables the pipeline to observe and validate its own execution behavior.


---

## Project Objective

To design a reusable and scalable data ingestion system that:

- Collects public user review data
- Cleans and structures semi-structured text content
- Stores the data in a relational SQL database
- Enables scalable querying for downstream NLP tasks
- Automatically monitors ingestion quality and execution health

The goal is to build a robust infrastructure layer that supports future AI-driven sentiment modeling and experimentation.

---

## Data Source

Platform: Google Play Store  
Application: ChatGPT  
Data Type: User reviews including rating, timestamp, text content, and metadata  
Scale: Approximately 100,000 unique reviews  

Google Play was selected due to its public accessibility, stable structure, and sufficient review volume.

---

## SQL Schema Design

Three relational tables are implemented:

### apps

- app_id (Primary Key)
- app_name
- platform

### reviews

- review_id (Primary Key)
- app_id (Foreign Key referencing apps.app_id)
- user_name (nullable)
- rating
- content
- thumbs_up
- review_date (ISO 8601 formatted)
- app_version

### pipeline_runs (Monitoring Layer)

- run_id (Primary Key)
- run_key
- source
- started_at
- finished_at
- status
- attempted_rows
- inserted_rows
- duplicate_rows
- duration_sec
- missing_rating_ratio
- missing_content_ratio
- missing_review_date_ratio

Design considerations:

- Primary and foreign key constraints enforce relational integrity.
- Nullable fields accommodate platform-level variability.
- Timestamps are normalized for consistency.
- Monitoring metadata is stored per run to ensure auditability.

---

## Automated Ingestion Pipeline

The ingestion workflow is implemented in:

run_pipeline.py

The pipeline performs the following steps:

1. Database initialization
2. CSV ingestion
3. Timestamp normalization
4. Bulk insertion using idempotent INSERT OR IGNORE logic
5. Record count verification
6. Run-level metric computation
7. Monitoring status update


---

## Lightweight Monitoring Layer

Each pipeline run automatically records:

- Whether the run succeeded or triggered a warning
- Total rows attempted
- Rows successfully inserted
- Duplicate counts
- Missing field ratios
- Execution duration

### Anomaly Detection Rules

The system flags abnormal runs under the following conditions:

- warning_zero_insert  
  Triggered when inserted_rows equals zero while attempted_rows is greater than zero.

- warning_high_duplicate  
  Triggered when duplicate ratio exceeds 0.9.

This allows the ingestion system to detect potential upstream data changes or ingestion failures.

---

## Indexing Strategy

Indexes are created on:

- reviews.app_id
- reviews.review_date
- reviews.rating

These indexes ensure efficient filtering by application, time window, and rating category.

---

## Data Quality Summary

Observed dataset characteristics:

- No duplicate primary keys
- Core fields largely complete
- Missing ratios near zero for essential attributes
- Stable ingestion behavior across runs
- Idempotent execution verified

---

## Engineering Properties

The system now supports:

- Idempotent ingestion
- Structured relational storage
- Run-level observability
- Automated data quality validation
- Lightweight anomaly detection

This moves the pipeline from simple automation to a self-monitoring ingestion system.

---

## Notes

- Raw CSV files and the SQLite database file are excluded from version control.
- The architecture is extensible to additional applications and platforms.
- Designed as a scalable entry point for AI-based sentiment modeling systems.
