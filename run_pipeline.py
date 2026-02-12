import pandas as pd
import sqlite3

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

    conn.commit()

    print(f"{len(records)} reviews loaded.")


def verify(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reviews;")
    count = cursor.fetchone()[0]

    print(f"Total reviews in database: {count}")


def main():
    conn = sqlite3.connect(DB_PATH)

    setup_database(conn)
    load_data(conn)
    verify(conn)

    conn.close()


if __name__ == "__main__":
    main()
