from google_play_scraper import reviews, Sort
import pandas as pd
import time
from datetime import datetime


# =========================
# App configuration
# =========================
APP_CONFIG = {
    "app_name": "ChatGPT",
    "app_id": "com.openai.chatgpt",
    "lang": "en",
    "country": "us"
}

TARGET_N_REVIEWS = 100000        
BATCH_SIZE = 200                
SLEEP_SECONDS = 0.5             


# =========================
# Core ingestion function
# =========================
def fetch_google_play_reviews(app_id, lang, country, target_n):
    """
    Fetch reviews from Google Play Store with pagination.
    """
    all_reviews = []
    continuation_token = None
    page = 0

    while len(all_reviews) < target_n:
        page += 1
        result, continuation_token = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=BATCH_SIZE,
            continuation_token=continuation_token
        )

        if not result:
            print("No more reviews returned by Google Play.")
            break

        all_reviews.extend(result)

        print(
            f"Page {page}: collected {len(result)} reviews "
            f"(total={len(all_reviews)})"
        )

        if continuation_token is None:
            print("Continuation token exhausted.")
            break

        time.sleep(SLEEP_SECONDS)

    return all_reviews[:target_n]


# =========================
# Data normalization
# =========================
def normalize_reviews(raw_reviews):
    """
    Convert raw review dicts into a clean DataFrame.
    """
    records = []

    for r in raw_reviews:
        records.append({
            "review_id": r.get("reviewId"),
            "user_name": r.get("userName"),
            "rating": r.get("score"),
            "content": r.get("content"),
            "thumbs_up": r.get("thumbsUpCount"),
            "review_date": (
                r.get("at").isoformat() if r.get("at") else None
            ),
            "app_version": r.get("reviewCreatedVersion")
        })

    df = pd.DataFrame(records)
    return df


# =========================
# Main
# =========================
def main():
    print("===================================")
    print("Google Play Review Ingestion")
    print(f"App: {APP_CONFIG['app_name']}")
    print("===================================")

    raw_reviews = fetch_google_play_reviews(
        app_id=APP_CONFIG["app_id"],
        lang=APP_CONFIG["lang"],
        country=APP_CONFIG["country"],
        target_n=TARGET_N_REVIEWS
    )

    df = normalize_reviews(raw_reviews)

    print("\nIngestion summary:")
    print(f"Total reviews collected: {len(df)}")

    if not df.empty:
        print(
            f"Date range: "
            f"{df['review_date'].min()}  →  {df['review_date'].max()}"
        )

    output_file = (
        f"google_play_{APP_CONFIG['app_name'].lower()}_reviews.csv"
    )

    df.to_csv(output_file, index=False)
    print(f"\nSaved to: {output_file}")

    print("\nSample rows:")
    print(df.head(5))


if __name__ == "__main__":
    main()
