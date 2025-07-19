from datetime import datetime
from django.http import JsonResponse

from api.database import get_calls_collection
from api.calls.schemas import CallData


def handle_vapi_webhok(report: dict):
    print("=== VAPI WEBHOOK RECEIVED ===")

    print(f"Webhook type: {report.get('message', {}).get('type')}")

    # Check if this is an end-of-call-report
    if report.get("message", {}).get("type") == "end-of-call-report":
        print("Processing end-of-call-report...")

        # Extract message data
        message = report.get("message", {})
        analysis = message.get("analysis", {})
        structured_data = analysis.get("structuredData", {})

        # Parse datetime strings
        started_at = None
        ended_at = None

        if message.get("startedAt"):
            started_at = datetime.fromisoformat(message["startedAt"].replace('Z', '+00:00'))

        if message.get("endedAt"):
            ended_at = datetime.fromisoformat(message["endedAt"].replace('Z', '+00:00'))

        # Create validated call data using Pydantic model
        call_data = CallData(
            summary=message.get("summary", ""),
            transcript=message.get("transcript", ""),
            recording_url=message.get("recordingUrl", ""),
            started_at=started_at,
            ended_at=ended_at,
            ended_reason=message.get("endedReason", ""),
            caller_name=structured_data.get("name", ""),
            success_evaluation=analysis.get("successEvaluation", ""),
            cost=message.get("cost", 0.0)
        )

        # Save to Firestore (convert to dict for Firestore)
        calls_collection = get_calls_collection()
        doc_ref = calls_collection.add(call_data.model_dump())
        doc_id = doc_ref[1].id

        print(f"Saved call to Firestore with ID: {doc_id}")
        print(f"Caller: {call_data.caller_name}")
        print(f"Summary: {call_data.summary}")

    else:
        print(f"Ignoring webhook type: {report.get('message', {}).get('type')}")

    print("=== END WEBHOOK DATA ===")

    # Return success response
    return JsonResponse({"status": "ok"})
