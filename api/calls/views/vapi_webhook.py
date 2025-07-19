import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View

from api.database import get_calls_collection
from api.calls.schemas import CallData
from api.calls.services.vapi_webhook_service import handle_vapi_webhok


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class VapiWebhookView(View):
    """
    Webhook endpoint for receiving Vapi events.
    """
    
    def post(self, request):
        """Handle Vapi webhook POST requests"""
        try:
            json_data = json.loads(request.body)

            return handle_vapi_webhok(json_data)
                    
        except json.JSONDecodeError:
            print("Could not parse body as JSON")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": "Internal server error"}, status=500) 