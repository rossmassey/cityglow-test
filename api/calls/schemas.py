from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CallData(BaseModel):
    """Pydantic model for call data saved to Firestore"""
    summary: str = Field(default="", description="AI-generated summary of the call")
    transcript: str = Field(default="", description="Complete transcript of the call")
    recording_url: str = Field(default="", description="URL to the call recording")
    started_at: Optional[datetime] = Field(None, description="When the call started")
    ended_at: Optional[datetime] = Field(None, description="When the call ended")
    ended_reason: str = Field(default="", description="Reason why the call ended")
    caller_name: str = Field(default="", description="Name extracted from structured data analysis")
    success_evaluation: str = Field(default="", description="Success evaluation from analysis")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the record was created")
    cost: float = Field(default=0.0, description="Cost of the call")

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Customer called asking about product availability",
                "transcript": "Hello, I was wondering if you have product XYZ in stock...",
                "recording_url": "https://example.com/recording.mp3",
                "started_at": "2025-07-19T00:06:31.932000",
                "ended_at": "2025-07-19T00:08:15.432000",
                "ended_reason": "customer-ended-call",
                "caller_name": "John Doe",
                "success_evaluation": "Good",
                "created_at": "2025-07-19T00:08:16.000000",
                "cost": 0.05
            }
        }


class VapiWebhookData(BaseModel):
    """Pydantic model for incoming Vapi webhook data"""
    message: dict = Field(..., description="The webhook message data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": {
                    "type": "end-of-call-report",
                    "summary": "Customer inquiry about product availability",
                    "transcript": "Hello, I was wondering...",
                    "recordingUrl": "https://example.com/recording.mp3",
                    "startedAt": "2025-07-19T00:06:31.932Z",
                    "endedAt": "2025-07-19T00:08:15.432Z",
                    "endedReason": "customer-ended-call",
                    "analysis": {
                        "structuredData": {
                            "name": "John Doe"
                        },
                        "successEvaluation": "Good"
                    }
                }
            }
        }
