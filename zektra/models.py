"""Data models for Zektra AI Gateway"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class AIResponse(BaseModel):
    """Response from AI service"""

    text: str = Field(..., description="Generated text response")
    model: str = Field(..., description="Model used for generation")
    usage: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Token usage information"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class PaymentResult(BaseModel):
    """Result of crypto payment"""

    success: bool = Field(..., description="Whether payment was successful")
    transaction_hash: Optional[str] = Field(
        default=None,
        description="Blockchain transaction hash"
    )
    amount: float = Field(..., description="Amount paid")
    token: str = Field(..., description="Token used for payment")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.now)


class QueryRequest(BaseModel):
    """Request for AI query"""

    prompt: str = Field(..., description="User prompt")
    service: str = Field(default="deepseek", description="AI service to use")
    model: Optional[str] = Field(default=None, description="Specific model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    payment_token: str = Field(default="ZEKTRA", description="Token for payment")
    payment_amount: Optional[float] = Field(default=None, description="Payment amount")
    encrypted_context: Optional[str] = Field(
        default=None,
        description="Encrypted context data"
    )


class ServiceInfo(BaseModel):
    """Information about an AI service"""

    name: str
    available: bool
    models: List[str]
    default_model: str
    cost_per_token: Optional[float] = None
    description: Optional[str] = None

