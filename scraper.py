import feedparser
import json
import logging
import os
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from config import RSS_FEEDS, DB_PATH

logger = logging.getLogger(__name__)

def load_history():
    """Load the history of processed article URLs."""
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Failed to parse history.json, starting fresh.")
            return []
    return []

def save_history(history):
    """Save the history of processed article URLs."""
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def clean_html(html_content):
    """Extract plain text from HTML content."""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=' ', strip=True)

def fetch_rss_feeds():
    """
    Fetch articles from all configured RSS feeds.
    Returns a list of dictionaries containing article details.
    """
    articles = []
    
    for feed_url in RSS_FEEDS:
        logger.info(f"Parsing feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            # Extract basic info
            title = entry.get('title', '')
            link = entry.get('link', '')
            
            # Extract content if available, fallback to summary
            content = ""
            if 'content' in entry and len(entry.content) > 0:
                content = entry.content[0].value
            elif 'summary' in entry:
                content = entry.summary
                
            clean_text = clean_html(content)
            
            # Simple crude filtering: only articles likely about AI
            if 'ai' in title.lower() or 'artificial intelligence' in title.lower() or 'openai' in title.lower() or 'chatgpt' in title.lower() or 'claude' in title.lower():
                articles.append({
                    'title': title,
                    'link': link,
                    'content': clean_text,
                    'source': feed.feed.get('title', feed_url),
                    'published': entry.get('published', '')
                })
    
    return articles

def get_new_articles():
    """Fetch all articles and filter out ones we have already processed."""
    history = set(load_history())
    all_articles = fetch_rss_feeds()
    
    new_articles = []
    for article in all_articles:
        if article['link'] not in history:
            new_articles.append(article)
            
    logger.info(f"Found {len(new_articles)} new articles out of {len(all_articles)} total fetched.")
    return new_articles

def mark_as_processed(link):
    """Mark an article URL as processed."""
    history = load_history()
    if link not in history:
        history.append(link)
        # Keep only the last 1000 items to prevent the file from growing indefinitely
        history = history[-1000:]
        save_history(history)
