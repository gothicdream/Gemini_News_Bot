# news_pipeline.py

from newsapi import NewsApiClient
from datetime import datetime, timedelta
from goose3 import Goose
from pymongo import MongoClient
from google import generativeai as genai
import json
import time

# ----------------- Configuration -----------------

API_KEY = "YOUR_NEWSAPI_KEY"
MONGO_URI = "mongodb://localhost:27017/"  # Change if needed
NEWS_SOURCES = "bbc-news,cnn"  # Comma-separated News API sources
SEARCH_QUERY = "technology OR science OR innovation"
DAYS_BACK = 7
PAGES = 3
GENAI_API_KEY = "YOUR_GEMINI_API_KEY"

RAW_DB_NAME = "New_Articles_raw_DB"
RAW_COLLECTION = "News_articles_raw"
SUMMARY_COLLECTION = "summarized_articles"

# ----------------- Fetch Articles -----------------

def fetch_articles(api_key, query, sources, days_back, pages):
    newsapi = NewsApiClient(api_key=api_key)
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days_back)
    all_articles = []

    for page in range(1, pages + 1):
        try:
            print(f"\nFetching page {page}")
            response = newsapi.get_everything(
                q=query,
                sources=sources,
                from_param=from_date.strftime('%Y-%m-%d'),
                to=to_date.strftime('%Y-%m-%d'),
                language='en',
                sort_by='publishedAt',
                page=page,
                page_size=20
            )
            if 'articles' in response and response['articles']:
                all_articles.extend(response['articles'])
            else:
                break
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

    print(f"\nTotal articles fetched: {len(all_articles)}")
    return all_articles

# ----------------- Extract Full Text -----------------

def extract_article_text(articles):
    goose = Goose()
    for item in articles:
        try:
            url = item['url']
            print(f"\nExtracting from: {url}")
            article = goose.extract(url=url)
            item['full_title'] = article.title
            item['full_text'] = article.cleaned_text
        except Exception as e:
            print(f"Extraction failed: {e}")
    return articles

# ----------------- Store Raw Articles -----------------

def store_raw_articles(articles, mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    inserted_count = 0
    for article in articles:
        article["fetched_at"] = datetime.utcnow()
        if collection.find_one({"url": article.get("url")}):
            print(f"⏩ Skipping duplicate: {article.get('title')}")
            continue
        try:
            collection.insert_one(article)
            inserted_count += 1
        except Exception as e:
            print(f"Insertion error: {e}")

    print(f"\nInserted {inserted_count} new raw articles.")

# ----------------- Summarize with Gemini -----------------

def summarize_articles(mongo_uri, db_name, raw_collection, summary_collection_name, genai_api_key):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    raw_col = db[raw_collection]
    summary_col = db[summary_collection_name]

    genai.configure(api_key=genai_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    articles = list(raw_col.find())
    print(f"\n📚 Articles to summarize: {len(articles)}")

    for i, article in enumerate(articles):
        article.pop("_id", None)
        prompt_data = {
            "title": article.get("title", "")[:200],
            "content": article.get("full_text", "")[:1500],
            "source": article.get("source", ""),
            "publishedAt": str(article.get("publishedAt", ""))
        }

        prompt = f'''
You are an assistant summarizing a news article.

Return valid JSON array with one dictionary having:
- "title", "summary", "keyword" (list), "topic", "entities" (list), "sentiment" ("positive"/"neutral"/"negative"), "relevancy_score" (1-10).

No newlines or explanations. Output must be JSON-parseable list.

Article:
{json.dumps(prompt_data)}
'''

        print(f"\nSummarizing {i+1}: {prompt_data['title']}")
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                clean_response = response.text.strip().replace("\n", "")
                summary = json.loads(clean_response)[0]

                summary["source"] = article.get("source", "")
                summary["original_publishedAt"] = article.get("publishedAt")
                summary["processedAt"] = datetime.utcnow().isoformat()

                summary_col.insert_one(summary)
                print(f"Summary inserted.")
                break
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)

# ----------------- Main Pipeline -----------------

if __name__ == "__main__":
    articles = fetch_articles(API_KEY, SEARCH_QUERY, NEWS_SOURCES, DAYS_BACK, PAGES)
    articles = extract_article_text(articles)
    store_raw_articles(articles, MONGO_URI, RAW_DB_NAME, RAW_COLLECTION)
    summarize_articles(MONGO_URI, RAW_DB_NAME, RAW_COLLECTION, SUMMARY_COLLECTION, GENAI_API_KEY)
