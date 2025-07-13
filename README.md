# Gemini_News_Bot
An automated AI-powered pipeline that fetches news articles, extracts full content, summarizes them using Google Gemini, and stores both raw and summarized data in MongoDB. Ideal for building intelligent news dashboards, alerts, or research databases.

**Gemini_News_Bot** is an automated AI-powered news intelligence pipeline that fetches the latest articles from trusted sources, extracts the full content, summarizes key points using **Google Gemini**, and stores both raw and summarized content in **MongoDB**. Perfect for research, news aggregation, dashboards, or intelligent alert systems.

---

## 🚀 Features

- 🔎 **Fetch Articles** from top sources using NewsAPI.
- 📄 **Extract Full Content** using Goose3 for clean, readable text.
- 🤖 **Summarize with Gemini AI**:
  - Intelligent summaries
  - Sentiment analysis
  - Keyword & entity extraction
  - Topic categorization
  - Relevancy scoring
- 🗃️ **Store in MongoDB** with deduplication and timestamps.
- 🛠️ Built with modular, readable Python code.

---

## 🧰 Tech Stack

- Python
- [NewsAPI](https://newsapi.org/)
- [Goose3](https://pypi.org/project/goose3/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- MongoDB (`pymongo`)
- JSON / REST

---

## 📦 Installation

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/NewsSage.git
cd NewsSage
2. Install Dependencies
bash
Copy
Edit
pip install newsapi-python goose3 pymongo google-generativeai
3. Add Your API Keys
Update the top of your script or use .env:

python
Copy
Edit
NEWS_API_KEY = "your_newsapi_key"
GENAI_API_KEY = "your_gemini_api_key"
MONGO_URI = "mongodb://localhost:27017/"
⚙️ Usage
Run the script to start the pipeline:

bash
Copy
Edit
python news_pipeline.py
This will:

Fetch recent news articles

Extract full content

Summarize with Gemini

Store results in MongoDB

🧾 Output (Summarized Article)
json
Copy
Edit
{
  "title": "AI Transforms Healthcare",
  "summary": "Artificial Intelligence is improving diagnosis accuracy, speeding up drug discovery...",
  "keyword": ["AI", "Healthcare", "Diagnosis"],
  "topic": "Science",
  "entities": ["Google Health", "FDA"],
  "sentiment": "positive",
  "relevancy_score": 8
}
📁 Project Structure
bash
Copy
Edit
news_pipeline.py       # Main pipeline script
README.md              # Project documentation
requirements.txt       # Optional: dependency list


