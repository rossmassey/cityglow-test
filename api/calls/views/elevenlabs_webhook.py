import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View

from api.calls.services.elevenlabs_webhook_service import handle_elevenlabs_webhook


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class ElevenLabsWebhookView(View):
    """
    Webhook endpoint for receiving ElevenLabs events.
    """
    
    def post(self, request):
        """Handle ElevenLabs webhook POST requests"""
        try:
            # Parse JSON data
            json_data = json.loads(request.body)
            
            # Delegate to service
            return handle_elevenlabs_webhook(json_data)
            
        except json.JSONDecodeError:
            print("Could not parse body as JSON")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            print(f"Error processing ElevenLabs webhook: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": "Internal server error"}, status=500) 