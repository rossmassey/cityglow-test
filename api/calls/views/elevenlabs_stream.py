from django.http import StreamingHttpResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.calls.services.elevenlabs_api import stream_conversation_audio
import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ElevenLabsStreamView(View):
    """
    Proxy endpoint that streams audio from ElevenLabs API to the frontend
    without exposing the API key.
    """
    
    def get(self, request, conversation_id):
        try:
            # Get the streaming response from ElevenLabs
            elevenlabs_response = stream_conversation_audio(conversation_id)
            
            # Check if the ElevenLabs request was successful
            if elevenlabs_response.status_code != 200:
                logger.error(f"ElevenLabs API error for conversation {conversation_id}: {elevenlabs_response.status_code}")
                return HttpResponseBadRequest(f"Audio not available for conversation {conversation_id}")
            
            # Create a generator to stream the content
            def audio_stream():
                for chunk in elevenlabs_response.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
            
            # Create streaming response with proper content type
            response = StreamingHttpResponse(
                audio_stream(),
                content_type=elevenlabs_response.headers.get('Content-Type', 'audio/mpeg')
            )
            
            # Copy relevant headers from ElevenLabs response
            if 'Content-Length' in elevenlabs_response.headers:
                response['Content-Length'] = elevenlabs_response.headers['Content-Length']
            
            response['Accept-Ranges'] = 'bytes'
            
            return response
            
        except Exception as e:
            logger.error(f"Error streaming audio for conversation {conversation_id}: {str(e)}")
            return HttpResponseBadRequest("Error streaming audio") 