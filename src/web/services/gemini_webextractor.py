import json
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_website(website_url: str, website_text: str) -> str:
    prompt = f"""
You are a senior social media marketing strategist.

Analyze the website below for social media marketing.

Website URL:
{website_url}

Website Content:
{website_text}

Return STRICT JSON with the following fields:
- entity_type (Product / Person / Place / Brand)
- industry
- brand_summary
- target_audience
- audience_pain_points
- value_proposition
- brand_tone
- content_pillars (array)
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.6,
            "response_mime_type": "application/json"
        }
    )

    return response.text

def analyze_website_marketing(website_url: str, website_text: str) -> str:
    prompt = f"""
You are a senior social media marketing strategist.

Analyze the website below for social media marketing.

Website URL:
{website_url}

Website Content:
{website_text}

Return STRICT JSON with the following fields:
- entity_type (Product / Person / Place / Brand)
- industry
- brand_summary
- target_audience
- audience_pain_points
- value_proposition
- brand_tone
- content_pillars (array)
- recommended_social_platforms (object with reasons)
- posting_frequency
- hashtag_strategy
- bio_description
- call_to_action_ideas
- sample_post_ideas (minimum 5)
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.6,
            "response_mime_type": "application/json"
        }
    )

    return response.text

def analyze_brand_social_strategy(brand_payload: dict) -> str:
    """
    brand_payload contains brand + style + positioning info from DB
    """

    prompt = f"""
You are a senior social media marketing strategist and creative director.

Using the brand details below, create a complete social media strategy
AND platform-specific post ideas with visual guidance.

Brand Details (JSON):
{json.dumps(brand_payload, indent=2)}

Return STRICT JSON with the following structure:

- recommended_social_platforms (object)
  - key: platform name
  - value: reason for choosing platform

- posting_frequency

- hashtag_strategy

- bio_description

- call_to_action_ideas (array)

- sample_post_ideas (object)
  - key: platform name
  - value: array of minimum 5 post objects
    - post_title
    - post_description
    - caption
    - image_idea
    - image_prompt (detailed prompt for AI image generation)
    - format (Image / Carousel / Reel / Video)

Ensure:
- Posts align with brand tone and content pillars
- Image prompts are descriptive and production-ready
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.6,
            "response_mime_type": "application/json"
        }
    )

    return response.text
