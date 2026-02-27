import logging
import google.generativeai as genai
import re
from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

# Initialize Gemini client
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.error("GEMINI_API_KEY is not set.")

# Use the free and fast Gemini 2.5 Flash model
MODEL_NAME = "gemini-2.5-flash"

def get_model():
    return genai.GenerativeModel(MODEL_NAME)

def generate_roundup_post(articles):
    """
    Takes a list of article dictionaries and generates a single comprehensive 'daily roundup' blog post.
    Returns a tuple of (title, markdown_content).
    """
    if not GEMINI_API_KEY or not articles:
        return None
        
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Prepare articles payload for prompt
    articles_text = ""
    for idx, article in enumerate(articles, 1):
        image_info = f"\n- Image URL: {article.get('image', '')}" if article.get('image') else ""
        articles_text += f"\n\n[News Item {idx}]\n- Title: {article.get('title', '')}\n- Source: {article.get('source', '')}\n- Link: {article.get('link', '')}{image_info}\n- Content: {article.get('content', '')[:1000]}"

    logger.info(f"Generating Daily Roundup English Markdown post using Gemini for {len(articles)} articles")
    
    prompt = f"""
    You are a highly opinionated, insightful human tech YouTuber and newsletter editor (use "I" and "my" occasionally) writing for a global audience deeply interested in artificial intelligence, practical tech tools, and the future of business.
    Your mission is to read the following breaking news items and synthesize them into ONE brilliant, highly engaging "Daily AI Roundup" or "Tech Newsletter" style blog post in Plain English.
    
    {articles_text}

    [Guidelines]
    1. **Format**: Create a standard Markdown document (.md).
    2. **Language**: English, Plain English.
    3. **Tone**: Engaging, conversational, sophisticated, and opinionated. Sound like a passionate human expert directly talking to an audience (like a YouTuber script). Never use AI robotic phrases like "As an AI..." or "In conclusion".
    4. **Core Content Focus**: 
       - Don't just list them one by one. Find the narrative thread between them or present them as the "Top Breaking Stories of the Day."
       - Emphasize practical applications, industry disruption, and real-world tools.
       - Highlight key figures or companies leading the charge.
    5. **Structure**: 
       - A **catchy YAML frontmatter** at the very top. MUST contain 'title' (create a provocative overarching title covering today's news), 'date' (MUST BE EXACTLY {current_date}), 'categories' (set to AI), 'tags', 'layout' (must be exactly 'post'), and 'author' (set to 'Jeong').
       - A **hook-driven introduction** (Why am I excited about today's news?).
       - **The Meat**: Break down the most important news items from the list contextually. 
       - **Images**: Whenever you talk about a specific news item that has an 'Image URL' provided, you MUST embed it in the markdown like this: `![Alt text](Image URL)`
       - **Links**: Hyperlink the original source links contextually when you mention the news.
       - A **thought-provoking sign-off** (Outro).
    
    Output nothing but the raw Markdown content containing the YAML frontmatter and the body! Do not wrap in ```markdown blocks if possible.
    """
    
    try:
        model = get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
            )
        )
        
        generated_md = response.text.strip()
        
        # Strip potential markdown formatting wrapper
        if generated_md.startswith("```markdown"):
            generated_md = generated_md[11:]
        if generated_md.startswith("```"):
            generated_md = generated_md[3:]
        if generated_md.endswith("```"):
            generated_md = generated_md[:-3]
            
        generated_md = generated_md.strip()
        
        # Extract title from YAML frontmatter
        title = f"AI Daily Briefing {current_date}"
        import re
        # More robust title extraction: find title property, handle optional quotes
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?$', generated_md, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            
        return title, generated_md
        
    except Exception as e:
        logger.error(f"Error generating roundup post via Gemini: {e}")
        return None
