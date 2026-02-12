# Database Schema – ChatGPT Google Play Reviews

## Overview

This schema stores structured review data collected from Google Play.
The design is extensible to support multiple applications and platforms.

---

## Table: apps

| Column | Type | Description |
|--------|------|------------|
| app_id | TEXT (PK) | Unique application identifier |
| app_name | TEXT | Application name |
| platform | TEXT | Data source platform |

---

## Table: reviews

| Column | Type | Description |
|--------|------|------------|
| review_id | TEXT (PK) | Unique review identifier |
| app_id | TEXT (FK) | References apps.app_id |
| user_name | TEXT | Reviewer name |
| rating | INTEGER | Star rating (1–5) |
| content | TEXT | Review text |
| thumbs_up | INTEGER | Number of helpful votes |
| review_date | TIMESTAMP | Review timestamp |
| app_version | TEXT | App version at time of review |

---

## Design Notes

- The schema separates applications from reviews to support multi-application scalability.
- review_date will be stored in ISO 8601 format for consistency.
- user_name is nullable due to potential missing values in source data.
- The schema is designed to support future integration with additional platforms.

