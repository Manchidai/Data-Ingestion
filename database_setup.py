import sqlite3

# Create database file
conn = sqlite3.connect("reviews.db")
cursor = conn.cursor()

# Creat apps table
cursor.execute("""
CREATE TABLE IF NOT EXISTS apps (
    app_id TEXT PRIMARY KEY,
    app_name TEXT,
    platform TEXT
);
""")

# Creat reviews table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id TEXT PRIMARY KEY,
    app_id TEXT,
    user_name TEXT,
    rating INTEGER,
    content TEXT,
    thumbs_up INTEGER,
    review_date TEXT,
    app_version TEXT,
    FOREIGN KEY (app_id) REFERENCES apps(app_id)
);
""")
# create indexes
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_reviews_app_id
ON reviews(app_id);
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_reviews_review_date
ON reviews(review_date);
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_reviews_rating
ON reviews(rating);
""")

# Create pipeline_runs table (monitoring)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_key TEXT UNIQUE,
    source TEXT NOT NULL,
    started_at TEXT,
    finished_at TEXT,
    status TEXT DEFAULT 'running',
    attempted_rows INTEGER DEFAULT 0,
    inserted_rows INTEGER DEFAULT 0,
    duplicate_rows INTEGER DEFAULT 0,
    duration_sec REAL,
    error_message TEXT,
    missing_rating_ratio REAL,
    missing_content_ratio REAL,
    missing_review_date_ratio REAL
);
""")

conn.commit()
conn.close()

print("Database and tables created successfully.")
