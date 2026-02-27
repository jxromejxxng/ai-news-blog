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
    You are a friendly, practical, and insightful tech reviewer (like the YouTuber JoCoding) writing for people who want to understand how AI is changing their work and life. 
    Your mission is to summarize these breaking news items into ONE clear, approachable "Daily AI Briefing" blog post.
    
    {articles_text}

    [Guidelines]
    1. **Format**: Create a standard Markdown document (.md).
    2. **Language**: Plain English.
    3. **Tone**: Direct, friendly, and practical. Sound like an expert friend explaining news clearly. **AVOID** overly dramatic or cringey "visionary" language like "collision course with superintelligence" or "rewiring our souls." Keep it grounded in facts and utility.
    4. **Source Attribution**: For every news item you discuss, you MUST include a clickable source link (e.g., [Source Name](URL)) immediately after that section.
    5. **Core Content Focus**: 
       - Summarize the top 3-5 most impactful stories from the list.
       - Focus on how people can use these tools or why companies should care.
    6. **Structure**: 
       - Catchy YAML frontmatter: 'title' (informative, not clickbaity), 'date' (EXACTLY {current_date}), 'categories' (AI), 'tags', 'layout' (post), 'author' (Jeong).
       - Friendly intro (e.g., "Hey everyone, here's a quick update on today's AI trends...").
       - Sectioned body with H2/H3 headers.
       - **Images**: Embed the 'Image URL' using `![Alt text](Image URL)` for relevant items.
       - Thought-provoking but grounded outro.
    
    Output nothing but the raw Markdown content!
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
