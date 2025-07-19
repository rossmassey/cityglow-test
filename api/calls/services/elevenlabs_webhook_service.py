from datetime import datetime
from django.http import JsonResponse

from api.database import get_calls_collection
from api.calls.schemas import CallData


def handle_elevenlabs_webhook(report: dict):
    """Handle ElevenLabs webhook data"""
    print("=== ELEVENLABS WEBHOOK RECEIVED ===")

    print(report)

    # concatenate transcript
    transcript_str = ""
    for transcript_item in report["data"]["transcript"]:
        transcript_str += f"{transcript_item['role']}: {transcript_item['message']}\n"

    # construct the API url that will stream the audio
    conversation_id = report["data"]["conversation_id"]
    recording_url = f"/calls/elevenlabs_stream/{conversation_id}/"
    
    try:
        call_data = CallData(
            summary=report["data"]["analysis"]["transcript_summary"],
            transcript=transcript_str,
            recording_url=recording_url,
            started_at=report["data"]["metadata"]["start_time_unix_secs"],
            ended_at=report["data"]["metadata"]["start_time_unix_secs"] + report["data"]["metadata"]["call_duration_secs"],
            ended_reason=report["data"]["metadata"]["termination_reason"],
            caller_name=report["data"]["analysis"]["data_collection_results"]["name"]["value"],
            success_evaluation=report["data"]["analysis"]["call_successful"],
            cost=report["data"]["metadata"]["cost"],
            phone_number=report["data"]["metadata"]["phone_call"]["external_number"]
        )

    except KeyError:
        print("ERROR: Could not parse elevenlabs webhook data!!")
        return()

    # Save to Firestore (convert to dict for Firestore)
    calls_collection = get_calls_collection()
    doc_ref = calls_collection.add(call_data.model_dump())
    doc_id = doc_ref[1].id

    print(f"Saved call to Firestore with ID: {doc_id}")
    print(f"Caller: {call_data.caller_name}")
    print(f"Summary: {call_data.summary}")


    print("=== END ELEVENLABS WEBHOOK DATA ===")

    # Return success response
    return JsonResponse({"status": "ok"})
