import os
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)

# The directory where Jekyll/Hugo expects Markdown posts
# This should point to your local git repository folder for the GitHub Pages site
POSTS_DIR = os.getenv("POSTS_DIR", "./_posts")

def create_slug(title):
    """Convert a title into a URL-friendly slug."""
    # Remove non-alphanumeric characters, replace spaces with hyphens, lowercase
    slug = re.sub(r'[^a-zA-Z0-9\s]', '', title).strip()
    slug = re.sub(r'\s+', '-', slug).lower()
    return slug[:50] if slug else "daily-update" # Fallback if slug is empty

def publish_to_github_pages(title, markdown_content):
    """
    Save the generated Markdown content as a file in the _posts directory.
    Format required by Jekyll: YYYY-MM-DD-title-slug.md
    """
    if not os.path.exists(POSTS_DIR):
        try:
            os.makedirs(POSTS_DIR)
            logger.info(f"Created posts directory at {POSTS_DIR}")
        except Exception as e:
            logger.error(f"Failed to create posts directory: {e}")
            return False

    today = datetime.now()
    date_prefix = today.strftime('%Y-%m-%d')
    slug = create_slug(title)
    
    filename = f"{date_prefix}-{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    try:
        # Check if we already have frontmatter from OpenAI
        # If not, we could inject it here, but our prompt instructs the LLM to write it.
        # Ensure proper encoding
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        logger.info(f"Successfully saved Markdown file: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error publishing to local filesystem for GitHub Pages: {e}")
        return False
