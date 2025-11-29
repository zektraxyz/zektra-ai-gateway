"""Base class for AI service integrations"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from zektra.models import AIResponse, ServiceInfo


class BaseAIService(ABC):
    """Base class for AI service integrations"""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key
        self.api_url = api_url
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate service configuration"""
        if not self.api_key:
            raise ValueError(f"{self.__class__.__name__} requires an API key")

    @abstractmethod
    def query(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        """Query the AI service"""
        pass

    @abstractmethod
    def get_service_info(self) -> ServiceInfo:
        """Get information about the service"""
        pass

    @abstractmethod
    def estimate_cost(self, prompt: str, model: Optional[str] = None) -> float:
        """Estimate cost for a query"""
        pass

