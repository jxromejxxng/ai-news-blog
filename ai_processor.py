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

def generate_blog_post(article):
    """
    Takes an article dictionary and generates a full blog post in Markdown format.
    Suitable for Jekyll/Hugo (GitHub Pages) with YAML frontmatter.
    """
    if not GEMINI_API_KEY:
        return None
        
    title = article.get('title', '')
    content = article.get('content', '')
    source = article.get('source', '')
    link = article.get('link', '')
    date = article.get('published', '')
    
    logger.info(f"Generating English Markdown post for: {title} using Gemini")
    
    prompt = f"""
    You are a highly opinionated, visionary human tech blogger (use "I" and "my" occasionally) writing for a global audience deeply interested in the future of AI, AGI, and the Technological Singularity.
    Rewrite the following article into an engaging, mind-blowing blog post in Plain English.
    
    [Source Material]
    - Original Title: {title}
    - Original Source: {source}
    - Reference Link: {link}
    - Content Summary: {content[:3000]}

    [Guidelines]
    1. **Format**: Create a standard Markdown document (.md).
    2. **Frontmatter**: You MUST start the document with valid YAML frontmatter containing 'title', 'date', 'categories' (set to AI), and 'tags'.
    3. **Tone**: Engaging, slightly provocative, visionary, and conversational. Sound like a passionate human expert sharing a mind-blowing discovery with a friend. Never use AI robotic phrases like "As an AI..." or "In conclusion".
    4. **Core Content Focus**: 
       - Emphasize any mentions of key figures (Sam Altman, Elon Musk, Ilya Sutskever, Demis Hassabis, etc.), their quotes, or their actions.
       - Highlight steps towards AGI, superintelligence, or major paradigm shifts.
    5. **Structure**: 
       - An intriguing, hook-driven introduction (Why am I writing about this today?).
       - A "TL;DR" bulleted summary.
       - Deep dive into the facts (simplify complex terms with human analogies).
       - **The Ripple Effect**: How this disrupts industries or brings us closer to the singularity (share a strong personal perspective/prediction).
       - A thought-provoking conclusion leaving the reader with a deep question.
    6. At the very bottom, include a small "Source: [Title](Link)" credit.
    
    Output nothing but the raw Markdown content! Do not wrap in ```markdown blocks if possible.
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
            
        return generated_md.strip()
        
    except Exception as e:
        logger.error(f"Error generating blog post via Gemini: {e}")
        return None

def generate_post_title(article):
    """Generate an attractive and SEO-friendly English title."""
    if not GEMINI_API_KEY:
        return article.get('title', '')
        
    title = article.get('title', '')
    try:
        model = get_model()
        prompt = f"Rewrite this news title into a highly clickable, provocative, and visionary English blog title (max 70 characters). Emphasize profound impact, AGI, or key AI figures if applicable. Make it sound mind-blowing but professional. Don't use quotes or any other extra text.\nOriginal Title: {title}"
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
            )
        )
        return response.text.strip().replace('"', '')
    except Exception as e:
        logger.error(f"Error generating title with Gemini: {e}")
        return title


