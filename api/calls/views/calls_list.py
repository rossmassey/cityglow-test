from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.calls.services.calls_service import get_all_calls


class CallsListView(APIView):
    @extend_schema(
        tags=['Calls'],
        summary='List all calls',
        description='Retrieve list of calls',
        responses={
            200: {
                'description': 'List of all calls',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'description': 'Call object from Firebase'
                            }
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        """
        Get all calls from Firebase Firestore and return as JSON list
        """
        calls = get_all_calls()
        return Response(calls, status=status.HTTP_200_OK) 