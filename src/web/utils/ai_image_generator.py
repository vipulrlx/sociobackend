import os
import uuid
import base64
import google.generativeai as genai
from django.conf import settings

# ✅ Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# ✅ IMPORTANT: correct image model
IMAGE_MODEL = "gemini-2.0-flash-preview-image-generation"


def generate_post_image(prompt: str):
    """
    Generates AI image using Gemini
    Saves to MEDIA and returns URL
    """

    try:
        model = genai.GenerativeModel(IMAGE_MODEL)

        response = model.generate_content(
            prompt,
            generation_config={
                "response_modalities": ["TEXT", "IMAGE"]
            }
        )

        # 🔥 Extract image from Gemini response
        image_bytes = None

        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_bytes = part.inline_data.data
                break

        if not image_bytes:
            print("No image returned from Gemini")
            return None

        # ✅ Save image
        file_name = f"post_{uuid.uuid4().hex}.png"
        folder_path = os.path.join(settings.MEDIA_ROOT, "ai_posts")
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        # ✅ Return public URL
        return settings.MEDIA_URL + "ai_posts/" + file_name

    except Exception as e:
        print("Gemini image generation failed:", str(e))
        return None