import json
import logging

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.calls.schemas import ErrorResponse
from api.calls.services.elevenlabs_webhook_service import handle_elevenlabs_webhook
from api.calls.utils import pydantic_to_openapi_schema

logger = logging.getLogger(__name__)


class ElevenLabsWebhookView(APIView):
    @extend_schema(
        tags=['ElevenLabs'],
        summary='Process ElevenLabs webhook event',
        responses={
            200: "Webhook processed successfully",
            400: OpenApiResponse(
                response=pydantic_to_openapi_schema(ErrorResponse),
                description="Invalid request data"
            ),
            500: OpenApiResponse(
                response=pydantic_to_openapi_schema(ErrorResponse),
                description="Internal server error"
            )
        }
    )
    def post(self, request):
        """
        receives webhook notification from ElevenLabs when conversation ends
        """
        try:
            # Get JSON data directly without validation
            json_data = request.data
            logger.info(f"Received ElevenLabs webhook")

            # Delegate to service
            service_response = handle_elevenlabs_webhook(json_data)

            # Extract response data 
            if hasattr(service_response, 'content'):
                response_data = json.loads(service_response.content.decode('utf-8'))
            else:
                response_data = {"status": "success", "message": "Webhook processed"}

            return Response(response_data, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            logger.error("Could not parse webhook body as JSON")
            error_response = ErrorResponse(
                error="Invalid JSON",
                details="Request body could not be parsed as valid JSON"
            )
            return Response(error_response.model_dump(), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error processing ElevenLabs webhook: {str(e)}", exc_info=True)
            error_response = ErrorResponse(
                error="Internal server error",
                details=str(e)
            )
            return Response(error_response.model_dump(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
