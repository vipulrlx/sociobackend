import requests
from django.conf import settings


def start_ai_call(phone_number: str, lead_id: int):
    url = "https://api.elevenlabs.io/v1/convai/twilio/outbound-call"

    payload = {
        "agent_id": settings.ELEVENLABS_AGENT_ID,
        "agent_phone_number_id": settings.ELEVENLABS_AGENT_PHONE_NUMBER_ID,
        "to_number": phone_number,
        "metadata": {
            "lead_id": lead_id
        }
    }

    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        return response.json()
    except Exception:
        return {"raw": response.text}