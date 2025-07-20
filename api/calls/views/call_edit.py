import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.calls.schemas import CallEditRequest, ErrorResponse
from api.calls.services.calls_service import update_call_response_status

logger = logging.getLogger(__name__)


class CallEditView(APIView):
    @extend_schema(
        tags=['Calls'],
        summary='Edit call response status',
        description='Update the did_respond field for a specific call',
        request=CallEditRequest,
        responses={
            200: {
                'description': 'Call updated successfully',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string'},
                                'did_respond': {'type': 'boolean'}
                            }
                        }
                    }
                }
            }
        }
    )
    def post(self, request, call_id):
        """
        Update the did_respond field for a specific call by ID
        """
        try:
            data = CallEditRequest(**request.data)

            if data.did_respond is not None:
                result = update_call_response_status(call_id, data.did_respond)
                return Response(result, status=status.HTTP_200_OK)

            return Response({'message': 'No updates provided'}, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.error(f"Call not found: {str(e)}")
            error_response = ErrorResponse(
                error="Call not found",
                details=str(e)
            )
            return Response(error_response.model_dump(), status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error updating call {call_id}: {str(e)}", exc_info=True)
            error_response = ErrorResponse(
                error="Internal server error",
                details=str(e)
            )
            return Response(error_response.model_dump(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
