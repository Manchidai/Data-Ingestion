from numpy import rint
import pandas as pd
import sqlite3
from datetime import datetime
import time

DB_PATH = "reviews.db"
CSV_PATH = "google_play_chatgpt_reviews.csv"

APP_ID = "com.openai.chatgpt"
APP_NAME = "ChatGPT"
PLATFORM = "google_play"


def setup_database(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS apps (
        app_id TEXT PRIMARY KEY,
        app_name TEXT,
        platform TEXT
    );
    """)

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

    conn.commit()


def load_data(conn):
    df = pd.read_csv(CSV_PATH, encoding="utf-8", engine="c", low_memory=False)

    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO apps (app_id, app_name, platform)
    VALUES (?, ?, ?)
    """, (APP_ID, APP_NAME, PLATFORM))

    records = [
        (
            row["review_id"],
            APP_ID,
            row["user_name"],
            int(row["rating"]) if not pd.isna(row["rating"]) else None,
            row["content"],
            int(row["thumbs_up"]) if not pd.isna(row["thumbs_up"]) else None,
            row["review_date"].isoformat() if pd.notna(row["review_date"]) else None,
            row["app_version"]
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO reviews
    (review_id, app_id, user_name, rating, content, thumbs_up, review_date, app_version)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    inserted_rows = cursor.rowcount
    attempted_rows = len(records)
    duplicate_rows = attempted_rows - inserted_rows

    # ---- Missing field ratios ----
    missing_rating = sum(1 for r in records if r[3] is None)
    missing_content = sum(1 for r in records if r[4] is None)
    missing_review_date = sum(1 for r in records if r[6] is None)

    missing_rating_ratio = missing_rating / attempted_rows if attempted_rows else 0
    missing_content_ratio = missing_content / attempted_rows if attempted_rows else 0
    missing_review_date_ratio = missing_review_date / attempted_rows if attempted_rows else 0

    print(f"Missing rating ratio: {missing_rating_ratio:.4f}")
    print(f"Missing content ratio: {missing_content_ratio:.4f}")
    print(f"Missing review_date ratio: {missing_review_date_ratio:.4f}")

    conn.commit()

    print(f"Attempted: {attempted_rows}")
    print(f"Inserted: {inserted_rows}")
    print(f"Duplicates: {duplicate_rows}")

    return (
    attempted_rows,
    inserted_rows,
    duplicate_rows,
    missing_rating_ratio,
    missing_content_ratio,
    missing_review_date_ratio
)


def verify(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reviews;")
    count = cursor.fetchone()[0]

    print(f"Total reviews in database: {count}")


def main():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    start_time = time.time()
    started_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO pipeline_runs (run_key, source, started_at, status)
        VALUES (?, ?, ?, ?)
    """, (
        f"run_{int(start_time)}",
        "google_play",
        started_at,
        "running"
    ))

    run_id = cursor.lastrowid
    conn.commit()

    setup_database(conn)
    (
    attempted_rows,
    inserted_rows,
    duplicate_rows,
    missing_rating_ratio,
    missing_content_ratio,
    missing_review_date_ratio
    ) = load_data(conn)
    verify(conn)

    finished_at = datetime.now().isoformat()
    duration = time.time() - start_time

    # ---- Anomaly Detection ----
    duplicate_ratio = duplicate_rows / attempted_rows if attempted_rows else 0

    final_status = "success"

    if inserted_rows == 0 and attempted_rows > 0:
        final_status = "warning_zero_insert"

    elif duplicate_ratio > 0.9:
        final_status = "warning_high_duplicate"

    cursor.execute("""
        UPDATE pipeline_runs
        SET status = ?, 
            finished_at = ?, 
            duration_sec = ?, 
            attempted_rows = ?, 
            inserted_rows = ?, 
            duplicate_rows = ?,
            missing_rating_ratio = ?,
            missing_content_ratio = ?,
            missing_review_date_ratio = ?
        WHERE run_id = ?
    """, (
        final_status,
        finished_at,
        duration,
        attempted_rows,
        inserted_rows,
        duplicate_rows,
        missing_rating_ratio,
        missing_content_ratio,
        missing_review_date_ratio,
        run_id
    ))
    conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
