from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CallData(BaseModel):
    """Pydantic model for call data saved to Firestore"""
    summary: Optional[str] = Field(default="", description="AI-generated summary of the call")
    transcript: Optional[str] = Field(default="", description="Complete transcript of the call")
    recording_url: Optional[str] = Field(default="", description="URL to the call recording")
    started_at: Optional[datetime] = Field(None, description="When the call started")
    ended_at: Optional[datetime] = Field(None, description="When the call ended")
    ended_reason: Optional[str] = Field(default="", description="Reason why the call ended")
    caller_name: Optional[str] = Field(default="", description="Name extracted from structured data analysis")
    success_evaluation: Optional[str] = Field(default="", description="Success evaluation from analysis")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the record was created")
    cost: float = Field(default=0.0, description="Cost of the call")
    phone_number: Optional[str] = Field(default="", description="Client phone number")

    @field_validator('summary',
                     'transcript',
                     'recording_url',
                     'ended_reason',
                     'caller_name',
                     'success_evaluation',
                     'phone_number',
                     mode='before')
    @classmethod
    def convert_none_to_empty_string(cls, v):
        """Convert None values to empty strings"""
        return "" if v is None else v

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
                "cost": 0.05,
                "phone_number": "+1234567890"
            }
        }


class ErrorResponse(BaseModel):
    """Generic error response model"""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid JSON",
                "details": "Request body could not be parsed as valid JSON"
            }
        }
