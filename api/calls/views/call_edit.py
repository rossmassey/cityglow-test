from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.calls.schemas import CallEditRequest
from api.calls.services.calls_service import update_call_response_status


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
        data = CallEditRequest(**request.data)
        
        if data.did_respond is not None:
            result = update_call_response_status(call_id, data.did_respond)
            return Response(result, status=status.HTTP_200_OK)
        
        return Response({'message': 'No updates provided'}, status=status.HTTP_200_OK) 
        