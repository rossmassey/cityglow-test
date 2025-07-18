from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiRequest, OpenApiResponse
from pydantic import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.calls.schemas import HelloRequest, HelloResponse
from api.calls.services import HelloService
from api.calls.utils import pydantic_to_openapi_schema


class HelloView(APIView):
    """
    Simple hello world view for testing the calls API
    """
    permission_classes = [AllowAny]  # No authentication required for hello world

    @extend_schema(
        tags=['Test'],
        summary='Get hello world message',
        description='Returns a hello world message with optional personalization',
        parameters=[
            OpenApiParameter(
                name='name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Optional name to personalize the greeting',
                required=False,
                examples=[
                    OpenApiExample('Default', value=''),
                    OpenApiExample('Personalized', value='CityGlow'),
                ]
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=pydantic_to_openapi_schema(HelloResponse),
                description='Successful hello world response'
            )
        },
        examples=[
            OpenApiExample(
                'Default Response',
                value={
                    "message": "Hello World! Welcome to CityGlow Calls API",
                    "service": "calls",
                    "version": "1.0.0",
                    "status": "active"
                }
            ),
            OpenApiExample(
                'Personalized Response',
                value={
                    "message": "Hello CityGlow! Welcome to CityGlow Calls API",
                    "service": "calls",
                    "version": "1.0.0",
                    "status": "active"
                }
            ),
        ]
    )
    def get(self, request):
        """
        GET /calls/hello/
        
        Returns a hello world message
        """
        name = request.query_params.get('name')

        # Use the service to get the hello message (returns Pydantic model)
        hello_response = HelloService.get_hello_message(name)

        # Convert Pydantic model to dict for DRF Response
        return Response(hello_response.model_dump(), status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Test'],
        summary='Post hello world message',
        description='Returns a hello world message with name from request body',
        request=OpenApiRequest(
            request=pydantic_to_openapi_schema(HelloRequest),
            examples=[
                OpenApiExample(
                    'Request with name',
                    value={"name": "Sveta"}
                ),
                OpenApiExample(
                    'Request without name',
                    value={}
                ),
            ]
        ),
        responses={
            200: OpenApiResponse(
                response=pydantic_to_openapi_schema(HelloResponse),
                description='Successful hello world response'
            )
        }
    )
    def post(self, request):
        """
        POST /calls/hello/
        
        Returns a hello world message with name from request body
        """
        try:
            # Validate request data with Pydantic
            hello_request = HelloRequest(**request.data)

            # Use the service to get the hello message (returns Pydantic model)
            hello_response = HelloService.get_hello_message(hello_request.name)

            # Convert Pydantic model to dict for DRF Response
            return Response(hello_response.model_dump(), status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {"error": "Invalid request data", "details": e.errors()},
                status=status.HTTP_400_BAD_REQUEST
            )


class FirestoreTestView(APIView):
    """
    Test view for Firestore database connection
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Test'],
        summary='Test Firestore connection',
        description='Tests the Firestore database connection by writing and reading a test document',
        responses={
            200: OpenApiResponse(
                description='Firestore connection successful',
                examples=[
                    OpenApiExample(
                        'Success',
                        value={
                            'status': 'success',
                            'message': 'Firestore connection working',
                            'test_doc_id': 'test_123',
                            'timestamp': '2024-01-15T10:30:00Z'
                        }
                    )
                ]
            ),
            500: OpenApiResponse(description='Firestore connection failed')
        }
    )
    def get(self, request):
        """
        GET /calls/hello/firestore-test/
        
        Tests Firestore database connection
        """
        try:
            from api.database import get_firestore_client
            from datetime import datetime

            # Get Firestore client
            db = get_firestore_client()

            # Create a test document
            test_doc = {
                'message': 'Firestore connection test',
                'timestamp': datetime.utcnow(),
                'source': 'cityglow-api'
            }

            # Write test document to logs collection
            doc_ref = db.collection('logs').add(test_doc)
            doc_id = doc_ref[1].id

            return Response({
                'status': 'success',
                'message': 'Firestore connection working',
                'test_doc_id': doc_id,
                'timestamp': test_doc['timestamp'].isoformat()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Firestore connection failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
