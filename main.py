import time
import logging
from scraper import get_new_articles, mark_as_processed
from ai_processor import generate_post_title, generate_blog_post
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
        
    for article in new_articles:
        # Step 3: AI Processing
        logger.info(f"Processing article: {article['title']}")
        
        post_title = generate_post_title(article)
        post_content = generate_blog_post(article)
        
        if not post_content:
            logger.error(f"Failed to generate content for {article['title']}. Skipping.")
            continue
            
        # Step 4: GitHub Pages Publishing (Saving Markdown file)
        logger.info(f"Saving markdown file for: {post_title}")
        filepath = publish_to_github_pages(title=post_title, markdown_content=post_content)
        
        if filepath:
            logger.info("Successfully generated Markdown file. Marking as processed.")
            mark_as_processed(article['link'])
            
        # Sleep to avoid hitting API rate limits too fast
        time.sleep(5)
        
    logger.info("Pipeline execution completed. Ready for 'git push'.")

if __name__ == "__main__":
    main()
