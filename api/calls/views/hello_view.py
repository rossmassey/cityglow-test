from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from pydantic import ValidationError

from api.calls.services import HelloService
from api.calls.schemas import HelloRequest, HelloResponse
from api.calls.serializers import HelloRequestSerializer, HelloResponseSerializer


class HelloView(APIView):
    """
    Simple hello world view for testing the calls API
    """
    permission_classes = [AllowAny]  # No authentication required for hello world

    @extend_schema(
        tags=['Hello'],
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
        responses={200: HelloResponseSerializer},
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
        tags=['Hello'],
        summary='Post hello world message',
        description='Returns a hello world message with name from request body',
        request=HelloRequestSerializer,
        responses={200: HelloResponseSerializer},
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
