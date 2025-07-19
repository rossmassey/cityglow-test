import logging

from django.http import StreamingHttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.calls.schemas import ErrorResponse
from api.calls.services.elevenlabs_api import stream_conversation_audio
from api.calls.utils import pydantic_to_openapi_schema

logger = logging.getLogger(__name__)


class ElevenLabsStreamView(APIView):
    @extend_schema(
        tags=['ElevenLabs'],
        summary='Stream conversation audio',
        parameters=[
            OpenApiParameter(
                name='conversation_id',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='id for elevenlabs conversation to be streamed',
                required=True
            )
        ],
        responses={
            (200, 'audio/mpeg'): OpenApiResponse(
                description='Streaming audio in MP3 format',
                response={'type': 'string', 'format': 'binary'}
            ),
            400: OpenApiResponse(
                response=pydantic_to_openapi_schema(ErrorResponse),
                description="Audio not available or invalid conversation ID"
            )
        }
    )
    def get(self, request, conversation_id):
        """
        Streams audio recording of a conversation from ElevenLabs API
        """
        try:
            logger.info(f"Streaming audio for conversation: {conversation_id}")

            # Get the streaming response from ElevenLabs
            elevenlabs_response = stream_conversation_audio(conversation_id)

            # Check if the ElevenLabs request was successful
            if elevenlabs_response.status_code != 200:
                logger.error(
                    f"ElevenLabs API error for conversation {conversation_id}: {elevenlabs_response.status_code}")
                error_response = ErrorResponse(
                    error=f"Audio not available for conversation {conversation_id}"
                )
                return Response(error_response.model_dump(), status=status.HTTP_400_BAD_REQUEST)

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
            logger.error(f"Error streaming audio for conversation {conversation_id}: {str(e)}", exc_info=True)
            error_response = ErrorResponse(
                error="Error streaming audio"
            )
            return Response(error_response.model_dump(), status=status.HTTP_400_BAD_REQUEST)
