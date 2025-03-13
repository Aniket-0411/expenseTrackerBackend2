from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from .models import ChatMessage
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.

def chat_view(request):
    return render(request, 'finance/chat.html')

@csrf_exempt
@require_http_methods(["POST"])
def save_chat_message(request):
    try:
        data = json.loads(request.body)
        message = data.get("message", "")
        sender = data.get("sender", "")
        if message and sender:
            ChatMessage.objects.create(message=message, sender=sender)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "error": "Invalid data"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)}, status=500)

@require_http_methods(["GET"])
def get_chat_history(request):
    messages = ChatMessage.objects.all().order_by("created_at")
    data = [{"message": m.message, "sender": m.sender} for m in messages]
    return JsonResponse(data, safe=False)

@require_POST
def clear_chat_history(request):
    ChatMessage.objects.all().delete()
    return JsonResponse({'status': 'success'})

@csrf_exempt
@require_http_methods(["POST"])
def get_rasa_response(request):
    try:
        data = json.loads(request.body)
        message = data.get("message", "")
        sender = data.get("sender", "default")
        if not message:
            return JsonResponse({"status": "error", "error": "No message provided."}, status=400)
        payload = {"sender": sender, "message": message}
        rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"  # update if needed
        rasa_resp = requests.post(rasa_endpoint, json=payload)
        if rasa_resp.status_code == 200:
            responses = rasa_resp.json()
            # Optionally, you can also save the bot responses to ChatMessage model here.
            return JsonResponse({"status": "success", "responses": responses})
        else:
            return JsonResponse({"status": "error", "error": "Rasa error"}, status=500)
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)}, status=500)
