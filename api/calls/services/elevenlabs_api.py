import requests
from api import settings

ELEVENLABS_HEADERS = {"xi-api-key": settings.ELEVENLABS_API_KEY}

def get_conversation_audio(conversation_id):
    conversation_audio_url = f"{settings.ELEVENLABS_BASE_URL}/v1/convai/conversations/{conversation_id}/audio"

    response = requests.get(conversation_audio_url, headers=ELEVENLABS_HEADERS)

    print(response.json())

def stream_conversation_audio(conversation_id):
    """
    Stream audio from ElevenLabs API for a given conversation ID.
    Returns a requests Response object with stream=True for proxying.
    """
    conversation_audio_url = f"{settings.ELEVENLABS_BASE_URL}/v1/convai/conversations/{conversation_id}/audio"
    
    response = requests.get(
        conversation_audio_url, 
        headers=ELEVENLABS_HEADERS,
        stream=True
    )
    
    return response