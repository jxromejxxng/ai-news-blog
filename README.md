# AI News Global Blog Automation (GitHub Pages & Google Gemini)

This project automatically scrapes the latest Artificial Intelligence news, processes them using Google Gemini's free API to generate high-quality, Easy-English blog posts, and publishes them automatically to a GitHub Pages blog.

## Features
- **100% Zero Cost**: Hosted entirely on GitHub Pages and powered by Google Gemini AI's free tier.
- **Global Targeting**: Automatically rewrites complex news into Plain English for a global audience.
- **SEO Optimized**: Generates Markdown with YAML Frontmatter for static site generators (Jekyll/Hugo/Hexo).
- **100% Automated**: Runs daily via GitHub Actions.

## Setup Instructions

### 1. Create your GitHub Pages Blog
1. Go to your GitHub account and create a new repository (e.g., `yourusername.github.io`).
2. Go to the repository **Settings** -> **Pages** and establish your Jekyll or Hugo theme. (There are thousands of free Jekyll themes available).
3. Clone this `BlogAutomation` code into that repository.

### 2. Configure GitHub Secrets
For the automation script to work, it needs access to the Google Gemini AI API.
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. In your GitHub repository, go to **Settings** -> **Secrets and variables** -> **Actions**.
3. Click **New repository secret**.
4. Name: `GEMINI_API_KEY`
5. Value: `your-actual-gemini-api-key`

*(Note: The script will automatically commit back to the repo using the default GitHub Actions token, so no Personal Access Token is needed unless your org restricts it).*

### 3. Usage & Customization
- The script runs automatically every day at 00:00 UTC.
- To change the RSS feed sources, edit the `RSS_FEEDS` list in `config.py`.
- To tweak the generated tone or structure, edit the Prompt in `ai_processor.py`.

### Local Testing
To test the script on your local machine before pushing to GitHub:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and put your GEMINI_API_KEY inside
python main.py
```
Check the `_posts/` folder to see the generated Markdown files!
