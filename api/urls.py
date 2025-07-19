"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """API health check endpoint"""

    @extend_schema(
        tags=['Test'],
        summary='Health check',
        description='Simple health check endpoint to verify API is running',
        responses={
            200: {
                'description': 'API is healthy',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': {
                                    'type': 'string',
                                    'example': 'healthy'
                                }
                            }
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        """Check API health status"""
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)


urlpatterns = [
    path('', HealthCheckView.as_view(), name='health-check'),
    path('admin/', admin.site.urls),
    path('calls/', include('api.calls.urls')),

    # Swagger/OpenAPI
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
