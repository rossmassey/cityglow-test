import logging
from datetime import datetime

import pytz
from django.http import JsonResponse

from api import settings
from api.calls.schemas import CallData
from api.database import get_calls_collection
from api.email_service import send_email

logger = logging.getLogger(__name__)


def format_call_email(call_data: CallData, doc_id: str, timezone='US/Eastern'):
    """Format call data into email subject and body"""

    # Format phone number for subject
    phone_display = call_data.phone_number
    if phone_display and len(phone_display) == 11 and phone_display.startswith('1'):
        # Format US number: +1XXXXXXXXXX -> (XXX) XXX-XXXX
        phone_display = f"({phone_display[1:4]}) {phone_display[4:7]}-{phone_display[7:]}"
    elif phone_display and len(phone_display) == 10:
        # Format US number: XXXXXXXXXX -> (XXX) XXX-XXXX
        phone_display = f"({phone_display[:3]}) {phone_display[3:6]}-{phone_display[6:]}"

    # Convert UTC datetime to specified timezone for display
    display_datetime = None
    if call_data.started_at:
        # Ensure datetime is timezone-aware (assume UTC if naive)
        if call_data.started_at.tzinfo is None:
            utc_datetime = pytz.UTC.localize(call_data.started_at)
        else:
            utc_datetime = call_data.started_at.astimezone(pytz.UTC)

        # Convert to display timezone
        target_tz = pytz.timezone(timezone)
        display_datetime = utc_datetime.astimezone(target_tz)

    # Format date for subject (MM/DD)
    date_str = ""
    if display_datetime:
        date_str = display_datetime.strftime("%m/%d")

    # Create subject
    subject = f"[{date_str} Call from {phone_display}]"

    # Format date and time for body with timezone indicator
    formatted_date = ""
    if display_datetime:
        tz_abbr = "EST" if timezone == 'US/Eastern' else display_datetime.strftime("%Z")
        formatted_date = display_datetime.strftime(f"%B %d, %Y at %I:%M %p ({tz_abbr})")

    # Calculate duration
    duration_str = "Unknown"
    if call_data.started_at and call_data.ended_at:
        duration_seconds = (call_data.ended_at - call_data.started_at).total_seconds()
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        if minutes > 0:
            duration_str = f"{minutes}m {seconds}s"
        else:
            duration_str = f"{seconds}s"

    # Create plain text body
    body_parts = []
    body_parts.append(f"Caller Phone Number: {call_data.phone_number}")

    if call_data.caller_name and call_data.caller_name.strip():
        body_parts.append(f"Caller Name: {call_data.caller_name}")

    body_parts.append(f"Date: {formatted_date}")
    body_parts.append(f"Duration: {duration_str}")
    body_parts.append(f"Summary: {call_data.summary}")
    body_parts.append(f"Full Transcript:\n{call_data.transcript}")

    plain_body = "\n".join(body_parts)

    # Create HTML body
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #2c5282;">Call Summary</h2>
        
        <div style="background-color: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
          <p><strong>Caller Phone Number:</strong> {call_data.phone_number}</p>
          {"<p><strong>Caller Name:</strong> " + call_data.caller_name + "</p>" if call_data.caller_name and call_data.caller_name.strip() else ""}
          <p><strong>Date:</strong> {formatted_date}</p>
          <p><strong>Duration:</strong> {duration_str}</p>
        </div>
        
        <div style="margin: 20px 0;">
          <h3 style="color: #2c5282;">Summary</h3>
          <p style="background-color: #e6f3ff; padding: 15px; border-radius: 5px; border-left: 4px solid #3182ce;">
            {call_data.summary}
          </p>
        </div>
        
        <div style="margin: 20px 0;">
          <h3 style="color: #2c5282;">Full Transcript</h3>
          <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; white-space: pre-wrap; font-family: monospace; border: 1px solid #e9ecef;">
{call_data.transcript}
          </div>
        </div>
      </body>
    </html>
    """

    return subject, plain_body, html_body


def handle_elevenlabs_webhook(report: dict):
    """Handle ElevenLabs webhook data"""
    logger.info("=== ELEVENLABS WEBHOOK RECEIVED ===")
    logger.info(report)

    # concatenate transcript
    transcript_str = ""
    for transcript_item in report["data"]["transcript"]:
        transcript_str += f"{transcript_item['role']}: {transcript_item['message']}\n"

    # construct the API url that will stream the audio
    conversation_id = report["data"]["conversation_id"]
    recording_url = f"/calls/elevenlabs_stream/{conversation_id}/"

    try:
        phone_number = report["data"]["metadata"]["phone_call"]["external_number"]
        if phone_number in settings.DEBUG_NUMBERS:
            logger.info(f"Debug number found, not saving to database: {phone_number}")
            return()

        # Convert unix timestamps to datetime objects
        started_at = datetime.fromtimestamp(report["data"]["metadata"]["start_time_unix_secs"])
        ended_at = datetime.fromtimestamp(
            report["data"]["metadata"]["start_time_unix_secs"] +
            report["data"]["metadata"]["call_duration_secs"]
        )

        call_data = CallData(
            summary=report["data"]["analysis"]["transcript_summary"],
            transcript=transcript_str,
            recording_url=recording_url,
            started_at=started_at,
            ended_at=ended_at,
            ended_reason=report["data"]["metadata"]["termination_reason"],
            caller_name=report["data"]["analysis"]["data_collection_results"]["name"]["value"],
            success_evaluation=report["data"]["analysis"]["call_successful"],
            cost=report["data"]["metadata"]["cost"],
            phone_number=phone_number,
            did_respond=False
        )

    except KeyError:
        logger.error("ERROR: Could not parse elevenlabs webhook data!!")
        return ()

    # Save to Firestore (convert to dict for Firestore)
    calls_collection = get_calls_collection()
    doc_ref = calls_collection.add(call_data.model_dump())
    doc_id = doc_ref[1].id

    # Send formatted email summary (display times in EST)
    subject, plain_body, html_body = format_call_email(call_data, doc_id, timezone='US/Eastern')
    send_email(settings.EMAIL_SUMMARY_RECIPIENT, subject, plain_body, html_body)

    logger.info(f"Saved call to Firestore with ID: {doc_id}")
    logger.info(f"Caller: {call_data.caller_name}")
    logger.info(f"Summary: {call_data.summary}")



    # Return success response
    return JsonResponse({"status": "ok"})
