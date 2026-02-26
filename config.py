import os
from dotenv import load_dotenv

load_dotenv()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# WordPress
WP_URL = os.getenv("WP_URL") # e.g., https://yourblog.com/wp-json/wp/v2
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# Feed Sources
RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    # Add more AI RSS feeds here
]

# Database/Storage for deduplication
DB_PATH = "history.json"
