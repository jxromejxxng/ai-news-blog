import time
import logging
from scraper import get_new_articles, mark_as_processed
from ai_processor import generate_roundup_post
from github_publisher import publish_to_github_pages

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting AI News Automation Pipeline (Global GitHub Pages Edition)...")
    
    # Step 1 & 2: Data Collection & Deduplication
    logger.info("Fetching and filtering new articles...")
    new_articles = get_new_articles()
    
    if not new_articles:
        logger.info("No new articles found. Exiting.")
        return
        
    # Limit to top 10 articles to not overload context window
    articles_to_process = new_articles[:10]
    logger.info(f"Processing {len(articles_to_process)} articles into a Daily Roundup...")
    
    # Step 3: AI Processing (N:1 Roundup)
    result = generate_roundup_post(articles_to_process)
    
    if not result:
        logger.error("Failed to generate roundup post. Exiting.")
        return
        
    post_title, post_content = result
    
    # Step 4: GitHub Pages Publishing (Saving Markdown file)
    logger.info(f"Saving markdown file for: {post_title}")
    filepath = publish_to_github_pages(title=post_title, markdown_content=post_content)
    
    if filepath:
        logger.info("Successfully generated Markdown roundup file. Marking as processed.")
        for article in articles_to_process:
            mark_as_processed(article['link'])
            
    logger.info("Pipeline execution completed. Ready for 'git push'.")

if __name__ == "__main__":
    main()
