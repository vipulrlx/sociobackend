import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from web.utils.website_extractor import extract_website_text
from web.utils.ai_image_generator import generate_post_image
from web.services.gemini_webextractor import analyze_website
from web.services.gemini_webextractor import analyze_brand_social_strategy, generate_daily_trending_posts
from web.models import Brand


class WebsiteMarketingAnalyzerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        website = request.data.get("website")

        if not website:
            return Response(
                {"error": "website is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        website_text = extract_website_text(website)

        gemini_response = analyze_website(
            website_url=website,
            website_text=website_text
        )

        try:
            analysis_json = json.loads(gemini_response)

            # 🔑 API-level rule: one brand per user (for now)
            brand = Brand.objects.filter(user=user).order_by("id").first()

            if brand:
                # Update existing brand
                brand.website = website
                brand.entity_type = analysis_json.get("entity_type")
                brand.industry = analysis_json.get("industry")
                brand.analysis_data = analysis_json
                brand.save()

                created = False
            else:
                # Create first brand
                brand = Brand.objects.create(
                    user=user,
                    website=website,
                    entity_type=analysis_json.get("entity_type"),
                    industry=analysis_json.get("industry"),
                    analysis_data=analysis_json
                )
                created = True

            return Response(
                {
                    "brand_id": brand.id,
                    "created": created,
                    "analysis": analysis_json
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {
                    "error": "Invalid Gemini JSON",
                    "raw_response": gemini_response
                },
                status=status.HTTP_200_OK
            )

class BrandStyleUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        photography_style = request.data.get("photography_style")
        font_style = request.data.get("font_style")
        filter_style = request.data.get("filter_style")

        # At least one value should be provided
        if not any([photography_style, font_style, filter_style]):
            return Response(
                {"error": "At least one style field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        brand = Brand.objects.filter(user=user).order_by("id").first()

        if not brand:
            return Response(
                {"error": "Brand not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        if photography_style is not None:
            brand.photography_style = photography_style

        if font_style is not None:
            brand.font_style = font_style

        if filter_style is not None:
            brand.filter_style = filter_style

        brand.save()

        # ✅ FINAL STEP OF INITIAL SETUP
        if user.initialsetup != "0":
            user.initialsetup = "0"
            user.save(update_fields=["initialsetup"])
            
        return Response(
            {
                "message": "Brand style updated successfully",
                "brand_id": brand.id,
                "styles": {
                    "photography_style": brand.photography_style,
                    "font_style": brand.font_style,
                    "filter_style": brand.filter_style
                }
            },
            status=status.HTTP_200_OK
        )

class BrandDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        brand = Brand.objects.filter(user=user).order_by("id").first()

        if not brand:
            return Response(
                {"error": "Brand not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "brand_id": brand.id,
                "website": brand.website,
                "entity_type": brand.entity_type,
                "industry": brand.industry,

                "analysis_data": brand.analysis_data,

                "styles": {
                    "photography_style": brand.photography_style,
                    "font_style": brand.font_style,
                    "filter_style": brand.filter_style
                },

                "created_at": brand.created_at,
                "updated_at": brand.updated_at
            },
            status=status.HTTP_200_OK
        )

class BrandSocialStrategyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        brand = Brand.objects.filter(user=user).order_by("id").first()

        if not brand:
            return Response(
                {"error": "Brand not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        analysis_data = brand.analysis_data or {}

        brand_payload = {
            "website": brand.website,
            "entity_type": brand.entity_type,
            "industry": brand.industry,

            "brand_summary": analysis_data.get("brand_summary"),
            "target_audience": analysis_data.get("target_audience"),
            "audience_pain_points": analysis_data.get("audience_pain_points"),
            "value_proposition": analysis_data.get("value_proposition"),
            "brand_tone": analysis_data.get("brand_tone"),
            "content_pillars": analysis_data.get("content_pillars"),

            "photography_style": brand.photography_style,
            "font_style": brand.font_style,
            "filter_style": brand.filter_style
        }

        gemini_response = analyze_brand_social_strategy(brand_payload)

        try:
            strategy_json = json.loads(gemini_response)

            return Response(
                {
                    "brand_id": brand.id,
                    "social_strategy": strategy_json
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {
                    "error": "Invalid Gemini JSON",
                    "raw_response": gemini_response
                },
                status=status.HTTP_200_OK
            )

class DailyTrendingPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        brand = Brand.objects.filter(user=user).order_by("id").first()

        if not brand:
            return Response(
                {"error": "Brand not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        analysis_data = brand.analysis_data or {}

        brand_payload = {
            "website": brand.website,
            "entity_type": brand.entity_type,
            "industry": brand.industry,

            "brand_summary": analysis_data.get("brand_summary"),
            "target_audience": analysis_data.get("target_audience"),
            "audience_pain_points": analysis_data.get("audience_pain_points"),
            "value_proposition": analysis_data.get("value_proposition"),
            "brand_tone": analysis_data.get("brand_tone"),
            "content_pillars": analysis_data.get("content_pillars"),

            "photography_style": brand.photography_style,
            "font_style": brand.font_style,
            "filter_style": brand.filter_style
        }

        gemini_response = generate_daily_trending_posts(brand_payload)

        try:
            posts_json = json.loads(gemini_response)

            posts = posts_json.get("daily_trending_posts", [])

            # 🔥 Generate image for each post
            for post in posts:
                image_prompt = post.get("image_prompt")

                if image_prompt:
                    try:
                        post["generated_image_url"] = generate_post_image(image_prompt)
                    except Exception as e:
                        post["generated_image_url"] = None
                        post["image_error"] = str(e)

            return Response(
                {
                    "brand_id": brand.id,
                    "daily_posts": posts_json
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {
                    "error": "Invalid Gemini JSON",
                    "raw_response": gemini_response
                },
                status=status.HTTP_200_OK
            )