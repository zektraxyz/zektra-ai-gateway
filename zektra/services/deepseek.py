"""DeepSeek AI service integration"""

import requests
from typing import Optional, Dict, Any
from zektra.services.base import BaseAIService
from zektra.models import AIResponse, ServiceInfo


class DeepSeekService(BaseAIService):
    """DeepSeek AI service integration"""

    DEFAULT_MODEL = "deepseek-chat"
    AVAILABLE_MODELS = [
        "deepseek-chat",
        "deepseek-coder",
    ]

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        super().__init__(api_key, api_url or "https://api.deepseek.com/v1/chat/completions")

    def query(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        """Query DeepSeek API"""

        model = model or self.DEFAULT_MODEL

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        # Add any additional parameters
        payload.update(kwargs)

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()

            # Extract response text
            text = data["choices"][0]["message"]["content"]

            # Extract usage information
            usage = data.get("usage", {})

            return AIResponse(
                text=text,
                model=model,
                usage=usage,
                metadata={
                    "id": data.get("id"),
                    "created": data.get("created"),
                    "finish_reason": data["choices"][0].get("finish_reason"),
                }
            )

        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API error: {str(e)}")

    def get_service_info(self) -> ServiceInfo:
        """Get DeepSeek service information"""
        return ServiceInfo(
            name="deepseek",
            available=bool(self.api_key),
            models=self.AVAILABLE_MODELS,
            default_model=self.DEFAULT_MODEL,
            description="DeepSeek AI - Advanced language model"
        )

    def estimate_cost(self, prompt: str, model: Optional[str] = None) -> float:
        """Estimate cost for DeepSeek query (tokens)"""
        # Rough estimation: 1 token ≈ 4 characters
        estimated_tokens = len(prompt) / 4
        # DeepSeek pricing (example, adjust based on actual pricing)
        cost_per_1k_tokens = 0.001  # $0.001 per 1k tokens
        return (estimated_tokens / 1000) * cost_per_1k_tokens

