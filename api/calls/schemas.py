from pydantic import BaseModel, Field
from typing import Optional


class HelloRequest(BaseModel):
    """Pydantic model for hello request data"""
    name: Optional[str] = Field(None, description="Name to personalize the greeting")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "CityGlow"
            }
        }


class HelloResponse(BaseModel):
    """Pydantic model for hello response data"""
    message: str = Field(..., description="The greeting message")
    service: str = Field(..., description="Service identifier")
    version: str = Field(..., description="API version")
    status: str = Field(..., description="Service status")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello CityGlow! Welcome to CityGlow Calls API",
                "service": "calls",
                "version": "1.0.0",
                "status": "active"
            }
        }
